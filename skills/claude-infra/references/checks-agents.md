# Phase 3 — Agents

## Inventaire

```bash
find ~/.claude/agents .claude/agents -name "*.md" 2>/dev/null
```

## Checks

### 3.1 — Frontmatter strict (cf. Phase 1)
Voir [checks-frontmatters.md](checks-frontmatters.md). Rappel : `:` interne, `—`, `×` non quoté → agent mort silencieux.

### 3.2 — Refs croisées CLAUDE.md → agent
Pour chaque agent mentionné dans un `CLAUDE.md` (racine ou pôle) :
- [ ] Le fichier `.claude/agents/<nom>.md` existe-t-il ?
- [ ] Le frontmatter est-il chargeable (cf. Phase 1) ?

```bash
# Agents mentionnés dans CLAUDE.md
grep -roP '\[`[^`]+`\]\(\.claude/agents/[^)]+\)' --include=CLAUDE.md .

# Comparer à la liste réelle
ls .claude/agents/*.md
```

### 3.3 — Refs croisées agent → agent
Un agent parent (`pole-a-pmo`) cite ses enfants (`pole-a-tile-pmo`, `pole-a-mj-pmo`) :
- [ ] Les enfants existent-ils ?
- [ ] Les enfants pointent-ils vers le bon parent ?

### 3.4 — Agents orphelins
Agent présent sur disque mais cité nulle part (ni CLAUDE.md, ni autres agents, ni hooks) :
- Si actif récent (mtime < 1 mois) → ❓ à qualifier (WIP ?)
- Sinon → 🟡 candidat archive

### 3.5 — Modèle déclaré vs disponible
Si l'agent déclare `model: opus` ou `model: haiku` :
- [ ] Le modèle est-il dans la liste actuelle (opus-4-7, sonnet-4-6, haiku-4-5) ?
- [ ] Pas de modèle déprécié ?

## Format de sortie

```
### Phase 3 — Agents (X agents audités)
✅ pole-a-pmo : OK (parent valide, 3 enfants présents)
❌ CRITIQUE pole-b-localisation : `:` dans description → frontmatter cassé
⚠️ CLAUDE.md cite `tile-master` mais .claude/agents/tile-master.md absent
🟡 old-experiment-agent : aucune ref ailleurs, mtime 2024-11 → archive candidate
```
