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


@pytest.mark.parametrize("cmd, attendu", [
    ('python -c "cur.execute(\'DROP TABLE x\')"', 2),
    ("python -c 'cur.execute(\"TRUNCATE TABLE x\")'", 2),
    ('python -c "print(1)"', 0),
    ("snow sql -i <<'EOF'\nDROP ROLE r;\nEOF", 2),
    ("snow sql -i <<EOF\nSELECT 1;\nEOF", 0),
    ("python - <<'EOF'\ncur.execute('DELETE FROM t')\nEOF", 2),
    ('echo "DROP TABLE x" | snow sql -i', 2),
    ('echo "SELECT 1" | snow sql -i', 0),
    ('snow sql -q "DROP USER u"', 2),
    ('snow sql -q "DROP ROLE r"', 2),
    ('snow sql -q "DROP WAREHOUSE w"', 2),
    ('snow sql -q "DROP TASK k"', 2),
    ('snow sql -q "DROP PIPE p"', 2),
    # un message de commit qui CITE snow sql, python et DROP n'est pas une exécution (faux positif réel)
    ("git commit -q -F - <<'EOF'\nfix: stdin de snow sql analyse, DROP USER bloque\nEOF", 0),
    ('git commit -m "snow sql -q DROP TABLE x"', 0),
    ("git commit -F - <<'EOF'\npython -c et DELETE FROM t\nEOF", 0),
    # l'exécutable entre guillemets (venv Windows) reste détecté
    ('"C:/p/venv/Scripts/python.exe" -c "cur.execute(\'DROP TABLE x\')"', 2),
    # limite assumée (docstring) : le garde ne sait pas si l'objet existe, donc ne bloque pas
    ('snow sql -q "CREATE OR REPLACE TABLE t AS SELECT 1"', 0),
    ('snow sql -q "REVOKE SELECT ON TABLE t FROM ROLE r"', 0),
])
def test_sql_guard_python_c_stdin_et_drop_etendus(cmd, attendu):
    assert sql_guard(cmd) == attendu


def test_sql_guard_lit_la_redirection_vers_snow(tmp_path):
    f = tmp_path / "purge.sql"
    f.write_text("DROP USER u;\n", encoding="utf-8")
    assert sql_guard(f'snow sql -i < "{f}"') == 2


def garde_git(cmd):
    p = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode("utf-8")
    return subprocess.run([sys.executable, "-B", str(SCRIPTS / "garde-git-large.py")], input=p, capture_output=True).returncode


@pytest.mark.parametrize("cmd, attendu", [
    ('git commit -m "corrige le flag -a de la CLI"', 0),
    ("git commit -m 'retire git add -A du script'", 0),
    ('git commit -m "$(cat <<\'EOF\'\nfix: option -a et --all\n\nCo-Authored-By: X\nEOF\n)"', 0),
    ('git commit -m "x" -a', 2),
    ('git commit -am "x"', 2),
    ("git commit --all -m x", 2),
    ("git add -A", 2),
    ("git add .", 2),
    ("git add a.py b.py", 0),
    # une option ne déborde pas sur la commande suivante (faux positif réel du 2026-10-03)
    ("git add -- a.py b.py && git diff --cached --numstat -- .", 0),
    ("git add -- a.py; git diff -- .", 0),
    ("git status && git add .", 2),
    ("git add a.py && git commit -am x", 2),
])
def test_garde_git_ignore_le_texte_du_message(cmd, attendu):
    assert garde_git(cmd) == attendu


def lancer_garde_secrets(cmd):
    p = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}}).encode("utf-8")
    return subprocess.run([sys.executable, "-B", str(SCRIPTS / "garde-secrets.py")], input=p, capture_output=True)


def test_garde_secrets_message_selon_la_cause():
    env = lancer_garde_secrets("cat .env")
    assert env.returncode == 2 and ".env.example" in env.stderr.decode("utf-8", "replace")
    dump = lancer_garde_secrets("printenv")
    err = dump.stderr.decode("utf-8", "replace")
    assert dump.returncode == 2 and "dump d'environnement" in err.lower() and ".env.example" not in err
    assert "/socle:secrets inventaire" in err and "/socle:secrets inventaire" in env.stderr.decode("utf-8", "replace")


sys.path.insert(0, str(SCRIPTS))
import garde_socle  # noqa: E402


def ecart(n):
    return garde_socle.Ecart("S-02", f"f{n}", 0, f"regle {n}", "c")


def test_pluriel_et_pointeur_vers_complet():
    assert garde_socle.rendu_complet([ecart(1)])[-1] == "Total : 1 écart"
    assert garde_socle.rendu_complet([ecart(1), ecart(2)])[-1] == "Total : 2 écarts"
    un = garde_socle.rendu_session([ecart(1)])
    assert un[0].startswith("SOCLE : 1 écart (") and not any("--complet" in l for l in un)
    trois = garde_socle.rendu_session([ecart(1), ecart(2), ecart(3)])
    assert trois[0].startswith("SOCLE : 3 écarts (") and "--complet" in trois[-1] and "1 de plus" in trois[-1]


def codes_s01(projet):
    r = subprocess.run([sys.executable, "-B", str(SCRIPTS / "garde_socle.py"), "--json", str(projet)],
                       capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return [e for e in json.loads(r.stdout) if e["code"] == "S-01"]


def test_s01_agents_md_est_la_convention_du_projet(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    assert [e["regle"] for e in codes_s01(tmp_path)] == ["CLAUDE.md absent"]
    (tmp_path / "AGENTS.md").write_text("# Convention du projet\n", encoding="utf-8")
    assert codes_s01(tmp_path) == []
    (tmp_path / "CLAUDE.md").write_text("\n".join(["x"] * 120), encoding="utf-8")
    assert len(codes_s01(tmp_path)) == 1  # un CLAUDE.md présent reste borné à 99 lignes


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
