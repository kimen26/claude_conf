# Registre des secrets (noms seulement)

Jamais de valeur ici. Tenu par `/socle:secrets poser NOM` ; contrôlé par `/socle:secrets verifier`.
"à confirmer" = posée avant le registre, date inconnue.
statut : `requis` = doit être posée (absente = MANQUE, exit 1) ; `reserve` = pas utilisée pour le moment, à poser
quand un projet en a besoin (absente = simple information). Une ligne sans colonne statut vaut `requis`.

| nom | statut | usage | consommateurs | posé le |
|---|---|---|---|---|
| `GITLAB_PAT` | requis | API GitLab | scripts GitLab, `glab` | à confirmer |
| `CONFLUENCE_API_TOKEN` | requis | API Confluence | skill confluence, MCP Atlassian | à confirmer |
| `N8N_API_KEY` | reserve | pas utilisé pour le moment, à poser quand un projet en a besoin (n8n local :5678) | skills et scripts n8n | à confirmer |
| `SUPABASE_ACCESS_TOKEN` | reserve | pas utilisé pour le moment, à poser quand un projet en a besoin (MCP supabase) | `.mcp.json` supabase | à confirmer |
| `NODE_EXTRA_CA_CERTS` | requis | config SSL, non secret : bundle Netskope pour Node | Claude Code, npm, MCP | 2026-10-01 |
| `SSL_CERT_FILE` | requis | config SSL, non secret : bundle Netskope pour Python, snow, curl | Python, snow | 2026-10-01 |
| `NETSKOPE_BUNDLE` | requis | config SSL, non secret : chemin du bundle pour `requests.get(url, verify=...)` | scripts Python | 2026-10-01 |
| `UV_NATIVE_TLS` | requis | config SSL, non secret : uv utilise le magasin Windows | uv, uvx | 2026-10-01 |
