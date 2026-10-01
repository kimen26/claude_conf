---
name: tache
description: "Créer, suivre, trancher et clôturer une tâche Backlog.md du projet, et détecter les conflits de périmètre entre tâches avant de lancer des exécutants en parallèle. À utiliser pour créer une tâche (numéro pris par l'outil), la faire changer de statut avec la preuve exigée, écrire un verdict Valide ou Rejete, clôturer (leçons et décisions versées), lister ce qui est Ready."
argument-hint: "creer|statut|verdict|cloturer|ready|conflits ..."
---

# /socle:tache : le cycle de vie d'une tâche en commandes

Une tâche = un fichier `backlog/tasks/task-NNN - titre.md`. La marche et le vocabulaire sont dans
`rules/methode.md` : ils ne sont pas recopiés ici. Ce skill dit **comment** manipuler la tâche et
**quelle preuve** exiger à chaque transition.

## Si `backlog` n'est pas installé

Vérifier : `backlog --version`. Absent : le dire à Yann (`npm i -g backlog.md`, une fois par PC,
sous proxy poser `NODE_EXTRA_CA_CERTS`) et continuer à la main, sans bloquer :
- numéro = max des `task-NNN` de `backlog/tasks/` et `backlog/completed/` plus 1, relu juste avant
  d'écrire (compteur partagé entre sessions) ;
- statut = champ `status:` du frontmatter, édité directement ;
- pas de `backlog board export` : tenir `backlog/board.md` à la main n'est pas demandé, ne pas l'inventer.
`backlog init` est à lancer une fois par projet (le gabarit `gabarits/backlog/config.yml` du plugin
fournit les statuts).

## Commandes

| Geste | Commande |
|---|---|
| Créer | `backlog task create "titre" --dep task-085 --labels ecran --assignee executant` : le **numéro vient de l'outil**, jamais de la main |
| Statut | `backlog task edit task-086 --status Dev` |
| Lister le prêt | `backlog task list --status Ready` |
| Tableau | `backlog board export backlog/board.md --force` (sans argument l'outil écrit `Backlog.md` à la racine) |
| Voir | `backlog task 86 --plain` |

Après `create`, remplir les sections du gabarit ci-dessous (`gabarits/tache.md` du plugin en donne
un exemple rempli). Frontmatter : `id`, `title`, `status`, `assignee`, `labels`, `priority`,
`dependencies`, `created_date`.

## Gabarit de tâche

```markdown
---
id: task-NNN
title: <verbe + objet>
status: Todo
assignee: []
labels: []
priority: medium
dependencies: []
created_date: 'AAAA-MM-JJ'
---

## Description
Le problème vu de l'utilisateur, pourquoi maintenant, ce qui est hors sujet.

## Acceptance Criteria
- [ ] #1 critère vérifiable par une commande ou une capture
- [ ] #2 ...

## Périmètre
- Autorisés : <fichiers, un par ligne>
- Interdits : <fichiers à ne pas toucher>
- Lane : <nom du couloir>

## Pièges connus
- L-NNN / D-NNN pertinents, une ligne chacun

## Implementation Plan
(écrit par l'exécutant AVANT de coder)

## Implementation Notes
(écrit par l'exécutant en rendant)

## Verdict
(décision humaine : Valide ou Rejete, date, motif)
```

## Preuve exigée à chaque transition

| Transition | Qui la pose | Preuve à voir avant de la poser |
|---|---|---|
| Todo → Ready | orchestrateur | `dependencies` toutes en `Livre`, critères vérifiables, périmètre rempli |
| Ready → Dev | `executant` | `## Implementation Plan` écrit ET relu par l'orchestrateur (plan, élégance) |
| Dev → Recette | `executant` | `python outils/portes.py` exit 0 prouvé par `greffier`, critères cochés avec preuve |
| Recette → Relecture | `banc` | captures produites par `photographe` ET regardées (obligatoire si écran touché ; sinon saut documenté) |
| Relecture → Valide | `relecteur` puis Yann | `## Relecture` sans BLOQUANT, orchestrateur a rejoué les portes, verdict humain écrit |
| Valide → Livre | `/socle:livrer` | commit, déploiement, smoke verts |
| tout → Rejete | orchestrateur | motif écrit dans `## Verdict` ; retour à `Dev` si reprise |

Un temps échoue deux fois pour la même raison : on s'arrête et on replanifie (retour au plan).

## Verdict

Poser le statut, puis ajouter dans `## Verdict` un bloc daté et jamais réécrit :
`AAAA-MM-JJ · Valide | Rejete · motif en une phrase`. Un verdict précédent reste en place.
Le motif est obligatoire. Pas de cadratin.

## Clôturer

Après `/socle:livrer` (statut `Livre`) :
1. Chaque correction humaine reçue pendant la tâche : bloc `L-NNN` dans `memory/LESSONS.md`
   (symptôme, cause, règle). Chaque arbitrage non évident : `D-NNN` dans `memory/DECISIONS.md`.
   Le numéro se prend en **relisant le fichier au moment d'écrire**.
2. `memory/TODO.md` : lignes concernées en `[x]`.
3. `backlog board export backlog/board.md --force`. La tâche est archivée par l'outil et n'est jamais réécrite ensuite.

## Conflits de périmètre

Avant de lancer deux `executant` en parallèle : lire `## Périmètre` des tâches `Dev` (et de celles
qu'on s'apprête à y passer), lister les fichiers autorisés de chacune, intersecter. Une
intersection non vide, ou deux tâches de même **lane**, veut dire : on ne parallélise pas, on
enchaîne (`dependencies`) ou on redécoupe. Règle : **1 dev par lane**. Un fichier partagé ne
part que dans une seule tâche. Pour plus de trois tâches, déléguer l'extraction des listes à
`socle:fouilleur`.
