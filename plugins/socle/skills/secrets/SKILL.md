---
name: secrets
description: "QUAND : dès qu'un secret, un token, une clé, un mot de passe, un .env, un MCP avec credentials, SSL Netskope ou l'auth Snowflake est en jeu, dans n'importe quel projet. Pose, inventorie et contrôle les secrets (variables d'environnement utilisateur + registre), sans jamais lire une valeur."
argument-hint: "poser --fichier | inventaire | verifier | poser NOM [--reserve] | ssl | purger | snow"
---

# /socle:secrets : secrets et accès

**Avant de dire à Yann où mettre un secret : lancer `verifier` et lire le registre
(`${CLAUDE_PLUGIN_ROOT}/rules/secrets-registre.md`). Jamais une réponse de tête.**
Doctrine complète : `${CLAUDE_PLUGIN_ROOT}/rules/secrets.md`.

## La doctrine en bref
0. Voies pour poser un secret, dans cet ordre : (1) écrire `NOM=valeur` dans `%LOCALAPPDATA%\socle\a_poser.env` (ouvert par `notepad "$env:LOCALAPPDATA\socle\a_poser.env"`), posé à la session suivante ou par `secrets.py poser --fichier` ; (2) l'écran Windows des variables utilisateur (`rundll32 sysdm.cpl,EditEnvironmentVariables`). `poser NOM` au clavier = seulement depuis un vrai terminal, jamais depuis le chat (Claude n'a pas de clavier). **Quand Yann demande de poser un secret depuis le chat, ouvrir le dépôt dans le Bloc-notes (`notepad "$env:LOCALAPPDATA\socle\a_poser.env"`), ne jamais lancer `poser NOM`.** Registre à deux statuts : `requis` (absent = MANQUE) et `reserve` (absent = information) ; `poser --reserve` pour le second.
1. Secret transverse (PAT, tokens, clés API) = **variable d'environnement UTILISATEUR Windows**. Pour poser : écrire `NOM=valeur` (un par ligne) dans `%LOCALAPPDATA%\socle\a_poser.env`. La session suivante le pose, inscrit le NOM au registre et vide le fichier. Ce fichier ne se lit jamais par un agent.
2. Secret propre à un projet = `.env` git-ignoré + `.env.example` versionné (noms seuls).
3. Secret d'un MCP ou d'un hook = variable user ; `.mcp.json` écrit `${NOM}`, jamais la valeur.
4. Interdit : `settings.json` → `env`, `.claude.json`, `secrets.ps1`, tout `.bak` d'un fichier qui porte un secret.
5. Snowflake = `~/.snowflake/connections.toml` seul : `authenticator = externalbrowser` et `client_store_temporary_credential = true`, le code ne connaît qu'un `connection_name`. Le socle le lit, ne l'écrit jamais. Pas de mot de passe, PAT ni clé.
6. Un CLI s'installe **isolé** : `uv tool install <outil> --native-tls`. Snowflake : `uv tool install snowflake-cli --native-tls --with "snowflake-connector-python[secure-local-storage]"`. Le MCP Snowflake : `uvx --with "snowflake-connector-python[secure-local-storage]" snowflake-labs-mcp`.
7. SSL : `ssl` pose `NODE_EXTRA_CA_CERTS`, `SSL_CERT_FILE`, `NETSKOPE_BUNDLE`, `UV_NATIVE_TLS` et pip.ini. **Jamais `REQUESTS_CA_BUNDLE`** : elle casse `snow` (mesuré 2026-10-01).
8. Git : Credential Manager pour push/pull ; `GITLAB_PAT` en env user pour l'API seulement.
9. Tourner un secret = le révoquer côté service, puis écrire la nouvelle valeur dans `a_poser.env` (voie 1).

## Les commandes
`python ${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/secrets.py <commande>`

| Commande | Rôle |
|---|---|
| `poser --fichier [chemin] [--sans-vider] [--reserve]` | **première voie** : pose chaque `NOM=valeur` de `a_poser.env` (`%LOCALAPPDATA%\socle\a_poser.env`), NOM au registre, fichier réécrit avec le gabarit seul. N'imprime que des noms. Fait aussi tout seul à l'ouverture de session |
| `inventaire [chemin] [--json]` | NOMS seulement : tableau `emplacement, nom, type, etat` (niveau user + projet). États : `conforme`, `a_deplacer`, `doublon`, `sauvegarde_a_purger`, `hors_registre`, `config_morte`, plus `exemple_manquant` (`.env` sans `.env.example`) et `non_conforme_sso` (connexion Snowflake sans externalbrowser ou sans cache) |
| `verifier` | registre contre environnement user : `requis` absent = MANQUE (exit 1), `reserve` absent = ligne d'information (exit 0), orphelines (exit 1), signale `REQUESTS_CA_BUNDLE` |
| `poser NOM [--usage "..."] [--reserve]` | **vrai terminal seulement, jamais depuis le chat** : saisie masquée, variable user, ligne au registre (`requis` par défaut). La valeur ne passe jamais par une ligne de commande |
| `ssl` | pose la config SSL Netskope (bundle vérifié), puis redémarrer VS Code |
| `purger [--oui]` | sans `--oui` : liste ; avec : déplace sauvegardes et `secrets*.ps1` dans `~/.claude/_a_supprimer/<date>/secrets/` avec `MANIFESTE.md`. Ne supprime jamais |
| `snow` | `snow` isolé (`~/.local/bin`), `keyring` présent, cache SSO (fichier). Imprime la commande d'installation sinon, n'installe rien |

## Traiter les états
`a_deplacer` : poser la valeur par `a_poser.env` (Yann y écrit `NOM=valeur`), remplacer par `${NOM}`, révoquer l'ancienne si elle a fuité. `doublon` : garder la variable user, retirer l'autre. `hors_registre` : inscrire ou supprimer. `config_morte` : `mcpServers` dans `settings.json` est ignoré, déplacer vers `.mcp.json`. Ne jamais ouvrir ni afficher un fichier de secret pour « vérifier ».

## Emplacements (hors secrets, même skill)
`C:/tmp` est interdit (`rules/emplacements.md`). `python ${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/emplacements.py purger` liste `C:/tmp/claude` (taille, date, verdict), propose `migrer-profil` pour le profil navigateur et imprime ce que Yann peut supprimer lui-même. Ne supprime ni ne déplace jamais rien. Le profil navigateur et les caches ne sont pas des secrets : rien au registre.
