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
python socle_projet.py init [chemin]
```

1. `git init` si absent.
2. Copie des gabarits **sans jamais écraser** un fichier existant : `CLAUDE.md`, `.gitignore` (avec `secrets*.ps1`), `.env.example` (noms seuls), `memory/*.md`, `outils/portes.py`, `outils/smoke.py`, `outils/deployer.py`, `backlog/config.yml`, et le shim `outils/preuve_navigateur.py` (5 lignes, voir skill `preuve-navigateur`).
3. `backlog init` si la commande existe, sinon dire `npm i -g backlog.md` (une fois par PC) et créer `backlog/tasks/` à la main.
4. Premier commit `chore: socle projet`, **par chemins listés** (jamais `git add -A`). `--sans-commit` pour s'en passer.
5. Remplir ensuite la mission, le routage et les invariants du `CLAUDE.md` (viser < 100 lignes dès le départ).
6. `garde_socle.py --session` doit rendre vide.

## Mode `remise-au-pas` (projet existant)

```
python socle_projet.py remise-au-pas [chemin] [--radical]        # simulation, ne modifie rien
python socle_projet.py remise-au-pas [chemin] [--radical] --oui  # applique, après accord de Yann
```

Lance d'abord `secrets.py inventaire <projet>` (skill `/socle:secrets`, noms seulement), puis `garde_socle.py --complet` (via `--json`), et traite les écarts dans l'ordre **S-30 à S-35** (secrets, accès Snowflake, snow isolé) → **S-10** (.mcp.json) → **S-20** (navigateur hors socle) → **S-01/02/03** (CLAUDE.md, memory/, .gitignore) → **S-50/60** (backlog, portes) → **S-40** (doublons plugin, settings mort) → **S-70** (venv non relocalisé) et **S-71** (`.py` sans `requirements*.txt` ni `pyproject.toml`, hors `outils/`) : ces deux-là ne sortent qu'en `--complet`/`--json`, pas en `--session`.

- **Chaque geste est confirmé par Yann** : présenter le plan de la simulation, attendre l'accord, relancer avec `--oui`. Jamais supprimer sans confirmation explicite.
- Le script complète ce qui manque (sans écraser) ; secrets, `.mcp.json` et le reste sont signalés « à traiter à la main » avec le correctif du garde.
- **`--radical`** : tout ce que S-40 et S-20 signalent est **déplacé, jamais supprimé**, dans `_a_supprimer/<AAAA-MM-JJ>/` en conservant l'arborescence relative, avec un `MANIFESTE.md` (fichier, raison, remplacé par quoi dans le plugin). Yann supprime le dossier lui-même.
- Un déplacement isolé : `python socle_projet.py deplacer <fichiers...> --raison "..." [--remplace-par "..."]`.

## Mode `venv` (recréer, jamais copier)

```
python socle_projet.py venv [chemin]        # simulation : affiche ce qui serait fait
python socle_projet.py venv [chemin] --oui  # applique
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
