# Phase 2 — Skills

## Inventaire

```bash
find ~/.claude/skills -name "SKILL.md" | while read f; do
  dir=$(dirname "$f")
  name=$(basename "$dir")
  mtime=$(stat -c %y "$f" 2>/dev/null || stat -f %Sm "$f")
  echo "$name | $f | $mtime"
done
```

## Checks

### 2.1 — Discovery quality
Pour chaque skill, lire `description:` du frontmatter :
- [ ] Contient des **mots-clés concrets** (pas "helper", "utils", "stuff") ?
- [ ] Mentionne **quand l'invoquer** (triggers, contextes) ?
- [ ] Écrite en **third person** ?
- [ ] ≤ 1024 chars ?

→ Description vague = skill jamais déclenché = mort-vivant.

### 2.2 — Doublons sémantiques
Comparer descriptions deux à deux. Deux skills qui couvrent ~le même domaine :
- Lequel est le plus récent / le plus utilisé ?
- L'autre peut-il être archivé ou fusionné ?

Exemples typiques :
- `cheikh` vs `challenge-roborock` (légitime : scopes distincts code vs GED)
- Deux skills "audit" ou "review" → vérifier les scopes
- Deux skills "deployment" → fusion candidate

### 2.3 — Fichiers référencés mais absents
Pour chaque SKILL.md, extraire les `[texte](references/X.md)` et `scripts/Y.py` :

```bash
grep -oP '\[[^\]]+\]\(([^)]+)\)' SKILL.md | grep -oP '\(\K[^)]+'
```

→ Vérifier que chaque cible existe sur disque.

### 2.4 — Skills jamais invoqués
Indicateurs (best-effort, pas certitude) :
- `mtime` du SKILL.md > 6 mois sans modification ET pas de mention récente dans git log
- Aucun fichier du projet ne fait référence au nom du skill

→ Marquer "candidat orphelin", pas verdict final.

### 2.5 — Body length
- SKILL.md > 500 lignes ? → ⚠️ Refactor : split en `references/`
- SKILL.md < 20 lignes ? → ⚠️ Probablement trop maigre pour être utile

## Format de sortie

```
### Phase 2 — Skills (X skills audités)
✅ markdown-lisibilite : OK (description claire, taille OK)
⚠️ helper-misc : description vague "helps with various tasks" → ne se déclenchera jamais
⚠️ deep-research : 850 lignes → split en references/ recommandé
❌ broken-skill : ref `references/missing.md` cité mais fichier absent
🟡 ancient-skill : mtime 2024-08, jamais cité ailleurs → candidat orphelin
```
