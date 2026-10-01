"""Tests de skills/nouveau-projet/scripts/socle_projet.py (plugin simulé en tmp)."""
import datetime
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/nouveau-projet/scripts/socle_projet.py"
spec = importlib.util.spec_from_file_location("socle_projet", SCRIPT)
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

GARDE_FAUX = """import json, sys
from pathlib import Path
f = Path(__file__).with_name("ecarts.json")
ecarts = json.loads(f.read_text()) if f.exists() else []
if "--json" in sys.argv:
    print(json.dumps(ecarts))
"""

DOUBLON = {"code": "S-40", "fichier": ".claude/agents/executant.md", "ligne": 0,
           "regle": "doublon d'un élément du plugin socle", "correctif": "x"}


@pytest.fixture
def plugin(tmp_path, monkeypatch):
    racine = tmp_path / "plugin"
    g = racine / "gabarits"
    gabarits = {"CLAUDE.md": "# gabarit\n", "gitignore": ".env\n_a_supprimer/\n",
                "backlog/config.yml": "x: 1\n", "outils/portes.py": "#p\n",
                "outils/smoke.py": "#s\n", "outils/deployer.py": "#d\n",
                "memory/TODO.md": "# TODO\n", "memory/LESSONS.md": "# L\n"}
    for rel, txt in gabarits.items():
        (g / rel).parent.mkdir(parents=True, exist_ok=True)
        (g / rel).write_text(txt, encoding="utf-8")
    (racine / "hooks/scripts").mkdir(parents=True)
    (racine / "hooks/scripts/garde_socle.py").write_text(GARDE_FAUX, encoding="utf-8")
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(racine))
    monkeypatch.setattr(sp.shutil, "which", lambda _n: None)  # pas de backlog réel
    return racine


def projet_avec_agent(tmp_path, plugin, ecarts):
    projet = tmp_path / "p"
    (projet / ".claude/agents").mkdir(parents=True)
    (projet / ".claude/agents/executant.md").write_text("a", encoding="utf-8")
    (plugin / "hooks/scripts/ecarts.json").write_text(json.dumps(ecarts), encoding="utf-8")
    return projet


def compte(racine: Path) -> int:
    return sum(1 for p in racine.rglob("*") if p.is_file() and ".git" not in p.parts)


def test_init_cree_et_n_ecrase_pas(plugin, tmp_path):
    projet = tmp_path / "p"
    projet.mkdir()
    (projet / "CLAUDE.md").write_text("MIEN\n", encoding="utf-8")
    assert sp.main(["init", str(projet), "--sans-commit"]) == 0
    assert (projet / "CLAUDE.md").read_text(encoding="utf-8") == "MIEN\n"
    for rel in (".gitignore", "memory/TODO.md", "memory/LESSONS.md", "outils/portes.py",
                "outils/smoke.py", "outils/deployer.py", "backlog/config.yml",
                "backlog/tasks/.gitkeep", "outils/preuve_navigateur.py"):
        assert (projet / rel).exists(), rel
    assert (projet / ".git").exists()
    shim = (projet / "outils/preuve_navigateur.py").read_text(encoding="utf-8")
    assert "plugins/data/socle/lib" in shim and len(shim.strip().splitlines()) == 3
    assert not (projet / ".claude").exists()


def test_remise_sans_oui_ne_modifie_rien(plugin, tmp_path):
    ecarts = [DOUBLON, {"code": "S-01", "fichier": "CLAUDE.md", "ligne": 0,
                        "regle": "absent", "correctif": "y"}]
    projet = projet_avec_agent(tmp_path, plugin, ecarts)
    avant = compte(projet)
    sp.main(["remise-au-pas", str(projet), "--radical"])
    assert compte(projet) == avant
    assert not (projet / "_a_supprimer").exists()
    assert not (projet / "CLAUDE.md").exists()


def test_radical_oui_deplace_et_ne_supprime_rien(plugin, tmp_path):
    projet = projet_avec_agent(tmp_path, plugin, [DOUBLON])
    avant = compte(projet)
    sp.main(["remise-au-pas", str(projet), "--radical", "--oui"])
    jour = projet / "_a_supprimer" / datetime.date.today().isoformat()
    assert (jour / ".claude/agents/executant.md").read_text(encoding="utf-8") == "a"
    assert not (projet / ".claude/agents/executant.md").exists()
    manifeste = (jour / "MANIFESTE.md").read_text(encoding="utf-8")
    assert ".claude/agents/executant.md" in manifeste and "socle:executant" in manifeste
    assert compte(projet) == avant + 1  # seul le manifeste s'ajoute, rien ne disparait


def test_sans_radical_s40_reste_manuel(plugin, tmp_path):
    projet = projet_avec_agent(tmp_path, plugin, [DOUBLON])
    sp.main(["remise-au-pas", str(projet), "--oui"])
    assert (projet / ".claude/agents/executant.md").exists()


def test_completer_s01_oui(plugin, tmp_path):
    projet = projet_avec_agent(tmp_path, plugin, [
        {"code": "S-01", "fichier": "CLAUDE.md", "ligne": 0, "regle": "absent", "correctif": "y"}])
    sp.main(["remise-au-pas", str(projet), "--oui"])
    assert (projet / "CLAUDE.md").read_text(encoding="utf-8") == "# gabarit\n"


def test_deplacer_cli(plugin, tmp_path):
    projet = tmp_path / "p"
    projet.mkdir()
    (projet / "a.txt").write_text("1", encoding="utf-8")
    sp.main(["deplacer", "a.txt", "--raison", "test", "--racine", str(projet)])
    jour = projet / "_a_supprimer" / datetime.date.today().isoformat()
    assert (jour / "a.txt").exists() and (jour / "MANIFESTE.md").exists()
    assert not (projet / "a.txt").exists()


def test_init_sur_le_vrai_plugin_rend_zero_ecart(tmp_path, monkeypatch):
    """Intégration : gabarits réels + garde_socle réel, sans fixture."""
    import subprocess
    reel = Path(__file__).resolve().parents[1]
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(reel))
    monkeypatch.setattr(sp.shutil, "which", lambda _n: None)
    projet = tmp_path / "reel"
    assert sp.main(["init", str(projet), "--sans-commit"]) == 0
    r = subprocess.run([sys.executable, str(reel / "hooks/scripts/garde_socle.py"), "--complet", str(projet)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, r.stdout
