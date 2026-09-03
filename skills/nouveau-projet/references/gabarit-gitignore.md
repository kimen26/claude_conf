# Gabarits fichiers de départ

## .gitignore

```
.env
*.env
!*.env.example
inbox/
_a_supprimer/
_corbeille*/
recette/                 # captures de la recette visuelle
state.json               # storage state Playwright (SSO) — jamais commité
.claude/settings.local.json
node_modules/
__pycache__/
dist/
build/
```

## memory/MEMORY.md

```markdown
# MEMORY — <NomProjet>
_État courant. Réécrit en fin de session, jamais un journal._

## Où on en est
- <une ligne par chantier vivant>

## Pointeurs
- <fichier> — <ce qu'on y trouve>
```

## memory/TODO.md

```markdown
# TODO — lanes
_Une session = une lane. Marquer (en cours) à l'ouverture, libérer à la fin._

## Lane A — <nom>
- [ ] <tâche>
```

## memory/DECISIONS.md et memory/LESSONS.md

```markdown
# DECISIONS
_D-NNN : relire le fichier au moment d'écrire pour prendre le numéro suivant._

## D-001 — <titre> (AAAA-MM-JJ)
<contexte, arbitrage, pourquoi>
```

(même structure pour LESSONS.md avec L-NNN : contexte, cause, correction, mnémonique)
