#!/usr/bin/env python3
"""Check anti-collision des briefs handoff — porte de vérification.

Lit tous les docs/handoffs/HO-*.md, extrait le frontmatter (id, statut, fichiers)
et ÉCHOUE (exit 1) si :
  - deux briefs ACTIFS (pret | en_cours) revendiquent le même fichier
  - un id est en doublon, ou ne correspond pas au nom du fichier
  - un statut n'est pas dans le vocabulaire fermé
  - un brief actif n'a aucun fichier déclaré
Affiche le registre (id, statut, fichiers) : c'est LE registre, dérivé des briefs,
jamais tenu à la main.

Usage : python handoff-check.py [docs/handoffs]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

STATUTS = {"brouillon", "pret", "en_cours", "fait", "abandonne"}
ACTIFS = {"pret", "en_cours"}


def parse_front(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    fm, cur = {}, None
    for line in m.group(1).splitlines():
        line = line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if re.match(r"^\s+-\s", line) and cur:
            fm.setdefault(cur, []).append(line.split("-", 1)[1].strip().strip("'\""))
        elif ":" in line:
            k, v = line.split(":", 1)
            cur, v = k.strip(), v.strip().strip("'\"")
            fm[cur] = v if v else []
    return fm


def main(root: Path) -> int:
    briefs = sorted(root.glob("HO-*.md"))
    if not briefs:
        print(f"aucun brief dans {root}")
        return 0
    errors, owners, ids = [], defaultdict(list), {}
    print(f"{'id':8} {'statut':10} fichiers")
    for b in briefs:
        fm = parse_front(b.read_text(encoding="utf-8"))
        hid, st = fm.get("id", "?"), fm.get("statut", "?")
        files = fm.get("fichiers") or []
        if isinstance(files, str):
            files = [files]
        print(f"{hid:8} {st:10} {', '.join(files) or '-'}")
        if not fm:
            errors.append(f"{b.name}: frontmatter absent")
            continue
        if not b.name.startswith(hid + "-") and b.name != hid + ".md":
            errors.append(f"{b.name}: id '{hid}' != nom de fichier")
        if hid in ids:
            errors.append(f"{b.name}: id {hid} deja pris par {ids[hid]}")
        ids[hid] = b.name
        if st not in STATUTS:
            errors.append(f"{b.name}: statut '{st}' hors vocabulaire {sorted(STATUTS)}")
        if st in ACTIFS:
            if not files:
                errors.append(f"{b.name}: actif sans fichier déclaré")
            for f in files:
                owners[f.replace("\\", "/")].append(hid)
    for f, hs in owners.items():
        if len(hs) > 1:
            errors.append(f"COLLISION {f} : {' + '.join(hs)}")
    print()
    if errors:
        print("HANDOFF KO")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"HANDOFF OK - {len(briefs)} brief(s), {sum(1 for _ in owners)} fichier(s) sous ownership actif")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "docs/handoffs")))
