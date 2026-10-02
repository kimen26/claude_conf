#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash|PowerShell|Read) : refuse d'exposer un .env.

Bloque toute lecture d'un fichier .env / .env.* (sauf *.env.example) par
Read, ou par une commande shell (cat, type, Get-Content, head, grep, …),
ainsi que les dumps d'environnement (printenv, env seul, Get-ChildItem Env:).
Pourquoi : ce qui entre dans le contexte peut finir dans un log ou un commit.
Exit 2 = refusé, message renvoyé à Claude.
"""
import json
import re
import sys

try:
    data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))  # UTF-8 explicite (cp1252 par défaut sous Windows)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
inp = data.get("tool_input") or {}

ENV_FILE = re.compile(r"(^|[\/\s\"'])\.env(\.[\w-]+)?(?<!\.example)(?<!\.sample)(?<!\.template)($|[\s\"'])")


CONSEIL_ENV = "Les .env ne se lisent pas ; se référer à .env.example."
CONSEIL_DUMP = "Un dump d'environnement expose les variables secrètes ; lire une variable précise par son nom, ou lister les NOMS sans valeur."


def refuse(what: str, conseil: str = CONSEIL_ENV) -> None:
    sys.stderr.reconfigure(encoding="utf-8")  # sinon cp1252 : emoji et accents illisibles
    sys.stderr.write(
        "\n🛑 GARDE SECRETS : lecture de secrets refusée.\n"
        f"   {what}\n"
        f"   {conseil} Inventaire des noms : /socle:secrets inventaire.\n"
    )
    sys.exit(2)


if tool == "Read":
    path = inp.get("file_path", "") or ""
    if ENV_FILE.search(path):
        refuse(f"Read : {path}")
    sys.exit(0)

if tool in ("Bash", "PowerShell"):
    cmd = inp.get("command", "") or ""
    if ENV_FILE.search(cmd) and re.search(
        r"(^|[;&|]\s*)(cat|type|Get-Content|gc|less|more|head|tail|grep|rg|sed|awk|bat|source|rtk\s+read|Select-String)\s",
        cmd,
    ):
        refuse(f"Commande : {cmd[:120]}")
    if re.search(r"(^|[;&|]\s*)(printenv|env|set)\s*($|[;&|>])", cmd) or re.search(
        r"Get-ChildItem\s+Env:|\bgci\s+env:", cmd, re.I
    ):
        refuse(f"Dump d'environnement : {cmd[:120]}", CONSEIL_DUMP)
sys.exit(0)
