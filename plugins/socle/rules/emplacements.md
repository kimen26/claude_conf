# Emplacements : où ça vit

Règle normative. `C:\tmp` (et `/c/tmp`, `C:/tmp`) est INTERDIT : mesuré le 2026-10-01, 1,5 Go,
23 dossiers, 126 fichiers en vrac, deux venvs dupliqués, restes de sessions.

| Chose | Emplacement UNIQUE | Interdit |
|---|---|---|
| Code, venv, outils | dans le projet (`.venv/`) | `C:\tmp`, copie d'un outil ou d'un repo ailleurs |
| État machine non versionné (profil navigateur SSO, caches) | `%LOCALAPPDATA%\socle\` (Windows natif, jamais synchronisé) ; profil Playwright : `%LOCALAPPDATA%\socle\pw-profile` | OneDrive, `C:\tmp`, le repo |
| Brouillon de session (essais, captures jetables) | le scratchpad fourni par Claude Code (`%TEMP%\claude\<projet>\<session>\scratchpad`) | un dossier maison |
| Preuves à conserver | `<projet>/recette/<AAAA-MM-JJ>/` (git-ignoré par le gabarit) | `C:\tmp`, vrac à la racine |
| Secrets | voir `secrets.md` | tout fichier |

- Venv recréable : `requirements-dev.txt` versionné à la racine, `.venv` jamais copié ni déplacé, toujours recréé
  (`/socle:nouveau-projet venv`) ; `session_start` signale un venv non relocalisé.
- Profil Playwright resté à l'ancien emplacement : `python outils/preuve_navigateur.py migrer-profil`
  (déplace, ne copie pas ; si rien à déplacer, relancer `setup <URL>`).
- Le projet sous OneDrive est un risque : fichiers écrasés, venv synchronisé, sessions qui fuient vers `C:\tmp`.
  Le repo vit hors OneDrive, git est la sauvegarde.
- Inventaire de `C:\tmp\claude` : `python ${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/emplacements.py purger`
  (liste, propose, ne supprime jamais ; Yann supprime).

## Gardes
- `garde_outils` refuse un Write/Edit dont le chemin est sous `C:\tmp`, et un Bash qui y crée quelque chose
  (`mkdir`, redirection, `cp`, `python -m venv`, `uv venv`, `New-Item`, `Copy-Item`...). La lecture reste permise.
  Les sources du plugin et ses tests sont exemptés.
- S-36 (`garde_socle`) : toute occurrence de `C:/tmp`, `C:\tmp`, `/c/tmp` dans les `.py`, `.ps1`, `.md`, `.json`
  du projet est un écart (hors `.snowflake/`, `archives/`, `_a_supprimer/`).
- `session_start` signale un projet sous OneDrive et un venv hors projet (`C:\tmp\claude\venv-*`).
