---
name: nouveau-projet
description: "À utiliser pour démarrer un projet neuf (init) ou remettre au pas un projet existant (remise-au-pas) selon le socle de Yann : CLAUDE.md court, quintette memory/, portes, backlog, preuve navigateur."
---

# Nouveau projet : le socle

Les agents, skills, règles et hooks viennent du **plugin socle**. Le projet ne contient que ses données : `CLAUDE.md`, `memory/`, `outils/`, `backlog/`. On n'installe **aucun** agent, skill ni hook dans le projet.

## Les 4 principes

1. **Une règle que ne vérifie aucune commande n'est pas une règle** : chaque invariant a sa porte (`outils/portes.py`).
2. **CLAUDE.md racine < 100 lignes** : mission en une phrase, table de routage, invariants numérotés, table des portes. Le détail vit dans les fichiers routés.
3. **Une correction humaine non gravée sera refaite** : le quintette `memory/` (MEMORY, TODO, DECISIONS, LESSONS, CHANGELOG) n'est pas optionnel.
4. **Les archives racontent le passé** : DECISIONS, LESSONS, MEMORY gardent leur syntaxe d'époque.

Script : `${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py` (stdlib, Python 3.11).

## Mode `init` (projet neuf)

```
python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" init [chemin]
```

1. `git init` si absent.
2. Copie des gabarits **sans jamais écraser** un fichier existant : `CLAUDE.md`, `.gitignore` (avec `secrets*.ps1`), `.env.example` (noms seuls), `memory/*.md`, `outils/portes.py`, `outils/smoke.py`, `outils/deployer.py`, `backlog/config.yml`, et le shim `outils/preuve_navigateur.py` (5 lignes, voir skill `preuve-navigateur`).
3. `backlog init` si la commande existe, sinon dire `npm i -g backlog.md` (une fois par PC) et créer `backlog/tasks/` à la main.
4. Premier commit `chore: socle projet`, **par chemins listés** (jamais `git add -A`). `--sans-commit` pour s'en passer.
5. Remplir ensuite la mission, le routage et les invariants du `CLAUDE.md` (viser < 100 lignes dès le départ).
6. `python "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/garde_socle.py" --session [chemin]` doit rendre vide.

## Mode `remise-au-pas` (projet existant)

```
python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" remise-au-pas [chemin] [--radical]        # simulation, ne modifie rien
python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" remise-au-pas [chemin] [--radical] --oui  # applique, après accord de Yann
```

Lance d'abord `python "${CLAUDE_PLUGIN_ROOT}/skills/secrets/scripts/secrets.py" inventaire <projet>` (skill `/socle:secrets`, noms seulement), puis `python "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/garde_socle.py" --complet` (via `--json`), et traite les écarts dans l'ordre **S-30 à S-37** (secrets, accès Snowflake, snow isolé, `C:/tmp`, `a_poser.env`) → **S-10** (.mcp.json) → **S-20** (navigateur hors socle) → **S-01/02/03** (CLAUDE.md, memory/, .gitignore ; un `AGENTS.md` sans `CLAUDE.md` est la convention du projet, pas un écart S-01) → **S-50/60** (backlog, portes) → **S-40** (doublons plugin, settings mort) → **S-70** (venv non relocalisé) et **S-71** (`.py` sans `requirements*.txt` ni `pyproject.toml`, hors `outils/`) : ces deux-là ne sortent qu'en `--complet`/`--json`, pas en `--session` → **S-73** (BOM UTF-8 dans un JSON lu par Node : réécrire sans BOM) et **S-72** (règle machine de `rules/machine/` du plugin absente ou différente dans `~/.claude/rules/` : absente, recopiée au prochain démarrage ; différente, jamais écrasée, reporter la modification dans `rules/machine` ou supprimer la copie locale ; hors projet) → **S-74** (clone sans fetch depuis plus de 7 jours : `git fetch`, vérifier l'avance de la branche distante).

- **Chaque geste est confirmé par Yann** : présenter le plan de la simulation, attendre l'accord, relancer avec `--oui`. Jamais supprimer sans confirmation explicite.
- Le script complète ce qui manque (sans écraser) ; secrets, `.mcp.json` et le reste sont signalés « à traiter à la main » avec le correctif du garde.
- **`--radical`** : tout ce que S-40 et S-20 signalent est **déplacé, jamais supprimé**, dans `_a_supprimer/<AAAA-MM-JJ>/` en conservant l'arborescence relative, avec un `MANIFESTE.md` (fichier, raison, remplacé par quoi dans le plugin). Yann supprime le dossier lui-même.
- Un déplacement isolé : `python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" deplacer <fichiers...> --raison "..." [--remplace-par "..."] [--racine <projet>]` (`--racine` : projet dont `_a_supprimer/` reçoit les fichiers, `.` par défaut ; jamais de suppression, un `MANIFESTE.md` est écrit).

## Les 21 contrôles (`garde_socle.py`)

- **S-01** CLAUDE.md absent (sans AGENTS.md) ou trop long · **S-02** quintette `memory/` incomplet · **S-03** `.gitignore` sans motifs requis
- **S-10** `.mcp.json` avec npx latest · **S-20** Playwright hors `preuve_navigateur`
- **S-30** `.env` suivi, secret en clair · **S-31** `env` en clair dans settings · **S-32** Snowflake hors `connections.toml`
- **S-33** `.mcp.json` en clair, sans keyring · **S-34** connexion Snowflake non SSO · **S-35** `snow` hors `~/.local/bin`
- **S-36** référence à `C:/tmp` · **S-37** `a_poser.env` non traité
- **S-40** doublon du plugin, `mcpServers` mort · **S-50** backlog absent ou board périmé · **S-60** `outils/` portes, smoke, deployer absents
- **S-70** venv non relocalisé · **S-71** `.py` sans requirements · **S-72** règle machine absente ou différente · **S-73** BOM UTF-8 dans un JSON · **S-74** clone sans fetch depuis plus de 7 jours

## Mode `venv` (recréer, jamais copier)

```
python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" venv [chemin]        # simulation : affiche ce qui serait fait
python "${CLAUDE_PLUGIN_ROOT}/skills/nouveau-projet/scripts/socle_projet.py" venv [chemin] --oui  # applique
```

Convention : `requirements-dev.txt` à la racine (dépendances DIRECTES du poste local, versions épinglées ; un `requirements*.txt` existant est lu à défaut). Le déploiement Snowflake garde son `environment.yml` : ne pas mélanger. Sans aucun `requirements*.txt` la commande **refuse** et propose `pip freeze > requirements-dev.txt` (à relire). Avec `--oui` : freeze de l'ancien venv sauvegardé dans `%LOCALAPPDATA%\socle\backups\<date>\<projet>-freeze.txt`, `.venv` supprimé (seul geste destructif, d'où le flag), `python -m venv .venv` avec le Python courant, `pip install -r`, puis affichage de `sys.prefix` et du nombre de mentions de l'ancien chemin restantes dans `Scripts/`. `session_start` signale un `.venv` dont `VIRTUAL_ENV` n'est pas `<projet>\.venv`.

## Fin des deux modes

`python ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/garde_socle.py --session` doit rendre **vide**. Sinon, traiter le reste avant de dire « fait ».

## Ce qui n'entre pas au socle

- Pas de skills ni d'agents projet au départ : un savoir-faire devient skill après 2 usages.
- Pas de marche à agents avant plusieurs sessions parallèles (le plugin fournit la méthode).
- Pas de miroir AGENTS.md sauf usage bi-outil réel.
- Pas de `storage_state` ni de hooks copiés par projet.

## Outillage machine (une fois par PC)

`npm i -g backlog.md` · SSO navigateur : `python outils/preuve_navigateur.py setup <URL>` · plugin caveman, context7 selon la stack.
