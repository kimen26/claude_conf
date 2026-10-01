# socle

Plugin Claude Code de Yann Ponaire : gardes (PreToolUse), audit de conformité d'un projet,
agents, skills et gabarits.

## Installer
    claude plugin marketplace add kimen26/claude_conf
    claude plugin install socle@yann

## Mettre à jour
    claude plugin marketplace update yann
    claude plugin update socle@yann
Redémarrer la session ensuite.

## Structure
- `.claude-plugin/plugin.json` : manifeste
- `hooks/hooks.json` : câblage ; `hooks/scripts/` : session_start, garde_socle, garde_outils, gardes rapatriées
- `lib/` : bibliothèques partagées, synchronisées vers `${CLAUDE_PLUGIN_DATA}/lib/` au démarrage
- `rules/` : règles (DIGEST.md injecté au démarrage) · `agents/` (7 agents) · `skills/` (nouveau-projet, tache, livrer, recette-ecran, preuve-navigateur) · `gabarits/` : modèles copiés par `init`
- `tests/` : `python -m pytest plugins/socle/tests`
Audit manuel : `python hooks/scripts/garde_socle.py --complet [chemin]`.

## Mettre à jour
Toute modification du plugin impose un bump de `version` dans `plugin.json` ET `marketplace.json` (même valeur), sinon `claude plugin update` répond « already at the latest version » et le cache garde l'ancien code.
