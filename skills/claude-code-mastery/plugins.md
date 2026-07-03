# Plugins officiels Anthropic — bonnes pratiques (2026-07-03)

> Source : `anthropics/claude-plugins-official` (cf. repos.md A.3). Install : `claude plugin install <nom>@claude-plugins-official`.
> Principe : les plugins sont lazy (description seule en contexte permanent). Le cout reel = bruit de declenchement,
> pas la memoire. **Desactiver (`claude plugin disable`) ce qui doublonne ou ne sert pas cette semaine** — reactivable en 1 commande.

## Setup Yann (etat 2026-07-03, rev2 : tout actif)

### Le kit de base (90% de l'usage)

| Plugin | Commande exacte | Quand |
|---|---|---|
| `feature-dev` | `/feature-dev <besoin>` | LE workflow dev : 7 phases guidees, 3 sub-agents (explorer/architect/reviewer) |
| `claude-code-setup` | "recommend automations for this project" (pas de slash) | 1 fois par nouveau repo |
| `claude-md-management` | `/revise-claude-md` · "audit my CLAUDE.md" | Fin de session / maintenance memoire projet |

Sequence debutant : nouveau repo → recommend automations → `/feature-dev X` → `/revise-claude-md`.

### Quand le besoin arrive

| Plugin | Commandes | Quand |
|---|---|---|
| `skill-creator` | "help me create a skill for X" | Meme explication repetee 3 fois → skill (intent → draft → test → eval) |
| `hookify` | `/hookify` · `/hookify:list` · `/hookify:configure` · `/hookify:help` | "Bloque-moi ca a chaque fois" → hook. Sait analyser la conversation |
| `code-review` | `/code-review` | Review de diff/PR. NB : doublonne agent `code-reviewer` + caveman-review — choisir UN par review |
| `code-simplifier` | agent (pas de slash) | Simplifier du code existant. NB : `/simplify` natif fait proche |
| `code-modernization` | `/modernize-assess` · `-map` · `-brief` · `-extract-rules` · `-preflight` · `-transform` · `-uplift` · `-harden` · `-reimagine` · `-status` | Migration/uplift legacy — pipeline complet en 10 commandes |
| `frontend-design` | skill auto (pas de slash) | Chantier UI/UX — LE top plugin officiel (277k+ installs) |
| `caveman` (communautaire JuliusBrussee) | `/caveman` · `/caveman-stats` | Style compact −65% tokens |

## Regles

1. **Officiel d'abord** : avant d'ecrire un skill maison, verifier qu'un plugin officiel ne couvre pas le besoin (`/plugin` → browse).
2. **1 besoin = 1 outil** : plugin OU agent OU skill natif, jamais les trois actifs pour la meme fonction.
3. Nouveau plugin installe/retire → MAJ la table routage du skill `claude-infra` (lignes "delegue") + ce fichier.
4. Audit collisions : skill `claude-infra` ("audite ma config").
