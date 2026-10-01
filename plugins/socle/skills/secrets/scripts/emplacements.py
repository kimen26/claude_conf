#!/usr/bin/env python3
"""Inventaire de C:\\tmp\\claude (stdlib seule). Ne supprime et ne déplace jamais rien.

    emplacements.py purger [--racine C:/tmp/claude]

Liste le contenu par dossier (taille, date), propose le déplacement du profil navigateur
(`preuve_navigateur.py migrer-profil`) et imprime ce que Yann peut supprimer lui-même.
"""
from __future__ import annotations

import argparse
import datetime
import os
import sys
from pathlib import Path

RACINE = Path("C:/tmp/claude")
EVIDENTS = ("venv-", "pw-shots")
PROFIL = "pw-profile"
MIGRER = "python outils/preuve_navigateur.py migrer-profil  (depuis un projet ayant le shim)"


def taille(p: Path) -> int:
    """Taille cumulée en octets ; les erreurs d'accès sont ignorées."""
    if p.is_file():
        try:
            return p.stat().st_size
        except OSError:
            return 0
    total = 0
    for dossier, _sous, fichiers in os.walk(p, onerror=lambda _e: None):
        for f in fichiers:
            try:
                total += os.path.getsize(os.path.join(dossier, f))
            except OSError:
                pass
    return total


def humain(n: int) -> str:
    for unite in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or unite == "Go":
            return f"{n:.0f} {unite}" if unite == "o" else f"{n:.1f} {unite}"
        n /= 1024
    return f"{n} o"


def date(p: Path) -> str:
    try:
        return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        return "?"


def inventorier(racine: Path) -> dict:
    dossiers, vrac = [], []
    for p in sorted(racine.iterdir(), key=lambda x: x.name.lower()):
        (dossiers if p.is_dir() else vrac).append(p)
    return {"dossiers": [(p, taille(p), date(p)) for p in dossiers],
            "vrac": (len(vrac), sum(taille(p) for p in vrac))}


def classer(p: Path) -> str:
    if p.name == PROFIL:
        return "a migrer"
    if p.name.startswith(EVIDENTS):
        return "candidat evident"
    return "a examiner"


def cmd_purger(args) -> int:
    racine = Path(args.racine)
    if not racine.is_dir():
        print(f"rien : {racine} n'existe pas")
        return 0
    inv = inventorier(racine)
    lignes = [("dossier", "taille", "date", "verdict")]
    for p, n, d in inv["dossiers"]:
        lignes.append((p.name, humain(n), d, classer(p)))
    nb, octets = inv["vrac"]
    if nb:
        lignes.append((f"(fichiers en vrac : {nb})", humain(octets), "-", "a examiner"))
    w = [max(len(l[i]) for l in lignes) for i in range(4)]
    print("\n".join("  ".join(l[i].ljust(w[i]) for i in range(4)).rstrip() for l in lignes))
    total = sum(n for _p, n, _d in inv["dossiers"]) + octets
    print(f"\nTotal : {humain(total)} dans {racine}")
    if any(classer(p) == "a migrer" for p, _n, _d in inv["dossiers"]):
        print(f"\nProfil navigateur : le déplacer plutôt que le supprimer :\n  {MIGRER}")
    a_supprimer = [p for p, _n, _d in inv["dossiers"] if classer(p) != "a migrer"]
    if a_supprimer:
        print("\nÀ supprimer par Yann, après coup d'oeil (rien n'est supprimé ici) :")
        for p in a_supprimer:
            print(f"  Remove-Item -Recurse -Force '{p}'" + ("   # candidat évident" if classer(p) == "candidat evident" else ""))
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="emplacements", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("purger")
    g.add_argument("--racine", default=str(RACINE))
    return ap


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parser().parse_args(argv)
    return cmd_purger(args)


if __name__ == "__main__":
    sys.exit(main())
