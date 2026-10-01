#!/usr/bin/env python3
"""Pilier secrets et accès du plugin socle (stdlib seule, Python 3.11, Windows).

    secrets.py inventaire [chemin] [--json]
    secrets.py verifier
    secrets.py poser NOM [--usage "..."] [--reserve]
    secrets.py poser --fichier [chemin] [--sans-vider] [--reserve]
    secrets.py ssl
    secrets.py purger [--oui]
    secrets.py snow

RÈGLE ABSOLUE : ce script ne lit, n'affiche et ne recopie JAMAIS la valeur d'un secret.
Il manipule des NOMS, des chemins et des états. Seule exception : `poser` reçoit la valeur par
saisie masquée et la passe par stdin à PowerShell (jamais en argument de ligne de commande).
Il ne supprime jamais rien : `purger` déplace dans ~/.claude/_a_supprimer/.
"""
from __future__ import annotations

import argparse
import datetime
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "hooks" / "scripts"))
import motifs_secrets as ms  # noqa: E402
import poser_secrets as ps  # noqa: E402

BUNDLE = r"C:\ProgramData\Netskope\stagent\data\netskope-complete-bundle.crt"
NOM_VALIDE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TAILLE_MAX = 5_000_000
EXEMPLES = (".example", ".sample", ".template")
MODELES_PS1 = (".template.ps1", ".example.ps1", ".sample.ps1")
ETATS = ("conforme", "a_deplacer", "doublon", "sauvegarde_a_purger", "hors_registre", "config_morte",
         "exemple_manquant", "non_conforme_sso")
INSTALL_SNOW = 'uv tool install snowflake-cli --native-tls --with "snowflake-connector-python[secure-local-storage]"'


# ------------------------------------------------------------------ localisation
def home() -> Path:
    return Path.home()


def dossier_claude() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env) if env else home() / ".claude"


def fichier_claude_json() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return (Path(env) if env else home()) / ".claude.json"


def chemin_registre() -> Path:
    """Registre des noms : le repo d'abord, puis CLAUDE_PLUGIN_ROOT, puis le cache le plus récent."""
    nom = "secrets-registre.md"
    repo = repo_registre()
    if repo.is_file():
        return repo
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env and (Path(env) / "rules" / nom).is_file():
        return Path(env) / "rules" / nom
    cache = home() / ".claude/plugins/cache/yann/socle"
    if cache.is_dir():
        def version(p: Path):
            return tuple(int(x) if x.isdigit() else 0 for x in re.split(r"[.\-]", p.name))
        for d in sorted((p for p in cache.iterdir() if p.is_dir()), key=version, reverse=True):
            if (d / "rules" / nom).is_file():
                return d / "rules" / nom
    return repo


def repo_registre() -> Path:
    return home() / ".claude/skills-sync-workspace/claude_conf/plugins/socle/rules/secrets-registre.md"


def avertir_hors_repo() -> None:
    if chemin_registre() != repo_registre():
        print("registre modifié hors repo : à reporter dans claude_conf et bumper la version")


# ------------------------------------------------------------------ environnement user (noms seulement)
def _powershell(script: str, entree: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                          input=entree, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=60)


def lire_env_user() -> list[str]:
    """NOMS des variables d'environnement utilisateur Windows. Les valeurs ne sont pas lues."""
    r = _powershell("[Environment]::GetEnvironmentVariables('User').Keys")
    return sorted({l.strip() for l in r.stdout.splitlines() if l.strip()})


def ecrire_env_user(nom: str, valeur: str) -> None:
    """Pose une variable utilisateur. La valeur passe par stdin, jamais par la ligne de commande."""
    if not NOM_VALIDE.match(nom):
        raise SystemExit(f"nom de variable invalide : {nom}")
    script = ("[Console]::InputEncoding=[Text.Encoding]::UTF8; "
              "$v=[Console]::In.ReadToEnd().TrimEnd(\"`r\",\"`n\"); "
              f"[Environment]::SetEnvironmentVariable('{nom}',$v,'User')")
    r = _powershell(script, entree=valeur)
    if r.returncode != 0:
        raise SystemExit(f"échec PowerShell pour {nom} (code {r.returncode})")


# ------------------------------------------------------------------ registre
STATUTS = ("requis", "reserve")
ENTETE_REGISTRE = ("| nom | statut | usage | consommateurs | posé le |\n"
                   "|---|---|---|---|---|\n")


def _cellules(ligne: str) -> list[str]:
    return [x.strip() for x in ligne.strip().strip("|").split("|")]


def _a_statut(lignes: list[str]) -> bool:
    """Le tableau porte-t-il une colonne statut ? (entête lue ; ancien format = non)"""
    for l in lignes:
        if l.strip().startswith("|"):
            c = [x.lower() for x in _cellules(l)]
            return len(c) > 1 and c[0] == "nom" and c[1] == "statut"
    return True


def lire_registre() -> dict[str, dict]:
    """{nom: {statut, usage, consommateurs, pose}}. Ancienne ligne sans colonne statut = requis."""
    p = chemin_registre()
    out: dict[str, dict] = {}
    if not p.is_file():
        return out
    lignes = p.read_text(encoding="utf-8", errors="replace").splitlines()
    nouveau = _a_statut(lignes)
    for l in lignes:
        if not l.strip().startswith("|"):
            continue
        c = _cellules(l)
        nom = c[0].strip("`") if c else ""
        if not (NOM_VALIDE.match(nom) and nom.upper() == nom):
            continue
        if nouveau and len(c) >= 5:
            statut = c[1].strip("`").lower()
            out[nom] = {"statut": statut if statut in STATUTS else "requis",
                        "usage": c[2], "consommateurs": c[3], "pose": c[4]}
        elif len(c) >= 4:
            out[nom] = {"statut": "requis", "usage": c[1], "consommateurs": c[2], "pose": c[3]}
    return out


def ajouter_registre(nom: str, usage: str, consommateurs: str = "-", statut: str = "requis") -> str:
    """Ajoute la ligne si absente ; si présente, rafraîchit la date. Rend 'ajoute' ou 'maj'."""
    if statut not in STATUTS:
        raise SystemExit(f"statut invalide : {statut} (requis ou reserve)")
    p = chemin_registre()
    jour = datetime.date.today().isoformat()
    if not p.is_file():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Registre des secrets (noms seulement)\n\n" + ENTETE_REGISTRE, encoding="utf-8")
    lignes = p.read_text(encoding="utf-8").splitlines()
    nouveau = _a_statut(lignes)
    for i, l in enumerate(lignes):
        c = _cellules(l)
        if l.strip().startswith("|") and c and c[0].strip("`") == nom and len(c) >= (5 if nouveau else 4):
            c[-1] = jour
            if nouveau:
                c[1] = statut
            lignes[i] = "| " + " | ".join(c) + " |"
            p.write_text("\n".join(lignes) + "\n", encoding="utf-8")
            return "maj"
    usage = usage or "à qualifier"
    if nouveau:
        lignes.append(f"| `{nom}` | {statut} | {usage} | {consommateurs} | {jour} |")
    else:
        lignes.append(f"| `{nom}` | {usage} | {consommateurs} | {jour} |")
    p.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return "ajoute"


# ------------------------------------------------------------------ lecture de fichiers (jamais d'affichage)
def _texte(p: Path) -> str:
    try:
        if p.stat().st_size > TAILLE_MAX:
            return ""
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _json_derniere(p: Path):
    """JSON où la dernière occurrence d'une clé dupliquée l'emporte (.claude.json en a)."""
    try:
        return json.loads(_texte(p), object_pairs_hook=lambda paires: dict(paires))
    except ValueError:
        return None


def _en_tete_secret(k: str) -> bool:
    return ms.nom_secret(k) or k.lower() in ("authorization", "x-api-key", "cookie")


def _etat_valeur(k, v, entete=False) -> str | None:
    """Etat d'une paire (nom, valeur) sans rien exposer : None si sans intérêt.

    Règle unique pour env et headers : une valeur banale (vide, nombre, booléen, ${VAR},
    chemin existant) n'est jamais un secret ; sinon motif, ou nom secret.
    """
    if ms.valeur_en_clair(k, v) or (entete and _en_tete_secret(k) and isinstance(v, str) and not ms.banal(v)):
        return "a_deplacer"
    if ms.nom_secret(k) or (isinstance(v, str) and "${" in v):
        return "conforme"
    return None


# ------------------------------------------------------------------ inventaire
class Ligne(dict):
    pass


def _ligne(emplacement, nom, type_, etat, chemin=None) -> Ligne:
    return Ligne(emplacement=emplacement, nom=nom, type=type_, etat=etat, chemin=chemin)


def _affiche(p: Path, projet: Path | None = None) -> str:
    try:
        return "~/" + p.relative_to(home()).as_posix()
    except ValueError:
        pass
    if projet is not None:
        try:
            return f"{projet.name}/" + p.relative_to(projet).as_posix()
        except ValueError:
            pass
    return p.as_posix()


def _mapping(rows, emplacement, mapping, type_, entete=False):
    if not isinstance(mapping, dict):
        return
    for k, v in mapping.items():
        e = _etat_valeur(k, v, entete)
        if e:
            l = _ligne(emplacement, k, type_, e)
            l["ref"] = isinstance(v, str) and "${" in v and not ms.a_motif(v)
            rows.append(l)


def _serveurs(rows, emplacement, serveurs, type_):
    if not isinstance(serveurs, dict):
        return
    for nom, srv in serveurs.items():
        if isinstance(srv, dict):
            _mapping(rows, f"{emplacement}:{nom}", srv.get("env"), type_)
            _mapping(rows, f"{emplacement}:{nom}", srv.get("headers"), type_, entete=True)


def _noms_env_fichier(texte: str) -> list[str]:
    return re.findall(r"(?m)^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", texte)


def _noms_ps1(texte: str) -> list[str]:
    noms = re.findall(r"\$env:([A-Za-z_][A-Za-z0-9_]*)\s*=", texte, re.I)
    noms += re.findall(r"(?m)^\s*\$([A-Za-z_][A-Za-z0-9_]*)\s*=", texte)
    return sorted(set(noms))


def sauvegardes() -> list[Path]:
    """Sauvegardes d'un fichier Claude/Snowflake qui contiennent un motif de secret."""
    cl, h = dossier_claude(), home()
    cand: list[Path] = []
    if cl.is_dir():
        cand += [p for p in cl.glob("*.bak*") if p.is_file()]
        cand += [p for p in cl.glob("*.tmp.*") if p.is_file()]
        for d in [cl / "backups"] + sorted(cl.glob("_corbeille*")):
            if d.is_dir():
                cand += [p for p in d.rglob("*") if p.is_file()]
            elif d.is_file():
                cand.append(d)
    for dossier, motif in ((fichier_claude_json().parent, ".claude.json.*"), (h / ".snowflake", "*.bak*")):
        if dossier.is_dir():
            cand += [p for p in dossier.glob(motif) if p.is_file()]
    vus, out = set(), []
    for p in cand:
        if "_a_supprimer" in p.parts or p in vus:
            continue
        vus.add(p)
        if ms.a_motif(_texte(p), large=True):
            out.append(p)
    return sorted(out)


def ps1_skills() -> list[Path]:
    return sorted(p for p in dossier_claude().glob("skills/*/config/secrets*.ps1")
                  if p.is_file() and not p.name.lower().endswith(MODELES_PS1))


def inventaire(projets: list[Path]) -> list[Ligne]:
    rows: list[Ligne] = []
    reg = lire_registre()
    cl, h = dossier_claude(), home()

    # 1. environnement utilisateur
    for n in lire_env_user():
        if ms.nom_secret(n):
            rows.append(_ligne("env utilisateur Windows", n, "env_user", "conforme" if n in reg else "hors_registre"))

    # 2. settings user et projets
    settings = sorted(cl.glob("settings*.json"))
    for pr in projets:
        settings += sorted((pr / ".claude").glob("settings*.json"))
    for f in settings:
        data = _json_derniere(f)
        if not isinstance(data, dict):
            continue
        pr = next((x for x in projets if x in f.parents), None)
        emp = _affiche(f, pr)
        _mapping(rows, emp, data.get("env"), "settings_env")
        if "mcpServers" in data:
            rows.append(_ligne(emp, "mcpServers", "settings_mcp", "config_morte"))

    # 3. ~/.claude.json
    data = _json_derniere(fichier_claude_json())
    if isinstance(data, dict):
        emp = _affiche(fichier_claude_json())
        _serveurs(rows, f"{emp}[global]", data.get("mcpServers"), "claude_json_mcp")
        for chemin, proj in (data.get("projects") or {}).items():
            if isinstance(proj, dict):
                _serveurs(rows, f"{emp}[{Path(chemin).name or chemin}]", proj.get("mcpServers"), "claude_json_mcp")

    # 4. fichiers de projet
    for pr in projets:
        mcp = _json_derniere(pr / ".mcp.json")
        if isinstance(mcp, dict):
            _serveurs(rows, _affiche(pr / ".mcp.json", pr), mcp.get("mcpServers"), "mcp_json")
        envs = [p for p in sorted(pr.glob(".env*")) if p.is_file() and not p.name.endswith(EXEMPLES)]
        for f in envs:
            for n in _noms_env_fichier(_texte(f)):
                if ms.nom_secret(n):
                    rows.append(_ligne(_affiche(f, pr), n, "env_fichier", "conforme"))
        if (pr / ".env").is_file() and not (pr / ".env.example").is_file():
            rows.append(_ligne(_affiche(pr / ".env", pr), ".env.example", "env_fichier", "exemple_manquant"))
        for f in sorted(p for p in pr.glob("secrets*.ps1") if p.is_file() and not p.name.lower().endswith(MODELES_PS1)):
            rows += _lignes_ps1(f, _affiche(f, pr))
    for f in ps1_skills():
        rows += _lignes_ps1(f, _affiche(f))

    # 5. Snowflake : par connexion, des défauts et des NOMS de champs, jamais de valeur
    toml = h / ".snowflake" / "connections.toml"
    if toml.is_file():
        for nom, c in ms.analyser_connexions(_texte(toml)).items():
            for k in c["interdits"]:
                rows.append(_ligne("~/.snowflake/connections.toml", f"{nom}.{k}", "snowflake", "a_deplacer"))
            d = [x for x in ms.defauts_connexion(c) if not x.startswith("champ ")]
            rows.append(_ligne("~/.snowflake/connections.toml", nom, "snowflake",
                               "non_conforme_sso" if d else "conforme"))

    # 6. sauvegardes
    for p in sauvegardes():
        rows.append(_ligne(_affiche(p), p.name, "sauvegarde", "sauvegarde_a_purger", chemin=p))

    # 7. doublons : même nom à deux emplacements (l'env user prime, sinon le premier trouvé)
    par_nom: dict[str, list[Ligne]] = {}
    for r in rows:
        if r["type"] in ("env_user", "settings_env", "claude_json_mcp", "mcp_json", "env_fichier") \
                and ms.nom_secret(r["nom"]):
            par_nom.setdefault(r["nom"], []).append(r)
    for lignes in par_nom.values():
        if len(lignes) < 2:
            continue
        gardee = next((x for x in lignes if x["type"] == "env_user"), lignes[0])
        for r in lignes:
            # une référence ${NOM} est l'usage voulu : jamais un doublon
            if r is gardee or r["type"] == "env_user" or r.get("ref"):
                continue
            if r["etat"] in ("conforme", "a_deplacer") and (r["etat"] == "conforme" or gardee["type"] == "env_user"):
                r["etat"] = "doublon"
    return rows


def _lignes_ps1(f: Path, emp: str) -> list[Ligne]:
    noms = [n for n in _noms_ps1(_texte(f)) if ms.nom_secret(n)] or ["(fichier)"]
    return [_ligne(emp, n, "secrets_ps1", "a_deplacer", chemin=f) for n in noms]


def rendre_table(rows: list[Ligne]) -> list[str]:
    cols = ("emplacement", "nom", "type", "etat")
    tab = [cols] + [tuple(r[c] for c in cols) for r in rows]
    w = [max(len(t[i]) for t in tab) for i in range(4)]
    out = ["  ".join(t[i].ljust(w[i]) for i in range(4)).rstrip() for t in tab]
    cpt: dict[str, int] = {}
    for r in rows:
        cpt[r["etat"]] = cpt.get(r["etat"], 0) + 1
    return out + ["", "Total : " + (", ".join(f"{k} x{v}" for k, v in sorted(cpt.items())) or "rien")]


def cmd_inventaire(args) -> int:
    projets = [Path(args.chemin).resolve()] if args.chemin else [Path.cwd().resolve()]
    rows = inventaire(projets)
    if args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "chemin"} for r in rows], ensure_ascii=False))
    else:
        print("\n".join(rendre_table(rows)))
    return 0


# ------------------------------------------------------------------ verifier
def ecarts_registre() -> tuple[list[str], list[str], list[str]]:
    """(requis manquants, orphelines, reserve non posees)."""
    reg = lire_registre()
    env = set(lire_env_user())
    manques = sorted(n for n, d in reg.items() if d["statut"] == "requis" and n not in env)
    reserve = sorted(n for n, d in reg.items() if d["statut"] == "reserve" and n not in env)
    orphelines = sorted(n for n in env - set(reg) if ms.nom_secret(n))
    return manques, orphelines, reserve


def cmd_verifier(_args) -> int:
    manques, orphelines, reserve = ecarts_registre()
    for n in manques:
        print(f"MANQUE : {n} est au registre (requis) mais absente de l'environnement utilisateur -> "
              f"ecrire {n}=valeur dans a_poser.env")
    for n in orphelines:
        print(f"ORPHELINE : {n} est dans l'environnement utilisateur mais pas au registre -> l'inscrire, ou la supprimer")
    for n in reserve:
        print(f"réserve non posée : {n}")
    interdite = "REQUESTS_CA_BUNDLE" in lire_env_user()
    if interdite:
        print("INTERDITE : REQUESTS_CA_BUNDLE est posée dans l'environnement utilisateur : elle casse snow "
              "(mesuré 2026-10-01) -> la retirer, SSL_CERT_FILE suffit")
    if not manques and not orphelines and not interdite:
        print("registre et environnement utilisateur concordent")
        return 0
    return 1


# ------------------------------------------------------------------ poser / ssl
def cmd_poser_fichier(args) -> int:
    """Pose chaque NOM=valeur du fichier de dépôt. N'imprime que des noms et des numéros de ligne."""
    g = globals()
    statut = "reserve" if getattr(args, "reserve", False) else "requis"

    def ajouter(nom, usage, consommateurs="-"):
        return ajouter_registre(nom, usage, consommateurs, statut)

    ps.BACKEND = types.SimpleNamespace(ecrire_env_user=g["ecrire_env_user"], lire_env_user=g["lire_env_user"],
                                       lire_registre=g["lire_registre"], ajouter_registre=ajouter)
    chemin = Path(args.fichier) if args.fichier else None
    poses, erreurs, echecs, vide = ps.poser_fichier(chemin, vider_apres=not args.sans_vider)
    for n in poses:
        print(f"posé : {n}")
    for i in erreurs:
        print(f"ligne {i} mal formée (NOM=valeur attendu), ignorée")
    for n in echecs:
        print(f"échec : {n} (fichier conservé)")
    print(f"total : {len(poses)} posé(s)" + (" ; fichier vidé" if vide else ""))
    if poses:
        avertir_hors_repo()
        print("Redémarrer VS Code pour que Claude Code les voie.")
    return 1 if echecs else 0


def cmd_poser(args) -> int:
    if args.fichier is not None:
        return cmd_poser_fichier(args)
    if not args.nom:
        print("NOM requis (ou --fichier)")
        return 2
    nom = args.nom
    if not NOM_VALIDE.match(nom):
        print(f"nom invalide : {nom} (lettres, chiffres, _)")
        return 2
    valeur = getpass.getpass(f"Valeur de {nom} (saisie masquée) : ")
    if not valeur:
        print("valeur vide : rien n'est posé")
        return 2
    ecrire_env_user(nom, valeur)
    res = ajouter_registre(nom, args.usage or "", statut="reserve" if args.reserve else "requis")
    avertir_hors_repo()
    print(f"{nom} posée dans l'environnement utilisateur ; registre : {res}. "
          "Redémarrer VS Code pour que Claude Code la voie.")
    return 0


def cmd_ssl(args) -> int:
    if args.sans_requests or args.requests:
        print("REQUESTS_CA_BUNDLE n'est jamais posée : elle casse snow (SSL error, bad handshake), "
              "mesuré 2026-10-01. SSL_CERT_FILE couvre Python.")
        return 2
    if not Path(BUNDLE).is_file():
        print(f"bundle Netskope introuvable : {BUNDLE}")
        return 1
    valeurs = {"NODE_EXTRA_CA_CERTS": BUNDLE, "SSL_CERT_FILE": BUNDLE, "NETSKOPE_BUNDLE": BUNDLE,
               "UV_NATIVE_TLS": "1"}
    for n, v in valeurs.items():
        ecrire_env_user(n, v)
        ajouter_registre(n, "config SSL, non secret", "tous les outils HTTPS")
    avertir_hors_repo()
    try:
        ps.assurer_gabarit()
    except OSError:
        pass
    code, _ = _executer([sys.executable, "-m", "pip", "config", "set", "global.cert", BUNDLE])
    print("posées (config SSL, non secrètes) : " + ", ".join(valeurs))
    print("pip.ini : global.cert posé" if code == 0
          else "pip config set global.cert a échoué : à faire à la main")
    if "REQUESTS_CA_BUNDLE" in lire_env_user():
        print("ATTENTION : REQUESTS_CA_BUNDLE est posée et casse snow : la retirer "
              "([Environment]::SetEnvironmentVariable('REQUESTS_CA_BUNDLE',$null,'User')).")
    print("Redémarrer VS Code (puis tout terminal ouvert). Scripts Python : "
          "requests.get(url, verify=os.environ['NETSKOPE_BUNDLE']).")
    return 0


# ------------------------------------------------------------------ purger
def cmd_purger(args) -> int:
    cand: list[tuple[Path, str, str]] = []
    for p in sauvegardes():
        cand.append((p, "sauvegarde d'un fichier qui porte un secret",
                     "rien : aucune sauvegarde d'un fichier qui porte un secret"))
    for p in ps1_skills():
        cand.append((p, "secrets*.ps1 : secret en fichier",
                     "variable d'environnement utilisateur (/socle:secrets poser NOM)"))
    if not cand:
        print("rien à purger")
        return 0
    jour = dossier_claude() / "_a_supprimer" / datetime.date.today().isoformat() / "secrets"
    for p, _, _ in cand:
        print(("déplace : " if args.oui else "à déplacer : ") + _affiche(p))
    if not args.oui:
        print(f"\n{len(cand)} fichier(s). Rien n'est déplacé ; relancer avec --oui. Destination : {_affiche(jour)}")
        return 0
    lignes = []
    for p, raison, remplace in cand:
        try:
            rel = p.relative_to(home())
        except ValueError:
            rel = Path(p.parent.name) / p.name
        dst = jour / rel
        n = 1
        while dst.exists():
            dst = dst.with_name(f"{dst.name}.{n}")
            n += 1
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dst))
        lignes.append(f"| `{rel.as_posix()}` | {raison} | {remplace} |")
    man = jour / "MANIFESTE.md"
    if not man.exists():
        man.write_text("# Manifeste secrets\n\nRien n'est supprimé : Yann supprime ce dossier lui-même.\n\n"
                       "| Fichier | Raison | Remplacé par |\n|---|---|---|\n", encoding="utf-8")
    with man.open("a", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"\n{len(cand)} fichier(s) déplacé(s) dans {_affiche(jour)} (MANIFESTE.md écrit).")
    return 0


# ------------------------------------------------------------------ snow
def _executer(cmd: list[str]) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
        return r.returncode, (r.stdout or r.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, type(e).__name__


def cache_sso() -> Path:
    """Cache de token SSO du connecteur Snowflake : un FICHIER, pas le Credential Manager."""
    base = os.environ.get("LOCALAPPDATA") or str(home() / "AppData/Local")
    return Path(base) / "Snowflake/Caches/credential_cache_v1.json"


def cmd_snow(_args) -> int:
    pb = []
    snow = shutil.which("snow")
    if not snow:
        pb.append("snow introuvable dans le PATH")
    else:
        norm = snow.replace("\\", "/").lower()
        code, sortie = _executer([snow, "--version"])
        print(f"snow : {snow} ({sortie.splitlines()[0] if sortie else 'sans sortie'})")
        if code != 0:
            pb.append("`snow --version` échoue")
        if "/.local/bin/" not in norm:
            pb.append("snow ne vient pas de ~/.local/bin (uv tool)"
                      + (" : installé dans un Python global" if "/scripts/" in norm and "python" in norm else ""))
    uv = shutil.which("uv")
    if not uv:
        pb.append("uv introuvable")
    else:
        code, dossier = _executer([uv, "tool", "dir"])
        py = None
        if code == 0 and dossier:
            for rel in ("snowflake-cli/Scripts/python.exe", "snowflake-cli/bin/python"):
                if (Path(dossier.splitlines()[0]) / rel).is_file():
                    py = Path(dossier.splitlines()[0]) / rel
        if py is None:
            pb.append("l'outil snowflake-cli n'est pas installé par uv tool")
        else:
            code, _ = _executer([str(py), "-c", "import keyring"])
            print("keyring dans l'environnement de l'outil : " + ("présent" if code == 0 else "ABSENT"))
            if code != 0:
                pb.append("keyring absent : pas de cache SSO")
    cache = cache_sso()
    if cache.is_file():
        date = datetime.datetime.fromtimestamp(cache.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"cache de token SSO : {cache.name} présent, modifié le {date}")
    else:
        pb.append(f"cache de token SSO absent ({cache.name}) : lancer deux fois `snow connection test`, "
                  "le second doit passer sans fenêtre")
    for p in pb:
        print(f"PROBLEME : {p}")
    if pb:
        print(f"Installation isolée (à lancer à la main, rien n'est installé ici) :\n  {INSTALL_SNOW}")
        return 1
    print("snow isolé, keyring présent")
    return 0


# ------------------------------------------------------------------ CLI
def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="secrets", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inventaire")
    i.add_argument("chemin", nargs="?")
    i.add_argument("--json", action="store_true")
    sub.add_parser("verifier")
    p = sub.add_parser("poser")
    p.add_argument("nom", nargs="?")
    p.add_argument("--usage", default="")
    p.add_argument("--fichier", nargs="?", const="", default=None,
                   help="pose les NOM=valeur de a_poser.env (chemin optionnel)")
    p.add_argument("--sans-vider", action="store_true")
    p.add_argument("--reserve", action="store_true", help="inscrit au registre en réserve (défaut : requis)")
    s = sub.add_parser("ssl")
    s.add_argument("--sans-requests", action="store_true", help="refusé : REQUESTS_CA_BUNDLE casse snow")
    s.add_argument("--requests", action="store_true", help=argparse.SUPPRESS)
    g = sub.add_parser("purger")
    g.add_argument("--oui", action="store_true")
    sub.add_parser("snow")
    return ap


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parser().parse_args(argv)
    return {"inventaire": cmd_inventaire, "verifier": cmd_verifier, "poser": cmd_poser, "ssl": cmd_ssl,
            "purger": cmd_purger, "snow": cmd_snow}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
