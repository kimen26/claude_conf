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
- `backlog/board.md` : le garde S-50 l'exige dès qu'une tâche existe et le veut plus récent que les tâches.
  Sans l'outil, le réécrire à la main après chaque changement de statut : un tableau `id · titre · statut`,
  rien de plus (S-50 ne compare que les dates).
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

## Recette
(écrit par `banc` : par critère visuel, tenu, non tenu ou non prouvé, avec le chemin de la capture)

## Relecture
(écrit par `relecteur` : un constat par ligne, puis critère par critère, puis l'avis)

## Verdict
(décision humaine : Valide ou Rejete, date, motif)
```

## Preuve exigée à chaque transition

La table des transitions (propriétaire et preuve, `Rejete` compris) vit dans `rules/methode.md`,
section « Statuts et transitions » : elle n'est pas recopiée ici. Avant de poser un statut, lire sa
ligne et voir la preuve qu'elle exige. Une dépendance absente de `backlog/tasks/` se cherche dans
`backlog/completed/` : elle y est `Livre`.

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
3. Déplacer le fichier de la tâche de `backlog/tasks/` vers `backlog/completed/` (déplacement simple :
   `backlog task archive` et `backlog task complete` refusent le statut `Livre`, mesuré le 2026-10-02 avec
   la CLI 1.53 : `complete` n'accepte que `Rejete`). Puis `backlog board export backlog/board.md --force`
   (ou le `board.md` à la main, voir plus haut). La tâche n'est jamais réécrite ensuite.

## Conflits de périmètre

Avant de lancer deux `executant` en parallèle : lire `## Périmètre` des tâches `Dev` (et de celles
qu'on s'apprête à y passer), lister les fichiers autorisés de chacune, intersecter. Une
intersection non vide, ou deux tâches de même **lane**, veut dire : on ne parallélise pas, on
enchaîne (`dependencies`) ou on redécoupe. Règle : **1 dev par lane**. Un fichier partagé ne
part que dans une seule tâche. Pour plus de trois tâches, déléguer l'extraction des listes à
`socle:fouilleur`.
