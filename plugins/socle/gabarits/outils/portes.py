#!/usr/bin/env python3
"""Portes mecaniques du projet : toutes les verifications vert/rouge, en une commande.

Convention du plugin socle : `python outils/portes.py` sort en code 0 si toutes les portes sont
vertes, 1 sinon. Les agents (greffier, executant, relecteur) et /socle:livrer n'appellent que ca.

Deux portes generiques sont deja la. Ajouter les portes propres au projet dans PORTES_PROJET :
chaque porte est une fonction sans argument qui rend une liste de problemes (vide = verte).
"""
from __future__ import annotations

import argparse
import py_compile
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
EXCLUS = {".venv", "venv", "node_modules", ".git", "_a_supprimer", "__pycache__", ".auth"}
CADRATINS = (chr(0x2014), chr(0x2013))


def fichiers(suffixes: tuple[str, ...]):
    for chemin in RACINE.rglob("*"):
        if chemin.is_file() and chemin.suffix in suffixes and not (EXCLUS & set(chemin.parts)):
            yield chemin


def porte_compilation() -> list[str]:
    """Tout .py du projet (hors venv) compile."""
    problemes = []
    for chemin in fichiers((".py",)):
        try:
            py_compile.compile(str(chemin), cfile=None, doraise=True, dfile=str(chemin))
        except py_compile.PyCompileError as exc:
            problemes.append(f"{chemin.relative_to(RACINE)} : {exc.msg.strip()}")
    # py_compile ecrit un .pyc par defaut ; on n'en laisse pas derriere soi.
    for cache in RACINE.rglob("__pycache__"):
        if not (EXCLUS - {"__pycache__"}) & set(cache.parts):
            for pyc in cache.glob("*.pyc"):
                pyc.unlink(missing_ok=True)
            try:
                cache.rmdir()
            except OSError:
                pass
    return problemes


def porte_cadratin() -> list[str]:
    """Aucun cadratin ni demi-cadratin dans les .py et .md (hors _a_supprimer)."""
    problemes = []
    for chemin in fichiers((".py", ".md")):
        if chemin.name == Path(__file__).name:
            continue
        texte = chemin.read_text(encoding="utf-8", errors="replace")
        for numero, ligne in enumerate(texte.splitlines(), start=1):
            if any(c in ligne for c in CADRATINS):
                problemes.append(f"{chemin.relative_to(RACINE)}:{numero} : cadratin")
    return problemes


PORTES_GENERIQUES = {"compilation": porte_compilation, "cadratin": porte_cadratin}
PORTES_PROJET: dict = {}  # ajouter ici : {"nom": fonction}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rejoue toutes les portes mecaniques du projet. Exit 0 = toutes vertes, 1 sinon.")
    parser.add_argument("--porte", help="ne jouer qu'une porte (par son nom)")
    args = parser.parse_args()

    portes = {**PORTES_GENERIQUES, **PORTES_PROJET}
    if args.porte:
        if args.porte not in portes:
            print(f"porte inconnue : {args.porte} (connues : {', '.join(portes)})")
            return 1
        portes = {args.porte: portes[args.porte]}

    rouges = 0
    for nom, porte in portes.items():
        problemes = porte()
        etat = "VERTE" if not problemes else "ROUGE"
        print(f"[{etat}] {nom}")
        for probleme in problemes[:20]:
            print(f"    {probleme}")
        if len(problemes) > 20:
            print(f"    +{len(problemes) - 20} autres")
        rouges += bool(problemes)
    print(f"{len(portes) - rouges}/{len(portes)} portes vertes")
    return 1 if rouges else 0


if __name__ == "__main__":
    sys.exit(main())
