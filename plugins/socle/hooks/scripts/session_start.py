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
    manque = [v for v in ("NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE")
              if not os.environ.get(v) or not os.path.exists(os.environ[v])]
    out = []
    if manque:
        out.append("ATTENTION variables SSL absentes (" + ", ".join(manque) + ") : /socle:secrets ssl "
                   "(une fois, puis redémarrer VS Code)")
    if os.environ.get("REQUESTS_CA_BUNDLE"):
        out.append("ATTENTION REQUESTS_CA_BUNDLE posée : elle casse snow (mesuré 2026-10-01), la retirer "
                   "des variables utilisateur (SSL_CERT_FILE suffit)")
    return out


TMP_CLAUDE = r"C:\tmp\claude"


def controle_emplacements():
    out = []
    projet = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    if "onedrive" in projet.lower():
        out.append(r"Projet sous OneDrive : fichiers écrasés, venv synchronisé, sessions qui fuient vers C:\tmp. "
                   "Déplacer le repo hors OneDrive (git est la sauvegarde).")
    import glob
    if glob.glob(os.path.join(TMP_CLAUDE, "venv-*")):
        out.append("venv hors projet détecté : /socle:nouveau-projet remise-au-pas")
    return out


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


def depot_secrets():
    """Pose les NOM=valeur de a_poser.env en variables utilisateur puis vide le fichier. Jamais la valeur."""
    sys.path.insert(0, HERE)
    import poser_secrets
    p = poser_secrets.assurer_gabarit()
    paires, _ = poser_secrets.lire_paires(p)
    if not paires:
        return []
    poses, _, echecs, vide = poser_secrets.poser_fichier(p)
    out = []
    if poses:
        out.append(f"SOCLE : {len(poses)} secret(s) posé(s) depuis a_poser.env"
                   + (" (fichier vidé)" if vide else " (fichier conservé)") + " : " + ", ".join(poses)
                   + ". Redémarrer VS Code pour que les process les voient.")
    if echecs:
        out.append("ATTENTION a_poser.env : échec de pose pour " + ", ".join(echecs)
                   + " : secrets.py poser --fichier")
    return out


def audit():
    sys.path.insert(0, HERE)
    import garde_socle
    projet = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    lignes, _ = garde_socle.main(["--session", projet])
    return lignes


def main():
    sortie = []
    for fn in (controle_ssl, depot_secrets, controle_emplacements, sync_lib, digest, audit):
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
