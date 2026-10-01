# Registre des secrets (noms seulement)

Jamais de valeur ici. Tenu par `/socle:secrets poser NOM` ; contrôlé par `/socle:secrets verifier`.
"à confirmer" = posée avant le registre, date inconnue.

| nom | usage | consommateurs | posé le |
|---|---|---|---|
| `GITLAB_PAT` | API GitLab | scripts GitLab, `glab` | à confirmer |
| `CONFLUENCE_API_TOKEN` | API Confluence | skill confluence, MCP Atlassian | à confirmer |
| `N8N_API_KEY` | n8n local :5678 | skills et scripts n8n | à confirmer |
| `SUPABASE_ACCESS_TOKEN` | MCP supabase (en réserve) | `.mcp.json` supabase | à confirmer |
| `TYPESAFE_API_KEY` | usage inconnu : à qualifier ou supprimer | inconnu | à confirmer |
| `NODE_EXTRA_CA_CERTS` | config SSL, non secret : bundle Netskope pour Node | Claude Code, npm, MCP | posée par `ssl` |
| `SSL_CERT_FILE` | config SSL, non secret : bundle Netskope pour Python, snow, curl | Python, snow | posée par `ssl` |
| `NETSKOPE_BUNDLE` | config SSL, non secret : chemin du bundle pour `requests.get(url, verify=...)` | scripts Python | posée par `ssl` |
| `UV_NATIVE_TLS` | config SSL, non secret : uv utilise le magasin Windows | uv, uvx | posée par `ssl` |
