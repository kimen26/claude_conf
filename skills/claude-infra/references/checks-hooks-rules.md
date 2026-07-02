# Phase 4 — Hooks & Rules

## Inventaire hooks

```bash
# settings.json déclare les hooks
cat ~/.claude/settings.json | grep -A 30 '"hooks"'
cat .claude/settings.json 2>/dev/null | grep -A 30 '"hooks"'

# Scripts hooks sur disque
ls ~/.claude/hooks 2>/dev/null
ls .claude/hooks 2>/dev/null
```

## Checks hooks

### 4.1 — Hooks déclarés → scripts existants
Pour chaque hook dans `settings.json` :
- [ ] Le chemin du script référencé existe ?
- [ ] Le script est-il exécutable ? (chmod sur Unix, .ps1/.sh approprié sur Windows)

### 4.2 — Scripts hooks orphelins
Script dans `.claude/hooks/` mais pas déclaré dans `settings.json` :
- → 🟡 candidat archive ou hook désactivé

### 4.3 — Hooks jamais déclenchés
Indicateur best-effort : si le hook a un fichier log et il est vide / vieux :
- `bot.err.log`, `signal-detector.log`, etc.
- → ⚠️ vérifier si le hook s'active vraiment

## Inventaire rules

```bash
ls ~/.claude/rules 2>/dev/null
```

## Checks rules

### 4.4 — Rules path-scoped
Une rule avec frontmatter `applies-to: src/**/*.ts` :
- [ ] Le pattern matche-t-il au moins un fichier du projet courant ?
- [ ] Si pattern jamais matché → rule morte

### 4.5 — Rules sans path-scoping (globales)
Rules chargées partout (pas de `applies-to`) :
- [ ] Contenu est-il toujours pertinent ?
- [ ] Pas de contradiction avec une CLAUDE.md projet ?

## Format de sortie

```
### Phase 4 — Hooks & Rules
✅ settings.json : 3 hooks déclarés, tous scripts présents
❌ CRITIQUE PreToolUse → .claude/hooks/missing.ps1 absent
🟡 .claude/hooks/old-validator.ps1 : pas déclaré, candidat archive
✅ rules/coding-style.md : globale, contenu pertinent
⚠️ rules/legacy-php.md : applies-to=*.php, aucun .php dans projet → rule morte
```
