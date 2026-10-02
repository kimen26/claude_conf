"""Isolation commune : aucun test ne lit le vrai HOME ni un snow installé dans le Python global."""
import os
import re
import shutil
from pathlib import Path

import pytest

PYTHON_SCRIPTS = re.compile(r"/python[^/]*/scripts$")


@pytest.fixture(autouse=True)
def home_isole(tmp_path_factory, monkeypatch):
    h = tmp_path_factory.mktemp("home_isole")
    monkeypatch.setenv("USERPROFILE", str(h))
    monkeypatch.setenv("HOME", str(h))
    # home « à jour » : règles machine déjà copiées (sinon S-72 sort sur tout test qui audite le vrai plugin)
    src = Path(__file__).resolve().parent.parent / "rules" / "machine"
    if src.is_dir():
        (h / ".claude" / "rules").mkdir(parents=True)
        for f in src.glob("*.md"):
            shutil.copy(f, h / ".claude" / "rules" / f.name)
    propre = [d for d in os.environ.get("PATH", "").split(os.pathsep)
              if not PYTHON_SCRIPTS.search(d.replace("\\", "/").rstrip("/").lower())]
    monkeypatch.setenv("PATH", os.pathsep.join(propre))
    yield h
