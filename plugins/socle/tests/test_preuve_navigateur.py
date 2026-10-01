"""Tests de lib/preuve_navigateur.py : unitaires sans navigateur + intégration si Playwright."""
import importlib.util
import os
import sys
from pathlib import Path

import pytest

LIB = Path(__file__).resolve().parents[1] / "lib"
sys.path.insert(0, str(LIB))
import preuve_navigateur as pn  # noqa: E402

PLAYWRIGHT = importlib.util.find_spec("playwright") is not None

HTML = ("<!doctype html><html><head><meta charset='utf-8'><title>t</title></head>"
        "<body><h1 id='titre'>Recette</h1><p>" + "Du texte de test. " * 200 + "</p></body></html>")


@pytest.fixture
def profil(tmp_path, monkeypatch):
    p = tmp_path / "profil"
    p.mkdir()
    monkeypatch.setattr(pn, "PROFIL", p)
    return p


def test_constantes():
    assert pn.VIEWPORTS == {"mobile": (390, 844), "desktop": (1440, 900), "large": (1850, 820)}
    assert pn.PROFIL.as_posix() == "C:/tmp/claude/pw-profile"


def test_verrou_libre(profil):
    assert pn.verrou_profil() is None


def test_verrou_singleton(profil):
    try:
        (profil / "SingletonLock").symlink_to("hote-4242")
    except (OSError, NotImplementedError):
        (profil / "SingletonLock").write_text("hote-4242")
    msg = pn.verrou_profil()
    assert msg and "déjà utilisé" in msg
    if (profil / "SingletonLock").is_symlink():
        assert "4242" in msg


def test_ouvrir_refuse_profil_verrouille(profil):
    (profil / "SingletonLock").write_text("x")
    with pytest.raises(pn.ProfilVerrouille):
        with pn.ouvrir():
            pass


class _Loc:
    def __init__(self, n):
        self.n = n

    def count(self):
        return self.n


class _Page:
    def __init__(self, url="https://app.snowflake.com/x", presents=()):
        self.url = url
        self.presents = presents

    def locator(self, sel):
        return _Loc(1 if any(p in sel for p in self.presents) else 0)


def test_login_expire_url():
    assert pn.login_expire(_Page("https://login.microsoftonline.com/abc"))


def test_login_expire_champs():
    assert pn.login_expire(_Page(presents=("loginfmt",)))
    assert pn.login_expire(_Page(presents=("Sign in",)))


def test_login_non_expire():
    assert not pn.login_expire(_Page())


def test_cli_parsing():
    ap = pn._parser()
    a = ap.parse_args(["recette", "http://x", "--attendre", "#a", "--sortie", "out"])
    assert (a.cmd, a.attendre, a.sortie) == ("recette", "#a", "out")
    a = ap.parse_args(["capture", "http://x", "p.png", "--viewport", "large"])
    assert a.viewport == "large"
    assert ap.parse_args(["pdf", "s.html", "o.pdf"]).cmd == "pdf"
    assert ap.parse_args(["verrou"]).cmd == "verrou"
    with pytest.raises(SystemExit):
        ap.parse_args(["capture", "http://x", "p.png", "--viewport", "inconnu"])


def test_cli_verrou(profil, capsys):
    assert pn.main(["verrou"]) == 0
    assert "libre" in capsys.readouterr().out


@pytest.mark.skipif(not PLAYWRIGHT, reason="playwright non installé")
def test_integration_recette_et_pdf(profil, tmp_path):
    page_html = tmp_path / "page.html"
    page_html.write_text(HTML, encoding="utf-8")
    sortie = tmp_path / "sortie"
    echecs = pn.recette(page_html.resolve().as_uri(), attendre="#titre", sortie=str(sortie))
    assert echecs == []
    assert sorted(p.name for p in sortie.glob("*.png")) == ["desktop.png", "mobile.png"]
    out = pn.pdf(str(page_html), tmp_path / "doc.pdf")
    assert out.stat().st_size > 1024
    # PREUVES_DIR (optionnel) : copie les sorties pour inspection visuelle
    dest = os.environ.get("PREUVES_DIR")
    if dest:
        Path(dest).mkdir(parents=True, exist_ok=True)
        for p in [*sortie.glob("*.png"), out]:
            (Path(dest) / p.name).write_bytes(p.read_bytes())
