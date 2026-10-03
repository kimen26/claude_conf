# socle

Plugin Claude Code de Yann Ponaire : méthode de travail, gardes (PreToolUse), audit de conformité d'un projet,
agents, skills, gabarits et règles machine. Marketplace `yann`, repo `kimen26/claude_conf`.

## Prérequis
- Windows 11, Claude Code (CLI ou extension VS Code).
- Python 3.11+ (gardes, audit, `secrets.py`, `socle_projet.py`).
- Node (garde `sql-guard.js`).
- Optionnels : `npm i -g backlog.md` (Backlog.md, tâches), Playwright Python (preuves d'écran), `uv` (isoler `snow`).

## Installer
    claude plugin marketplace add kimen26/claude_conf
    claude plugin install socle@yann

## Mettre à jour
    claude plugin marketplace update yann
    claude plugin update socle@yann
Redémarrer la session ensuite (le hook de démarrage recopie `lib/` et les règles machine).

## Parcours
- **Projet neuf** : `/socle:nouveau-projet init` crée CLAUDE.md court, quintette `memory/`, backlog, `outils/{portes,smoke,deployer}.py`, `.env.example`.
- **Projet existant** : `/socle:nouveau-projet remise-au-pas` fait d'abord une simulation qui ne modifie rien ; après accord, relancer avec `--oui`. `--radical` pour une remise à plat. Un `AGENTS.md` sans `CLAUDE.md` est la convention du projet : pas de CLAUDE.md proposé.
- **Commandes du script** (`socle_projet.py`, chemin complet : `python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" <commande>`, dans une session Claude Code ; hors session, le dossier du plugin sous `~/.claude/plugins/cache`) : `init [chemin] [--sans-commit]` · `remise-au-pas [chemin] [--radical] [--oui]` · `deplacer <fichiers...> --raison "..." [--remplace-par "..."] [--racine .]` (déplace dans `_a_supprimer/<date>/` avec `MANIFESTE.md`, ne supprime jamais) · `venv [chemin] [--oui]` (recrée `.venv` depuis `requirements-dev.txt`, jamais copié ; simulation sans `--oui`).
- **Une tâche** : `/socle:tache` crée la tâche (numéro pris par l'outil) et la fait avancer dans la marche en 8 temps (reconnaissance et plan, exécution, DoD, preuve rejouée, relecture, verdict, mise en service, capitalisation ; voie courte sans fiche si le diff se décrit en une phrase ; détail dans `rules/methode.md` du plugin, que `Glob **/socle/*/rules/methode.md` sous `~/.claude/plugins/cache` retrouve), puis `/socle:livrer <numéros>` commite par chemins listés, pousse, déploie, passe en Livre.
- **Secrets** : `/socle:secrets` (`inventaire`, `verifier`, `poser`, `ssl`, `purger`, `snow`). Un secret est une variable utilisateur ; aucune commande ne lit ni n'affiche une valeur.
- **Les 21 contrôles** : `garde_socle.py` audite un projet (secrets, `.mcp.json`, CLAUDE.md, memory/, backlog, portes, venv, BOM, règles machine). Liste et ordre de traitement dans `skills/nouveau-projet/SKILL.md`. Audit manuel : `python hooks/scripts/garde_socle.py --complet [chemin]`.
- **Règles machine** : livrées par le plugin dans `rules/machine/` (contradicteur, conception, memoire-projet, interaction-style, pas-d-artifact) et copiées vers `~/.claude/rules/` à chaque démarrage seulement si absentes. Jamais d'écrasement ni de suppression : une copie différente est conservée et signalée par la garde S-72.
- **HO** : la même tâche hors projet, un fichier `%LOCALAPPDATA%\socle\taches\AAAA-MM-JJ_<nom>.md`, même gabarit, sans Backlog (vocabulaire dans `rules/methode.md`).

## Structure
- `.claude-plugin/plugin.json` : manifeste
- `hooks/hooks.json` : câblage ; `hooks/scripts/` : session_start, garde_socle, garde_outils, gardes rapatriées
- `lib/` : bibliothèques partagées, synchronisées vers `${CLAUDE_PLUGIN_DATA}/lib/` au démarrage
- `rules/` : DIGEST.md (injecté au démarrage), méthode, doctrines ; `rules/machine/` : règles copiées vers `~/.claude/rules/`
- `agents/` (5) · `skills/` (nouveau-projet, tache, livrer, recette-ecran, preuve-navigateur, secrets) · `gabarits/` : modèles copiés par `init`
- `tests/` : `python -m pytest plugins/socle/tests`

## Versionner
Toute modification du plugin impose un bump de `version` dans `plugin.json` ET `marketplace.json` (même valeur), sinon `claude plugin update` répond « already at the latest version » et le cache garde l'ancien code.

## Secrets
- Voies, dans cet ordre : (1) écrire `NOM=valeur` dans `%LOCALAPPDATA%\socle\a_poser.env` (`notepad "$env:LOCALAPPDATA\socle\a_poser.env"`), posé à la session suivante ou par `secrets.py poser --fichier` ; (2) l'écran Windows des variables (`rundll32 sysdm.cpl,EditEnvironmentVariables`). `poser NOM` au clavier : vrai terminal seulement, jamais depuis le chat. Le nom figure au registre `rules/secrets-registre.md`.
- Jamais dans `settings.json`, `.claude.json`, un `.bak` ou un `secrets.ps1` : les gardes S-30 à S-37 et `garde_outils` refusent.
- Projet : `.env` git-ignoré + `.env.example` versionné. MCP : `${NOM}` dans `.mcp.json`. Snowflake : SSO `connections.toml` seul.
- `purger` déplace dans `~/.claude/_a_supprimer/`, ne supprime jamais. Doctrine : `rules/secrets.md` ; emplacements : `rules/emplacements.md`.
