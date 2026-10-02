"""Hooks : sql-guard limité au SQL réel, bannière selon adoption, auto-exclusion du plugin."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN / "hooks" / "scripts"


def sql_guard(cmd):
    p = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode("utf-8")
    return subprocess.run(["node", str(SCRIPTS / "sql-guard.js")], input=p, capture_output=True).returncode


@pytest.mark.parametrize("cmd, attendu", [
    ('git commit -m "doc: explain DROP TABLE guard"', 0),
    ('grep -rn "DROP TABLE" sql/', 0),
    ('snow sql -q "DROP TABLE x"', 2),
    ('snow sql -q "DELETE FROM t WHERE 1=1"', 0),
    ('snow sql -q "DELETE FROM t"', 2),
    ('snow sql -q "UPDATE a SET x=1 WHERE id=1; DELETE FROM b"', 2),
])
def test_sql_guard_ne_juge_que_le_sql_reel(cmd, attendu):
    assert sql_guard(cmd) == attendu


def test_sql_guard_lit_le_fichier_sql(tmp_path):
    f = tmp_path / "purge.sql"
    f.write_text("TRUNCATE TABLE t;\n", encoding="utf-8")
    assert sql_guard(f'snow sql -f "{f}"') == 2
    f.write_text("SELECT 1;\n", encoding="utf-8")
    assert sql_guard(f'snow sql -f "{f}"') == 0


def test_sql_guard_message_sans_faux_contournement():
    p = json.dumps({"tool_name": "Bash", "tool_input": {"command": 'snow sql -q "DROP TABLE x"'}}).encode()
    r = subprocess.run(["node", str(SCRIPTS / "sql-guard.js")], input=p, capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    assert "relance" not in err.lower()
    assert "Yann" in err


def banniere(projet, tmp_path):
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), CLAUDE_PROJECT_DIR=str(projet),
               CLAUDE_PLUGIN_DATA=str(tmp_path / "data"), USERPROFILE=str(tmp_path / "home"),
               HOME=str(tmp_path / "home"), PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPTS / "session_start.py")], input=b"{}", capture_output=True, env=env)
    return r.stdout.decode("utf-8", "replace")


def test_banniere_projet_non_adopte(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    out = banniere(proj, tmp_path)
    assert "projet non adopté" in out
    assert "Les 6 règles" not in out
    assert "${CLAUDE_PLUGIN_ROOT}" not in out


def test_banniere_projet_adopte_substitue_la_racine(tmp_path):
    proj = tmp_path / "proj"
    (proj / "backlog").mkdir(parents=True)
    out = banniere(proj, tmp_path)
    assert "Les 6 règles" in out
    assert "${CLAUDE_PLUGIN_ROOT}" not in out
    assert "rules/methode.md" in out


def test_auto_exclusion_sur_le_repo_du_plugin():
    sys.path.insert(0, str(SCRIPTS))
    import garde_socle
    repo = PLUGIN.parents[1]
    if not (repo / ".claude-plugin" / "marketplace.json").exists():
        pytest.skip("pas un repo de plugin")
    codes = {e.code for fn in (garde_socle.s_20, garde_socle.s_30, garde_socle.s_32) for e in fn(str(repo))}
    assert not codes & {"S-20", "S-30", "S-32"}, codes
