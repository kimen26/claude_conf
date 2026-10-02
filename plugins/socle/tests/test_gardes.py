"""Tests des gardes du plugin socle. Lancer : python -m pytest plugins/socle/tests"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN / "hooks" / "scripts"
# Projet de référence : variable SOCLE_PROJET_REF, sinon ~/CLAUDE_CODE_PROJECTS/chainsnow_max_reglementaire ; absent = test sauté.
CHAINSNOW = Path(os.environ.get("SOCLE_PROJET_REF") or Path.home() / "CLAUDE_CODE_PROJECTS" / "chainsnow_max_reglementaire")

# Valeurs fabriquées à l'exécution : le fichier de test ne porte aucun secret en clair.
SBP = "sbp_" + "0123456789abcdef01234567"


@pytest.fixture(scope="session", autouse=True)
def donnees_isolees(tmp_path_factory):
    """Cache d'audit isolé : les tests ne touchent jamais ~/.claude/plugins/data."""
    d = tmp_path_factory.mktemp("plugin_data")
    os.environ["CLAUDE_PLUGIN_DATA"] = str(d)
    yield d
    os.environ.pop("CLAUDE_PLUGIN_DATA", None)


def lancer(script, stdin=None, args=(), env=None, cwd=None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    e.update(env or {})
    return subprocess.run([sys.executable, "-B", str(SCRIPTS / script), *args], input=stdin,
                          capture_output=True, text=True, encoding="utf-8", env=e, cwd=cwd)


def garde(outil, **ti):
    return lancer("garde_outils.py", stdin=json.dumps({"tool_name": outil, "tool_input": ti}))


REFUSES = [
    ("Bash", {"command": "claude mcp add -s user x -- npx y"}),
    ("Write", {"file_path": "outils/x.py", "content": "ctx = browser.new_context(storage_state='a.json')"}),
    ("Edit", {"file_path": "README.md", "old_string": "a", "new_string": "cle " + SBP}),
    ("Bash", {"command": "npx @playwright/mcp"}),
]
ACCEPTES = [
    ("Bash", {"command": "pip install playwright"}),
    ("Write", {"file_path": "lib/preuve_navigateur.py", "content": "p.chromium.launch_persistent_context(d)"}),
    ("Edit", {"file_path": ".env", "old_string": "a", "new_string": "SUPABASE_ACCESS_TOKEN=" + SBP}),
    ("Bash", {"command": "git status"}),
]


@pytest.mark.parametrize("outil,ti", REFUSES)
def test_garde_outils_refuse(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 2
    assert r.stderr.strip()
    assert SBP not in r.stderr and "0123456789abcdef" not in r.stderr


@pytest.mark.parametrize("outil,ti", ACCEPTES)
def test_garde_outils_accepte(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 0
    assert r.stderr == ""


def test_garde_outils_robuste():
    assert lancer("garde_outils.py", stdin="pas du json").returncode == 0
    assert lancer("garde_outils.py", stdin="{}").returncode == 0
    assert garde("Write", content="x").returncode == 0


def test_garde_outils_multiedit_et_settings():
    r = garde("MultiEdit", file_path="a.py", edits=[{"old_string": "a", "new_string": "ok"},
                                                    {"old_string": "b", "new_string": "x = connect_over_cdp(u)"}])
    assert r.returncode == 2
    r = garde("Write", file_path="/home/y/.claude/settings.json", content='{"mcpServers": {"a": {"command": "npx"}}}')
    assert r.returncode == 2


def git_init(p):
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    return p


def codes(p):
    r = lancer("garde_socle.py", args=("--json", str(p)))
    assert r.returncode == 0
    return {e["code"] for e in json.loads(r.stdout)}, r.stdout


def test_garde_socle_detecte(tmp_path):
    git_init(tmp_path)
    (tmp_path / ".mcp.json").write_text(json.dumps({"mcpServers": {"s": {
        "command": "npx", "args": ["-y", "truc@latest"], "env": {"CLE": "en-clair-12345"}}}}))
    (tmp_path / "nav.py").write_text("from playwright.sync_api import sync_playwright\n")
    (tmp_path / "conf.txt").write_text("cle = " + SBP + "\n")
    subprocess.run(["git", "add", "conf.txt", "nav.py"], cwd=tmp_path, check=True)
    trouves, sortie = codes(tmp_path)
    assert {"S-10", "S-20", "S-30", "S-60"} <= trouves
    assert SBP not in sortie  # la valeur n'est jamais imprimée


def test_garde_socle_sans_git_ignore(tmp_path):
    r = lancer("garde_socle.py", args=("--session", str(tmp_path)))
    assert r.returncode == 0 and r.stdout == ""


def test_garde_socle_conforme(tmp_path):
    git_init(tmp_path)
    (tmp_path / "CLAUDE.md").write_text("# Projet\n")
    mem = tmp_path / "memory"
    mem.mkdir()
    for f in ("TODO", "LESSONS", "DECISIONS", "CHANGELOG", "MEMORY"):
        (mem / f"{f}.md").write_text("x\n")
    (tmp_path / ".gitignore").write_text(".env\n.auth/\n__pycache__/\n_a_supprimer/\n")
    bl = tmp_path / "backlog"
    (bl / "tasks").mkdir(parents=True)
    (bl / "tasks" / "t1.md").write_text("t\n")
    (bl / "config.yml").write_text("statuses: [Todo, Ready, Dev, Recette, Relecture, Valide, Livre, Rejete]\n", encoding="utf-8")
    time.sleep(0.05)
    (bl / "board.md").write_text("b\n")
    out = tmp_path / "outils"
    out.mkdir()
    for f in ("portes", "smoke", "deployer"):
        (out / f"{f}.py").write_text("")
    r = lancer("garde_socle.py", args=("--session", str(tmp_path)))
    assert r.returncode == 0 and r.stdout == ""
    assert lancer("garde_socle.py", args=("--complet", str(tmp_path))).returncode == 0


def test_garde_socle_complet_sort_1(tmp_path):
    git_init(tmp_path)
    r = lancer("garde_socle.py", args=("--complet", str(tmp_path)))
    assert r.returncode == 1 and "Total" in r.stdout


@pytest.mark.skipif(not CHAINSNOW.is_dir(), reason="projet de référence absent")
def test_garde_socle_session_rapide():
    """Mesure l'audit lui-même (cache chaud), hors démarrage de l'interpréteur et premier import."""
    sys.path.insert(0, str(SCRIPTS))
    import garde_socle
    garde_socle.main(["--session", str(CHAINSNOW)])  # premier passage : remplit le cache
    mesures = []
    for _ in range(5):
        garde_socle._CACHE.clear()
        t = time.perf_counter()
        _, code = garde_socle.main(["--session", str(CHAINSNOW)])
        mesures.append(time.perf_counter() - t)
        assert code == 0
    t = time.perf_counter()
    lancer("garde_socle.py", args=("--session", str(CHAINSNOW)))
    mur = time.perf_counter() - t
    print(f"--session : {min(mesures) * 1000:.0f} ms (audit, meilleur de 5) ; {mur * 1000:.0f} ms en processus complet")
    assert min(mesures) <= 0.3


def test_session_start(tmp_path):
    data = tmp_path / "data"
    proj = git_init(tmp_path / "proj") if (tmp_path / "proj").mkdir() is None else None
    env = {"CLAUDE_PLUGIN_ROOT": str(PLUGIN), "CLAUDE_PLUGIN_DATA": str(data), "CLAUDE_PROJECT_DIR": str(proj)}
    lib = PLUGIN / "lib"
    cree = not (lib / "README.md").exists()
    if cree:
        (lib / "README.md").write_text("Test de synchronisation.\n")
    try:
        (data / "lib").mkdir(parents=True)
        (data / "lib" / "orphelin.txt").write_text("a supprimer\n")
        (proj / "backlog").mkdir()  # projet adopté : le DIGEST complet est injecté
        r = lancer("session_start.py", env=env)
        assert r.returncode == 0
        assert (data / "lib" / "README.md").read_text() == (lib / "README.md").read_text()
        assert not (data / "lib" / "orphelin.txt").exists()
        assert "synchronisée" in r.stdout
        assert "Socle actif" in r.stdout  # DIGEST
        # deuxième passage : plus rien à copier
        assert "synchronisée" not in lancer("session_start.py", env=env).stdout
    finally:
        if cree:
            (lib / "README.md").unlink()


# ---------------------------------------------------------------- pilier secrets et emplacements
BS = chr(92)
GLPAT = "glpat-" + "FAUX0000000000000000"
MSG_SECRET = "/socle:secrets poser NOM"


@pytest.mark.parametrize("outil,ti", [
    ("Edit", {"file_path": "/home/y/.claude/settings.json", "old_string": "a", "new_string": '"FAUX_TOKEN": "' + GLPAT + '"'}),
    ("Write", {"file_path": "/home/y/.claude.json", "content": '{"k": "' + GLPAT + '"}'}),
    ("Write", {"file_path": "/home/y/.claude/settings.json.bak", "content": "GITLAB_PAT = " + "z" * 14}),
    ("Write", {"file_path": "/home/y/.claude/backups/x.backup", "content": GLPAT}),
    ("Write", {"file_path": "/home/y/.claude/skills/c/config/secrets.ps1", "content": '$env:X_TOKEN = "' + GLPAT + '"'}),
])
def test_garde_outils_secret_dans_fichier_claude(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 2
    assert MSG_SECRET in r.stderr and "${NOM}" in r.stderr
    assert GLPAT not in r.stderr and "FAUX0000" not in r.stderr


@pytest.mark.parametrize("cmd", [
    "Copy-Item settings.json settings.json.bak",
    "cp ~/.claude/settings.json ~/.claude/settings.json.bak",
    "copy .claude.json .claude.json.bak",
    "Copy-Item -Path ~/.claude/settings.json -Destination ~/.claude/settings.json.bak",
])
def test_garde_outils_refuse_sauvegarde_de_settings(cmd):
    r = garde("Bash", command=cmd)
    assert r.returncode == 2 and "pas de sauvegarde" in r.stderr and "/socle:secrets purger" in r.stderr


@pytest.mark.parametrize("outil,ti", [
    ("Edit", {"file_path": ".env", "old_string": "a", "new_string": "GITLAB_PAT=" + GLPAT}),
    ("Edit", {"file_path": "/home/y/.claude/settings.json", "old_string": "a",
              "new_string": '"env": {"GITLAB_PAT": "${GITLAB_PAT}"}'}),
    ("Bash", {"command": "cp ~/.claude/settings.json.bak ~/.claude/settings.json"}),
    ("Bash", {"command": "cp a.txt b.txt.bak"}),
])
def test_garde_outils_accepte_secrets(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 0 and r.stderr == ""


REFUSES_TMP = [
    ("Write", {"file_path": "C:/tmp/claude/x.py", "content": "x"}),
    ("Edit", {"file_path": "C:" + BS + "tmp" + BS + "x.txt", "old_string": "a", "new_string": "b"}),
    ("Write", {"file_path": "/c/tmp/x.txt", "content": "x"}),
    ("Bash", {"command": "mkdir -p C:/tmp/claude/x"}),
    ("Bash", {"command": "python -m venv C:/tmp/claude/venv-a"}),
    ("Bash", {"command": "uv venv /c/tmp/claude/v"}),
    ("Bash", {"command": "echo a > C:/tmp/claude/x.txt"}),
    ("Bash", {"command": "cp a.txt C:/tmp/"}),
    ("Bash", {"command": "Copy-Item a.txt C:" + BS + "tmp" + BS + "b.txt"}),
    ("Bash", {"command": "New-Item -ItemType Directory C:" + BS + "tmp" + BS + "claude"}),
]
ACCEPTES_TMP = [
    ("Bash", {"command": "ls C:/tmp/claude"}),
    ("Bash", {"command": "cat C:/tmp/claude/x.txt"}),
    ("Bash", {"command": "cp C:/tmp/claude/a.txt ./a.txt"}),
    ("Write", {"file_path": "/home/y/socle/tests/x.py", "content": "p = 'C:/tmp/x'"}),
    ("Write", {"file_path": "/home/y/proj/recette/a.txt", "content": "x"}),
]


@pytest.mark.parametrize("outil,ti", REFUSES_TMP)
def test_garde_outils_refuse_tmp(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 2
    assert "interdit" in r.stderr and "scratchpad" in r.stderr and "LOCALAPPDATA" in r.stderr


@pytest.mark.parametrize("outil,ti", ACCEPTES_TMP)
def test_garde_outils_accepte_tmp_en_lecture(outil, ti):
    r = garde(outil, **ti)
    assert r.returncode == 0 and r.stderr == ""


def projet_secrets(p):
    git_init(p)
    (p / ".claude").mkdir()
    (p / ".claude" / "settings.json").write_text(json.dumps({"env": {"FAUX_TOKEN": GLPAT, "OK": "x", "REF_TOKEN": "${REF_TOKEN}"}}))
    (p / ".env").write_text("SNOWFLAKE_PASSWORD=" + "x" * 4 + "\nA=1\n")
    (p / "secrets.ps1").write_text("$env:X = 1\n")
    (p / "app.py").write_text('cfg = {"private_key_path": "k.p8"}\n')
    (p / ".mcp.json").write_text(json.dumps({"mcpServers": {
        "a": {"command": "npx", "args": ["x@latest"], "env": {"CLE": "en-clair-12345", "OK": "${OK}"},
              "headers": {"Authorization": "Bearer " + "z" * 20, "X": "Bearer ${T}"}},
        "sf": {"command": "uvx", "args": ["snowflake-labs-mcp", "--service-config-file", "c.yaml"]},
        "sf2": {"command": "uvx", "args": ["--with", "snowflake-connector-python[secure-local-storage]",
                                           "snowflake-labs-mcp"]}}}))
    subprocess.run(["git", "add", ".env"], cwd=p, check=True)
    return p


def test_garde_socle_s30_a_s33(tmp_path):
    projet_secrets(tmp_path)
    r = lancer("garde_socle.py", args=("--json", str(tmp_path)))
    ecarts = json.loads(r.stdout)
    codes_ = [e["code"] for e in ecarts]
    assert GLPAT not in r.stdout and "xxxx" not in r.stdout
    regles = {(e["code"], e["regle"]) for e in ecarts}
    assert ("S-30", ".env suivi par git") in regles
    assert ("S-30", "secrets.ps1 non ignoré par git") in regles
    assert ("S-30", ".env présent sans .env.example") in regles
    assert ("S-31", "env FAUX_TOKEN en clair") in regles
    assert not any(e["code"] == "S-31" and "REF_TOKEN" in e["regle"] for e in ecarts)
    assert any(e["code"] == "S-32" and e["fichier"] == ".env" for e in ecarts)
    assert any(e["code"] == "S-32" and e["fichier"] == "app.py" for e in ecarts)
    s33 = [e["regle"] for e in ecarts if e["code"] == "S-33"]
    assert "serveur a : env CLE en clair" in s33 and "serveur a : header Authorization en clair" in s33
    assert not any("OK" in r_ or "header X" in r_ for r_ in s33)
    assert any("serveur sf :" in r_ and "keyring" in r_ for r_ in s33) and not any("serveur sf2" in r_ for r_ in s33)
    # ordre de gravité : S-30, S-31, S-33, S-32, ..., S-10
    ordre = [c for c in dict.fromkeys(codes_)]
    assert ordre.index("S-30") < ordre.index("S-31") < ordre.index("S-33") < ordre.index("S-32") < ordre.index("S-10")


def test_garde_socle_secrets_conformes(tmp_path):
    git_init(tmp_path)
    (tmp_path / ".gitignore").write_text(".env\nsecrets*.ps1\n")
    (tmp_path / ".env").write_text("A_TOKEN=\n")
    (tmp_path / ".env.example").write_text("A_TOKEN=\n")
    (tmp_path / "secrets.ps1").write_text("$env:X = 1\n")
    (tmp_path / ".mcp.json").write_text(json.dumps({"mcpServers": {"a": {"url": "https://x", "headers": {"Authorization": "Bearer ${T}"}}}}))
    trouves, _ = codes(tmp_path)
    assert not trouves & {"S-30", "S-31", "S-32", "S-33"}


def faux_home(p, toml=None, snow=None):
    h = p / "fauxhome"
    (h / ".snowflake").mkdir(parents=True)
    if toml is not None:
        (h / ".snowflake" / "connections.toml").write_text(toml, encoding="utf-8")
    return h


TOML = ('[connections.sso]\nauthenticator = "externalbrowser"\nclient_store_temporary_credential = true\n'
        '[connections.nocache]\nauthenticator = "externalbrowser"\n'
        '[connections.pwd]\nauthenticator = "externalbrowser"\nclient_store_temporary_credential = true\n'
        'password = "' + "mdp" + 'Factice987"\n')


def test_garde_socle_s34(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    git_init(proj)
    h = faux_home(tmp_path, TOML)
    r = lancer("garde_socle.py", args=("--json", str(proj)), env={"USERPROFILE": str(h), "HOME": str(h)})
    s34 = [e for e in json.loads(r.stdout) if e["code"] == "S-34"]
    assert len(s34) == 2
    regles = " ".join(e["regle"] for e in s34)
    assert "nocache" in regles and "client_store_temporary_credential" in regles
    assert "pwd" in regles and "champ password present" in regles
    assert "connexion sso" not in regles
    assert "Factice987" not in r.stdout


def test_garde_socle_s34_conforme_ou_absent(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    git_init(proj)
    h = faux_home(tmp_path, TOML.split("[connections.nocache]")[0])
    env = {"USERPROFILE": str(h), "HOME": str(h)}
    assert not [e for e in json.loads(lancer("garde_socle.py", args=("--json", str(proj)), env=env).stdout)
                if e["code"] == "S-34"]
    h2 = tmp_path / "vide"
    h2.mkdir()
    env = {"USERPROFILE": str(h2), "HOME": str(h2)}
    assert not [e for e in json.loads(lancer("garde_socle.py", args=("--json", str(proj)), env=env).stdout)
                if e["code"] == "S-34"]


def test_garde_socle_s35(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    git_init(proj)
    mauvais = tmp_path / "Python312" / "Scripts"
    bon = tmp_path / "fauxhome" / ".local" / "bin"
    for d in (mauvais, bon):
        d.mkdir(parents=True)
        (d / "snow.exe").write_text("")
    r = lancer("garde_socle.py", args=("--json", str(proj)), env={"PATH": str(mauvais)})
    assert [e["code"] for e in json.loads(r.stdout) if e["code"] == "S-35"] == ["S-35"]
    r = lancer("garde_socle.py", args=("--json", str(proj)), env={"PATH": str(bon)})
    assert not [e for e in json.loads(r.stdout) if e["code"] == "S-35"]


def test_garde_socle_s36(tmp_path):
    git_init(tmp_path)
    (tmp_path / "a.py").write_text("P = 'C:/tmp/claude/pw'\n")
    (tmp_path / "b.md").write_text("voir C:" + BS + "tmp" + BS + "x et /c/tmp/y\n")
    (tmp_path / "c.json").write_text('{"p": "C:/tmpfoo"}')
    (tmp_path / "archives").mkdir()
    (tmp_path / "archives" / "vieux.md").write_text("C:/tmp/old\n")
    (tmp_path / "memory" / "handoffs" / "archives").mkdir(parents=True)
    (tmp_path / "memory" / "handoffs" / "archives" / "h.md").write_text("C:/tmp/old\n")
    r = lancer("garde_socle.py", args=("--json", str(tmp_path)))
    fichiers = sorted(e["fichier"] for e in json.loads(r.stdout) if e["code"] == "S-36")
    assert fichiers == ["a.py", "b.md"]
    assert "LOCALAPPDATA" in r.stdout


def test_session_start_ssl_onedrive_venv(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    import session_start as ss
    monkeypatch.setenv("NODE_EXTRA_CA_CERTS", "")
    monkeypatch.setenv("SSL_CERT_FILE", "")
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "x")
    msgs = ss.controle_ssl()
    assert any("variables SSL absentes" in m and "/socle:secrets ssl" in m and "redémarrer VS Code" in m for m in msgs)
    assert any("REQUESTS_CA_BUNDLE posée" in m and "casse snow" in m for m in msgs)
    bundle = tmp_path / "b.crt"
    bundle.write_text("x")
    monkeypatch.setenv("NODE_EXTRA_CA_CERTS", str(bundle))
    monkeypatch.setenv("SSL_CERT_FILE", str(bundle))
    monkeypatch.delenv("REQUESTS_CA_BUNDLE")
    assert ss.controle_ssl() == []
    # emplacements
    monkeypatch.setattr(ss, "TMP_CLAUDE", str(tmp_path / "tmpclaude"))
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "OneDrive - X" / "proj"))
    out = ss.controle_emplacements()
    assert len(out) == 1 and "Projet sous OneDrive" in out[0] and "git est la sauvegarde" in out[0]
    (tmp_path / "tmpclaude" / "venv-a").mkdir(parents=True)
    out = ss.controle_emplacements()
    assert len(out) == 2 and "venv hors projet détecté" in out[1] and "remise-au-pas" in out[1]
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "proj"))
    assert len(ss.controle_emplacements()) == 1


def _faux_venv(projet, virtual_env):
    sc = projet / ".venv" / "Scripts"
    sc.mkdir(parents=True)
    (sc / "activate.bat").write_text(f'@echo off\r\nset "VIRTUAL_ENV={virtual_env}"\r\n', encoding="utf-8")


def test_session_start_venv_non_relocalise(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(SCRIPTS))
    import session_start as ss
    monkeypatch.setattr(ss, "TMP_CLAUDE", str(tmp_path / "absent"))
    proj = tmp_path / "proj"
    _faux_venv(proj, r"C:\Autre\Chemin\.venv")
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(proj))
    out = ss.controle_emplacements()
    assert len(out) == 1 and "non relocalisé" in out[0] and "nouveau-projet venv" in out[0]
    ok = tmp_path / "ok"
    _faux_venv(ok, str(ok / ".venv").upper())  # casse différente : normcase
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(ok))
    assert ss.controle_emplacements() == []


def test_garde_socle_s70_s71_complet_seulement(tmp_path):
    git_init(tmp_path)
    _faux_venv(tmp_path, r"C:\Autre\.venv")
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    c, _ = codes(tmp_path)
    assert {"S-70", "S-71"} <= c
    r = lancer("garde_socle.py", args=("--session", str(tmp_path)))
    assert "S-70" not in r.stdout and "S-71" not in r.stdout
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    assert "S-71" not in codes(tmp_path)[0]


def test_porte_dependances_gabarit_avertit_sans_bloquer(tmp_path):
    outils = tmp_path / "outils"
    outils.mkdir()
    gab = PLUGIN / "gabarits" / "outils" / "portes.py"
    (outils / "portes.py").write_text(gab.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "app.py").write_text("x = 1\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(outils / "portes.py")], capture_output=True, text=True,
                       encoding="utf-8")
    assert r.returncode == 0 and "[AVERT] dependances" in r.stdout
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(outils / "portes.py")], capture_output=True, text=True,
                       encoding="utf-8")
    assert r.returncode == 0 and "AVERT" not in r.stdout
