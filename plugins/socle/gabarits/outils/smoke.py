#!/usr/bin/env python3
"""Preuve d'ecran du projet : lance les scenarios, produit des captures et un mesures.json.

Convention du plugin socle : `python outils/smoke.py` est la seule commande que `photographe`
et `banc` appellent pour voir un ecran. Contrat de sortie a respecter une fois implemente :
  - une capture PNG par scenario et par largeur dans --sortie ;
  - un fichier mesures.json (cle -> valeur chiffree : chevauchements, debordements, durees) ;
  - sur stdout : une ligne `A OUVRIR : <chemin>` par capture ;
  - exit 0 si les scenarios ont tourne (cela ne prouve rien sur les pixels : on regarde les captures).
Conseil : Playwright Python, profil SSO partage machine C:/tmp/claude/pw-profile, headless.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preuve d'ecran : captures + mesures.json. Squelette a implementer pour ce projet.")
    parser.add_argument("--scenarios", default="pages", help="liste de scenarios separes par des virgules")
    parser.add_argument("--largeurs", default="1440", help="largeurs en px, separees par des virgules")
    parser.add_argument("--sortie", default="captures", help="dossier de sortie des captures")
    parser.add_argument("--prefixe", default="", help="prefixe des fichiers (avant, apres)")
    parser.parse_args()
    print("non implemente pour ce projet : voir ${CLAUDE_PLUGIN_ROOT}/skills/recette-ecran/SKILL.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
