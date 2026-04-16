---
name: n8n-website
description: "Generate complete HTML websites hosted via n8n webhook + Code node JS. Auto-triggers on: n8n site, n8n landing page, n8n HTML, n8n webhook site, n8n frontend, heberger site n8n, Code node HTML, site via webhook. Handles template literal escaping, CSS themes, multi-page layouts, Model Selector, MCP tools, validation, and n8n workflow structure."
---

# n8n Website — Site web via Webhook + Code Node

> **Pattern** : Un workflow n8n sert un site web complet via un webhook GET.
> Le HTML est genere par un Code node JS et retourne par un Respond node.
> Ce skill couvre les contraintes, le format obligatoire, et les bonnes pratiques.

---

## Architecture du workflow

### Option A — Monolithique (sites simples, < 15KB)
```
Webhook GET → Code (1 seul, retourne { html }) → Serve HTML
```

### Option B — Pipeline multi-nodes (recommande pour sites > 15KB)
```
Webhook GET → Code: CSS → Code: Pages → Code: JS → Code: Assemble → Serve HTML
```
Chaque Code node retourne un fragment (`{ css }`, `{ pageHtml }`, `{ js }`).
Le node Assemble lit les precedents via `$('NodeName').first().json.xxx` et combine le tout.

**Avantages** : chaque fichier < 300 lignes, modification ciblee, ajout de pages facile.
**Compromis** : +100-200ms de latence (acceptable avec cache 5min).

### Option C — 2 workflows separes (site + API)
Pour les sites avec chatbot ou API backend :
- **Workflow UI** : Webhook GET → pipeline Code nodes → Serve HTML
- **Workflow Agent** : Webhook POST → Normalise → AI Agent → Respond JSON

### Nodes necessaires

| Node | Type | Config cle |
|------|------|------------|
| **Webhook** | `n8n-nodes-base.webhook` | `path`, `httpMethod: GET`, `responseMode: responseNode` |
| **Code** | `n8n-nodes-base.code` | `jsCode` contenant le template literal HTML |
| **Respond** | `n8n-nodes-base.respondToWebhook` | `respondWith: text`, body `={{ $json.html }}`, headers Content-Type + Cache-Control |
| **Model Selector** | `@n8n/n8n-nodes-langchain.modelSelector` | Route entre modeles selon condition (ex: flag useSonnet) |
| **MCP Client** | `@n8n/n8n-nodes-langchain.mcpClientTool` | Connecte un serveur MCP comme tool de l'Agent (ex: design system) |

---

## Format obligatoire du Code node

```js
// Variables interpolees declarees EN DEHORS du template literal
const apiUrl = 'https://mon-n8n.example.com/webhook/mon-api';

const html = `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Mon Site</title>
<style>
/* CSS ici — pas de </style> a echapper dans un template literal */
</style>
</head>
<body>
<!-- HTML ici -->
<script>
// JS client ici
// IMPORTANT: fetch vers ${apiUrl} sera interpole
<\/script>
</body>
</html>`;

return [{ json: { html } }];
```

---

## Regles d'echappement CRITIQUES

### Regle 1 — `<\/script>` (BLOQUANT)

**TOUJOURS** echapper `</script>` en `<\/script>` dans le template literal.

```js
// CASSE (silencieusement — pas d'erreur, pas d'output) :
const html = `...<script src="marked.min.js"></script>...`;

// CORRECT :
const html = `...<script src="marked.min.js"><\/script>...`;
```

**Pourquoi** : Le parseur HTML de n8n voit `</script>` et croit que le bloc `<script>` du node n8n est termine. Le code JS est tronque avant le `return`. Resultat : pas d'output, pas d'erreur visible.

**Verification** : Chercher tous les `</script>` dans le code genere et les remplacer par `<\/script>`.

### Regle 2 — `<\/style>` (par securite)

Echapper aussi `</style>` en `<\/style>` si le style est dans le template literal. Meme raison que `</script>`.

### Regle 2b — Données riches embarquées : utiliser base64 (CRITIQUE)

**JAMAIS** embarquer du JSON/HTML contenant `'`, `"` ou `\` dans un template literal via `JSON.parse('...')`.
Le template literal est une couche d'interprétation : les escapes sont transformés AVANT que le code client ne tourne.

| Dans le fichier `.js` | Template literal produit | Résultat |
|-----------------------|--------------------------|----------|
| `'` directement | `'` | 💥 casse la string outer |
| `\u0027` | `'` (template interprète `\uXXXX`) | 💥 idem |
| `\\u0027` | `\u0027` → JS interprète → `'` | 💥 idem |
| `\"` de json.dumps | `"` → casse le JSON à la 1ère `"` dans HTML | 💥 position 2620 |
| **`atob('BASE64')`** | alphabet A-Za-z0-9+/= uniquement | ✅ SAFE |

**Solution unique et définitive : base64**

```python
# Génération (Python) :
import json, base64
clean_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
b64 = base64.b64encode(clean_json.encode('utf-8')).decode('ascii')
line = f"var DATA=JSON.parse(atob('{b64}'));"
```

```js
// Dans le HTML client — toujours safe :
var FICHES=JSON.parse(atob('eyJGMSI6eyJ0aXRs...'));
```

**Règle** : Dès qu'un objet `> 500 chars` avec du texte riche (HTML, FR, apostrophes) doit être embarqué → **base64 systématique**. Taille +33% mais zéro bug.

### Regle 3 — `${}` interpolation

Les expressions `${...}` dans le template literal sont evaluees par JS. C'est utile pour les variables (`${apiUrl}`) mais dangereux si le HTML contient des `${...}` non voulus.

```js
// Variable declaree avant le template :
const apiUrl = 'https://...';

// Interpolee dans le HTML :
const html = `...fetch('${apiUrl}/chat', ...)...`;

// Si le HTML contient un $ literal suivi de { :
const html = `...cost: \${amount}...`;  // echapper avec backslash
```

### Regle 4 — Unicode double-echappement

Dans les strings JS A L'INTERIEUR du template literal, les sequences `\uXXXX` sont interpretees une premiere fois par le template literal, puis une deuxieme fois par le JS client.

```js
// Dans le JS client embarque dans le HTML :
const html = `...<script>
var msg = '\\u2014';  // tiret cadratin — double backslash
var warn = '\\u26a0'; // symbole warning
<\/script>...`;
```

### Regle 5 — Guillemets et backticks

```js
// Backticks dans le HTML : echapper avec backslash
const html = `...\`code\`...`;

// Ou utiliser des entites HTML :
const html = `...&#96;code&#96;...`;

// Guillemets simples/doubles : OK sans echappement dans un template literal
const html = `...<div class="foo" data-bar='baz'>...`;
```

### Regle 6 — Caracteres d'echappement JS dans template literals (\n, \t, etc.)

**JAMAIS** utiliser directement `\n`, `\t`, `\r` dans un template literal n8n. Ces sequences sont interpretees comme des retours à la ligne/tabulations LITTERAUX dans le code HTML genere, cassant la syntaxe JS.

```js
// CASSE :
const html = `<script>
var lines=content.split('\n');  // 💥 Le \n devient un vrai retour à la ligne
<\/script>`;

// CORRECT — Utiliser String.fromCharCode() :
const html = `<script>
var lines=content.split(String.fromCharCode(10));  // 10 = code ASCII de \n
<\/script>`;

// Alternative acceptable — Concatenation de caracteres :
var lines=content.split(String.fromCharCode(10));
```

**Autres caracteres problematiques** :
- `\n` (newline) → `String.fromCharCode(10)`
- `\t` (tab) → `String.fromCharCode(9)`
- `\r` (carriage return) → `String.fromCharCode(13)`

**Verification** : Chercher ces patterns dans le code généré :
- `split('\n')` → `split(String.fromCharCode(10))`
- `join('\n')` → `join(String.fromCharCode(10))`
- `replace('\n'` → `replace(String.fromCharCode(10)`
- `.split('\`, `.join('\`, `replace('\`

### Regle 7 — Regex dans template literals (CRITIQUE — piege silencieux)

**TOUJOURS** doubler les backslashes dans les regex ecrites a l'interieur d'un template literal.
Le template literal interprete `\s` comme un escape sequence (qui produit juste `s`), pas comme la classe regex `\s`.

```js
// CASSE (silencieusement — la regex ne matche plus rien) :
const html = `<script>
var m = line.match(/^#{1,3}\s+.+\{#anchor-([\w-]+)\}/);  // 💥 \s → "s", \w → "w", \{ → "{"
<\/script>`;

// CORRECT — doubler les backslashes :
const html = `<script>
var m = line.match(/^#{1,3}\\s+.+\\{#anchor-([\\w-]+)\\}/);  // ✅ \\s → \s (classe regex)
<\/script>`;
```

**Pourquoi c'est un piege silencieux** : pas d'erreur JS, pas d'erreur n8n, la regex compile et s'execute — elle ne matche simplement jamais. Le code tombe dans le fallback sans aucun message.

**Caracteres concernes** (dans les regex a l'interieur d'un template literal) :
- `\s` (whitespace) → `\\s`
- `\w` (word char) → `\\w`
- `\d` (digit) → `\\d`
- `\b` (word boundary) → `\\b`
- `\{` `\}` (braces) → `\\{` `\\}`
- `\(` `\)` (parens) → `\\(` `\\)`
- **`\*` (etoile echappee) → `\\*`** — cas CRASH, voir ci-dessous

**Cas CRASH avec `\*` (ReferenceError: g is not defined)** :

```js
// CASSE — crash navigateur, pas d'erreur n8n :
const html = `<script>
def=def.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
// Template literal produit : /**([^*]+)**/g
// Le navigateur lit /** comme un commentaire JS block !
// Le g apres le commentaire est un identifiant → ReferenceError: g is not defined
<\/script>`;

// CORRECT :
const html = `<script>
def=def.replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>');
// Produit : /\*\*([^*]+)\*\*/g ✅
<\/script>`;
```

**Verification** : chercher tous les `line.match(`, `str.match(`, `.replace(/`, `new RegExp(` dans le template literal et verifier que chaque backslash est double.

**Astuce** : si la regex est complexe, la definir via `new RegExp()` avec une string double-echappee, ou la stocker dans une variable hors du template literal.

---

## Architecture CSS pour les themes

**NE PAS** dupliquer le CSS pour chaque theme. Utiliser des CSS custom properties.

```css
/* Definition des themes via data-attribute */
[data-theme="default"] {
  --bg: #001A3A;
  --fg: #e0e6ed;
  --accent: #69BE28;
  --font: 'DM Sans', sans-serif;
}
[data-theme="corporate"] {
  --bg: #1251BD;
  --fg: #ffffff;
  --accent: #ffffff;
  --font: 'Roboto', sans-serif;
}

/* Un seul set de classes — jamais duplique */
.header { background: var(--bg); color: var(--fg); font-family: var(--font); }
.btn { background: var(--accent); color: var(--bg); }
```

```js
// Switch de theme en JS client
function setTheme(name) {
  document.documentElement.setAttribute('data-theme', name);
  localStorage.setItem('theme', name);
}
// Restore au chargement
const saved = localStorage.getItem('theme');
if (saved) setTheme(saved);
```

**Regles** :
- Variables CSS courtes (--bg, --fg, --accent, --font) pour limiter la taille
- Un theme = un bloc `[data-theme="x"]` avec ~10-15 variables
- Classes CSS generiques, jamais prefixees par le nom du theme
- Theme sauvegarde en localStorage
- Favicon dynamique via SVG data URI (changer couleur selon theme)

---

## Structure HTML recommandee

```html
<!DOCTYPE html>
<html lang="fr" data-theme="default">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>Titre</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...">
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
  <style>
    /* Themes */
    /* Reset minimal */
    /* Layout */
    /* Components */
    /* Responsive */
  </style>
</head>
<body>
  <!-- Structure HTML -->
  <script>
    // Libraries externes (marked.js, etc.)
  <\/script>
  <script>
    // Application JS
  <\/script>
</body>
</html>
```

**Optimisations de taille** :
- Noms de classes courts (.hdr, .msg, .btn au lieu de .header, .message, .button)
- Pas de commentaires dans le CSS/JS final
- CSS minifie (pas de lignes vides, proprietes sur une ligne)
- JS minifie (noms de variables courts)
- Viser < 25 KB pour le HTML complet (maintenabilite)

---

## Multi-pages et modes de layout

Pour gerer plusieurs "pages" dans un seul HTML (SPA client-side) :

```js
// Modes de layout via classe CSS sur le container
window.setLayout = function(mode) {
  var p = document.getElementById('page');
  p.classList.remove('collapsed', 'training');
  if (mode === 'collapsed') p.classList.add('collapsed');
  if (mode === 'training') p.classList.add('training');
};
```

```css
/* Normal: hero 42% + chat 58% */
.hero { flex: 0 0 42%; }

/* Training: panel 66% + chat 34% */
.page.training .hero { flex-basis: 66% !important; }
.page.training .chat { flex-basis: 34%; }

/* Focus: chat 100% */
.page.collapsed .hero { flex-basis: 0 !important; opacity: 0; }
```

**Swapper le contenu** du panel gauche selon le mode :
```css
.page.training .hc-default { display: none; }
.page.training .hc-training { display: flex !important; }
```

---

## Chat UI avec contexte

Si le site inclut un chat, le frontend peut envoyer du **contexte** avec chaque message :

```js
var payload = { message: text, sessionId: sid };
// En mode Training, ajouter le contexte de la page
if (currentLayout === 'training') {
  payload.context = {
    currentPage: 'training',
    userName: document.getElementById('user-input').value,
    formData: { /* donnees du formulaire */ }
  };
}
// Toggle modele (ex: Sonnet via bouton cache)
if (useSonnet) payload.useSonnet = true;
fetch(apiUrl, { method: 'POST', body: JSON.stringify(payload) });
```

**Cote n8n (workflow Agent)** :
- Le node **Normalise Input** extrait `context` et `useSonnet` du body
- Le **system prompt** de l'Agent recoit `contextPrompt` (page, user, contenu)
- Le **Model Selector** route vers Haiku (defaut) ou Sonnet (si `useSonnet`)
- Les tools (**DOC_SEARCH**, **MCP Client**) sont connectes a l'Agent

```
Webhook POST → Normalise Input → AI Agent ← Model Selector ← Haiku / Sonnet
                                     ↑
                                     ├── DOC_SEARCH (Cortex Search)
                                     ├── MCP Client (design system, etc.)
                                     └── Memory (buffer window)
```

---

## Validation avant livraison

### Checklist obligatoire

1. **Echappement** :
   - [ ] Tous les `</script>` remplaces par `<\/script>`
   - [ ] Tous les `</style>` remplaces par `<\/style>`
   - [ ] Unicode double-echappe dans le JS embarque
   - [ ] Pas de `${}` non voulu
   - [ ] **Regex** : tous les `\s`, `\w`, `\d`, `\b`, `\{`, `\}` doubles dans les regex (`\\s`, `\\w`, etc.) — cf. Regle 7
   - [ ] Pas de `\n`, `\t` dans les strings — cf. Regle 6

2. **Format n8n** :
   - [ ] Le code commence par des declarations de variables (si besoin)
   - [ ] Le HTML est dans `const html = \`...\`;`
   - [ ] Le code se termine par `return [{ json: { html } }];`

3. **Test syntaxe** :
   ```bash
   # Tester que le JS est valide
   node -e "$(cat mon_code.js)" > /dev/null
   # Verifier la taille
   wc -c mon_code.js
   ```

4. **Fonctionnel** :
   - [ ] Le HTML s'affiche correctement dans un navigateur
   - [ ] Les themes switchent sans erreur
   - [ ] Le chat (si present) envoie et recoit des messages
   - [ ] Le favicon s'affiche
   - [ ] Responsive (mobile + desktop)

---

## Workflow n8n complet (export JSON)

Template minimal pour un site statique via webhook :

```json
{
  "nodes": [
    {
      "parameters": {
        "path": "mon-site",
        "responseMode": "responseNode",
        "options": { "allowedOrigins": "*" }
      },
      "name": "Webhook Landing",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "webhookId": "unique-id"
    },
    {
      "parameters": {
        "jsCode": "const html = `<!DOCTYPE html>...HTML...<\\/script></html>`;\nreturn [{ json: { html } }];"
      },
      "name": "Generate HTML",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "={{ $json.html }}",
        "options": {
          "responseHeaders": {
            "entries": [
              { "name": "Content-Type", "value": "text/html; charset=utf-8" },
              { "name": "Cache-Control", "value": "public, max-age=300" }
            ]
          }
        }
      },
      "name": "Serve HTML",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1
    }
  ],
  "connections": {
    "Webhook Landing": { "main": [[{ "node": "Generate HTML", "type": "main", "index": 0 }]] },
    "Generate HTML": { "main": [[{ "node": "Serve HTML", "type": "main", "index": 0 }]] }
  }
}
```

---

## Erreurs courantes

| Symptome | Cause | Solution |
|----------|-------|----------|
| Webhook retourne vide, pas d'erreur | `</script>` non echappe | Remplacer par `<\/script>` |
| `${variable}` affiche "undefined" | Variable pas declaree avant le template | Declarer `const variable = '...'` avant `const html = ...` |
| Caracteres bizarres dans le HTML | Unicode simple-echappe | Double-echapper : `\\uXXXX` |
| CSS themes ne marchent pas | Classes dupliquees par theme | Utiliser CSS custom properties |
| Site trop gros pour n8n | HTML > 50KB (rare) | Minifier CSS/JS, mutualiser les themes |
| CORS bloque les appels API | Headers manquants sur Respond | Ajouter `Access-Control-Allow-Origin: *` |
| **Regex ne matche rien, pas d'erreur** | **`\s` `\w` `\d` dans regex a l'interieur d'un template literal** | **Doubler : `\\s` `\\w` `\\d` — cf. Regle 7. Piege silencieux : la regex compile mais `\s` devient `s` litteral** |
| Logique JS tombe toujours dans le fallback | Idem — regex cassee par template literal | Verifier TOUTES les regex dans le template, doubler les backslashes |

---

## Effets visuels et animations

### Confettis de célébration (canvas-confetti)

Pour ajouter une animation de confettis (ex: récompense quiz, succès) :

```js
// 1. Ajouter le canvas et la librairie CDN dans le HTML
const html = `...
<canvas id="confetti-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;display:none"></canvas>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"><\/script>
...`;

// 2. Déclencher l'animation
if(typeof confetti!=='undefined'){
  var originX=Math.random()>0.5?0:1; // gauche ou droite aléatoire
  confetti({
    particleCount:100,
    spread:70,
    origin:{x:originX,y:0.6},
    gravity:1.2,
    scalar:1.2,
    colors:['#1251BD','#69BE28','#FBBC42','#E63946']
  });
}
```

**Configuration recommandée** :
- `particleCount` : 50-150 (plus = plus lourd)
- `spread` : 60-90 (angle de dispersion)
- `origin.x` : 0 (gauche) ou 1 (droite) pour explosion latérale
- `gravity` : 1-1.5 (chute réaliste)
- `scalar` : 0.8-1.5 (taille des confettis)

---

## Exemples de projets utilisant ce pattern

- **SAN DOKU** (Infopro Digital) — Chatbot doc technique, 4 themes, i18n FR/EN, pipeline 4 Code nodes, Training mode (66/34), Model Selector (Haiku/Sonnet), MCP Cobalt, confettis quiz, 2 workflows separes (UI + Agent)
