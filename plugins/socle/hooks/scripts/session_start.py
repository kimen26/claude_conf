#!/usr/bin/env python3
"""SessionStart (startup|resume|clear|compact) : SSL Netskope, sync de lib/ et des règles machine,
DIGEST (complet dans un projet adopté, une ligne ailleurs), audit du projet.

Ne doit jamais échouer : tout est dans try/except, exit 0 toujours.
La sortie standard est ajoutée au contexte de la session.
"""
import hashlib
import json
import os
import shutil
import sys

AUDIT_NON_ADOPTE = {f"S-{n}" for n in range(30, 38)} | {"S-73"}
BUNDLE = r"C:\ProgramData\Netskope\stagent\data\netskope-complete-bundle.crt"
HERE = os.path.dirname(os.path.abspath(__file__))


def racine_plugin():
    return os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(HERE))


def controle_ssl():
    """Netskope absent (ni variable NETSKOPE_BUNDLE ni bundle sur disque) : aucune alerte, machine hors proxy."""
    if not os.environ.get("NETSKOPE_BUNDLE") and not os.path.isfile(BUNDLE):
        return []
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
    try:
        sys.path.insert(0, HERE)
        import garde_socle
        ancien = garde_socle.venv_non_relocalise(os.path.abspath(projet))
    except Exception:
        ancien = None
    if ancien:
        out.append(f"ATTENTION .venv non relocalisé (VIRTUAL_ENV={ancien}) : le recréer, jamais le copier "
                   "-> /socle:nouveau-projet venv --oui (requirements-dev.txt requis)")
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


def sync_regles():
    """Copie rules/machine/*.md vers ~/.claude/rules/ si absent ou différent (fins de ligne en LF). Jamais de suppression."""
    src = os.path.join(racine_plugin(), "rules", "machine")
    if not os.path.isdir(src):
        return []
    dst = os.path.join(os.path.expanduser("~"), ".claude", "rules")
    copiees = []
    for nom in sorted(os.listdir(src)):
        if not nom.endswith(".md"):
            continue
        with open(os.path.join(src, nom), "rb") as f:
            ref = f.read().replace(b"\r\n", b"\n")
        cible = os.path.join(dst, nom)
        try:
            with open(cible, "rb") as f:
                if f.read().replace(b"\r\n", b"\n") == ref:
                    continue
        except OSError:
            pass
        os.makedirs(dst, exist_ok=True)
        with open(cible, "wb") as f:
            f.write(ref)
        copiees.append(nom)
    return [f"SOCLE : règles machine copiées vers ~/.claude/rules ({', '.join(copiees)})"] if copiees else []


def projet_courant():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def projet_adopte(projet=None):
    """Adopté = outils/portes.py, ou backlog/, ou un CLAUDE.md qui mentionne « socle »."""
    projet = projet or projet_courant()
    if os.path.isfile(os.path.join(projet, "outils", "portes.py")) or os.path.isdir(os.path.join(projet, "backlog")):
        return True
    try:
        with open(os.path.join(projet, "CLAUDE.md"), encoding="utf-8", errors="replace") as f:
            return "socle" in f.read().lower()
    except OSError:
        return False


def version_plugin():
    try:
        with open(os.path.join(racine_plugin(), ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
            return json.load(f).get("version") or "?"
    except Exception:
        return "?"


def digest():
    """DIGEST complet (${CLAUDE_PLUGIN_ROOT} substitué) si le projet a adopté le socle, sinon une ligne."""
    if not projet_adopte():
        return [f"# Socle v{version_plugin()} actif (gardes) ; projet non adopté : "
                "/socle:nouveau-projet init | remise-au-pas"]
    p = os.path.join(racine_plugin(), "rules", "DIGEST.md")
    if os.path.isfile(p):
        with open(p, encoding="utf-8") as f:
            return [f.read().rstrip().replace("${CLAUDE_PLUGIN_ROOT}", racine_plugin().replace("\\", "/"))]
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
    projet = os.path.abspath(projet_courant())
    ecarts = garde_socle.auditer(projet, complet=False)
    if not projet_adopte(projet):  # non adopté : secrets/auth (S-30 à S-37) et BOM (S-73) seulement
        ecarts = [e for e in ecarts if e.code in AUDIT_NON_ADOPTE]
    return garde_socle.rendu_session(ecarts)


def main():
    sortie = []
    for fn in (controle_ssl, depot_secrets, controle_emplacements, sync_lib, sync_regles, digest, audit):
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
