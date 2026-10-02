"""Tests des gardes S-72 (règles machine), sync_regles et S-73 (BOM) : jamais le vrai ~/.claude, home toujours fabriqué."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "hooks" / "scripts"
BOM = b"\xef\xbb\xbf"


@pytest.fixture
def garde(monkeypatch, tmp_path):
    """Module garde_socle, avec un faux home (USERPROFILE et HOME) et un projet vide."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    import garde_socle
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("HOME", str(home))
    proj = tmp_path / "proj"
    proj.mkdir()
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path / "plugin"))
    garde_socle.home, garde_socle.proj = home, proj
    garde_socle.plugin = tmp_path / "plugin"
    return garde_socle


def poser_repo(plugin, **regles):
    """Source livrée par le plugin : <plugin>/rules/machine/."""
    d = Path(plugin) / "rules" / "machine"
    d.mkdir(parents=True, exist_ok=True)
    for nom, contenu in regles.items():
        (d / f"{nom}.md").write_bytes(contenu)


def poser_machine(home, **regles):
    d = home / ".claude" / "rules"
    d.mkdir(parents=True, exist_ok=True)
    for nom, contenu in regles.items():
        (d / f"{nom}.md").write_bytes(contenu)


def test_s72_identique_meme_avec_fins_de_ligne_differentes(garde):
    poser_repo(garde.plugin, conception=b"# A\nligne\n", contradicteur=b"# B\nx\n")
    poser_machine(garde.home, conception=b"# A\r\nligne\r\n", contradicteur=b"# B\nx\n")
    assert garde.s_72(str(garde.proj)) == []


def test_s72_derive(garde):
    poser_repo(garde.plugin, conception=b"# A\nnouvelle version\n")
    poser_machine(garde.home, conception=b"# A\nancienne version\n")
    e = garde.s_72(str(garde.proj))
    assert [x.code for x in e] == ["S-72"]
    assert "conception.md dérive" in e[0].regle and e[0].fichier.endswith("conception.md")


def test_s72_absente(garde):
    poser_repo(garde.plugin, conception=b"# A\n")
    poser_machine(garde.home, autre=b"en plus, non signale\n")
    e = garde.s_72(str(garde.proj))
    assert [x.code for x in e] == ["S-72"] and "conception.md absente" in e[0].regle


def test_s72_repo_absent(garde):
    poser_machine(garde.home, conception=b"# A\n")
    assert garde.s_72(str(garde.proj)) == []


def test_s72_ignore_les_fichiers_non_md(garde):
    poser_repo(garde.plugin)
    (garde.plugin / "rules" / "machine" / "notes.txt").write_text("x")
    assert garde.s_72(str(garde.proj)) == []


def ecrire(chemin, contenu):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_bytes(contenu)


def test_s73_bom_projet_et_user(garde):
    ecrire(garde.proj / ".claude" / "settings.json", BOM + b"{}")
    ecrire(garde.proj / ".claude" / "settings.local.json", BOM + b"{}")
    ecrire(garde.proj / ".mcp.json", BOM + b'{"mcpServers": {}}')
    ecrire(garde.home / ".claude" / "settings.json", BOM + b"{}")
    e = garde.s_73(str(garde.proj))
    assert sorted(x.fichier for x in e) == sorted(
        [".claude/settings.json", ".claude/settings.local.json", ".mcp.json", "~/.claude/settings.json"])
    assert {x.code for x in e} == {"S-73"}


def test_s73_sans_bom(garde):
    ecrire(garde.proj / ".claude" / "settings.json", b"{}")
    ecrire(garde.proj / ".mcp.json", b'{"mcpServers": {}}')
    ecrire(garde.home / ".claude" / "settings.json", b"{}")
    assert garde.s_73(str(garde.proj)) == []


def test_s73_fichiers_absents(garde):
    assert garde.s_73(str(garde.proj)) == []


def test_s72_s73_branches_dans_l_audit(tmp_path):
    """Bout en bout : le script, lancé sur un projet git, sort S-72 et S-73 (et en --session aussi)."""
    home = tmp_path / "h"
    proj = tmp_path / "p"
    proj.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=proj, check=True)
    poser_repo(tmp_path / "plugin", conception=b"# A\n")
    ecrire(proj / ".mcp.json", BOM + b'{"mcpServers": {}}')
    env = dict(os.environ, USERPROFILE=str(home), HOME=str(home), PYTHONDONTWRITEBYTECODE="1",
               CLAUDE_PLUGIN_ROOT=str(tmp_path / "plugin"))
    for mode in ("--json", "--session"):
        r = subprocess.run([sys.executable, "-B", str(SCRIPTS / "garde_socle.py"), mode, str(proj)],
                           capture_output=True, text=True, encoding="utf-8", env=env)
        assert "S-72" in r.stdout and "S-73" in r.stdout
    codes = [e["code"] for e in json.loads(subprocess.run(
        [sys.executable, "-B", str(SCRIPTS / "garde_socle.py"), "--json", str(proj)],
        capture_output=True, text=True, encoding="utf-8", env=env).stdout)]
    assert codes.index("S-72") < codes.index("S-73")


@pytest.fixture
def session(monkeypatch, tmp_path):
    """Module session_start, plugin factice et faux home."""
    monkeypatch.syspath_prepend(str(SCRIPTS))
    import session_start
    home = tmp_path / "home"
    home.mkdir()
    for v in ("USERPROFILE", "HOME"):
        monkeypatch.setenv(v, str(home))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path / "plugin"))
    session_start.home = home
    session_start.plugin = tmp_path / "plugin"
    return session_start


def test_sync_regles_absent_copie(session):
    poser_repo(session.plugin, conception=b"# A\r\nx\r\n", contradicteur=b"# B\n")
    out = session.sync_regles()
    assert len(out) == 1 and "conception.md" in out[0] and "contradicteur.md" in out[0]
    assert (session.home / ".claude" / "rules" / "conception.md").read_bytes() == b"# A\nx\n"


def test_sync_regles_different_recopie(session):
    poser_repo(session.plugin, conception=b"# A\nnouvelle\n")
    poser_machine(session.home, conception=b"# A\nancienne\n")
    assert session.sync_regles()
    assert (session.home / ".claude" / "rules" / "conception.md").read_bytes() == b"# A\nnouvelle\n"


def test_sync_regles_identique_rien(session):
    poser_repo(session.plugin, conception=b"# A\nx\n")
    poser_machine(session.home, conception=b"# A\r\nx\r\n")
    assert session.sync_regles() == []
    assert (session.home / ".claude" / "rules" / "conception.md").read_bytes() == b"# A\r\nx\r\n"


def test_sync_regles_fichier_en_plus_conserve(session):
    poser_repo(session.plugin, conception=b"# A\n")
    poser_machine(session.home, perso=b"a moi\n")
    session.sync_regles()
    assert (session.home / ".claude" / "rules" / "perso.md").read_bytes() == b"a moi\n"


def test_sync_regles_source_absente(session):
    assert session.sync_regles() == []
