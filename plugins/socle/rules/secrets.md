# Secrets et accès : la doctrine

Vocabulaire : **secret** (une valeur), **registre** (la liste des noms, `secrets-registre.md`),
**poser** (mettre en variable d'environnement utilisateur), **tourner** (révoquer et reposer).
**Poser = écrire `NOM=valeur` dans `%LOCALAPPDATA%\socle\a_poser.env`, c'est tout.** À l'ouverture de la
session suivante (ou par `secrets.py poser --fichier`), chaque ligne devient une variable utilisateur, son NOM
entre au registre et le fichier est vidé (gabarit seul). Ce fichier ne se lit jamais par un agent
(`garde_outils` refuse Read, cat, type, Get-Content) et c'est le seul où un Write contenant un secret passe.
Outil : `/socle:secrets` (inventaire, verifier, poser, ssl, purger, snow). Le script ne lit, n'affiche
et ne recopie jamais une valeur.

| Chose | Emplacement UNIQUE | Interdit |
|---|---|---|
| Secret transverse (PAT GitLab, token Confluence, n8n, Supabase, clés API) | variable d'environnement UTILISATEUR Windows, posée une fois en écrivant `NOM=valeur` dans `a_poser.env` (ou `/socle:secrets poser NOM`, saisie masquée) ; son NOM est inscrit au registre `rules/secrets-registre.md` (nom, usage, consommateurs, date de pose) | `settings.json` → `env`, `.claude.json`, `secrets.ps1`, tout `.bak` |
| Secret propre à un projet, lu par un script | `.env` git-ignoré + `.env.example` versionné (noms seuls), chargé par python-dotenv | valeur dans le code, un `.md`, un test |
| Secret consommé par un MCP ou un hook | variable d'environnement user (Claude Code n'étend `${VAR}` que depuis l'environnement du process, pas depuis `.env`) ; `.mcp.json` écrit `${NOM}` | valeur en clair dans `.mcp.json` ou `settings.json` |
| Snowflake | `~/.snowflake/connections.toml` seul, `authenticator = externalbrowser` et `client_store_temporary_credential = true` sur chaque connexion, le code ne connaît qu'un `connection_name`. Le socle LIT ce fichier, ne l'écrit jamais | `SNOWFLAKE_PASSWORD`, clé privée, PAT, account/user en dur, « sandbox », « compte de service » |
| Git | Credential Manager pour push/pull ; `GITLAB_PAT` en env user seulement pour l'API | `.git-credentials`, PAT dans un fichier |
| SSL Netskope | `NODE_EXTRA_CA_CERTS`, `SSL_CERT_FILE`, `NETSKOPE_BUNDLE` (chemin du bundle), `UV_NATIVE_TLS=1` en variables user Windows, et `global.cert` dans pip.ini, posés une fois par `/socle:secrets ssl` ; bundle `C:\ProgramData\Netskope\stagent\data\netskope-complete-bundle.crt` | `REQUESTS_CA_BUNDLE` (casse `snow`, mesuré 2026-10-01), export à la main dans chaque shell, raccourci de lancement |
| OAuth Claude (`~/.claude/.credentials.json`), cache Azure (`~/.azure/msal_*`) | gérés par leurs outils | toute copie, toute lecture |
| Sauvegardes | aucune sauvegarde d'un fichier qui porte un secret ; les `.bak` vont dans `_a_supprimer/` | `cp settings.json settings.json.bak` |

## Snowflake : un seul mécanisme d'auth

SSO + cache de token, pour le CLI, les scripts et le MCP. Toute connexion de `connections.toml` porte
`authenticator = externalbrowser` et `client_store_temporary_credential = true`. Rien d'autre : pas de
mot de passe, pas de PAT, pas de clé. Contrôle : S-34.

- **Un CLI s'installe ISOLÉ, jamais dans le Python global** : `uv tool install <outil> --native-tls`.
  Pour Snowflake : `uv tool install snowflake-cli --native-tls --with "snowflake-connector-python[secure-local-storage]"`
  (l'extra apporte `keyring`, donc le cache SSO). Un lanceur résiduel dans `Python312\Scripts` est un
  écart : `which snow` doit pointer sous `~/.local/bin` (S-35).
- **Le MCP Snowflake** se lance avec le même extra et lit le MÊME `connections.toml` : dans `.mcp.json`,
  `command: uvx`, `args: ["--with", "snowflake-connector-python[secure-local-storage]", "snowflake-labs-mcp", ...]`.
  Sans l'extra : écart S-33.
- **Le cache de token SSO est un FICHIER** : `%LOCALAPPDATA%\Snowflake\Caches\credential_cache_v1.json`
  (pas le Credential Manager). Preuve du cache : un second `snow connection test` passe sans fenêtre.
  `/socle:secrets snow` vérifie le CLI, `keyring`, et la date du fichier.

## SSL et snow

`REQUESTS_CA_BUNDLE=<bundle>` fait échouer `snow connection test` (`SSL error, bad handshake`) ;
`SSL_CERT_FILE` et `NODE_EXTRA_CA_CERTS` passent. Donc `ssl` ne pose jamais `REQUESTS_CA_BUNDLE`, et la
signale si elle existe. Pour `requests` : `verify=os.environ["NETSKOPE_BUNDLE"]`.

## Gardes

S-30 `.env` suivi, `secrets*.ps1` non ignoré, `.env` sans `.env.example`, secret dans un fichier suivi ·
S-31 `env` en clair dans `.claude/settings*.json` · S-32 auth Snowflake hors `connections.toml` ·
S-33 `.mcp.json` en clair, ou `snowflake-labs-mcp` sans keyring · S-34 connexion non SSO / sans cache ·
S-35 `snow` hors `~/.local/bin` · S-37 `a_poser.env` avec une ligne `NOM=valeur` non posée, ou posée mais fichier non vidé. `garde_outils` refuse d'écrire un secret dans un fichier Claude
(`settings*.json`, `.claude.json`, `*.bak*`, `secrets*.ps1`, `backups/`) et de copier `settings.json` en `.bak`.
