#!/usr/bin/env python3
"""Moteur d'audit du socle (lecture seule).

Usage : python garde_socle.py [--session | --complet | --json] [chemin]
Un dossier sans .git est ignoré (sortie vide, exit 0). Exit 0 toujours,
sauf --complet qui sort 1 s'il y a des écarts.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import namedtuple

Ecart = namedtuple("Ecart", "code fichier ligne regle correctif")

GRAVITE = ["S-30", "S-31", "S-33", "S-32", "S-34", "S-35", "S-36", "S-37", "S-10", "S-20", "S-40", "S-01", "S-02", "S-03", "S-50", "S-60", "S-70", "S-71", "S-72", "S-73", "S-74"]
EXCLUS = {".venv", "venv", "node_modules", "_a_supprimer", ".git", ".snowflake", "__pycache__"}
PROFIL_OK = "/socle/pw-profile"
STATUTS = ["Todo", "Ready", "Dev", "Recette", "Relecture", "Valide", "Livre", "Rejete"]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motifs_secrets as ms  # noqa: E402

SECRETS = [i for i, _ in ms.LIGNE_RE]
SECRETS_RE = [rx for _, rx in ms.LIGNE_RE]
EXT_S32 = (".py", ".toml", ".yaml", ".yml")
S32_RE = re.compile(r"SNOWFLAKE_PASSWORD|SNOWFLAKE_PRIVATE_KEY\w*|private_key_path|SNOWFLAKE_PAT(?![A-Za-z_])")
EXEMPLES = (".example", ".sample", ".template")
EXT_S36 = (".py", ".ps1", ".md", ".json")
S36_RE = re.compile(r"(?<![A-Za-z0-9])(?:c:[\\/]+|/c/)tmp(?![A-Za-z0-9_])", re.I)
EXCLUS_S36 = {"archives"}


def plugin_root():
    r = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if r:
        return r
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _lire(chemin, defaut=""):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return defaut


_CACHE = {}


def _index_git(racine):
    """Fichiers suivis lus dans .git/index (versions 2 à 4), sans lancer git. None si illisible."""
    import struct
    with open(os.path.join(racine, ".git", "index"), "rb") as f:
        b = f.read()
    if b[:4] != b"DIRC":
        return None
    ver, n = struct.unpack(">II", b[4:12])
    if ver not in (2, 3, 4):
        return None
    pos, prev, out = 12, b"", []
    for _ in range(n):
        flags = struct.unpack(">H", b[pos + 60:pos + 62])[0]
        debut = pos
        pos += 62
        if ver >= 3 and flags & 0x4000:
            pos += 2
        if ver == 4:
            c = b[pos]
            pos += 1
            retire = c & 127
            while c & 128:
                c = b[pos]
                pos += 1
                retire = ((retire + 1) << 7) | (c & 127)
            fin = b.index(b"\0", pos)
            chemin = prev[:len(prev) - retire] + b[pos:fin]
            pos = fin + 1
        else:
            fin = b.index(b"\0", pos)
            chemin = b[pos:fin]
            pos = debut + ((fin + 8 - debut) // 8) * 8
        prev = chemin
        out.append(chemin.decode("utf-8", "replace"))
    return sorted(set(out))


def _fichiers_suivis(racine):
    cle = ("suivis", racine)
    if cle not in _CACHE:
        res = None
        if os.path.isdir(os.path.join(racine, ".git")):
            try:
                res = _index_git(racine)
            except Exception:
                res = None
        if res is None:
            try:
                out = subprocess.run(["git", "ls-files", "-z"], cwd=racine, capture_output=True, timeout=10).stdout
                res = [p for p in out.decode("utf-8", "replace").split("\0") if p]
            except Exception:
                res = []
        _CACHE[cle] = res
    return _CACHE[cle]


def _parcours(racine):
    """Tous les fichiers du projet (suivis ou non), dossiers exclus élagués. Mis en cache."""
    cle = ("parcours", racine)
    if cle not in _CACHE:
        out = []
        for dossier, sous, fichiers in os.walk(racine):
            sous[:] = [d for d in sous if d not in EXCLUS]
            for f in fichiers:
                out.append(os.path.relpath(os.path.join(dossier, f), racine).replace("\\", "/"))
        _CACHE[cle] = out
    return _CACHE[cle]


def _fichiers_py(racine):
    """Tous les .py du projet (suivis ou non), dossiers exclus élagués."""
    return [r for r in _parcours(racine) if r.endswith(".py")]


def _est_env(base):
    return base.startswith(".env") and not base.endswith(EXEMPLES)


def _scan_s32(rel):
    base = os.path.basename(rel)
    return rel.endswith(EXT_S32) or base.startswith(".env")


def _scan_s36(rel):
    return rel.lower().endswith(EXT_S36) and "plugins/socle/" not in rel.replace("\\", "/")


def _scan_extra(rel):
    return _scan_s32(rel) or _scan_s36(rel)


def _cache_fichier(racine):
    import hashlib
    d = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(os.path.expanduser("~"), ".claude", "plugins", "data", "socle")
    return os.path.join(d, "cache", hashlib.sha1(racine.encode("utf-8", "replace")).hexdigest()[:16] + ".json")


def _charger_cache(racine):
    try:
        with open(_cache_fichier(racine), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _sauver_cache(racine, cache):
    try:
        p = _cache_fichier(racine)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except Exception:
        pass


def _exclu(rel):
    return any(p in EXCLUS for p in rel.replace("\\", "/").split("/"))


def s_01(racine):
    """CLAUDE.md absent ou trop long. Un AGENTS.md sans CLAUDE.md est la convention du projet : pas d'écart."""
    p = os.path.join(racine, "CLAUDE.md")
    if not os.path.isfile(p):
        if os.path.isfile(os.path.join(racine, "AGENTS.md")):
            return []
        return [Ecart("S-01", "CLAUDE.md", 0, "CLAUDE.md absent", "créer un CLAUDE.md court (/socle:nouveau-projet)")]
    n = len(_lire(p).splitlines())
    if n >= 100:
        return [Ecart("S-01", "CLAUDE.md", n, f"CLAUDE.md fait {n} lignes (max 99)", "déplacer le détail vers des skills ou rules")]
    return []


def s_02(racine):
    mem = os.path.join(racine, "memory")
    manque = [f for f in ("TODO.md", "LESSONS.md", "DECISIONS.md", "CHANGELOG.md", "MEMORY.md")
              if not os.path.isfile(os.path.join(mem, f))]
    if not manque:
        return []
    for nom in ("CLAUDE.md", "AGENTS.md"):
        t = _lire(os.path.join(racine, nom))
        if "memoire/" in t or "docs/adr/" in t:
            return []
    return [Ecart("S-02", "memory/", 0, "mémoire incomplète, manque " + ", ".join(manque),
                  "créer le quintette memory/ ou déclarer la convention propre dans CLAUDE.md")]


def s_03(racine):
    t = _lire(os.path.join(racine, ".gitignore"))
    lignes = {l.strip().lstrip("/") for l in t.splitlines()}
    out = []
    for motif, variantes in ((".env", {".env", ".env*"}), (".auth/", {".auth/", ".auth"}),
                             ("__pycache__/", {"__pycache__/", "__pycache__", "*.pyc"}),
                             ("_a_supprimer/", {"_a_supprimer/", "_a_supprimer"})):
        if not variantes & lignes:
            out.append(Ecart("S-03", ".gitignore", 0, f".gitignore ne couvre pas {motif}", f"ajouter {motif} au .gitignore"))
    return out


def s_10(racine):
    p = os.path.join(racine, ".mcp.json")
    if not os.path.isfile(p):
        return []
    try:
        data = json.loads(_lire(p))
    except ValueError:
        return [Ecart("S-10", ".mcp.json", 0, ".mcp.json illisible", "corriger le JSON")]
    out = []
    for nom, srv in (data.get("mcpServers") or {}).items():
        if not isinstance(srv, dict):
            continue
        cmd = str(srv.get("command", ""))
        args = [str(a) for a in (srv.get("args") or [])]
        if "npx" in os.path.basename(cmd).lower() and any("@latest" in a for a in args):
            out.append(Ecart("S-10", ".mcp.json", 0, f"serveur {nom} : npx avec @latest", "épingler une version exacte, ou passer en HTTP"))
        if any("@playwright/mcp" in a for a in [cmd] + args):
            out.append(Ecart("S-10", ".mcp.json", 0, f"serveur {nom} : @playwright/mcp", "utiliser preuve_navigateur, pas le MCP"))
    return out


def _analyser(racine, rel, py):
    """Lit un fichier et rend ses constats bruts : {'s30': [[ligne, motif]], 's20': [[ligne, kind]]}."""
    p = os.path.join(racine, rel)
    res = {"s30": [], "s20": [], "s32": [], "s36": []}
    try:
        if os.path.getsize(p) > 2_000_000:
            return res
        with open(p, "rb") as f:
            b = f.read()
    except OSError:
        return res
    if b"\0" in b[:8192]:
        return res
    t = b.decode("utf-8", "replace")
    est_lib = os.path.basename(rel) == "preuve_navigateur.py"
    scan32 = _scan_s32(rel)
    scan36 = _scan_s36(rel)
    if py and not est_lib:
        if re.search(r"(from|import)\s+playwright", t) and "preuve_navigateur" not in t:
            res["s20"].append([0, "pw"])
    for i, l in enumerate(t.splitlines(), 1):
        if len(l) > 5000:
            continue
        for k, rx in enumerate(SECRETS_RE):
            if rx.search(l):
                res["s30"].append([i, SECRETS[k]])
        if scan36 and S36_RE.search(l):
            res["s36"].append([i, "tmp"])
        if scan32 and S32_RE.search(l):
            res["s32"].append([i, S32_RE.search(l).group(0)])
        if py and not est_lib:
            if "storage_state" in l or "connect_over_cdp" in l:
                res["s20"].append([i, "st"])
            m = (re.search(r"launch_persistent_context\(\s*[rf]?[\"']([^\"']+)", l)
                 or re.search(r"user_data_dir\s*=\s*[rf]?[\"']([^\"']+)", l))
            if m and not m.group(1).replace("\\", "/").lower().endswith(PROFIL_OK):
                res["s20"].append([i, "pf"])
    return res


def _constats(racine):
    """Analyse (avec cache par taille et mtime) des fichiers suivis et des .py du projet."""
    if ("constats", racine) in _CACHE:
        return _CACHE[("constats", racine)]
    suivis = _fichiers_suivis(racine)
    tous = {r: False for r in suivis}
    for r in _parcours(racine):
        if r.endswith(".py"):
            tous[r] = True
        elif _scan_extra(r):
            tous.setdefault(r, False)
    for r in suivis:
        if r.endswith(".py") and not _exclu(r):
            tous[r] = True
    cache = _charger_cache(racine)
    neuf, a_faire = {}, []
    for rel, py in tous.items():
        try:
            st = os.stat(os.path.join(racine, rel))
        except OSError:
            continue
        cle = [st.st_size, st.st_mtime_ns, py, ms.VERSION]
        old = cache.get(rel)
        if old and old["k"] == cle:
            neuf[rel] = old
        else:
            a_faire.append((rel, py, cle))
    if a_faire:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(8) as ex:
            for (rel, py, cle), res in zip(a_faire, ex.map(lambda a: _analyser(racine, a[0], a[1]), a_faire)):
                neuf[rel] = dict(res, k=cle)
        _sauver_cache(racine, neuf)
    elif len(neuf) != len(cache):
        _sauver_cache(racine, neuf)
    _CACHE[("constats", racine)] = neuf
    return neuf


LIBELLES_S20 = {
    "pw": ("playwright sans preuve_navigateur", "importer preuve_navigateur"),
    "st": ("storage_state/connect_over_cdp interdit", "le SSO vit dans le profil partagé, setup_sso() de preuve_navigateur"),
    "pf": ("profil persistant hors %LOCALAPPDATA%/socle/pw-profile", "utiliser le profil partagé via preuve_navigateur"),
}


PLUGIN_AUTO_EXCLUS = re.compile(r"^plugins/[^/]+/(hooks/scripts|tests)/|^(plugins/[^/]+/)?skills/[^/]+/references/")


def _auto_exclu(racine, rel):
    """Dans un repo de plugin (.claude-plugin/marketplace.json), S-20/S-30/S-32 ignorent scripts, tests et références."""
    return os.path.isfile(os.path.join(racine, ".claude-plugin", "marketplace.json")) \
        and bool(PLUGIN_AUTO_EXCLUS.match(rel.replace("\\", "/")))


def s_20(racine):
    out = []
    for rel, c in _constats(racine).items():
        if _exclu(rel) or _auto_exclu(racine, rel):
            continue
        for ligne, kind in c["s20"]:
            out.append(Ecart("S-20", rel, ligne, *LIBELLES_S20[kind]))
    return out


def _ignore_git(racine, rel):
    """Vrai si git ignore ce chemin (git check-ignore), faux si doute."""
    try:
        r = subprocess.run(["git", "check-ignore", "-q", "--", rel], cwd=racine, capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False


def s_30(racine):
    suivis = set(_fichiers_suivis(racine))
    out = []
    for rel in sorted(suivis):
        if _est_env(os.path.basename(rel)):
            out.append(Ecart("S-30", rel, 0, ".env suivi par git", "git rm --cached et l'ajouter au .gitignore"))
    for rel in sorted(_parcours(racine)):
        base = os.path.basename(rel)
        if base.lower().startswith("secrets") and base.lower().endswith(".ps1")                 and (rel in suivis or not _ignore_git(racine, rel)):
            out.append(Ecart("S-30", rel, 0, f"{base} non ignoré par git", "l'ajouter au .gitignore (secrets*.ps1), puis /socle:secrets"))
    if os.path.isfile(os.path.join(racine, ".env")) and not os.path.isfile(os.path.join(racine, ".env.example")):
        out.append(Ecart("S-30", ".env", 0, ".env présent sans .env.example", "créer .env.example (noms seuls, versionné)"))
    for rel, c in _constats(racine).items():
        if rel in suivis and not _auto_exclu(racine, rel):
            for ligne, motif in c["s30"]:
                out.append(Ecart("S-30", rel, ligne, f"secret probable (motif {motif})", "retirer la valeur, la révoquer, la mettre dans .env"))
    return out


def _json_fichier(chemin):
    try:
        return json.loads(_lire(chemin))
    except ValueError:
        return None


def s_31(racine):
    """Valeur secrète en clair dans la clé env d'un .claude/settings*.json du projet."""
    d = os.path.join(racine, ".claude")
    out = []
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if not (f.startswith("settings") and f.endswith(".json")):
            continue
        data = _json_fichier(os.path.join(d, f))
        env = data.get("env") if isinstance(data, dict) else None
        for k, v in (env or {}).items():
            if ms.valeur_en_clair(k, v):
                out.append(Ecart("S-31", f".claude/{f}", 0, f"env {k} en clair",
                                 "Yann écrit NOM=valeur dans %LOCALAPPDATA%\\socle\\a_poser.env, puis référencer en ${NOM}"))
    return out


def s_32(racine):
    """Auth Snowflake hors connections.toml (mot de passe, clé privée, PAT)."""
    out = []
    for rel, c in sorted(_constats(racine).items()):
        if _exclu(rel) or _auto_exclu(racine, rel):
            continue
        for ligne, nom in c.get("s32", []):
            out.append(Ecart("S-32", rel, ligne, f"{nom} : Snowflake = SSO connections.toml seul",
                             "ne garder qu'un connection_name, authenticator externalbrowser"))
    return out


def s_33(racine):
    """Valeur en clair dans les env/headers de .mcp.json, et snowflake-labs-mcp sans keyring."""
    p = os.path.join(racine, ".mcp.json")
    if not os.path.isfile(p):
        return []
    data = _json_fichier(p)
    if not isinstance(data, dict):
        return []
    out = []
    for nom, srv in (data.get("mcpServers") or {}).items():
        if not isinstance(srv, dict):
            continue
        for k, v in (srv.get("env") or {}).items():
            if not ms.REFERENCE.match(str(v)):
                out.append(Ecart("S-33", ".mcp.json", 0, f"serveur {nom} : env {k} en clair",
                                 "écrire ${VAR} ; Yann écrit VAR=valeur dans %LOCALAPPDATA%\\socle\\a_poser.env"))
        for k, v in (srv.get("headers") or {}).items():
            if "${" not in str(v):
                out.append(Ecart("S-33", ".mcp.json", 0, f"serveur {nom} : header {k} en clair",
                                 "écrire ${VAR} ; Yann écrit VAR=valeur dans %LOCALAPPDATA%\\socle\\a_poser.env"))
        args = [str(a) for a in (srv.get("args") or [])]
        if os.path.basename(str(srv.get("command", ""))).lower().split(".")[0] == "uvx"                 and any("snowflake-labs-mcp" in a for a in args)                 and not any("snowflake-connector-python[secure-local-storage]" in a for a in args):
            out.append(Ecart("S-33", ".mcp.json", 0, f"serveur {nom} : snowflake-labs-mcp sans keyring (pas de cache SSO)",
                             'args : ["--with", "snowflake-connector-python[secure-local-storage]", "snowflake-labs-mcp", ...]'))
    return out


def s_34(racine):
    """Niveau user : chaque connexion de ~/.snowflake/connections.toml est SSO avec cache de token."""
    p = os.path.join(os.path.expanduser("~"), ".snowflake", "connections.toml")
    if not os.path.isfile(p):
        return []
    out = []
    for nom, c in ms.analyser_connexions(_lire(p)).items():
        d = ms.defauts_connexion(c)
        if d:
            out.append(Ecart("S-34", "~/.snowflake/connections.toml", 0, f"connexion {nom} non conforme ({'; '.join(d)})",
                             "authenticator = externalbrowser et client_store_temporary_credential = true, rien d'autre (a faire a la main : le socle ne l'ecrit jamais)"))
    return out


def s_35(racine):
    """Niveau user : snow s'installe isolé (uv tool, ~/.local/bin), jamais dans Python*/Scripts."""
    out = []
    vus = set()
    for d in os.environ.get("PATH", "").split(os.pathsep):
        norm = d.replace("\\", "/").rstrip("/").lower()
        for exe in ("snow.exe", "snow"):
            p = os.path.join(d, exe)
            if d and os.path.isfile(p) and p not in vus:
                vus.add(p)
                if re.search(r"/python[^/]*/scripts$", norm):
                    out.append(Ecart("S-35", d, 0, "snow installé dans le Python global (Python*/Scripts)",
                                     'uv tool install snowflake-cli --native-tls --with "snowflake-connector-python[secure-local-storage]", puis retirer le lanceur résiduel'))
    return out[:1]


def s_37(racine):
    """Niveau user : a_poser.env ne doit porter aucune ligne NOM=valeur (ni posée, ni à poser)."""
    import poser_secrets
    chemin = poser_secrets.chemin_depot()
    paires, _ = poser_secrets.lire_paires(chemin)
    if not paires:
        return []
    connus = poser_secrets.env_user_noms()
    if connus is None:
        return []
    out = []
    for nom, _v in paires:
        if nom not in connus:
            out.append(Ecart("S-37", str(chemin), 0, f"{nom} déposée dans a_poser.env mais pas posée",
                             "lancer secrets.py poser --fichier"))
        else:
            out.append(Ecart("S-37", str(chemin), 0, f"{nom} posée mais a_poser.env non vidé",
                             "fichier non vidé : secrets.py poser --fichier, puis tourner le secret s'il a fuité"))
    return out[:2]


def s_36(racine):
    """C:/tmp interdit : projet, %LOCALAPPDATA%/socle ou scratchpad."""
    out = []
    for rel, c in sorted(_constats(racine).items()):
        parts = set(rel.replace("\\", "/").split("/"))
        if _exclu(rel) or parts & EXCLUS_S36:
            continue
        for ligne, _ in c.get("s36", [])[:3]:
            out.append(Ecart("S-36", rel, ligne, "référence à C:/tmp (interdit)",
                             "%LOCALAPPDATA%\\socle (état machine) ou le scratchpad de session"))
    return out


def s_40(racine):
    out = []
    pr = plugin_root()
    for sous, plug, suffixe in ((".claude/agents", "agents", ".md"), (".claude/hooks", "hooks/scripts", ".py")):
        d = os.path.join(racine, sous)
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(suffixe) and os.path.isfile(os.path.join(pr, plug, f)):
                    out.append(Ecart("S-40", f"{sous}/{f}", 0, "doublon d'un élément du plugin socle", "supprimer la copie du projet"))
    d = os.path.join(racine, ".claude", "skills")
    if os.path.isdir(d):
        for f in os.listdir(d):
            if os.path.isfile(os.path.join(d, f, "SKILL.md")) and os.path.isdir(os.path.join(pr, "skills", f)):
                out.append(Ecart("S-40", f".claude/skills/{f}/SKILL.md", 0, "doublon d'un skill du plugin socle", "supprimer la copie du projet"))
    if '"mcpServers"' in _lire(os.path.join(racine, ".claude", "settings.json")):
        out.append(Ecart("S-40", ".claude/settings.json", 0, "mcpServers dans settings.json : clé ignorée", "déplacer vers .mcp.json"))
    return out


def s_50(racine):
    b = os.path.join(racine, "backlog")
    if not os.path.isdir(b):
        return [Ecart("S-50", "backlog/", 0, "backlog/ absent", "créer le backlog (config.yml, tasks/, board.md)")]
    out = []
    cfg = _lire(os.path.join(b, "config.yml"))
    if not cfg:
        out.append(Ecart("S-50", "backlog/config.yml", 0, "config.yml absent", "créer config.yml avec les 8 statuts"))
    else:
        manque = [s for s in STATUTS if s not in cfg]
        if manque:
            out.append(Ecart("S-50", "backlog/config.yml", 0, "statuts manquants : " + ", ".join(manque), "ajouter les statuts au config.yml"))
    board = os.path.join(b, "board.md")
    td = os.path.join(b, "tasks")
    tm = [os.path.getmtime(os.path.join(td, f)) for f in os.listdir(td) if f.endswith(".md")] if os.path.isdir(td) else []
    if not tm:
        return out  # aucune tâche : pas de board à exiger (projet neuf)
    if not os.path.isfile(board):
        out.append(Ecart("S-50", "backlog/board.md", 0, "board.md absent", "backlog board export"))
    elif os.path.getmtime(board) < max(tm):
        out.append(Ecart("S-50", "backlog/board.md", 0, "board.md plus ancien que les tâches", "backlog board export"))
    return out


def s_60(racine):
    return [Ecart("S-60", f"outils/{f}", 0, f"outils/{f} absent", f"créer outils/{f} (commande conventionnelle)")
            for f in ("portes.py", "smoke.py", "deployer.py") if not os.path.isfile(os.path.join(racine, "outils", f))]


def venv_non_relocalise(racine):
    """Ancien chemin lu dans .venv/Scripts/activate.bat si VIRTUAL_ENV n'est pas <racine>/.venv, sinon None.

    Lecture seule d'un petit fichier ; jamais d'exception (None en cas de doute).
    """
    try:
        t = _lire(os.path.join(racine, ".venv", "Scripts", "activate.bat"))
        m = re.search(r'(?im)^\s*set\s+"?VIRTUAL_ENV=([^"\r\n]+)', t)
        if not m:
            return None

        def norm(p):
            return os.path.normcase(os.path.realpath(p.strip()))
        ancien = m.group(1).strip()
        return None if norm(ancien) == norm(os.path.join(racine, ".venv")) else ancien
    except Exception:
        return None


def s_70(racine):
    """Venv non relocalisé : un .venv copié ou déplacé garde l'ancien chemin dans ses lanceurs."""
    ancien = venv_non_relocalise(racine)
    if not ancien:
        return []
    return [Ecart("S-70", ".venv", 0, f"venv non relocalisé (VIRTUAL_ENV={ancien})",
                  "/socle:nouveau-projet venv --oui : recréer, jamais copier ni déplacer")]


def s_71(racine):
    """Du Python exécutable sans dépendances déclarées (requirements*.txt ou pyproject.toml à la racine)."""
    if any(f.startswith("requirements") and f.endswith(".txt") for f in os.listdir(racine)) \
            or os.path.isfile(os.path.join(racine, "pyproject.toml")):
        return []
    py = [r for r in _fichiers_py(racine) if not r.startswith("outils/")]
    if not py:
        return []
    return [Ecart("S-71", py[0], 0, f"{len(py)} fichier(s) .py sans requirements*.txt ni pyproject.toml",
                  "pip freeze > requirements-dev.txt (à relire, dépendances directes épinglées)")]


def _octets_lf(chemin):
    """Contenu d'un fichier, fins de ligne normalisées en LF. None si illisible."""
    try:
        with open(chemin, "rb") as f:
            return f.read().replace(b"\r\n", b"\n")
    except OSError:
        return None


def _registre_regles():
    """Registre de session_start : nom de règle -> sha256 (LF) de la dernière copie faite par le plugin."""
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(os.path.expanduser("~"), ".claude", "plugins", "data", "socle")
    try:
        data = json.loads(_lire(os.path.join(base, "regles_copiees.json"), "{}"))
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}


def s_72(racine):
    """Niveau user : chaque règle livrée par le plugin (rules/machine/) existe à l'identique dans ~/.claude/rules/.
    Différente et jamais touchée depuis la copie : en attente de mise à jour. Sinon : modifiée localement."""
    home = os.path.expanduser("~")
    src = os.path.join(plugin_root(), "rules", "machine")
    if not os.path.isdir(src):
        return []
    registre = _registre_regles()
    out = []
    for nom in sorted(os.listdir(src)):
        ref = _octets_lf(os.path.join(src, nom)) if nom.endswith(".md") else None
        if ref is None:
            continue
        cible = os.path.join(home, ".claude", "rules", nom)
        actuel = _octets_lf(cible)
        if actuel == ref:
            continue
        if actuel is None:
            etat, correctif = "absente de la source plugin", "redémarrer la session (session_start copie la règle absente)"
        elif registre.get(nom) == hashlib.sha256(actuel).hexdigest():
            etat, correctif = "en attente de mise à jour", "rien à faire : la version du plugin sera recopiée au prochain démarrage"
        else:
            etat, correctif = "modifiée localement", "reporter dans plugins/socle/rules/machine ou supprimer la copie (la version du plugin sera recopiée au démarrage)"
        out.append(Ecart("S-72", f"~/.claude/rules/{nom}", 0, f"règle {nom} {etat}", correctif))
    return out


def _git_dirs(racine):
    """(gitdir, commondir) : suit `.git` fichier (worktree) puis `commondir`."""
    git = os.path.join(racine, ".git")
    if os.path.isfile(git):
        ligne = _lire(git).strip()
        if ligne.startswith("gitdir:"):
            git = os.path.normpath(os.path.join(racine, ligne[7:].strip()))
    commun = _lire(os.path.join(git, "commondir")).strip()
    if commun:
        commun = os.path.normpath(os.path.join(git, commun))
    return git, commun or git


def _plus_recent_mtime(chemin):
    """mtime du fichier, ou le plus récent des fichiers d'un dossier ; None si rien."""
    if os.path.isfile(chemin):
        return os.path.getmtime(chemin)
    best = None
    for d, _, fichiers in os.walk(chemin):
        for n in fichiers:
            try:
                t = os.path.getmtime(os.path.join(d, n))
            except OSError:
                continue
            best = t if best is None or t > best else best
    return best


def s_74(racine):
    """Clone sans fetch récent : repère = le plus récent de FETCH_HEAD, packed-refs, refs/remotes/ (worktree : via
    commondir), dans un repo avec remote. Aucun repère : « aucun fetch enregistré ». Aucun réseau."""
    git, commun = _git_dirs(racine)
    if "[remote " not in _lire(os.path.join(commun, "config")):
        return []
    reperes = []
    for base, nom in ((git, "FETCH_HEAD"), (commun, "FETCH_HEAD"), (commun, "packed-refs"), (commun, os.path.join("refs", "remotes"))):
        t = _plus_recent_mtime(os.path.join(base, nom))
        if t is not None:
            reperes.append(t)
    age = int((time.time() - max(reperes)) // 86400) if reperes else None
    if age is not None and age <= 7:
        return []
    quand = "aucun fetch enregistré" if age is None else f"dernier fetch il y a {age} j"
    return [Ecart("S-74", ".git/FETCH_HEAD", 0, quand,
                  "git fetch, puis vérifier l'avance de la branche distante avant de travailler")]


def s_73(racine):
    """BOM UTF-8 en tête d'un JSON lu par Node (settings du projet, .mcp.json, settings user) : l'extension échoue."""
    home = os.path.expanduser("~")
    cibles = [(os.path.join(racine, ".claude", "settings.json"), ".claude/settings.json"),
              (os.path.join(racine, ".claude", "settings.local.json"), ".claude/settings.local.json"),
              (os.path.join(racine, ".mcp.json"), ".mcp.json"),
              (os.path.join(home, ".claude", "settings.json"), "~/.claude/settings.json")]
    out, vus = [], set()
    for chemin, nom in cibles:
        reel = os.path.normcase(os.path.realpath(chemin))
        if reel in vus:
            continue
        vus.add(reel)
        try:
            with open(chemin, "rb") as f:
                bom = f.read(3) == b"\xef\xbb\xbf"
        except OSError:
            continue
        if bom:
            out.append(Ecart("S-73", nom, 0, f"{nom} commence par un BOM UTF-8 (Node : « not valid JSON »)",
                             "réécrire sans BOM (Python ou Edit, jamais Out-File/Set-Content de PowerShell 5.1)"))
    return out


CONTROLES = [s_01, s_02, s_03, s_10, s_20, s_30, s_31, s_32, s_33, s_34, s_35, s_36, s_37, s_40, s_50, s_60,
             s_70, s_71, s_72, s_73, s_74]
COMPLETS_SEULEMENT = (s_70, s_71)  # hors --session : S-70 est déjà signalé par session_start, S-71 est trop bavard


def _rang(code):
    return GRAVITE.index(code) if code in GRAVITE else 99


def auditer(racine, complet=True):
    if not os.path.isdir(os.path.join(racine, ".git")):
        return []
    out = []
    for fn in CONTROLES:
        if not complet and fn in COMPLETS_SEULEMENT:
            continue
        try:
            out.extend(fn(racine))
        except Exception as e:  # un contrôle cassé ne casse pas les autres
            out.append(Ecart(fn.__name__.replace("s_", "S-"), "", 0, f"contrôle en erreur : {type(e).__name__}", "corriger garde_socle.py"))
    out.sort(key=lambda e: _rang(e.code))
    return out


def _loc(e):
    return f"{e.fichier}:{e.ligne}" if e.ligne else e.fichier


def rendu_session(ecarts):
    if not ecarts:
        return []
    cpt = {}
    for e in ecarts:
        cpt[e.code] = cpt.get(e.code, 0) + 1
    resume = ", ".join(f"{c} x{cpt[c]}" for c in sorted(cpt, key=_rang))
    lignes = [f"SOCLE : {_nb_ecarts(len(ecarts))} ({resume}) -> /socle:nouveau-projet remise-au-pas"]
    lignes += [f"  {e.code} {_loc(e)} : {e.regle}" for e in ecarts[:2]]
    if len(ecarts) > 2:
        lignes.append(f"  ... {len(ecarts) - 2} de plus : python \"{os.path.abspath(__file__)}\" --complet")
    return lignes


def _nb_ecarts(n):
    """« 1 écart », « 3 écarts » (accord au pluriel dès 2)."""
    return f"{n} écart" + ("s" if n > 1 else "")


def rendu_complet(ecarts):
    if not ecarts:
        return ["SOCLE : 0 écart"]
    rows = [("code", "fichier:ligne", "règle", "correctif")] + [(e.code, _loc(e), e.regle, e.correctif) for e in ecarts]
    w = [max(len(r[i]) for r in rows) for i in range(3)]
    lignes = ["  ".join(r[i].ljust(w[i]) for i in range(3)) + "  " + r[3] for r in rows]
    return lignes + ["", f"Total : {_nb_ecarts(len(ecarts))}"]


def main(argv):
    """Rend (lignes, code de sortie)."""
    mode = "session"
    chemin = None
    for a in argv:
        if a in ("--session", "--complet", "--json"):
            mode = a[2:]
        elif not a.startswith("--"):
            chemin = a
    racine = os.path.abspath(chemin or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    ecarts = auditer(racine, complet=(mode != "session"))
    if mode == "json":
        lignes = [json.dumps([e._asdict() for e in ecarts], ensure_ascii=False)]
    elif mode == "complet":
        lignes = rendu_complet(ecarts) if os.path.isdir(os.path.join(racine, ".git")) else []
    else:
        lignes = rendu_session(ecarts)
    return lignes, (1 if (mode == "complet" and ecarts) else 0)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        lignes, code = main(sys.argv[1:])
        if lignes:
            print("\n".join(lignes))
        sys.exit(code)
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
