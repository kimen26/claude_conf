---
name: secrets
description: "QUAND : dès qu'un secret, un token, une clé, un mot de passe, un .env, un MCP avec credentials, SSL Netskope ou l'auth Snowflake est en jeu, dans n'importe quel projet. Pose, inventorie et contrôle les secrets (variables d'environnement utilisateur + registre), sans jamais lire une valeur."
argument-hint: "inventaire | verifier | poser NOM | ssl | purger | snow"
---

# /socle:secrets : secrets et accès

**Avant de dire à Yann où mettre un secret : lancer `verifier` et lire le registre
(`${CLAUDE_PLUGIN_ROOT}/rules/secrets-registre.md`). Jamais une réponse de tête.**
Doctrine complète : `${CLAUDE_PLUGIN_ROOT}/rules/secrets.md`.

## La doctrine en bref
1. Secret transverse (PAT, tokens, clés API) = **variable d'environnement UTILISATEUR Windows**, posée une fois par `poser NOM` (saisie masquée), son NOM au registre.
2. Secret propre à un projet = `.env` git-ignoré + `.env.example` versionné (noms seuls).
3. Secret d'un MCP ou d'un hook = variable user ; `.mcp.json` écrit `${NOM}`, jamais la valeur.
4. Interdit : `settings.json` → `env`, `.claude.json`, `secrets.ps1`, tout `.bak` d'un fichier qui porte un secret.
5. Snowflake = `~/.snowflake/connections.toml` seul : `authenticator = externalbrowser` et `client_store_temporary_credential = true`, le code ne connaît qu'un `connection_name`. Le socle le lit, ne l'écrit jamais. Pas de mot de passe, PAT ni clé.
6. Un CLI s'installe **isolé** : `uv tool install <outil> --native-tls`. Snowflake : `uv tool install snowflake-cli --native-tls --with "snowflake-connector-python[secure-local-storage]"`. Le MCP Snowflake : `uvx --with "snowflake-connector-python[secure-local-storage]" snowflake-labs-mcp`.
7. SSL : `ssl` pose `NODE_EXTRA_CA_CERTS`, `SSL_CERT_FILE`, `NETSKOPE_BUNDLE`, `UV_NATIVE_TLS` et pip.ini. **Jamais `REQUESTS_CA_BUNDLE`** : elle casse `snow` (mesuré 2026-10-01).
8. Git : Credential Manager pour push/pull ; `GITLAB_PAT` en env user pour l'API seulement.
9. Tourner un secret = le révoquer côté service, puis `poser NOM` à nouveau.

## Les commandes
`python ${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/secrets.py <commande>`

| Commande | Rôle |
|---|---|
| `inventaire [chemin] [--json]` | NOMS seulement : tableau `emplacement, nom, type, etat` (niveau user + projet). États : `conforme`, `a_deplacer`, `doublon`, `sauvegarde_a_purger`, `hors_registre`, `config_morte`, plus `exemple_manquant` (`.env` sans `.env.example`) et `non_conforme_sso` (connexion Snowflake sans externalbrowser ou sans cache) |
| `verifier` | registre contre environnement user : manques et orphelines, signale `REQUESTS_CA_BUNDLE`. Exit 1 si écart |
| `poser NOM [--usage "..."]` | saisie masquée, variable user, ligne au registre. La valeur ne passe jamais par une ligne de commande |
| `ssl` | pose la config SSL Netskope (bundle vérifié), puis redémarrer VS Code |
| `purger [--oui]` | sans `--oui` : liste ; avec : déplace sauvegardes et `secrets*.ps1` dans `~/.claude/_a_supprimer/<date>/secrets/` avec `MANIFESTE.md`. Ne supprime jamais |
| `snow` | `snow` isolé (`~/.local/bin`), `keyring` présent, cache SSO (fichier). Imprime la commande d'installation sinon, n'installe rien |

## Traiter les états
`a_deplacer` : poser la valeur par `poser NOM` (Yann la saisit), remplacer par `${NOM}`, révoquer l'ancienne si elle a fuité. `doublon` : garder la variable user, retirer l'autre. `hors_registre` : inscrire ou supprimer. `config_morte` : `mcpServers` dans `settings.json` est ignoré, déplacer vers `.mcp.json`. Ne jamais ouvrir ni afficher un fichier de secret pour « vérifier ».

## Emplacements (hors secrets, même skill)
`C:/tmp` est interdit (`rules/emplacements.md`). `python ${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/emplacements.py purger` liste `C:/tmp/claude` (taille, date, verdict), propose `migrer-profil` pour le profil navigateur et imprime ce que Yann peut supprimer lui-même. Ne supprime ni ne déplace jamais rien. Le profil navigateur et les caches ne sont pas des secrets : rien au registre.
