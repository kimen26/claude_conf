# Socle actif v2026.10.13

Méthode complète : ${CLAUDE_PLUGIN_ROOT}/rules/methode.md (deux voies, huit temps, statuts, transitions).

Les 6 règles qui tiennent tout
1. Cerveau d'abord, mains si c'est moins cher : voie courte (diff en une phrase) sans fiche ni agent, sinon `executant`.
2. Une seule fiche, la tâche (Backlog dans un projet, HO hors projet) ; vocabulaire : tâche, porte, preuve, verdict, lane.
3. Séquentiel par défaut ; parallèle seulement si périmètres disjoints et sans renommage.
4. Aucun « fait » sans preuve rejouée par l'orchestrateur ; un livrable visuel s'ouvre et se regarde.
5. Une correction humaine non gravée sera refaite : L-NNN avant de clore.
6. Commits par chemins listés, jamais add -A, add . ni commit -a.

Trois commandes conventionnelles : python outils/portes.py · python outils/smoke.py · python outils/deployer.py
Statuts : Todo, Ready, Dev, Recette, Relecture, Valide, Livre, Rejete.
Principes (règles `contradicteur` et `conception`) : contre-avis avant d'exécuter une proposition de Yann ; chercher l'existant avant d'écrire, extraire au 2e usage, aucune abstraction hypothétique.
Piège BOM : JSON lu par Node (settings*.json, .mcp.json, package.json) jamais écrit par PowerShell 5.1 Out-File/Set-Content (BOM, l'extension VS Code échoue « Settings file is not valid JSON ») ; Python ou Edit.
Délégation : 3 recherches ou plus, ou 100 lignes de sortie, vers les soldats Haiku (socle:fouilleur, socle:photographe).
Skills : /socle:tache · /socle:livrer · /socle:recette-ecran · /socle:secrets · /socle:nouveau-projet · /socle:preuve-navigateur
Secret : écrire NOM=valeur dans %LOCALAPPDATA%\socle\a_poser.env (notepad "$env:LOCALAPPDATA\socle\a_poser.env") ; la session suivante le pose en variable user et vide le fichier ; sinon l'écran Windows des variables (rundll32 sysdm.cpl,EditEnvironmentVariables) ; jamais `poser NOM` depuis le chat ; registre requis/reserve, contrôle : /socle:secrets verifier. Jamais dans un fichier Claude ; Snowflake = SSO `connections.toml` seul.
Emplacements : `C:/tmp` interdit ; code et venv dans le projet, état machine dans `%LOCALAPPDATA%/socle`, jetable dans le scratchpad de session ; venv jamais copié, toujours recréé depuis `requirements-dev.txt` (`/socle:nouveau-projet venv`) (`rules/emplacements.md`).
Règles machine : rules/machine, copiées dans ~/.claude/rules au démarrage.
Règles complètes : ${CLAUDE_PLUGIN_ROOT}/rules/
