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
- `rules/` : règles (DIGEST.md injecté au démarrage) · `agents/` (7 agents) · `skills/` (nouveau-projet, tache, livrer, recette-ecran, preuve-navigateur, secrets) · `gabarits/` : modèles copiés par `init`
- `tests/` : `python -m pytest plugins/socle/tests`
Audit manuel : `python hooks/scripts/garde_socle.py --complet [chemin]`.

## Versionner
Toute modification du plugin impose un bump de `version` dans `plugin.json` ET `marketplace.json` (même valeur), sinon `claude plugin update` répond « already at the latest version » et le cache garde l'ancien code.

## Secrets
- Un secret est une variable d'environnement utilisateur. Voies, dans cet ordre : (1) écrire `NOM=valeur` dans `%LOCALAPPDATA%\socle\a_poser.env` (ouvert par `notepad "$env:LOCALAPPDATA\socle\a_poser.env"`), posé à la session suivante ou par `secrets.py poser --fichier` ; (2) l'écran Windows des variables utilisateur (`rundll32 sysdm.cpl,EditEnvironmentVariables`). `poser NOM` au clavier = seulement depuis un vrai terminal, jamais depuis le chat (Claude n'a pas de clavier). Le nom est au registre `rules/secrets-registre.md` (statut `requis` ou `reserve`).
- Jamais dans `settings.json`, `.claude.json`, un `.bak` ou un `secrets.ps1` : les gardes S-30 à S-37 et `garde_outils` le refusent.
- Projet : `.env` git-ignoré + `.env.example` versionné. MCP : `${NOM}` dans `.mcp.json`. Snowflake : SSO `connections.toml` seul.
- Commandes : `inventaire`, `verifier`, `poser` (`--fichier`), `ssl`, `purger`, `snow`. Doctrine complète : `rules/secrets.md`. Emplacements (`C:/tmp` interdit) : `rules/emplacements.md`.
- Aucune commande ne lit ni n'affiche une valeur ; `purger` déplace dans `~/.claude/_a_supprimer/`, ne supprime jamais.
