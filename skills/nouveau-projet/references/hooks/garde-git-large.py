#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash) — refuse les commits « filet ».

Bloque : git add -A / --all / . / -u, git commit -a / -am.
Pourquoi : l'index git est partagé entre sessions ; un add global emporte le
travail d'autrui. Un commit liste ses fichiers un par un.
Exit 2 = commande refusée, message renvoyé à Claude.
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

if data.get("tool_name") not in ("Bash", "PowerShell"):
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

PATTERNS = [
    r"\bgit\s+add\s+(-A|--all|-u|--update|\.)(\s|$)",
    r"\bgit\s+add\s+(\S+\s+)*(-A|--all|\.)(\s|$)",
    r"\bgit\s+commit\s+(\S+\s+)*(-a|-am|--all)(\s|$)",
]
for p in PATTERNS:
    if re.search(p, cmd):
        sys.stderr.write(
            "\n🛑 GARDE GIT — add/commit global refusé.\n"
            f"   Commande : {cmd[:120]}\n"
            "   Lister les fichiers un par un : git add <f1> <f2> ; git commit -m ...\n"
        )
        sys.exit(2)
sys.exit(0)
