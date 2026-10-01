"""Motifs de secrets partagés (garde_socle, garde_outils, secrets.py).

Aucune fonction ne rend la valeur d'un secret : elles rendent des booléens ou des identifiants
de motif. Les tests fabriquent leurs fausses valeurs à l'exécution.
"""
import os
import re

# Jetons à préfixe reconnaissable : sûrs dans n'importe quel fichier.
FORTS = [
    ("glpat", r"glpat-[A-Za-z0-9_.-]{15,}"),
    ("ghp", r"ghp_[A-Za-z0-9]{20,}"),
    ("sbp", r"sbp_[0-9a-f]{20,}"),
    ("atatt", r"ATATT3[A-Za-z0-9_=-]{20,}"),
    ("jwt", r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("sk_ant", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("akia", r"AKIA[0-9A-Z]{16}"),
    ("apikey", r"apikey_[A-Za-z0-9_]{20,}"),
]
# Forme générique NOM = valeur (large : réservée aux fichiers qui ne portent jamais de secret).
AFFECTATION = ("affectation",
               r"(?<![A-Za-z])(?:TOKEN|SECRET|PASSWORD|MOT_DE_PASSE|API_KEY|PAT)[\"']?\s*[:=]\s*[\"']?[^\"'\s$]{12,}")
# Héritage de S-30 : affectation entre guillemets seulement (peu de faux positifs dans du code).
HERITAGE = [
    ("supabase_env", r"SUPABASE_ACCESS_TOKEN=\S+"),
    ("quote", r"(?:PASSWORD|MOT_DE_PASSE|TOKEN|SECRET)\s*=\s*['\"][^'\"$]{8,}"),
]

FORTS_RE = [(i, re.compile(p)) for i, p in FORTS]
LIGNE_RE = FORTS_RE + [(i, re.compile(p)) for i, p in HERITAGE]
LARGE_RE = FORTS_RE + [(AFFECTATION[0], re.compile(AFFECTATION[1]))]

NOM_SECRET = re.compile(
    r"(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_KEY|ACCESS_KEY)|(^|_)PAT(_|$)")
REFERENCE = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_]*(:-[^}]*)?\}$")
VERSION = "m3"  # à changer quand les motifs changent : invalide les caches d'audit


def nom_secret(nom):
    """Vrai si le NOM de variable désigne un secret (PATH n'en est pas un)."""
    return bool(NOM_SECRET.search(str(nom).upper()))


def trouver(texte, large=False):
    """Identifiants des motifs présents dans texte (jamais les valeurs)."""
    liste = LARGE_RE if large else FORTS_RE
    return [i for i, rx in liste if rx.search(texte)]


def a_motif(texte, large=False):
    return bool(trouver(texte, large))


def valeur_en_clair(nom, valeur):
    """Vrai si (nom, valeur) est un secret écrit en clair : motif, ou nom secret avec valeur non ${...}."""
    if not isinstance(valeur, str) or not valeur.strip():
        return False
    if "${" in valeur and not a_motif(valeur):
        return False
    if a_motif(valeur):
        return True
    return nom_secret(nom) and not banal(valeur) and not valeur.lstrip().startswith("${")


def banal(valeur):
    """Jamais un secret : vide, nombre, booléen, ${VAR}, ou chemin d'un fichier/dossier existant."""
    v = str(valeur).strip()
    if not v or v.startswith("${"):
        return True
    if re.fullmatch(r"[0-9.]+|true|false|none|null", v, re.I):
        return True
    try:
        return len(v) < 260 and "\n" not in v and os.path.exists(v)
    except (OSError, ValueError):
        return False


def est_reference(valeur):
    return bool(REFERENCE.match(str(valeur)))


# ---- connexions Snowflake : lecture par lignes, seules les CLÉS (et authenticator) sont retenues
INTERDITES = ("password", "private_key", "token")


def analyser_connexions(texte):
    """{connexion: {'authenticator': str|None, 'cache': bool|None, 'interdits': [clés]}}.

    Scanner de lignes : ne retient jamais la valeur d'un champ, sauf authenticator
    et client_store_temporary_credential, qui ne sont pas des secrets.
    """
    out, cour = {}, None
    for brut in texte.splitlines():
        l = brut.strip()
        if not l or l.startswith("#"):
            continue
        m = re.match(r"^\[\s*(?:connections\.)?([^\]\s.]+)\s*\]$", l)
        if m:
            cour = m.group(1).strip("\"'")
            out.setdefault(cour, {"authenticator": None, "cache": None, "interdits": []})
            continue
        if cour is None:
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*=\s*(.*)$", l)
        if not m:
            continue
        cle, val = m.group(1).lower(), m.group(2).strip()
        c = out[cour]
        if cle == "authenticator":
            c["authenticator"] = val.strip("\"'").lower()
        elif cle == "client_store_temporary_credential":
            c["cache"] = val.lower().startswith("true")
        elif any(cle.startswith(p) for p in INTERDITES):
            c["interdits"].append(cle)
    return out


def defauts_connexion(c):
    """Liste des défauts d'une connexion (clés seulement)."""
    d = []
    if c["authenticator"] != "externalbrowser":
        d.append("authenticator != externalbrowser")
    if c["cache"] is not True:
        d.append("client_store_temporary_credential != true")
    d += [f"champ {k} present" for k in c["interdits"]]
    return d
