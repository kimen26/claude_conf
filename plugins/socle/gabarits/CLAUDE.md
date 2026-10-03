# CLAUDE.md

<!-- Copier à la racine du projet. Ce fichier dit CE QU'EST le projet, pas COMMENT on travaille :
     la méthode vit dans le plugin socle (rules/methode.md ; le digest en est injecté au démarrage d'un projet adopté). -->

## Mission

- **Problème** : <qui souffre de quoi, en une phrase>
- **Livrable** : <ce que le projet produit, et ce qu'il ne produit pas>
- **Critère de succès** : <comment on saura que c'est réussi, vérifiable>

## Méthode

Elle vient du plugin `socle` : deux voies et marche en huit temps, tâches Backlog.md, officiers et soldats,
mémoire en quintette `memory/`. Ne rien en recopier ici. Chemin : Glob `**/socle/*/rules/methode.md` sous `~/.claude/plugins/cache`.

Les trois commandes conventionnelles du projet (à implémenter dans `outils/`) :
- `python outils/portes.py` : toutes les portes mécaniques, exit 0 ou 1
- `python outils/smoke.py` : preuve d'écran (captures PNG dans `recette/<date>/`)
- `python outils/deployer.py` : mise en service de HEAD

## Routage : le projet touche à… alors…

| Le travail touche à… | Utiliser |
|---|---|
| créer, suivre, clore une tâche | skill `/socle:tache` |
| mettre en service du travail validé | skill `/socle:livrer` |
| voir un écran avant de le déclarer réparé | skill `/socle:recette-ecran` |
| <domaine du projet 1> | <skill, outil ou fichier de référence> |
| <domaine du projet 2> | <skill, outil ou fichier de référence> |

## Invariants du projet

<!-- Uniquement ce qui est propre à CE projet et qui a déjà coûté une panne. 10 lignes au plus. -->
- <invariant 1 : environnement, rôle, base, périmètre de données>
- <invariant 2 : ce qu'on ne touche jamais>
- Secrets uniquement dans `.env` git-ignoré. Jamais de valeur dans un fichier suivi.

## Mémoire

`memory/` : DECISIONS, TODO, LESSONS, MEMORY, CHANGELOG. Lire TODO et LESSONS au démarrage.
Si le projet a déjà sa propre mémoire, elle prime : ne pas créer un second système.
