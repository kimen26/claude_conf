---
name: n8n-llm-json-parse
description: Parse robust output JSON d'un AI Agent n8n (LangChain). Auto-trigger sur n8n agent JSON parse, LLM output non-JSON, Bad control character, JSON.parse Code node n8n, fiche_md manquant. Couvre 6 cas pathologiques et fournit un parser drop-in.
---

# n8n — Parser robuste pour output JSON d'un AI Agent

> **Pattern** : un AI Agent n8n (LangChain, Bedrock, OpenAI…) doit retourner un JSON structuré, qui est ensuite parsé dans un Code node aval. `JSON.parse` brut casse dans 1 cas sur 3. Ce skill fournit un parser drop-in qui couvre 6 cas pathologiques.

---

## Pourquoi le parse `JSON.parse(output)` casse

Quand un AI Agent (langchain) retourne du JSON, n8n ne garantit ni la forme du wrapper ni la qualité du JSON :

| # | Forme du `$input.first().json` | Cassure |
|---|--------------------------------|---------|
| 1 | `{ output: "{\"fiche_md\": \"x\"}" }` | OK avec `JSON.parse(output)` |
| 2 | `{ output: "\"{\\\"fiche_md\\\":...}\"" }` (double-encoded) | `JSON.parse` retourne une string, pas un objet |
| 3 | `{ output: "```json\n{...}\n```" }` (fence) | `JSON.parse` throw au 1er backtick |
| 4 | `{ output: "{ \"fiche_md\": \"# Titre\nligne 2\" }" }` (vrais `\n` non échappés) | `Bad control character in string literal` |
| 5 | `{ output: "Voici la réponse :\n```json\n{...}\n```" }` (préfixe + fence) | `JSON.parse` throw |
| 6 | `{ output: { fiche_md: "x", ... } }` (objet déjà parsé par n8n) | `JSON.parse(object)` throw |

Aucune solution unique ne couvre les 6 cas. Il faut un parser **multi-niveau** qui essaie chaque approche jusqu'à obtenir un objet utilisable.

---

## Parser drop-in (à coller dans un Code node n8n)

À adapter aux noms de tes champs (`fiche_md`, `delta`, `questions`…). Ce parser :

1. **Déballe** récursivement les wrappers `{output|text|json: ...}`
2. **Strip** les ```json fences éventuels
3. **JSON.parse** direct
4. Si échec : **escape** les ctrl chars (`\n`, `\r`, `\t`) à l'intérieur des strings JSON via state machine
5. Si encore échec : **extracteur regex champ par champ** (parser JSON maison qui gère les escapes `\n`, `\"`, `\\`, `\u00XX`)

```js
// === Niveau 1 : déballe les wrappers n8n récursifs ===
function unwrap(x) {
  for (let i = 0; i < 5; i++) {
    if (x == null) return null;
    if (typeof x === 'object' && !Array.isArray(x)) {
      // CHAMP CLÉ MÉTIER : adapter à ton output (ex: fiche_md, summary, answer…)
      if (x.fiche_md) return x;
      if (typeof x.output === 'string' || (x.output && typeof x.output === 'object')) { x = x.output; continue; }
      if (typeof x.text === 'string'   || (x.text   && typeof x.text   === 'object')) { x = x.text;   continue; }
      if (typeof x.json === 'object') { x = x.json; continue; }
      return x;
    }
    if (typeof x === 'string') {
      // strip fence ```json éventuel
      x = x.replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/```\s*$/, '').trim();
      try {
        const p = JSON.parse(x);
        if (p && typeof p === 'object') return p;
        if (typeof p === 'string') { x = p; continue; }  // double-encoded → reparse
        return p;
      } catch (e) { return x; }  // pas du JSON parsable → on rend la string pour l'extracteur
    }
    return x;
  }
  return x;
}

// === Niveau 2 : escape les \n \r \t à l'intérieur des strings JSON (state machine) ===
function escapeCtrlInsideStrings(s) {
  let out = '';
  let inStr = false, esc = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (esc) { out += c; esc = false; continue; }
    if (inStr && c === '\\') { out += c; esc = true; continue; }
    if (c === '"') { inStr = !inStr; out += c; continue; }
    if (inStr && c === '\n') { out += '\\n'; continue; }
    if (inStr && c === '\r') { out += '\\r'; continue; }
    if (inStr && c === '\t') { out += '\\t'; continue; }
    out += c;
  }
  return out;
}

// === Niveau 3 : extracteur regex champ par champ (gère les escapes JSON) ===
function extractField(s, field) {
  const re = new RegExp('"' + field + '"\\s*:\\s*"');
  const m = re.exec(s);
  if (!m) return null;
  let i = m.index + m[0].length;
  let out = '';
  while (i < s.length) {
    const c = s[i];
    if (c === '\\' && i + 1 < s.length) {
      const n = s[i+1];
      if (n === 'n') { out += '\n'; i += 2; continue; }
      if (n === 'r') { out += '\r'; i += 2; continue; }
      if (n === 't') { out += '\t'; i += 2; continue; }
      if (n === '"') { out += '"';  i += 2; continue; }
      if (n === '\\') { out += '\\'; i += 2; continue; }
      if (n === '/') { out += '/';  i += 2; continue; }
      if (n === 'u' && i + 5 < s.length) {
        const hex = s.slice(i+2, i+6);
        if (/^[0-9a-fA-F]{4}$/.test(hex)) { out += String.fromCharCode(parseInt(hex,16)); i += 6; continue; }
      }
      out += n; i += 2; continue;
    }
    if (c === '"') return out;
    out += c; i++;  // newline réel non échappé : on garde
  }
  return out;
}

function extractArrayOfStrings(s, field) {
  const re = new RegExp('"' + field + '"\\s*:\\s*\\[');
  const m = re.exec(s);
  if (!m) return [];
  let i = m.index + m[0].length;
  const items = [];
  while (i < s.length) {
    while (i < s.length && /[\s,]/.test(s[i])) i++;
    if (s[i] === ']') return items;
    if (s[i] !== '"') { i++; continue; }
    i++;
    let item = '';
    while (i < s.length && s[i] !== '"') {
      if (s[i] === '\\' && i + 1 < s.length) { item += s[i+1]; i += 2; continue; }
      item += s[i]; i++;
    }
    items.push(item);
    i++;
  }
  return items;
}

// === Pipeline complet ===
const raw = $input.first().json.output ?? $input.first().json.text ?? $input.first().json;

let parsed = unwrap(raw);
if (typeof parsed === 'string') {
  // Niveau 2 : escape ctrl chars
  let s = parsed;
  try { const p = JSON.parse(escapeCtrlInsideStrings(s)); if (p && p.fiche_md) parsed = p; } catch (e) {}
  // Niveau 3 : extracteur direct
  if (typeof parsed === 'string') {
    const fiche = extractField(s, 'fiche_md');
    if (fiche) {
      parsed = {
        fiche_md: fiche,
        delta: extractField(s, 'delta') || '',
        input_type: extractField(s, 'input_type') || 'autre',
        questions: extractArrayOfStrings(s, 'questions')
      };
    }
  }
}

if (!parsed || typeof parsed !== 'object' || !parsed.fiche_md) {
  const preview = (typeof raw === 'string' ? raw : JSON.stringify(raw)).slice(0, 400);
  throw new Error('LLM output non-JSON ou champ manquant : ' + preview);
}

// `parsed` est garanti d'être un objet avec ton champ clé
return [{ json: { ...parsed } }];
```

---

## Adaptation à ton schéma

Cherche les **3 occurrences** de `fiche_md` et remplace par ton champ clé métier (`summary`, `answer`, `extracted`…) :

1. Dans `unwrap()` ligne `if (x.fiche_md) return x;`
2. Dans la condition de fin `if (... !parsed.fiche_md)`
3. Dans la condition `if (p && p.fiche_md)`

Puis adapte les autres `extractField(s, '...')` à tes champs (`delta`, `input_type`, `questions` → tes noms).

---

## Tests à jouer (6 cas)

```js
// Cas 1 : output réel n8n (le plus fréquent)
const raw1 = { output: '{\n  "fiche_md": "# Titre\\nligne 2"\n}' };

// Cas 2 : vrais newlines NON échappés (Bad control character)
const raw2 = `{
  "fiche_md": "# Titre
ligne 2",
  "questions": []
}`;

// Cas 3 : objet déjà parsé par n8n
const raw3 = { fiche_md: 'x', questions: [] };

// Cas 4 : avec ```json fence
const raw4 = '```json\n{"fiche_md":"y","questions":[]}\n```';

// Cas 5 : double-encoded (JSON dans JSON dans JSON)
const raw5 = { output: JSON.stringify(JSON.stringify({fiche_md: 'double', questions: []})) };

// Cas 6 : préfixe textuel + fence
const raw6 = 'Voici :\n```json\n{"fiche_md":"noisy","questions":[]}\n```';
```

Les 6 doivent retourner `{ fiche_md: "...", questions: [...] }`.

---

## Anti-patterns

| ❌ Anti-pattern | Pourquoi |
|----------------|----------|
| `JSON.parse($input.first().json.output)` | Casse sur 5/6 cas |
| `output.replace(/\n/g, '\\n')` | Double-échappe les `\n` déjà échappés → JSON cassé différemment |
| `output.match(/{[\s\S]*}/)` puis parse | Idem échec sur newlines internes |
| Demander à l'agent de "vraiment renvoyer du JSON valide" via prompt | Marche 70% du temps, pas 100% |
| Re-générer si parse fail | Coûteux, latence x2, l'agent peut re-rater pareil |

---

## Conseil prompt côté agent

En complément du parser, ajoute toujours dans le system prompt :

```
Retourne UNIQUEMENT du JSON valide :
{ "fiche_md": "<...>", "questions": [...] }
- Pas de texte avant ou après le JSON.
- Pas de fence ```json.
- Échappe les \n dans les strings.
```

Mais NE COMPTE PAS DESSUS — le parser au-dessus est ton filet de sécurité.

---

## Pour aller plus loin

Si tu as plusieurs agents qui retournent des JSON différents, factorise le parser dans un Code node "Parse LLM Output" générique qui prend en input le nom du champ clé via un Set node amont :

```js
const keyField = $('Set Config').first().json.key_field;  // ex: "fiche_md", "summary"
// remplace les 3 occurrences de 'fiche_md' par keyField dans le code ci-dessus
```
