#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash|Read) — refuse d'exposer un .env.

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
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
inp = data.get("tool_input") or {}

ENV_FILE = re.compile(r"(^|[\/\s\"'])\.env(\.[\w-]+)?(?<!\.example)(?<!\.sample)(?<!\.template)($|[\s\"'])")


def refuse(what: str) -> None:
    sys.stderr.write(
        "\n🛑 GARDE SECRETS — lecture de secrets refusée.\n"
        f"   {what}\n"
        "   Les .env ne se lisent pas ; se référer à .env.example.\n"
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
        refuse(f"Dump d'environnement : {cmd[:120]}")
sys.exit(0)
