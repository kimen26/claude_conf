# Plugins officiels Anthropic — bonnes pratiques (2026-07-03)

> Source : `anthropics/claude-plugins-official` (cf. repos.md A.3). Install : `claude plugin install <nom>@claude-plugins-official`.
> Principe : les plugins sont lazy (description seule en contexte permanent). Le cout reel = bruit de declenchement,
> pas la memoire. **Desactiver (`claude plugin disable`) ce qui doublonne ou ne sert pas cette semaine** — reactivable en 1 commande.

## Setup Yann (etat 2026-07-03)

### Actifs

| Plugin | Usage | Declencheur |
|---|---|---|
| `claude-code-setup` | Scanne UN repo → recommande hooks/skills/MCP adaptes. Read-only | "recommend automations for this project" |
| `skill-creator` | Creer + TESTER un skill (draft → tests subagents → eval → benchmark) | `/plugin` → skill-creator |
| `claude-md-management` | Audit qualite CLAUDE.md + capture apprentissages fin de session | "audit my CLAUDE.md" · `/revise-claude-md` |
| `hookify` | Creer un hook depuis un besoin decrit en langage naturel | "hookify..." |
| `feature-dev` | Workflow feature 7 phases avec 3 sub-agents | `/feature-dev <besoin>` |
| `caveman` (communautaire JuliusBrussee) | Style reponses compact −65% tokens | `/caveman` |

### Desactives (installes, dormants — 0 token)

| Plugin | Pourquoi coupe | Reactiver quand |
|---|---|---|
| `code-review` | Triple doublon : agent `code-reviewer` + `/code-review` natif + caveman-review | jamais probablement |
| `code-simplifier` | Doublon `/simplify` natif | — |
| `code-modernization` | Cible legacy JS/Java — pas le quotidien data/SQL | migration/uplift d'un vieux codebase |
| `frontend-design` | Front ponctuel seulement (n8n-website couvre) | vrai chantier UI/UX (c'est LE top plugin officiel, 277k+ installs) |

## Regles

1. **Officiel d'abord** : avant d'ecrire un skill maison, verifier qu'un plugin officiel ne couvre pas le besoin (`/plugin` → browse).
2. **1 besoin = 1 outil** : plugin OU agent OU skill natif, jamais les trois actifs pour la meme fonction.
3. Nouveau plugin installe/retire → MAJ la table routage du skill `claude-infra` (lignes "delegue") + ce fichier.
4. Audit collisions : skill `claude-infra` ("audite ma config").
