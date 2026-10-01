#!/usr/bin/env python3
"""Dépôt de secrets : lit a_poser.env, pose chaque NOM=valeur en variable utilisateur, vide le fichier.

Module partagé par secrets.py (poser --fichier), session_start.py et garde_socle.py (S-37).
RÈGLE ABSOLUE : aucune fonction ne logge, n'imprime ni ne renvoie une valeur. La valeur n'est
transmise qu'à ecrire_env_user (qui la passe par stdin à PowerShell). Les messages ne portent que
des noms et des numéros de ligne.
"""
import datetime
import importlib.util
import os
import re
from pathlib import Path

NOM_VALIDE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
HERE = Path(__file__).resolve().parent
RACINE = HERE.parents[1]
GABARIT = RACINE / "gabarits" / "a_poser.env"
# Surchargeable par les tests : objet avec ecrire_env_user, lire_env_user, lire_registre, ajouter_registre.
BACKEND = None


def chemin_depot() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    racine = Path(base) if base else Path.home() / "AppData" / "Local"
    return racine / "socle" / "a_poser.env"


def texte_gabarit() -> str:
    try:
        return GABARIT.read_text(encoding="utf-8")
    except OSError:
        return "# Écris NOM=valeur, un par ligne. Ne jamais commiter, ne jamais lire par un agent.\n"


def assurer_gabarit(chemin=None) -> Path:
    """Écrit le gabarit à l'emplacement s'il n'existe pas. Ne touche jamais un fichier existant."""
    p = Path(chemin) if chemin else chemin_depot()
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texte_gabarit(), encoding="utf-8")
    return p


def analyser(texte: str):
    """([(nom, valeur)], [numéros de lignes mal formées]). Commentaires et lignes vides ignorés."""
    paires, erreurs = [], []
    for i, brut in enumerate(texte.splitlines(), 1):
        ligne = brut.strip().lstrip("﻿")
        if not ligne or ligne.startswith("#"):
            continue
        nom, sep, val = ligne.partition("=")
        nom, val = nom.strip(), val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        if not sep or not NOM_VALIDE.match(nom) or not val:
            erreurs.append(i)
        else:
            paires.append((nom, val))
    return paires, erreurs


def lire_paires(chemin=None):
    p = Path(chemin) if chemin else chemin_depot()
    if not p.is_file():
        return [], []
    return analyser(p.read_text(encoding="utf-8", errors="replace"))


def _backend():
    if BACKEND is not None:
        return BACKEND
    spec = importlib.util.spec_from_file_location("secrets_cli_partage", RACINE / "skills/secrets/scripts/secrets.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def env_user_noms():
    """Noms des variables utilisateur, ou None si illisible."""
    try:
        return set(_backend().lire_env_user())
    except Exception:
        return None


def vider(chemin: Path) -> None:
    """Écrase d'octets nuls la taille du fichier (best effort), puis réécrit le gabarit seul."""
    try:
        taille = chemin.stat().st_size
        with open(chemin, "r+b") as f:
            f.write(b"\0" * taille)
            f.flush()
            os.fsync(f.fileno())
    except OSError:
        pass
    chemin.write_text(texte_gabarit(), encoding="utf-8")


def poser_fichier(chemin=None, vider_apres: bool = True):
    """Pose chaque NOM=valeur. Rend (noms posés, numéros mal formés, noms en échec, fichier vidé)."""
    p = assurer_gabarit(chemin)
    paires, erreurs = lire_paires(p)
    b = _backend()
    poses, echecs = [], []
    registre = None
    for nom, val in paires:
        try:
            b.ecrire_env_user(nom, val)
        except (SystemExit, Exception):
            echecs.append(nom)
            continue
        try:
            if registre is None:
                registre = b.lire_registre()
            if nom not in registre:
                b.ajouter_registre(nom, f"posé par fichier le {datetime.date.today().isoformat()}")
        except Exception:
            pass
        poses.append(nom)
    est_vide = False
    if vider_apres and not echecs and (paires or erreurs):
        vider(p)
        est_vide = True
    return poses, erreurs, echecs, est_vide
