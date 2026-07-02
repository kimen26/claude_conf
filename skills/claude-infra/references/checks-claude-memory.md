# Phase 5 — CLAUDE.md & Memory

## Inventaire CLAUDE.md

```bash
find . -name "CLAUDE.md" -not -path "*/node_modules/*" -not -path "*/_archive/*"
```

## Checks CLAUDE.md

### 5.1 — Hiérarchie & taille
- [ ] Racine `CLAUDE.md` < 100 lignes ? (recommandation Anthropic : racine légère, re-injectée après /compact)
- [ ] Pôles ont leur propre `CLAUDE.md` auto-loadé ?
- [ ] Pas de duplication massive racine vs pôle ?

### 5.2 — Refs agents/skills cités
Pour chaque mention `[`agent-name`](.claude/agents/X.md)` ou `[skill](...)` :
- [ ] Cible existe ?
- [ ] Cohérent avec Phase 3 (agents) et Phase 2 (skills) ?

### 5.3 — Triggers signal-detector
Si CLAUDE.md cite un hook `signal-detector.ps1` ou similaire :
- [ ] Hook existe et déclaré dans settings.json (cf. Phase 4) ?

## Inventaire Memory

```bash
# Memory projet
ls memory/ 2>/dev/null

# Auto-memory user-level pour ce projet
ls ~/.claude/projects/<projet-hash>/memory/ 2>/dev/null
```

## Checks Memory

### 5.4 — MEMORY.md = index intègre
Le `MEMORY.md` cite des fichiers `.md` voisins. Pour chaque ref :
- [ ] Le fichier existe ?
- [ ] Inversement : tout `.md` du dossier memory est-il indexé dans MEMORY.md ?

```bash
# Refs sortantes de MEMORY.md
grep -oP '\[[^\]]+\]\([^)]+\.md\)' memory/MEMORY.md

# Fichiers réels du dossier
ls memory/*.md
```

### 5.5 — Knowledge rot
Pour chaque fichier memory :
- [ ] Date absolue mentionnée > 3 mois → encore valide ?
- [ ] "TODO en attente droits" → toujours en attente ? Si oui depuis quand ?
- [ ] Feedback marqué "incident XXXX-XX-XX" → toujours pertinent ou résolu ?

### 5.6 — Doublons sémantiques
Deux fichiers memory qui disent ~la même chose → fusion candidate.

## Format de sortie

```
### Phase 5 — CLAUDE.md & Memory
✅ CLAUDE.md racine : 92 lignes, OK
✅ game/CLAUDE.md : auto-loadé, cohérent
⚠️ MEMORY.md cite feedback_old_pattern.md → fichier absent (déplacé vers _archive ?)
🟡 memory/project_old_idea.md : "Non validé" depuis 2026-04-24, statut à clarifier
⚠️ memory/todo_skill_name_sonority_check.md : TODO "en attente droits" depuis 6 semaines
```
