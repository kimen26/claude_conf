# Socle actif v2026.10.6

Méthode complète : ${CLAUDE_PLUGIN_ROOT}/rules/methode.md (dix temps, statuts, transitions).

Les 6 règles qui tiennent tout
1. Orchestrateur = cerveau, pas les mains : il cadre la tâche, relit, tranche, ne code pas.
2. Une tâche = un fichier Backlog.md ; vocabulaire unique : tâche, porte, preuve, verdict, lane.
3. 1 dev par lane : périmètres de fichiers disjoints, sinon on enchaîne.
4. Aucun « fait » sans preuve ; un livrable visuel s'ouvre et se regarde.
5. Une correction humaine non gravée sera refaite : L-NNN avant de clore.
6. Commits par chemins listés, jamais add -A, add . ni commit -a.

Trois commandes conventionnelles : python outils/portes.py · python outils/smoke.py · python outils/deployer.py
Statuts : Todo, Ready, Dev, Recette, Relecture, Valide, Livre, Rejete.
Délégation : 3 recherches ou plus, ou 100 lignes de sortie, vers les soldats Haiku (socle:fouilleur, socle:greffier, socle:photographe).
Skills : /socle:tache · /socle:livrer · /socle:recette-ecran · /socle:secrets
Secret : écrire NOM=valeur dans %LOCALAPPDATA%\socle\a_poser.env, la session suivante le pose en variable user et vide le fichier ; registre /socle:secrets verifier. Jamais dans un fichier Claude ; Snowflake = SSO `connections.toml` seul.
Emplacements : `C:/tmp` interdit ; code et venv dans le projet, état machine dans `%LOCALAPPDATA%/socle`, jetable dans le scratchpad de session (`rules/emplacements.md`).
Règles complètes : ${CLAUDE_PLUGIN_ROOT}/rules/
