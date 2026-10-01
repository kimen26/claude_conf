---
name: preuve-navigateur
description: À utiliser pour toute preuve d'écran (capture, vidéo, PDF, recette, smoke) dans n'importe quel projet, y compris une app Streamlit dans Snowsight.
---

# Preuve navigateur

Deux modes, jamais l'inverse :

1. **Preuve** : Playwright Python headless via `preuve_navigateur` (reproductible, produit des fichiers).
2. **Regard** : Comet via l'extension, pour explorer ou montrer à Yann. Ne prouve rien, ne remplace jamais le mode 1.

## Profil partagé

Un seul profil par PC : `%LOCALAPPDATA%\socle\pw-profile` (constante `PROFIL`, jamais synchronisé, jamais `C:/tmp`). Profil resté à l'ancien emplacement : `python outils/preuve_navigateur.py migrer-profil` (déplace, sinon relancer `setup`). Le SSO s'y fait **une fois par PC** :

```
python outils/preuve_navigateur.py setup <URL>    # seul usage headed : connecte-toi, ferme la fenêtre
```

Ensuite tout est headless. Session Entra expirée : la lib rend le code 3 / « login expiré », on relance `setup`. Deux navigateurs ne partagent pas le profil : `verrou` dit qui le tient (`ProfilVerrouille`).

## Importer la lib (shim de 5 lignes)

La lib vit dans `~/.claude/plugins/data/socle/lib/` (recopiée par le hook SessionStart). Le projet n'en garde que le shim `outils/preuve_navigateur.py` :

```python
import sys; from pathlib import Path
sys.path.insert(0, str(Path.home()/".claude/plugins/data/socle/lib")); from preuve_navigateur import *
```

## API

| Fonction | Rôle |
|---|---|
| `ouvrir(headed, viewport, video_dir)` | context manager `(ctx, page)`, ferme toujours |
| `setup_sso(url)` | SSO manuel, une fois par PC |
| `login_expire(page)` | vrai si Entra / Snowflake demande de se connecter |
| `cadre_app(page)` | frame Streamlit (iframe Snowsight) ou `page` |
| `capturer(page, chemin, pleine_page)` | PNG |
| `exceptions_streamlit(page)` | textes des `stException` |
| `recette(url, attendre, viewports, sortie, tolerer_console)` | liste d'échecs, vide = succès |
| `pdf(html_ou_url, chemin)` | PDF (Playwright, repli Chrome/Edge) |
| `verrou_profil()` | message ou `None` |

CLI : `setup URL` · `recette URL [--attendre SEL] [--sortie DIR]` · `capture URL CHEMIN [--viewport large]` · `pdf SRC CHEMIN` · `verrou`. Sortie 0 ok, 1 échec, 3 login expiré. Viewports : mobile 390x844, desktop 1440x900, large 1850x820.

## Qui lance, qui regarde

Lancer via le sous-agent `socle:photographe` (il produit les fichiers, ne juge rien). **L'orchestrateur ouvre et regarde les images** : un code retour 0 ne prouve rien sur des pixels.

## Interdits

- `storage_state` : le SSO vit dans le profil.
- `connect_over_cdp` : jamais sur le Chrome de Yann.
- Le MCP Playwright pour une preuve : il ouvre son propre profil, hors socle.
- Un profil persistant ailleurs que `PROFIL` (le garde S-20 le signale).
- Saisir un identifiant ou un mot de passe.

## Fermer toujours

`ouvrir` ferme dans un `finally`. Un navigateur resté ouvert verrouille le profil pour toutes les sessions : en cas de doute, `verrou`.
