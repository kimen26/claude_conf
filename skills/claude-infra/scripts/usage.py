#!/usr/bin/env python3
"""Mesure d'usage des skills, agents et MCP de ~/.claude (stdlib seule).

    usage.py                      rapport (tableau nom | type | appels | dernier usage | verdict)
    usage.py --radical            montre ce qui serait déplacé (skills et agents inutilisés)
    usage.py --radical --oui      déplace vers ~/.claude/_a_supprimer/<AAAA-MM-JJ>/ + MANIFESTE.md

Source : transcripts ~/.claude/projects/*/*.jsonl (appels Skill, Agent, outils mcp__*, et
commandes slash <command-name>). Verdict : actif < 30 j, dormant 30 à 90 j, inutilisé > 90 j
ou jamais. Ne supprime JAMAIS rien : on déplace, Yann supprime lui-même.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

HOME = Path.home() / ".claude"
EXCLUS = {"nouveau-projet", "claude-infra", "Sync-Skills-github-ProPerso", "netskope-ssl"}
SLASH = re.compile(r"<command-name>/?([^<\s]+)</command-name>")


def derniere_valeur(paires):
    """Clés dupliquées : la dernière gagne (~/.claude.json en contient)."""
    d = {}
    for k, v in paires:
        d[k] = v
    return d


def date_de(ts, repli: dt.datetime) -> dt.datetime:
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone().replace(tzinfo=None)
    except (AttributeError, ValueError):
        return repli


def parcourir() -> dict:
    """{(type, nom): [appels, premier, dernier]} lu dans les transcripts."""
    stats: dict = collections.defaultdict(lambda: [0, None, None])

    def noter(cle, quand):
        s = stats[cle]
        s[0] += 1
        s[1] = quand if s[1] is None or quand < s[1] else s[1]
        s[2] = quand if s[2] is None or quand > s[2] else s[2]

    for f in (HOME / "projects").glob("*/*.jsonl"):
        mtime = dt.datetime.fromtimestamp(f.stat().st_mtime)
        try:
            flux = f.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with flux:
            for ligne in flux:
                if '"tool_use"' not in ligne and "<command-name>" not in ligne:
                    continue
                try:
                    d = json.loads(ligne)
                except ValueError:
                    continue
                quand = date_de(d.get("timestamp"), mtime)
                contenu = (d.get("message") or {}).get("content")
                if isinstance(contenu, str):
                    contenu = [{"type": "text", "text": contenu}]
                for b in contenu if isinstance(contenu, list) else []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_use":
                        nom, inp = b.get("name", ""), b.get("input") or {}
                        if nom == "Skill" and inp.get("skill"):
                            noter(("skill", str(inp["skill"])), quand)
                        elif nom == "Agent" and inp.get("subagent_type"):
                            noter(("agent", str(inp["subagent_type"])), quand)
                        elif nom.startswith("mcp__"):
                            noter(("mcp", nom.split("__")[1]), quand)
                    elif b.get("type") == "text" and d.get("type") == "user":
                        for m in SLASH.findall(b.get("text", "")):
                            noter(("skill", m), quand)
    return stats


def inventaire() -> list[tuple[str, str, Path | None]]:
    inv = []
    for s in sorted((HOME / "skills").glob("*/SKILL.md")):
        inv.append(("skill", s.parent.name, s.parent))
    for a in sorted((HOME / "agents").glob("*.md")):
        inv.append(("agent", a.stem, a))
    cj = Path.home() / ".claude.json"
    if cj.is_file():
        try:
            data = json.loads(cj.read_text(encoding="utf-8"), object_pairs_hook=derniere_valeur)
        except ValueError:
            data = {}
        noms = set(data.get("mcpServers") or {})
        for p in (data.get("projects") or {}).values():
            if isinstance(p, dict):
                noms |= set(p.get("mcpServers") or {})
        inv += [("mcp", n, None) for n in sorted(noms)]
    return inv


def cherche(stats, typ, nom):
    """Totalise les entrées dont le nom, avec ou sans préfixe plugin:, correspond."""
    tot = [0, None]
    cible = nom.replace("-", "_").replace(".", "_").replace(" ", "_")
    for (t, n), (c, _p, der) in stats.items():
        if t != typ:
            continue
        ok = n == nom or n.split(":")[-1] == nom
        if typ == "mcp":
            ok = ok or n.replace("-", "_").replace(".", "_") == cible
        if ok:
            tot[0] += c
            tot[1] = der if tot[1] is None or (der and der > tot[1]) else tot[1]
    return tot


def verdict(dernier, maintenant):
    if dernier is None:
        return "inutilisé"
    j = (maintenant - dernier).days
    return "actif" if j < 30 else "dormant" if j <= 90 else "inutilisé"


def construire(maintenant):
    stats = parcourir()
    lignes = []
    for typ, nom, chemin in inventaire():
        c, der = cherche(stats, typ, nom)
        lignes.append({"nom": nom, "type": typ, "appels": c, "dernier": der,
                       "verdict": verdict(der, maintenant), "chemin": chemin})
    ordre = {"inutilisé": 0, "dormant": 1, "actif": 2}
    lignes.sort(key=lambda r: (ordre[r["verdict"]], r["type"], r["nom"]))
    return lignes


def tableau(lignes):
    rows = [("nom", "type", "appels", "dernier usage", "verdict")]
    for r in lignes:
        rows.append((r["nom"], r["type"], str(r["appels"]),
                     r["dernier"].strftime("%Y-%m-%d") if r["dernier"] else "jamais", r["verdict"]))
    w = [max(len(x[i]) for x in rows) for i in range(5)]
    return "\n".join("  ".join(x[i].ljust(w[i]) for i in range(5)).rstrip() for x in rows)


def radical(lignes, oui):
    cibles = [r for r in lignes if r["verdict"] == "inutilisé" and r["type"] in ("skill", "agent")
              and r["nom"] not in EXCLUS and r["chemin"] is not None]
    if not cibles:
        print("\nRien à déplacer.")
        return
    jour = HOME / "_a_supprimer" / dt.date.today().isoformat()
    print(f"\n{'Déplacement vers' if oui else 'SIMULATION, serait déplacé vers'} {jour} ({len(cibles)}) :")
    manifeste = []
    for r in cibles:
        dst = jour / (r["type"] + "s") / r["chemin"].name
        print(f"  {r['type']:5} {r['nom']}")
        if oui:
            dst.parent.mkdir(parents=True, exist_ok=True)
            n = 1
            while dst.exists():
                dst = dst.with_name(f"{dst.name}.{n}")
                n += 1
            shutil.move(str(r["chemin"]), str(dst))
            d = r["dernier"].strftime("%Y-%m-%d") if r["dernier"] else "jamais"
            manifeste.append(f"| {r['nom']} | {r['type']} | {d} | inutilisé (aucun appel depuis plus de 90 j) |")
    if oui and manifeste:
        man = jour / "MANIFESTE.md"
        if not man.exists():
            man.write_text(f"# Manifeste {jour.name}\n\nRien n'est supprimé : Yann supprime ce dossier "
                           "lui-même.\n\n| Nom | Type | Dernier usage | Raison |\n|---|---|---|---|\n",
                           encoding="utf-8")
        with man.open("a", encoding="utf-8") as f:
            f.write("\n".join(manifeste) + "\n")
        print(f"MANIFESTE : {man}")
    elif not oui:
        print("Relancer avec --oui après accord de Yann.")


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--radical", action="store_true")
    ap.add_argument("--oui", action="store_true")
    a = ap.parse_args(argv)
    lignes = construire(dt.datetime.now())
    print(tableau(lignes))
    cpt = collections.Counter(r["verdict"] for r in lignes)
    print(f"\n{len(lignes)} éléments : " + ", ".join(f"{cpt[v]} {v}" for v in ("actif", "dormant", "inutilisé")))
    if a.radical:
        radical(lignes, a.oui)
    return 0


if __name__ == "__main__":
    sys.exit(main())
