#!/usr/bin/env python3
"""Mise en place et remise au pas du socle d'un projet (stdlib seule).

    socle_projet.py init [chemin] [--sans-commit]
    socle_projet.py remise-au-pas [chemin] [--radical] [--oui]
    socle_projet.py deplacer <fichiers...> --raison "..." [--remplace-par "..."] [--racine .]

Règles : on n'écrase jamais un fichier existant, on ne supprime jamais rien (les fichiers
retirés du projet sont DÉPLACÉS dans ``_a_supprimer/<AAAA-MM-JJ>/``, Yann supprime lui-même).
``remise-au-pas`` n'applique rien sans ``--oui`` : il imprime ce qu'il ferait.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SHIM = (
    "import sys; from pathlib import Path\n"
    'sys.path.insert(0, str(Path.home()/".claude/plugins/data/socle/lib"))\n'
    "from preuve_navigateur import *  # noqa: F401,F403\n"
)
# (source dans gabarits/, destination dans le projet)
GABARITS_FIXES = [
    ("CLAUDE.md", "CLAUDE.md"),
    ("gitignore", ".gitignore"),
    ("backlog/config.yml", "backlog/config.yml"),
    ("outils/portes.py", "outils/portes.py"),
    ("outils/smoke.py", "outils/smoke.py"),
    ("outils/deployer.py", "outils/deployer.py"),
]
ORDRE_REMISE = ["S-30", "S-10", "S-20", "S-01", "S-02", "S-03", "S-50", "S-60", "S-40"]


# ------------------------------------------------------------------ localisation
def racine_plugin() -> Path:
    """Racine du plugin socle : CLAUDE_PLUGIN_ROOT, sinon cache le plus récent, sinon le repo."""
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env and Path(env).is_dir():
        return Path(env)
    cache = Path.home() / ".claude/plugins/cache"
    candidats = [p for p in cache.glob("*/socle*/versions/*") if p.is_dir()] if cache.is_dir() else []
    candidats += [p for p in cache.glob("*/socle*/*") if p.is_dir() and (p / "hooks").is_dir()] \
        if cache.is_dir() else []
    if candidats:
        return max(candidats, key=lambda p: p.stat().st_mtime)
    repo = Path.home() / ".claude/skills-sync-workspace/claude_conf/plugins/socle"
    if repo.is_dir():
        return repo
    raise SystemExit("plugin socle introuvable (définir CLAUDE_PLUGIN_ROOT)")


def garde_socle() -> Path:
    return racine_plugin() / "hooks/scripts/garde_socle.py"


def lancer_garde(projet: Path, mode: str) -> str:
    """Sortie brute de garde_socle.py, ou chaîne vide s'il est absent."""
    g = garde_socle()
    if not g.exists():
        sys.stderr.write(f"garde_socle.py introuvable : {g}\n")
        return ""
    r = subprocess.run([sys.executable, str(g), mode, str(projet)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip()


def ecarts(projet: Path) -> list[dict]:
    brut = lancer_garde(projet, "--json")
    try:
        data = json.loads(brut) if brut else []
    except json.JSONDecodeError:
        sys.stderr.write("sortie --json illisible\n")
        return []
    return data if isinstance(data, list) else []


# ------------------------------------------------------------------ copie sans écraser
def copier(src: Path, dst: Path) -> bool:
    """Copie ``src`` vers ``dst`` sans écraser. Rend vrai si créé."""
    if dst.exists() or not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return True


def fichiers_gabarits() -> list[tuple[Path, str]]:
    g = racine_plugin() / "gabarits"
    paires = [(g / s, d) for s, d in GABARITS_FIXES]
    if (g / "memory").is_dir():
        paires += [(f, f"memory/{f.name}") for f in sorted((g / "memory").glob("*.md"))]
    return paires


def poser_shim(projet: Path) -> bool:
    dst = projet / "outils/preuve_navigateur.py"
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SHIM, encoding="utf-8")
    return True


def git(projet: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(projet), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


# ------------------------------------------------------------------------ init
def cmd_init(args) -> int:
    projet = Path(args.chemin).resolve()
    projet.mkdir(parents=True, exist_ok=True)
    if not (projet / ".git").exists():
        git(projet, "init")
        print("git init")
    crees = []
    for src, rel in fichiers_gabarits():
        if copier(src, projet / rel):
            crees.append(rel)
        elif (projet / rel).exists():
            print(f"existe, conservé : {rel}")
        else:
            print(f"gabarit absent, ignoré : {rel}")
    if poser_shim(projet):
        crees.append("outils/preuve_navigateur.py")
    crees += initialiser_backlog(projet)
    for rel in crees:
        print(f"créé : {rel}")
    if crees and not args.sans_commit:
        git(projet, "add", "--", *crees)
        r = git(projet, "commit", "-m", "chore: socle projet", "--", *crees)
        print("commit « chore: socle projet »" if r.returncode == 0
              else f"commit non fait : {r.stderr.strip() or r.stdout.strip()}")
    return finir(projet)


def initialiser_backlog(projet: Path) -> list[str]:
    """`backlog init` si la commande existe, sinon crée backlog/tasks/ à la main."""
    crees: list[str] = []
    tasks = projet / "backlog/tasks"
    if tasks.is_dir():
        return crees
    if shutil.which("backlog"):
        config = projet / "backlog/config.yml"
        avant = config.read_bytes() if config.is_file() else None
        try:
            r = subprocess.run(["backlog", "init", projet.name], cwd=projet, capture_output=True,
                               text=True, stdin=subprocess.DEVNULL, timeout=60)
            if r.returncode == 0 and tasks.is_dir():
                return ["backlog/tasks"]
        except (subprocess.TimeoutExpired, OSError):
            pass
        finally:
            if avant is not None and (not config.is_file() or config.read_bytes() != avant):
                config.write_bytes(avant)  # nos statuts priment sur ceux de `backlog init`
        print("backlog init a échoué : création manuelle de backlog/tasks/")
    else:
        print("commande backlog absente : npm i -g backlog.md (une fois par PC)")
    tasks.mkdir(parents=True, exist_ok=True)
    (tasks / ".gitkeep").touch()
    return ["backlog/tasks/.gitkeep"]


def finir(projet: Path) -> int:
    reste = lancer_garde(projet, "--session")
    if reste:
        print("garde_socle --session, écarts restants :\n" + reste)
        return 1
    print("garde_socle --session : vide")
    return 0


# ------------------------------------------------------------------ déplacement
def remplace_par(code: str, fichier: str) -> str:
    p = Path(fichier)
    if code == "S-20":
        return "lib preuve_navigateur du plugin socle (shim outils/preuve_navigateur.py)"
    if "agents" in p.parts:
        return f"agent socle:{p.stem}"
    if "skills" in p.parts:
        nom = p.parent.name if p.name == "SKILL.md" else p.stem
        return f"skill socle:{nom}"
    if "hooks" in p.parts:
        return "hooks du plugin socle (hooks/hooks.json)"
    return "élément équivalent du plugin socle"


def deplacer(projet: Path, fichiers: list[str], raison: str, remplace: str = "") -> list[Path]:
    """Déplace sans jamais supprimer vers ``_a_supprimer/<date>/`` et tient le MANIFESTE."""
    jour = projet / "_a_supprimer" / datetime.date.today().isoformat()
    lignes, faits = [], []
    for rel in fichiers:
        src = projet / rel
        if src.name == "SKILL.md" and src.parent.parent.name == "skills":
            src = src.parent
            rel = src.relative_to(projet).as_posix()
        if not src.exists():
            print(f"absent, ignoré : {rel}")
            continue
        dst = jour / rel
        n = 1
        while dst.exists():
            dst = dst.with_name(f"{dst.name}.{n}")
            n += 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        lignes.append(f"| `{rel}` | {raison} | {remplace or 'à préciser'} |")
        faits.append(dst)
        print(f"déplacé : {rel} -> {dst.relative_to(projet).as_posix()}")
    if lignes:
        man = jour / "MANIFESTE.md"
        if not man.exists():
            man.write_text(f"# Manifeste {jour.name}\n\nRien n'est supprimé : Yann supprime ce "
                           "dossier lui-même.\n\n| Fichier | Raison | Remplacé par |\n|---|---|---|\n",
                           encoding="utf-8")
        with man.open("a", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
    return faits


def cmd_deplacer(args) -> int:
    deplacer(Path(args.racine).resolve(), args.fichiers, args.raison, args.remplace_par or "")
    return 0


# ----------------------------------------------------------------- remise au pas
def planifier(projet: Path, radical: bool) -> list[dict]:
    """Transforme les écarts en gestes : creer / ajouter / deplacer / manuel."""
    liste = sorted(ecarts(projet), key=lambda e: ORDRE_REMISE.index(e["code"])
                   if e["code"] in ORDRE_REMISE else 99)
    gestes: list[dict] = []
    vus: set = set()
    for e in liste:
        code, fichier = e["code"], e.get("fichier", "")
        regle, correctif = e.get("regle", ""), e.get("correctif", "")
        g = {"code": code, "fichier": fichier, "regle": regle, "correctif": correctif}
        if code in ("S-01", "S-02", "S-03", "S-50", "S-60"):
            g["geste"] = "completer"
        elif code in ("S-40", "S-20") and radical and fichier and "mcpServers" not in regle \
                and fichier != "outils/preuve_navigateur.py":
            g["geste"] = "deplacer"
        else:
            g["geste"] = "manuel"
        cle = (g["geste"], code, fichier) if g["geste"] != "completer" else ("completer", code)
        if cle in vus:
            continue
        vus.add(cle)
        gestes.append(g)
    return gestes


def completer(projet: Path, code: str) -> list[str]:
    """Pose ce qui manque pour S-01/02/03/50/60, sans rien écraser."""
    voulus = {"S-01": ["CLAUDE.md"], "S-02": ["memory/"], "S-03": [".gitignore"],
              "S-50": ["backlog/"], "S-60": ["outils/portes.py", "outils/smoke.py",
                                             "outils/deployer.py"]}[code]
    crees = []
    for src, rel in fichiers_gabarits():
        if any(rel == v or (v.endswith("/") and rel.startswith(v)) for v in voulus):
            if rel == ".gitignore" and (projet / rel).exists():
                if ajouter_gitignore(src, projet / rel):
                    crees.append(f"{rel} (lignes ajoutées)")
            elif copier(src, projet / rel):
                crees.append(rel)
    if code == "S-50":
        crees += initialiser_backlog(projet)
    return crees


def ajouter_gitignore(src: Path, dst: Path) -> bool:
    actuel = dst.read_text(encoding="utf-8", errors="replace").splitlines()
    manque = [ligne for ligne in src.read_text(encoding="utf-8").splitlines()
              if ligne.strip() and not ligne.startswith("#") and ligne not in actuel]
    if not manque:
        return False
    with dst.open("a", encoding="utf-8") as f:
        f.write("\n" + "\n".join(manque) + "\n")
    return True


def cmd_remise(args) -> int:
    projet = Path(args.chemin).resolve()
    gestes = planifier(projet, args.radical)
    if not gestes:
        print("aucun écart")
        return finir(projet)
    mode = "APPLIQUE" if args.oui else "SIMULATION (rien n'est modifié ; relancer avec --oui après accord de Yann)"
    print(f"Remise au pas{' radicale' if args.radical else ''} : {mode}\n")
    for g in gestes:
        lib = {"completer": "compléter", "deplacer": "déplacer vers _a_supprimer/",
               "manuel": "à traiter à la main"}[g["geste"]]
        cible = f" {g['fichier']}" if g["fichier"] else ""
        print(f"[{g['code']}]{cible} : {g['regle']} -> {lib}"
              + (f" ({g['correctif']})" if g["geste"] == "manuel" and g["correctif"] else ""))
        if not args.oui:
            continue
        if g["geste"] == "completer":
            for c in completer(projet, g["code"]):
                print(f"   créé : {c}")
        elif g["geste"] == "deplacer":
            deplacer(projet, [g["fichier"]], g["regle"], remplace_par(g["code"], g["fichier"]))
    return finir(projet) if args.oui else 0


# -------------------------------------------------------------------------- CLI
def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="socle_projet", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init", help="projet neuf")
    i.add_argument("chemin", nargs="?", default=".")
    i.add_argument("--sans-commit", action="store_true")
    r = sub.add_parser("remise-au-pas", help="projet existant")
    r.add_argument("chemin", nargs="?", default=".")
    r.add_argument("--radical", action="store_true")
    r.add_argument("--oui", action="store_true")
    d = sub.add_parser("deplacer", help="déplacer dans _a_supprimer/ avec manifeste")
    d.add_argument("fichiers", nargs="+")
    d.add_argument("--raison", required=True)
    d.add_argument("--remplace-par", default="")
    d.add_argument("--racine", default=".")
    return ap


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parser().parse_args(argv)
    return {"init": cmd_init, "remise-au-pas": cmd_remise, "deplacer": cmd_deplacer}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
