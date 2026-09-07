#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GABARIT — recompte tout sur disque et signale les ÉCARTS avec ce qui est annoncé.

⚠️ À ADAPTER au projet : les compteurs de `compter_disque()` et les motifs de `ecarts()`
sont ceux d'un projet de recherche documentaire (sources CSV, rapports, leçons, décisions).
Garder la MÉCANIQUE — compter sur disque, comparer à l'annoncé, ne rien corriger — et
remplacer les compteurs par ceux du projet.

Incarnation du principe n°1 du socle : « une règle que ne vérifie aucune commande n'est pas
une règle ». Un compteur annoncé dans un README dérive toujours ; seul un script le dit.

Pourquoi : l'étape 6 de la clôture de passe (CLAUDE.md §7bis) demande de « recompter les
compteurs ». Faite à la main, elle se rate — le 07/09/2026 trois écarts coexistaient
(README annonçait 320 sources l.117 et 326 l.29 ; 137 rapports pour 139 réels ; §8
annonçait 130 sources d'export pour 129).

Ce script ne corrige rien : il DIT ce qui diverge. La correction reste un acte éditorial.

Usage :  python3 tools/check_coherence.py
Sortie : code 0 si tout concorde, 1 si au moins un écart.
"""
import sys, io
for _s in ("stdout", "stderr"):                     # console Windows = cp1252
    _f = getattr(sys, _s)
    if hasattr(_f, "reconfigure"):
        _f.reconfigure(encoding="utf-8", errors="replace")

import csv, json, os, re, sys, collections

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lire(p):
    with open(os.path.join(R, p), encoding="utf-8") as f:
        return f.read()


def compter_disque():
    """Les chiffres RÉELS, lus sur le disque."""
    d = {}
    if not os.path.exists(os.path.join(R, "data", "sources.csv")):
        sys.exit("GABARIT NON ADAPTÉ : compter_disque() et ecarts() décrivent encore le projet "
                 "d'origine (data/sources.csv, research/, memory/acquis.md). Remplacer les compteurs "
                 "par ceux de CE projet avant de l'utiliser — voir l'en-tête du fichier.")
    with open(os.path.join(R, "data", "sources.csv"), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    d["sources_csv"] = len(rows)
    d["colonnes_csv"] = len(rows[0]) if rows else 0

    e = json.load(open(os.path.join(R, "data", "export", "sources-noyau.json"), encoding="utf-8"))
    d["export"] = e["meta"].get("nb_sources")
    lots = collections.Counter(s.get("lot") for s in e["sources"])
    d["lots"] = "A=%d B=%d C=%d" % (lots["A"], lots["B"], lots["C"])
    ham = collections.Counter((s.get("qualite_prix") or {}).get("hammer_ou_frais")
                              for s in e["sources"])
    d["hammer"] = dict(ham)

    rp = os.path.join(R, "research")
    d["research"] = len([f for f in os.listdir(rp) if f.endswith(".md")])
    d["docs_numerotes"] = len([f for f in os.listdir(os.path.join(R, "docs")) if re.match(r"\d\d-", f)])

    d["lecons"] = len(re.findall(r"^## L\d+", lire("memory/lessons.md"), re.M))
    d["decisions"] = len(re.findall(r"^## D\d+", lire("memory/decisions.md"), re.M))
    d["acquis"] = len(re.findall(r"^\d+\. ", lire("memory/acquis.md"), re.M))
    d["acquis_indexes"] = len(re.findall(r"^\| \*\*(\d+)\*\* \|", lire("CLAUDE.md"), re.M))
    d["archives_bak"] = len([f for f in os.listdir(os.path.join(R, "data", "_archive")) if ".bak" in f])
    return d


def ecarts(d):
    """Compare aux chiffres ANNONCÉS dans README.md et CLAUDE.md."""
    out = []
    rd = lire("README.md")
    cl = lire("CLAUDE.md")

    for label, motif, attendu in [
        # motif ancré sur "dans data/sources.csv" : "129 sources" désigne l'EXPORT, pas le CSV
        ("README : sources dans sources.csv",
         r"\*\*(\d{3}) sources\*\*[^.]{0,40}dans `?data/sources\.csv", d["sources_csv"]),
        ("README : fichiers dans research/",  r"\*\*(\d{2,3}) fichiers\*\* dans `research/`", d["research"]),
    ]:
        vals = {int(v) for v in re.findall(motif, rd)}
        if len(vals) > 1:
            out.append("%s : valeurs CONTRADICTOIRES dans le fichier %s (réel : %s)"
                       % (label, sorted(vals), attendu))
        elif vals and attendu not in vals:
            out.append("%s : annoncé %s, réel %s" % (label, sorted(vals)[0], attendu))

    m = re.search(r"CHIFFRES COURANTS \([^)]*\) : \*\*?(\d+) sources", cl) or \
        re.search(r"CHIFFRES COURANTS[^\n]*?(\d{3}) sources", cl)
    if m and int(m.group(1)) != d["export"]:
        out.append("CLAUDE.md §8 bandeau : annonce %s sources d'export, réel %s"
                   % (m.group(1), d["export"]))

    refs = set(re.findall(r"research/(\d+)-", cl))
    have = {f.split("-")[0] for f in os.listdir(os.path.join(R, "research")) if f[:1].isdigit()}
    manquants = sorted(refs - have, key=int)
    if manquants:
        out.append("CLAUDE.md : %d référence(s) research/ introuvable(s) : %s"
                   % (len(manquants), manquants))

    # T40 : chaque acquis de memory/acquis.md doit avoir sa ligne dans l'index du §8
    txt = {int(x) for x in re.findall(r"^(\d+)\. ", lire("memory/acquis.md"), re.M)}
    idx = {int(x) for x in re.findall(r"^\| \*\*(\d+)\*\* \|", lire("CLAUDE.md"), re.M)}
    if txt - idx:
        out.append("acquis SANS ligne dans l'index du §8 : %s (invisibles)" % sorted(txt - idx))
    if idx - txt:
        out.append("index du §8 : ligne(s) sans acquis correspondant : %s" % sorted(idx - txt))

    a = lire("AGENTS.md")
    if a.split("-->", 1)[-1].strip() != cl.strip():
        out.append("AGENTS.md n'est plus le miroir exact de CLAUDE.md — régénérer")
    return out


def main() -> int:
    d = compter_disque()
    print("== Compteurs réels (disque) ==")
    for k, v in d.items():
        print("   %-18s %s" % (k, v))

    e = ecarts(d)
    print("\n== Écarts avec ce qui est annoncé ==")
    if not e:
        print("   aucun — les fichiers disent vrai.")
        return 0
    for x in e:
        print("   ⚠️  " + x)
    print("\n   → corriger les fichiers, PAS les compteurs (CLAUDE.md §7bis étape 6).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
