# lib/ : bibliothèques partagées du plugin socle

Contenu : `preuve_navigateur.py`, la bibliothèque de preuve d'écran (captures, vidéo, PDF,
profil SSO partagé `C:/tmp/claude/pw-profile`, sondes de débordement). Elle s'appuie sur
Playwright, installé dans le venv du projet.

Chemin stable : à chaque SessionStart, `session_start.py` copie `lib/` vers
`~/.claude/plugins/data/socle/lib/` (`${CLAUDE_PLUGIN_DATA}/lib/`). Ce chemin ne change pas
quand le plugin se met à jour, contrairement au cache versionné du plugin.

Import côté projet : le shim `outils/preuve_navigateur.py` (écrit par `/socle:nouveau-projet init`)
ajoute ce dossier au `sys.path`, puis fait `from preuve_navigateur import *`.
Les scripts du projet importent donc `preuve_navigateur` sans connaître le plugin.
Ne jamais ouvrir Playwright à la main : le garde `garde_outils` l'interdit.
