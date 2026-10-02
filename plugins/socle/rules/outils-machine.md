# Outils de la machine : navigateur, MCP, consoles

Doctrine globale, tous projets. Écrite le 2026-10-01 après inventaire : 4 façons de piloter un
navigateur coexistaient, 12 node + 13 cmd tournaient pour des MCP que personne n'appelait.

## Navigateur : deux modes, pas plus

| Besoin | Mode | Visible ? |
|---|---|---|
| **Preuve** (smoke, banc de rendu, capture, recette, vidéo) | Playwright **Python**, `launch_persistent_context` sur le profil SSO **partagé machine** `%LOCALAPPDATA%\socle\pw-profile` (hors OneDrive, hors repo, jamais synchronisé ; ancien emplacement `C:/tmp` interdit, `migrer-profil` le déplace), **headless** | Non, rien dans la barre des tâches |
| **Regard** (explorer une page, repérer un menu, voir avec Yann) | Extension Claude in Chrome branchée sur **Comet** | Oui, dans Comet |

- `--headed` sert **une seule fois par PC** : un seul `setup_sso` remplit le profil partagé. Ensuite headless.
- Le profil étant partagé, deux sessions qui lancent une preuve en même temps se heurtent au verrou du profil : c'est attendu, la seconde attend ou réessaie.
- Une preuve ne passe **jamais** par l'extension (session partagée, instable, pas de vidéo).
- Un regard ne passe **jamais** par un script (lent, SSO à refaire).
- **Pas de MCP Playwright** : navigateur invisible, 4 process par session, aucun script ni skill ne
  l'appelle. Si un projet en a un vrai besoin, il le déclare dans **son** `.mcp.json`, jamais au
  niveau user. Pour de l'automatisation interactive hors script, préférer **Playwright CLI** (snapshots
  sur disque, ~4x moins de tokens que le MCP, recommandé par Microsoft pour les agents avec shell).
- **Packaging** : le navigateur se pilote depuis un **sous-agent Haiku** qui ne rend que chemins de
  captures, mesures et exceptions (c'est le rôle de `socle:photographe`). L'orchestrateur
  regarde les images, il ne tient pas le navigateur.
- Sortie de script : toujours fermer le contexte (`with sync_playwright()` + `ctx.close()`), sinon un
  chromium headless survit à la session.

## MCP : zéro process au repos

- Niveau user (`~/.claude.json`) : **uniquement des MCP HTTP/SSE** (0 process). Aujourd'hui :
  aucun.
- **Jamais `npx -y …@latest` en config user** : chaque MCP npx = `cmd → node (npx) → cmd → node`
  + conhost, dans **chaque** session, plus un contrôle réseau via Netskope au démarrage.
- Un MCP à process vit dans le `.mcp.json` du projet qui l'utilise. Si on le remet en user malgré
  tout : installer le paquet en global (`npm i -g`) et pointer le binaire, pas npx.
- Réserve, à réactiver dans un projet par `claude mcp add` :
  - `supabase` : `npx -y @supabase/mcp-server-supabase@latest --read-only --project-ref=<ref>`,
    env `SUPABASE_ACCESS_TOKEN` (depuis `.env`, jamais en clair dans un fichier commité) et
    `NODE_EXTRA_CA_CERTS`.

## Sessions et consoles

- **1 fenêtre VS Code = 1 session Claude par projet.** Deux sessions sur le même repo = MCP en
  double et travail git qui s'écrase.
- Un hook shell qui pend survit à la fermeture (vu le 2026-10-01 : `bash.exe` d'un
  `posttooluse.py` orphelin depuis la veille). Ménage :
  ```powershell
  $p = Get-CimInstance Win32_Process; $ids = @{}; $p | % { $ids[$_.ProcessId] = $_ }
  $p | ? { $_.Name -in 'node.exe','cmd.exe','bash.exe','conhost.exe','python.exe' -and -not $ids.ContainsKey($_.ParentProcessId) } | % { Stop-Process -Id $_.ProcessId -Force }
  ```
- Les `~/.claude.json.tmp.*` à 0 octet sont des résidus de crash : supprimables.
- « Hôte de service » dans le gestionnaire des tâches = `svchost` Windows, rien à voir avec Claude.

## Credentials

- Les secrets vivent dans un `.env` **git-ignoré**, jamais dans un fichier suivi.
- Un `.mcp.json` les référence en `${VAR}` : jamais la valeur.
- Jamais de `state.json` ni d'export de session d'authentification dans le dépôt.
- Jamais de valeur de secret dans un fichier suivi, une mémoire, un log ou un message de commit.
