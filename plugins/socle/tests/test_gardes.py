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
CHAINSNOW = Path(r"C:\Users\yann.ponaire\OneDrive - Infopro Digital\Documents\CLAUDE_CODE_PROJECTS\chainsnow_max_reglementaire")

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
