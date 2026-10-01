#!/usr/bin/env python3
"""Mise en service de HEAD : la seule commande de deploiement que /socle:livrer appelle.

Convention du plugin socle. Contrat une fois implemente :
  - deploie le commit HEAD (jamais l'arbre de travail non commite) ;
  - controle apres coup que ce qui est servi est identique a HEAD (hachage fichier par fichier) ;
  - exit 0 seulement si tout est identique, 1 sinon ; aucun secret affiche ;
  - --dry-run decrit ce qui serait fait sans rien ecrire.
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Met HEAD en service et verifie le resultat. Squelette a implementer pour ce projet.")
    parser.add_argument("--dry-run", action="store_true", help="decrire sans ecrire")
    parser.parse_args()
    print("non implemente pour ce projet : voir ${CLAUDE_PLUGIN_ROOT}/skills/livrer/SKILL.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
