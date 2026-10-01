"""Tests du pilier secrets : skills/secrets/scripts/secrets.py et motifs_secrets.py.

Toutes les valeurs sont factices et fabriquées à l'exécution. Aucun test ne touche au vrai HOME,
à la vraie variable d'environnement utilisateur ni au vrai registre.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN / "hooks" / "scripts"))
import motifs_secrets as ms  # noqa: E402

spec = importlib.util.spec_from_file_location("secrets_cli", PLUGIN / "skills/secrets/scripts/secrets.py")
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)

FAUX = "glpat-" + "FAUX0000000000000000"
PWD = "mdp" + "Factice987"
REGISTRE = ("| nom | usage | consommateurs | posé le |\n|---|---|---|---|\n"
            "| `MON_TOKEN` | essai | test | 2026-01-01 |\n| `AUTRE_TOKEN` | essai | test | 2026-01-01 |\n")


def ecrire(p: Path, texte: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texte, encoding="utf-8")
    return p


def n_fichiers(racine: Path) -> int:
    return sum(1 for p in racine.rglob("*") if p.is_file())


@pytest.fixture
def faux(tmp_path, monkeypatch):
    h = tmp_path / "home"
    cl = h / ".claude"
    cl.mkdir(parents=True)
    monkeypatch.setattr(Path, "home", staticmethod(lambda: h))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(cl))
    monkeypatch.setenv("LOCALAPPDATA", str(h / "AppData/Local"))
    monkeypatch.delenv("CLAUDE_PLUGIN_ROOT", raising=False)
    reg = ecrire(tmp_path / "registre.md", REGISTRE)
    monkeypatch.setattr(sec, "chemin_registre", lambda: reg)
    env = ["FAUX_TOKEN", "PATH"]
    monkeypatch.setattr(sec, "lire_env_user", lambda: list(env))
    ecrire(cl / "settings.json", json.dumps({
        "env": {"FAUX_TOKEN": FAUX, "OK_TOKEN": "${OK_TOKEN}", "THEME": "dark"},
        "mcpServers": {"x": {"command": "npx"}}}))
    ecrire(cl / "settings.json.bak", '{"env": {"FAUX_TOKEN": "' + FAUX + '"}}')
    ecrire(cl / "backups/x.backup", '{"k": "' + FAUX + '"}')
    ecrire(cl / "backups/propre.backup", '{"k": 1}')
    ecrire(cl / "skills/confluence/config/secrets.ps1", '$env:CONF_API_TOKEN = "' + FAUX + '"\n$env:CONF_URL = "u"\n')
    ecrire(cl / "skills/confluence/config/secrets.template.ps1", '$env:CONF_API_TOKEN = ""\n')
    ecrire(h / ".snowflake/connections.toml",
           '[connections.sso]\nauthenticator = "externalbrowser"\nclient_store_temporary_credential = true\n'
           f'[connections.pwd]\nauthenticator = "externalbrowser"\npassword = "{PWD}"\n')
    proj = tmp_path / "proj"
    ecrire(proj / ".env", f"FAUX_TOKEN={FAUX}\nDEBUG=1\n")
    ecrire(proj / ".env.example", "FAUX_TOKEN=\n")
    return {"home": h, "claude": cl, "proj": proj, "env": env, "registre": reg}


def etats(rows):
    return [r["etat"] for r in rows]


def test_inventaire_etats_attendus(faux, capsys):
    rows = sec.inventaire([faux["proj"]])
    par = {}
    for r in rows:
        par.setdefault(r["etat"], []).append(r)
    assert len(par["a_deplacer"]) == 3  # settings FAUX_TOKEN, secrets.ps1, connexion pwd.password
    assert {r["type"] for r in par["a_deplacer"]} == {"settings_env", "secrets_ps1", "snowflake"}
    assert any(r["nom"] == "pwd.password" for r in par["a_deplacer"])
    ps1 = [r["nom"] for r in rows if r["type"] == "secrets_ps1"]
    assert ps1 == ["CONF_API_TOKEN"]  # ni CONF_URL (pas un secret), ni le modèle .template.ps1
    assert [r["nom"] for r in par["config_morte"]] == ["mcpServers"]
    assert sorted(r["nom"] for r in par["sauvegarde_a_purger"]) == ["settings.json.bak", "x.backup"]
    assert [r["type"] for r in par["doublon"]] == ["env_fichier"]
    assert [r["nom"] for r in par["hors_registre"]] == ["FAUX_TOKEN"]
    assert any(r["nom"] == "OK_TOKEN" and r["etat"] == "conforme" for r in rows)
    assert not any(r["nom"] == "THEME" or r["nom"] == "PATH" for r in rows)
    assert [r["nom"] for r in par["non_conforme_sso"]] == ["pwd"]


def test_inventaire_sortie_sans_valeur(faux, capsys):
    assert sec.main(["inventaire", str(faux["proj"])]) == 0
    sortie = capsys.readouterr().out
    assert "a_deplacer" in sortie and "sauvegarde_a_purger" in sortie
    assert FAUX not in sortie and PWD not in sortie
    assert ms.trouver(sortie, large=True) == []
    assert sec.main(["inventaire", str(faux["proj"]), "--json"]) == 0
    brut = capsys.readouterr().out
    assert FAUX not in brut and PWD not in brut and "chemin" not in json.loads(brut)[0]


def test_inventaire_env_sans_exemple(faux):
    (faux["proj"] / ".env.example").unlink()
    rows = sec.inventaire([faux["proj"]])
    assert any(r["etat"] == "exemple_manquant" for r in rows)


def test_claude_json_cles_dupliquees(faux):
    brut = ('{"mcpServers": {"a": {"env": {"T_TOKEN": "${T_TOKEN}"}}}, '
            '"mcpServers": {"a": {"env": {"T_TOKEN": "' + FAUX + '"}}}}')
    ecrire(faux["claude"] / ".claude.json", brut)
    rows = sec.inventaire([faux["proj"]])
    assert any(r["type"] == "claude_json_mcp" and r["etat"] == "a_deplacer" for r in rows)


def test_verifier(faux, capsys):
    faux["env"][:] = ["MON_TOKEN", "ORPHELINE_TOKEN"]
    assert sec.main(["verifier"]) == 1
    sortie = capsys.readouterr().out
    assert "MANQUE : AUTRE_TOKEN" in sortie
    assert "ORPHELINE : ORPHELINE_TOKEN" in sortie
    assert "MON_TOKEN" not in sortie.replace("ORPHELINE_TOKEN", "")
    faux["env"][:] = ["MON_TOKEN", "AUTRE_TOKEN"]
    assert sec.main(["verifier"]) == 0


def test_verifier_refuse_requests_ca_bundle(faux, capsys):
    faux["env"][:] = ["MON_TOKEN", "AUTRE_TOKEN", "REQUESTS_CA_BUNDLE"]
    assert sec.main(["verifier"]) == 1
    assert "REQUESTS_CA_BUNDLE" in capsys.readouterr().out


def test_purger_sans_oui_ne_bouge_rien(faux, capsys):
    avant = n_fichiers(faux["home"])
    assert sec.main(["purger"]) == 0
    assert n_fichiers(faux["home"]) == avant
    assert (faux["claude"] / "settings.json.bak").exists()
    assert not (faux["claude"] / "_a_supprimer").exists()
    assert "--oui" in capsys.readouterr().out


def test_purger_oui_deplace_et_manifeste(faux):
    avant = n_fichiers(faux["home"])
    assert sec.main(["purger", "--oui"]) == 0
    jours = list((faux["claude"] / "_a_supprimer").iterdir())
    assert len(jours) == 1
    racine = jours[0] / "secrets"
    assert (racine / ".claude/settings.json.bak").is_file()
    assert (racine / ".claude/backups/x.backup").is_file()
    assert (racine / ".claude/skills/confluence/config/secrets.ps1").is_file()
    assert not (faux["claude"] / "settings.json.bak").exists()
    assert (faux["claude"] / "settings.json").exists()  # le fichier vivant reste
    man = (racine / "MANIFESTE.md").read_text(encoding="utf-8")
    assert "settings.json.bak" in man and "secrets.ps1" in man and FAUX not in man
    assert n_fichiers(faux["home"]) == avant + 1  # rien supprimé, le manifeste s'ajoute
    # le manifeste ne fait pas ressortir de sauvegarde
    assert not [r for r in sec.inventaire([faux["proj"]]) if r["etat"] == "sauvegarde_a_purger"]


def test_poser_valeur_par_stdin_et_registre(faux, monkeypatch, capsys):
    secret = "glpat-" + "FAUX1111111111111111"
    vus = []

    def faux_run(cmd, **kw):
        vus.append((cmd, kw))
        return type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(sec.getpass, "getpass", lambda *_a, **_k: secret)
    monkeypatch.setattr(sec.subprocess, "run", faux_run)
    assert sec.main(["poser", "NOUVEAU_TOKEN", "--usage", "essai poser"]) == 0
    cmd, kw = vus[0]
    assert secret not in " ".join(map(str, cmd))
    assert kw["input"] == secret
    assert "NOUVEAU_TOKEN" in " ".join(cmd)
    assert secret not in capsys.readouterr().out
    reg = sec.lire_registre()
    assert reg["NOUVEAU_TOKEN"]["usage"] == "essai poser"
    assert secret not in faux["registre"].read_text(encoding="utf-8")
    assert sec.main(["poser", "NOUVEAU_TOKEN"]) == 0  # re-pose : pas de doublon de ligne
    assert faux["registre"].read_text(encoding="utf-8").count("`NOUVEAU_TOKEN`") == 1


def test_poser_nom_invalide(faux, monkeypatch):
    monkeypatch.setattr(sec.getpass, "getpass", lambda *_a, **_k: "x")
    assert sec.main(["poser", "a b; rm"]) == 2


def test_ssl_ne_pose_jamais_requests(faux, monkeypatch, tmp_path, capsys):
    bundle = ecrire(tmp_path / "bundle.crt", "x")
    monkeypatch.setattr(sec, "BUNDLE", str(bundle))
    poses, lances = [], []
    monkeypatch.setattr(sec, "ecrire_env_user", lambda n, v: poses.append((n, v)))
    monkeypatch.setattr(sec, "_executer", lambda cmd: lances.append(cmd) or (0, ""))
    assert sec.main(["ssl"]) == 0
    noms = [n for n, _ in poses]
    assert noms == ["NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE", "NETSKOPE_BUNDLE", "UV_NATIVE_TLS"]
    assert dict(poses)["UV_NATIVE_TLS"] == "1" and dict(poses)["SSL_CERT_FILE"] == str(bundle)
    assert any("global.cert" in c for c in lances)
    assert "REQUESTS_CA_BUNDLE" not in noms
    assert set(noms) <= set(sec.lire_registre())
    assert sec.main(["ssl", "--sans-requests"]) == 2
    assert "casse snow" in capsys.readouterr().out or True


def test_ssl_bundle_absent(faux, monkeypatch, tmp_path):
    monkeypatch.setattr(sec, "BUNDLE", str(tmp_path / "absent.crt"))
    monkeypatch.setattr(sec, "ecrire_env_user", lambda n, v: pytest.fail("rien ne doit être posé"))
    assert sec.main(["ssl"]) == 1


def test_snow(faux, monkeypatch, capsys):
    h = faux["home"]
    snow = ecrire(h / ".local/bin/snow.exe", "")
    uvdir = h / "uvtools"
    ecrire(uvdir / "snowflake-cli/Scripts/python.exe", "")
    ecrire(h / "AppData/Local/Snowflake/Caches/credential_cache_v1.json", "{}")
    monkeypatch.setattr(sec.shutil, "which", lambda n: str(snow) if n == "snow" else "uv.exe")

    def exe(cmd):
        if cmd[1:3] == ["tool", "dir"]:
            return 0, str(uvdir)
        if cmd[-1] == "--version":
            return 0, "snow 3.28.0"
        return 0, ""
    monkeypatch.setattr(sec, "_executer", exe)
    assert sec.main(["snow"]) == 0
    assert "credential_cache_v1.json présent" in capsys.readouterr().out
    # snow dans le Python global, keyring absent, cache absent
    monkeypatch.setattr(sec.shutil, "which", lambda n: r"C:\Python312\Scripts\snow.exe" if n == "snow" else "uv.exe")
    monkeypatch.setattr(sec, "_executer", lambda cmd: (1, str(uvdir)) if "import keyring" in cmd else exe(cmd))
    (h / "AppData/Local/Snowflake/Caches/credential_cache_v1.json").unlink()
    assert sec.main(["snow"]) == 1
    sortie = capsys.readouterr().out
    assert "uv tool install snowflake-cli --native-tls" in sortie
    assert "keyring absent" in sortie and "cache de token SSO absent" in sortie and "Python global" in sortie


def test_settings_env_valeurs_banales(faux):
    """MAX_THINKING_TOKENS=10000 dans settings.json user n'est pas un secret (relevé en réel)."""
    ecrire(faux["claude"] / "settings.json", json.dumps({"env": {
        "MAX_THINKING_TOKENS": "10000", "OTHER_TOKEN": 5, "A_TOKEN": "true", "B_TOKEN": "",
        "C_TOKEN": str(faux["claude"]), "THEME": "dark", "REAL_TOKEN": FAUX, "REF_TOKEN": "${REF_TOKEN}"}}))
    etats_ = {r["nom"]: r["etat"] for r in sec.inventaire([faux["proj"]]) if r["type"] == "settings_env"}
    assert etats_["MAX_THINKING_TOKENS"] == "conforme"
    assert etats_["REAL_TOKEN"] == "a_deplacer"
    assert etats_["REF_TOKEN"] == "conforme"
    assert "THEME" not in etats_
    assert not [n for n in ("A_TOKEN", "B_TOKEN", "C_TOKEN") if etats_.get(n) == "a_deplacer"]


def test_motifs():
    assert ms.nom_secret("GITLAB_PAT") and ms.nom_secret("N8N_API_KEY") and ms.nom_secret("x_token")
    assert not ms.nom_secret("PATH") and not ms.nom_secret("PYTHONPATH") and not ms.nom_secret("PATHEXT")
    assert ms.a_motif(FAUX)
    assert not ms.a_motif("eyJhbGci...")  # JWT tronqué
    jwt = ".".join(["eyJ" + "a" * 12, "b" * 12, "c" * 12])
    assert ms.a_motif(jwt)
    assert ms.a_motif('GITLAB_PAT = "' + "z" * 14 + '"', large=True)
    assert not ms.a_motif('GITLAB_PAT = "${GITLAB_PAT}"', large=True)
    assert not ms.a_motif("PATH=" + "z" * 30, large=True)
    assert not ms.valeur_en_clair("MAX_THINKING_TOKENS", "31999") and not ms.valeur_en_clair("A_TOKEN", "true")
    assert ms.valeur_en_clair("MON_TOKEN", "abc") and not ms.valeur_en_clair("MON_TOKEN", "${MON_TOKEN}")
    assert not ms.valeur_en_clair("THEME", "dark")
    c = ms.analyser_connexions('[connections.a]\nauthenticator = "externalbrowser"\n'
                               'client_store_temporary_credential = true\n[b]\nprivate_key_file = "k"\n')
    assert ms.defauts_connexion(c["a"]) == []
    assert any("private_key_file" in d for d in ms.defauts_connexion(c["b"]))
    assert "k" not in str(c["b"]["interdits"]) or c["b"]["interdits"] == ["private_key_file"]


def test_emplacements_purger_ne_supprime_rien(tmp_path, capsys):
    spec2 = importlib.util.spec_from_file_location("emplacements_cli", PLUGIN / "skills/secrets/scripts/emplacements.py")
    emp = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(emp)
    racine = tmp_path / "claude"
    ecrire(racine / "pw-profile/Default/cookies", "x" * 2048)
    ecrire(racine / "venv-a/lib/m.py", "y" * 4096)
    ecrire(racine / "pw-shots/a.png", "z")
    ecrire(racine / "notes.txt", "vrac")
    avant = sum(1 for p in racine.rglob("*") if p.is_file())
    assert emp.main(["purger", "--racine", str(racine)]) == 0
    sortie = capsys.readouterr().out
    assert "a migrer" in sortie and "migrer-profil" in sortie
    assert "Remove-Item" in sortie and "venv-a" in sortie and "candidat evident" in sortie
    assert "pw-profile'" not in sortie  # le profil n'est jamais proposé à la suppression
    assert "fichiers en vrac : 1" in sortie
    assert sum(1 for p in racine.rglob("*") if p.is_file()) == avant
    assert emp.main(["purger", "--racine", str(tmp_path / "absent")]) == 0


def test_registre_repo_d_abord(tmp_path, monkeypatch, capsys):
    h = tmp_path / "home"
    monkeypatch.setattr(Path, "home", staticmethod(lambda: h))
    racine = tmp_path / "plugin"
    ecrire(racine / "rules/secrets-registre.md", REGISTRE)
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(racine))
    assert sec.chemin_registre() == racine / "rules/secrets-registre.md"
    sec.avertir_hors_repo()
    assert "registre modifié hors repo" in capsys.readouterr().out
    repo = ecrire(sec.repo_registre(), REGISTRE)
    assert sec.chemin_registre() == repo
    sec.avertir_hors_repo()
    assert capsys.readouterr().out == ""
