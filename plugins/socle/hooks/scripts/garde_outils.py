#!/usr/bin/env python3
"""PreToolUse (Bash|Write|Edit|MultiEdit) : refuse les gestes que le socle interdit.

Exit 2 + motif sur stderr (une phrase, jamais la valeur d'un secret).
Tout le reste, y compris entrée invalide : exit 0 silencieux.

Exemption volontaire : les écritures dans les sources du socle lui-même (chemins contenant
/socle/hooks/, /socle/tests/, /socle/lib/) ne sont pas contrôlées. Ces fichiers citent les
motifs interdits (storage_state=, jetons de test, etc.) pour les détecter ou les tester ;
sans cette exemption le garde bloquerait sa propre maintenance.
"""
import json
import os
import re
import sys

SECRETS_RE = [re.compile(p) for p in (
    r"sbp_[0-9a-f]{20,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"glpat-[A-Za-z0-9_-]{15,}",
    r"SUPABASE_ACCESS_TOKEN=\S+",
    r"(PASSWORD|MOT_DE_PASSE|TOKEN|SECRET)\s*=\s*['\"][^'\"$]{8,}",
)]


def refuser(msg):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stderr.write(f"GARDE SOCLE : {msg}\n")
    sys.exit(2)


def verifier_bash(cmd):
    if re.search(r"\bclaude\s+mcp\s+add\b", cmd):
        user = re.search(r"(-s|--scope)[\s=]+user\b", cmd)
        proc = re.search(r"(^|[\s/\\])(npx|uvx|node|python3?)(\.exe|\.cmd)?(\s|$)", cmd)
        if user and proc:
            refuser("pas de MCP à process au niveau user : déclare-le dans le .mcp.json du projet, HTTP de préférence.")
    if "@playwright/mcp" in cmd:
        refuser("le navigateur de preuve est preuve_navigateur, pas le MCP : importe preuve_navigateur.")
    if re.search(r"playwright\s+codegen", cmd) and "--save-storage" in cmd:
        refuser("le SSO vit dans le profil partagé C:/tmp/claude/pw-profile : utilise setup_sso() de preuve_navigateur.")


def textes_ajoutes(ti):
    out = [ti[k] for k in ("content", "new_string") if isinstance(ti.get(k), str)]
    for e in ti.get("edits") or []:
        if isinstance(e, dict) and isinstance(e.get("new_string"), str):
            out.append(e["new_string"])
    return out


def verifier_fichier(chemin, textes):
    p = chemin.replace("\\", "/")
    base = os.path.basename(p)
    texte = "\n".join(textes)
    # Les sources du socle citent ces motifs pour les détecter : on ne les bloque pas.
    if any(s in p for s in ("/socle/hooks/", "/socle/tests/", "/socle/lib/")):
        return
    if base != "preuve_navigateur.py" and any(
            m in texte for m in ("storage_state=", "connect_over_cdp(", "launch_persistent_context(")):
        refuser("le contexte navigateur ne s'ouvre pas à la main : importe preuve_navigateur.")
    if not base.startswith(".env") and any(rx.search(texte) for rx in SECRETS_RE):
        refuser("un secret va dans .env, et dans .mcp.json sous la forme ${VAR}.")
    if base in (".claude.json", "settings.json", "settings.local.json") and '"mcpServers"' in texte and "npx" in texte:
        refuser("pas de MCP à process au niveau user : déclare-le dans le .mcp.json du projet, HTTP de préférence.")


def main():
    try:
        data = json.load(sys.stdin)
        outil = data.get("tool_name")
        ti = data.get("tool_input") or {}
        if not isinstance(ti, dict):
            return
    except Exception:
        return
    if outil == "Bash":
        if isinstance(ti.get("command"), str):
            verifier_bash(ti["command"])
    elif outil in ("Write", "Edit", "MultiEdit"):
        if isinstance(ti.get("file_path"), str):
            verifier_fichier(ti["file_path"], textes_ajoutes(ti))


if __name__ == "__main__":
    main()
    sys.exit(0)
