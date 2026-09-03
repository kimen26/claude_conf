#!/usr/bin/env python3
"""Recette visuelle — porte de vérification pour tout projet avec un écran.

Ouvre l'URL en mobile ET desktop, capture, ÉCHOUE sur : erreur console,
exception page, réponse HTTP >= 400 sur le document principal, sélecteur
attendu absent. Les captures sont la preuve — les OUVRIR, un exit 0 ne dit
pas que l'œil voit juste.

Usage :
  python recette-visuelle.py URL [--wait "#app"] [--out recette] [--auth state.json]
                                 [--allow-console "regex"] [--timeout 30000]
  --auth   : storage state Playwright (SSO, cookies) — créer une fois avec
             `playwright codegen --save-storage=state.json URL`, NE PAS commiter.
  --allow-console : regex des messages console tolérés (bruit tiers connu).

Prérequis (une fois par machine) : pip install playwright && playwright install chromium
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

VIEWPORTS = {"mobile": (390, 844), "desktop": (1440, 900)}


def run(args) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    allow = re.compile(args.allow_console) if args.allow_console else None
    failures: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, (w, h) in VIEWPORTS.items():
            ctx_kwargs = {"viewport": {"width": w, "height": h}}
            if args.auth:
                ctx_kwargs["storage_state"] = args.auth
            ctx = browser.new_context(**ctx_kwargs)
            page = ctx.new_page()
            errors: list[str] = []
            page.on(
                "console",
                lambda m: errors.append(f"console.{m.type}: {m.text}")
                if m.type == "error" and not (allow and allow.search(m.text))
                else None,
            )
            page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))

            resp = page.goto(args.url, wait_until="networkidle", timeout=args.timeout)
            if resp is not None and resp.status >= 400:
                errors.append(f"HTTP {resp.status} sur le document principal")
            if args.wait:
                try:
                    page.wait_for_selector(args.wait, timeout=args.timeout)
                except Exception:
                    errors.append(f"selecteur absent : {args.wait}")

            shot = out / f"{stamp}-{name}.png"
            page.screenshot(path=str(shot), full_page=True)
            verdict = "OK " if not errors else "KO "
            print(f"[{verdict}] {name:8} {w}x{h}  -> {shot}")
            for e in errors:
                print(f"       - {e}")
            failures += [f"{name}: {e}" for e in errors]
            ctx.close()
        browser.close()

    if failures:
        print(f"\nRECETTE KO - {len(failures)} anomalie(s). Ouvrir les captures dans {out}/")
        return 1
    print(f"\nRECETTE OK - ouvrir quand meme les captures dans {out}/ (l'oeil tranche).")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--wait", help="sélecteur CSS qui doit apparaître")
    ap.add_argument("--out", default="recette", help="dossier des captures (à .gitignore)")
    ap.add_argument("--auth", help="storage state Playwright (SSO)")
    ap.add_argument("--allow-console", help="regex des erreurs console tolérées")
    ap.add_argument("--timeout", type=int, default=30000)
    sys.exit(run(ap.parse_args()))
