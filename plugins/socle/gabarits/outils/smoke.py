#!/usr/bin/env python3
"""Preuve d'ecran du projet : lance les scenarios et produit des captures PNG.

Gabarit du plugin socle, il tourne tel quel. Tant que SCENARIOS est vide, il n'ouvre aucun
navigateur, affiche AUCUNE CAPTURE et rend 0 : rien n'a ete prouve. Pour l'utiliser, remplir
SCENARIOS (nom -> URL).

Contrat (celui que `photographe` et `banc` attendent) :
  - une capture PNG par scenario et par largeur dans --sortie
    (defaut recette/<AAAA-MM-JJ>/, dossier git-ignore) ;
  - sur stdout : une ligne `A OUVRIR : <chemin>` par capture ;
  - exit 0 si les scenarios ont tourne, 1 si l'un d'eux a echoue. Cela ne prouve rien sur les
    pixels : on ouvre et on regarde les captures ;
  - des mesures chiffrees sont facultatives : si le projet en ecrit, il en annonce le chemin.
Largeurs : 390 (mobile), 1440 (desktop), 1850 (large), celles de la bibliotheque preuve_navigateur,
dont le shim outils/preuve_navigateur.py est voisin de ce fichier.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

SCENARIOS: dict[str, str] = {}  # ex. {"accueil": "http://localhost:8501"}
VIEWPORTS = {390: "mobile", 1440: "desktop", 1850: "large"}


def capturer_scenario(nom: str, url: str, largeur: int, sortie: Path, prefixe: str) -> Path:
    from preuve_navigateur import capturer, ouvrir  # shim voisin, importe seulement si utile

    with ouvrir(viewport=VIEWPORTS[largeur]) as (_ctx, page):
        page.goto(url, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        return capturer(page, sortie / f"{prefixe}{nom}_{largeur}.png")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preuve d'ecran : captures PNG. Sans scenario defini : AUCUNE CAPTURE, exit 0.")
    parser.add_argument("--scenarios", default="", help="noms separes par des virgules (defaut : tous)")
    parser.add_argument("--largeurs", default="1440", help="largeurs en px parmi 390, 1440, 1850, separees par des virgules")
    parser.add_argument("--sortie", default=f"recette/{date.today():%Y-%m-%d}", help="dossier de sortie (defaut : recette/<date>)")
    parser.add_argument("--prefixe", default="", help="prefixe des fichiers (avant, apres)")
    args = parser.parse_args()

    noms = [n for n in args.scenarios.split(",") if n] or list(SCENARIOS)
    if not noms:
        print(f"AUCUNE CAPTURE : aucun scenario defini (SCENARIOS vide dans {Path(__file__).name}). "
              f"Sortie prevue : {args.sortie}")
        return 0
    largeurs = [int(x) for x in args.largeurs.split(",") if x]
    inconnues = [x for x in largeurs if x not in VIEWPORTS] + [n for n in noms if n not in SCENARIOS]
    if inconnues:
        print(f"ECHEC : inconnu(s) {inconnues} (largeurs {sorted(VIEWPORTS)}, scenarios {sorted(SCENARIOS)})")
        return 1
    sortie, ok = Path(args.sortie), True
    for nom in noms:
        for largeur in largeurs:
            try:
                print(f"A OUVRIR : {capturer_scenario(nom, SCENARIOS[nom], largeur, sortie, args.prefixe)}")
            except Exception as exc:  # un scenario en echec ne masque pas les autres
                ok = False
                print(f"ECHEC : {nom} a {largeur} px : {exc}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
