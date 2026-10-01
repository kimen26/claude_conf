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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motifs_secrets as ms  # noqa: E402

SECRETS_RE = [rx for _, rx in ms.LIGNE_RE]
FICHIER_SENSIBLE = re.compile(r"(^|/)(settings[^/]*\.json|\.claude\.json|secrets[^/]*\.ps1)$|\.bak|(^|/)backups/", re.I)
COPIE_SAUVEGARDE = re.compile(
    r"(?<![\w-])(?:cp|copy|Copy-Item)(?:\s+-[A-Za-z]+)*\s+[\"']?\S*(?:settings(?:\.local)?\.json|\.claude\.json)[\"']?"
    r"(?:\s+-Destination)?\s+[\"']?\S*\.bak", re.I)

TMP_PATH = re.compile(r"^(?:c:|/c|/mnt/c)/+tmp(?:/|$)", re.I)
TMP_MENTION = re.compile(r"(?<![A-Za-z0-9])(?:c:[\\/]+|/mnt/c/|/c/)tmp(?![A-Za-z0-9_])", re.I)
TMP_CREE = re.compile(
    r"(?:>>?|(?<![\w-])tee(?:\s+-a)?|-OutFile|Out-File|-Destination|\s-o)\s*[\"']?"
    r"(?:c:[\\/]+|/mnt/c/|/c/)tmp(?![A-Za-z0-9_])", re.I)
TMP_VERBES = re.compile(
    r"(?<![\w-])(?:mkdir|md|New-Item|virtualenv|git\s+clone|python3?\s+-m\s+venv|uv\s+venv)(?![\w-])", re.I)
TMP_COPIE = re.compile(r"(?<![\w-])(?:cp|mv|copy|move|Copy-Item|Move-Item|robocopy|xcopy)(?![\w-])", re.I)
MSG_TMP = ("C:\\tmp est interdit : projet pour le code et le venv, %LOCALAPPDATA%\\socle pour l'état machine, "
           "scratchpad de session pour le jetable.")


def tmp_cree(cmd):
    """Vrai si la commande crée ou écrit quelque chose sous C:\\tmp (la lecture reste permise)."""
    if not TMP_MENTION.search(cmd):
        return False
    if TMP_CREE.search(cmd) or TMP_VERBES.search(cmd):
        return True
    for stmt in re.split(r"[;\n]|&&|\|\|", cmd):
        if TMP_COPIE.search(stmt):
            dernier = (stmt.split() or [""])[-1].strip("\"'")
            if TMP_MENTION.match(dernier):
                return True
    return False


def refuser(msg):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stderr.write(f"GARDE SOCLE : {msg}\n")
    sys.exit(2)


def verifier_bash(cmd):
    if tmp_cree(cmd):
        refuser(MSG_TMP)
    if re.search(r"\bclaude\s+mcp\s+add\b", cmd):
        user = re.search(r"(-s|--scope)[\s=]+user\b", cmd)
        proc = re.search(r"(^|[\s/\\])(npx|uvx|node|python3?)(\.exe|\.cmd)?(\s|$)", cmd)
        if user and proc:
            refuser("pas de MCP à process au niveau user : déclare-le dans le .mcp.json du projet, HTTP de préférence.")
    if COPIE_SAUVEGARDE.search(cmd):
        refuser("pas de sauvegarde d'un fichier qui porte un secret : purge ou /socle:secrets purger.")
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
    if TMP_PATH.match(p) and not any(s in p for s in ("/socle/hooks/", "/socle/tests/", "/socle/lib/")):
        refuser(MSG_TMP)
    # Les sources du socle citent ces motifs pour les détecter : on ne les bloque pas.
    if any(s in p for s in ("/socle/hooks/", "/socle/tests/", "/socle/lib/")):
        return
    if FICHIER_SENSIBLE.search(p) and ms.a_motif(texte, large=True):
        refuser("un secret se pose par /socle:secrets poser NOM, et se référence en ${NOM}.")
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
