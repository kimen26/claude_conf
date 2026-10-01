"""Preuve navigateur partagée : captures, recette, PDF, sur un profil SSO unique par PC.

Doctrine :
  * la preuve se fait en Playwright Python HEADLESS sur le profil persistant ``PROFIL`` ;
  * ``setup_sso`` (headed) ne sert qu'UNE fois par PC, pour se connecter à la main ;
  * jamais ``storage_state``, jamais ``connect_over_cdp`` ;
  * le navigateur est TOUJOURS fermé (``finally``), sinon le profil reste verrouillé.

Importable (``from preuve_navigateur import *``) et exécutable en CLI :
``python preuve_navigateur.py setup|recette|capture|pdf|verrou|migrer-profil``.
Codes de sortie CLI : 0 succès, 1 échec, 3 login expiré.
Aucun ``print`` hors CLI : la bibliothèque journalise via ``logging``.
"""
from __future__ import annotations

import argparse
import contextlib
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

log = logging.getLogger("preuve_navigateur")

def racine_etat() -> Path:
    """État machine non versionné (profil SSO, caches) : %LOCALAPPDATA%/socle, jamais synchronisé."""
    base = os.environ.get("LOCALAPPDATA")
    return (Path(base) if base else Path.home() / "AppData" / "Local") / "socle"


PROFIL = racine_etat() / "pw-profile"
ANCIEN_PROFIL = Path("C:/tmp/claude/pw-profile")  # emplacement interdit : sert à migrer-profil seulement
VIEWPORTS = {"mobile": (390, 844), "desktop": (1440, 900), "large": (1850, 820)}

EXIT_OK, EXIT_ECHEC, EXIT_LOGIN = 0, 1, 3

_MARQUEURS_URL_LOGIN = ("login.microsoftonline.com", "login.live.com")
_MARQUEURS_SELECTEURS = ('input[name="loginfmt"]', 'input[type="password"]')
_MARQUEURS_TEXTE = ("Sign in", "Sign in to Snowflake")


class ProfilVerrouille(RuntimeError):
    """Le profil Chromium est déjà utilisé par un autre processus."""


class LoginExpire(RuntimeError):
    """La session SSO a expiré : relancer ``setup_sso``."""


def _import_playwright():
    from playwright.sync_api import sync_playwright
    return sync_playwright


# --------------------------------------------------------------------- verrou
def verrou_profil() -> str | None:
    """Rend un message si le profil est déjà utilisé par une autre session, sinon None.

    Chromium pose ``SingletonLock`` (Linux/mac, lien symbolique « hote-pid ») ou
    ``lockfile`` (Windows, ouvert en exclusivité tant que le navigateur tourne).
    """
    for nom in ("SingletonLock", "lockfile"):
        f = PROFIL / nom
        if not (f.exists() or f.is_symlink()):
            continue
        if nom == "lockfile":
            # Sous Windows, un lockfile résiduel d'un navigateur fermé est supprimable.
            try:
                f.unlink()
                continue
            except OSError:
                pass
        pid = ""
        with contextlib.suppress(OSError):
            cible = str(f.readlink()) if f.is_symlink() else ""
            m = re.search(r"-(\d+)$", cible)
            if m:
                pid = f" (pid {m.group(1)})"
        return f"profil déjà utilisé par une autre session{pid} : {PROFIL / nom}"
    return None


# ------------------------------------------------------------------- ouverture
@contextlib.contextmanager
def ouvrir(headed: bool = False, viewport: str = "desktop", video_dir=None):
    """Ouvre le profil partagé et rend ``(ctx, page)``. Ferme TOUJOURS le contexte.

    Lève ``ProfilVerrouille`` si une autre session tient le profil.
    """
    msg = verrou_profil()
    if msg:
        raise ProfilVerrouille(msg)
    largeur, hauteur = VIEWPORTS[viewport]
    PROFIL.mkdir(parents=True, exist_ok=True)
    with _import_playwright()() as pw:
        options = dict(headless=not headed, viewport={"width": largeur, "height": hauteur})
        if video_dir:
            Path(video_dir).mkdir(parents=True, exist_ok=True)
            options["record_video_dir"] = str(video_dir)
        ctx = pw.chromium.launch_persistent_context(str(PROFIL), **options)
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            yield ctx, page
        finally:
            ctx.close()


def migrer_profil() -> tuple[int, str]:
    """Déplace l'ancien profil (C:/tmp/claude/pw-profile) vers PROFIL. Rend (code, message)."""
    if PROFIL.exists():
        suite = f" ; l'ancien {ANCIEN_PROFIL} est à supprimer par Yann" if ANCIEN_PROFIL.exists() else ""
        return EXIT_OK, f"profil déjà à sa place : {PROFIL}{suite}"
    if not ANCIEN_PROFIL.exists():
        return EXIT_OK, f"aucun profil à migrer : lancer 'setup <URL>' pour créer {PROFIL}"
    try:
        PROFIL.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(ANCIEN_PROFIL), str(PROFIL))
    except OSError as e:
        return EXIT_ECHEC, f"déplacement impossible ({type(e).__name__}) : fermer le navigateur qui tient le profil"
    return EXIT_OK, f"profil déplacé vers {PROFIL}"


def setup_sso(url: str) -> None:
    """Seul usage headed : ouvre ``url``, laisse Yann se connecter, attend la fermeture."""
    log.info("connecte-toi, puis ferme la fenêtre")
    with ouvrir(headed=True) as (ctx, page):
        page.goto(url, wait_until="domcontentloaded")
        while ctx.pages:
            time.sleep(1)
            try:
                ctx.pages[0].title()
            except Exception:
                break


# ------------------------------------------------------------------ détections
def login_expire(page) -> bool:
    """Vrai si la page est un écran de connexion Entra ou Snowflake (SSO expiré)."""
    try:
        if any(m in (page.url or "") for m in _MARQUEURS_URL_LOGIN):
            return True
        for sel in _MARQUEURS_SELECTEURS:
            if page.locator(sel).count() > 0:
                return True
        for txt in _MARQUEURS_TEXTE:
            if page.locator(f"text={txt}").count() > 0:
                return True
    except Exception:
        return False
    return False


def cadre_app(page):
    """Rend la frame Streamlit si l'app est servie en iframe (Snowsight), sinon ``page``."""
    try:
        for frame in page.frames:
            try:
                if frame.locator('[data-testid="stApp"]').count() > 0 and frame != page.main_frame:
                    return frame
            except Exception:
                continue
    except Exception:
        pass
    return page


def exceptions_streamlit(page) -> list[str]:
    """Textes des exceptions Streamlit affichées (``[data-testid="stException"]``)."""
    cible = cadre_app(page)
    loc = cible.locator('[data-testid="stException"]')
    return [loc.nth(i).inner_text()[:500] for i in range(min(loc.count(), 5))]


# --------------------------------------------------------------------- captures
def capturer(page, chemin, pleine_page: bool = True) -> Path:
    """Capture ``page`` en PNG vers ``chemin`` (dossier créé) et rend le chemin."""
    p = Path(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(p), full_page=pleine_page)
    return p


def recette(url, attendre=None, viewports=("mobile", "desktop"), sortie="recette",
            tolerer_console=None) -> list[str]:
    """Charge ``url`` par viewport et rend la liste des échecs (vide = succès).

    Échecs : erreur console (hors regex ``tolerer_console``), pageerror, HTTP >= 400 sur le
    document, sélecteur ``attendre`` absent, exception Streamlit, login expiré (message
    explicite « lance setup_sso »). Une capture ``<sortie>/<viewport>.png`` est produite.
    """
    tolere = re.compile(tolerer_console) if tolerer_console else None
    echecs: list[str] = []
    for vp in viewports:
        erreurs: list[str] = []
        statut = {}
        with ouvrir(viewport=vp) as (_ctx, page):
            page.on("console", lambda m, e=erreurs: e.append(f"console: {m.text}")
                    if m.type == "error" and not (tolere and tolere.search(m.text)) else None)
            page.on("pageerror", lambda x, e=erreurs: e.append(f"pageerror: {x}"))
            page.on("response", lambda r, s=statut: s.setdefault("doc", r.status)
                    if r.request.resource_type == "document" else None)
            page.goto(url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            if login_expire(page):
                echecs.append(f"[{vp}] login expiré : lance setup_sso")
                capturer(page, Path(sortie) / f"{vp}_login.png", pleine_page=False)
                continue
            if attendre:
                try:
                    cadre_app(page).locator(attendre).first.wait_for(state="visible", timeout=30000)
                except Exception:
                    echecs.append(f"[{vp}] sélecteur absent : {attendre}")
            capturer(page, Path(sortie) / f"{vp}.png")
            echecs += [f"[{vp}] {e}" for e in erreurs]
            if statut.get("doc", 0) >= 400:
                echecs.append(f"[{vp}] HTTP {statut['doc']} sur le document")
            echecs += [f"[{vp}] exception Streamlit : {t}" for t in exceptions_streamlit(page)]
    return echecs


# -------------------------------------------------------------------------- PDF
def _url(src) -> tuple[str, Path | None]:
    s = str(src)
    if s.startswith(("http://", "https://", "file://")):
        return s, None
    if s.lstrip().startswith("<"):
        tmp = Path(tempfile.mkdtemp(prefix="pdf_src_")) / "source.html"
        tmp.write_text(s, encoding="utf-8")
        return tmp.resolve().as_uri(), tmp
    return Path(s).resolve().as_uri(), None


def _navigateur_systeme() -> str | None:
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if Path(p).exists():
            return p
    return shutil.which("chrome") or shutil.which("msedge")


def pdf(html_ou_url, chemin) -> Path:
    """Imprime un HTML (chemin, balisage ou URL) en PDF.

    Playwright chromium headless d'abord ; repli ``--headless=new --print-to-pdf`` de
    Chrome/Edge si Playwright est indisponible. Utilise un profil jetable, pas ``PROFIL``.
    """
    out = Path(chemin).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    url, tmp = _url(html_ou_url)
    try:
        try:
            sync_playwright = _import_playwright()
            with sync_playwright() as pw:
                nav = pw.chromium.launch(headless=True)
                try:
                    page = nav.new_page()
                    page.goto(url, wait_until="load")
                    page.pdf(path=str(out), print_background=True)
                finally:
                    nav.close()
            return out
        except ImportError:
            log.info("Playwright indisponible, repli sur chrome/edge")
        exe = _navigateur_systeme()
        if not exe:
            raise RuntimeError("ni Playwright ni Chrome/Edge disponibles pour le PDF")
        profil = Path(tempfile.mkdtemp(prefix="pdf_prof_"))
        try:
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-sandbox",
                            f"--user-data-dir={profil}", f"--print-to-pdf={out}",
                            "--print-to-pdf-no-header", url],
                           capture_output=True, text=True, timeout=60, check=True)
        finally:
            shutil.rmtree(profil, ignore_errors=True)
        return out
    finally:
        if tmp:
            shutil.rmtree(tmp.parent, ignore_errors=True)


# -------------------------------------------------------------------------- CLI
def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="preuve_navigateur", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup", help="SSO manuel une fois par PC (headed)").add_argument("url")
    r = sub.add_parser("recette", help="recette multi-viewports")
    r.add_argument("url")
    r.add_argument("--attendre", help="sélecteur CSS qui doit être visible")
    r.add_argument("--sortie", default="recette")
    r.add_argument("--tolerer-console", help="regex d'erreurs console tolérées")
    c = sub.add_parser("capture", help="une capture")
    c.add_argument("url")
    c.add_argument("chemin")
    c.add_argument("--viewport", default="desktop", choices=sorted(VIEWPORTS))
    p = sub.add_parser("pdf", help="HTML ou URL vers PDF")
    p.add_argument("src")
    p.add_argument("chemin")
    sub.add_parser("verrou", help="dit si le profil est verrouillé")
    sub.add_parser("migrer-profil", help="déplace C:/tmp/claude/pw-profile vers %LOCALAPPDATA%/socle/pw-profile")
    return ap


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = _parser().parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if args.cmd == "verrou":
            msg = verrou_profil()
            print(msg or "profil libre")
            return EXIT_ECHEC if msg else EXIT_OK
        if args.cmd == "migrer-profil":
            code, msg = migrer_profil()
            print(msg)
            return code
        if args.cmd == "setup":
            setup_sso(args.url)
            return EXIT_OK
        if args.cmd == "recette":
            echecs = recette(args.url, args.attendre, sortie=args.sortie,
                             tolerer_console=args.tolerer_console)
            for e in echecs:
                print("ECHEC", e)
            if any("login expiré" in e for e in echecs):
                return EXIT_LOGIN
            print("recette OK" if not echecs else f"{len(echecs)} échec(s)")
            return EXIT_ECHEC if echecs else EXIT_OK
        if args.cmd == "capture":
            with ouvrir(viewport=args.viewport) as (_c, page):
                page.goto(args.url, wait_until="domcontentloaded")
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                if login_expire(page):
                    print("login expiré : lance 'setup'")
                    return EXIT_LOGIN
                print(capturer(page, args.chemin))
            return EXIT_OK
        if args.cmd == "pdf":
            print(pdf(args.src, args.chemin))
            return EXIT_OK
    except ProfilVerrouille as e:
        print(f"ECHEC {e}")
        return EXIT_ECHEC
    return EXIT_ECHEC


if __name__ == "__main__":
    sys.exit(main())
