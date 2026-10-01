"""Isolation commune : aucun test ne lit le vrai HOME ni un snow installé dans le Python global."""
import os
import re

import pytest

PYTHON_SCRIPTS = re.compile(r"/python[^/]*/scripts$")


@pytest.fixture(autouse=True)
def home_isole(tmp_path_factory, monkeypatch):
    h = tmp_path_factory.mktemp("home_isole")
    monkeypatch.setenv("USERPROFILE", str(h))
    monkeypatch.setenv("HOME", str(h))
    propre = [d for d in os.environ.get("PATH", "").split(os.pathsep)
              if not PYTHON_SCRIPTS.search(d.replace("\\", "/").rstrip("/").lower())]
    monkeypatch.setenv("PATH", os.pathsep.join(propre))
    yield h
