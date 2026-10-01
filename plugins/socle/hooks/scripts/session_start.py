#!/usr/bin/env python3
"""SessionStart (startup) : SSL Netskope, sync de lib/, DIGEST, audit du projet.

Ne doit jamais échouer : tout est dans try/except, exit 0 toujours.
La sortie standard est ajoutée au contexte de la session.
"""
import hashlib
import os
import shutil
import sys

BUNDLE = r"C:\ProgramData\Netskope\stagent\data\netskope-complete-bundle.crt"
HERE = os.path.dirname(os.path.abspath(__file__))


def racine_plugin():
    return os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(HERE))


def controle_ssl():
    manque = [v for v in ("NODE_EXTRA_CA_CERTS", "REQUESTS_CA_BUNDLE")
              if not os.environ.get(v) or not os.path.exists(os.environ[v])]
    if manque:
        return [f"ATTENTION SSL Netskope : {', '.join(manque)} absent ou introuvable "
                f"(bundle {BUNDLE}). Relancer VS Code via le Desktop Shortcut."]
    return []


def _sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def synchroniser(src, dst):
    """Copie src vers dst si le sha256 diffère, supprime les orphelins. Rend le nombre de copies."""
    if not os.path.isdir(src):
        return 0
    copies = 0
    vus = set()
    for dossier, sous, fichiers in os.walk(src):
        sous[:] = [d for d in sous if d != "__pycache__"]
        for f in fichiers:
            s = os.path.join(dossier, f)
            rel = os.path.relpath(s, src)
            vus.add(rel)
            d = os.path.join(dst, rel)
            if not os.path.isfile(d) or _sha(s) != _sha(d):
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
                copies += 1
    if os.path.isdir(dst):
        for dossier, _sous, fichiers in os.walk(dst, topdown=False):
            for f in fichiers:
                d = os.path.join(dossier, f)
                if os.path.relpath(d, dst) not in vus:
                    os.remove(d)
            if dossier != dst and not os.listdir(dossier):
                os.rmdir(dossier)
    return copies


def donnees_plugin():
    return os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(
        os.path.expanduser("~"), ".claude", "plugins", "data", "socle")


def sync_lib():
    n = synchroniser(os.path.join(racine_plugin(), "lib"), os.path.join(donnees_plugin(), "lib"))
    return [f"SOCLE : lib/ synchronisée ({n} fichier(s) copié(s))"] if n else []


def digest():
    p = os.path.join(racine_plugin(), "rules", "DIGEST.md")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            return [f.read().rstrip()]
    return []


def audit():
    sys.path.insert(0, HERE)
    import garde_socle
    projet = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    lignes, _ = garde_socle.main(["--session", projet])
    return lignes


def main():
    sortie = []
    for fn in (controle_ssl, sync_lib, digest, audit):
        try:
            sortie += fn() or []
        except Exception:
            pass
    if sortie:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        print("\n".join(sortie))


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        pass
    sys.exit(0)
