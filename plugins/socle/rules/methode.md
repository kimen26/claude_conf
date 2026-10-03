# La méthode du socle

Norme de travail de tout projet qui active le plugin `socle`. Elle prescrit : elle doit dire vrai
en permanence.

## Vocabulaire (un mot, un sens)

- **Tâche** : la fiche de travail, un seul gabarit. Dans un projet adopté : un fichier Backlog.md,
  `backlog/tasks/task-NNN - titre.md`.
- **HO** : la même tâche, même gabarit, hors projet (plugin, machine) : un fichier
  `%LOCALAPPDATA%\socle\taches\AAAA-MM-JJ_<nom>.md`, sans Backlog ni statut à poser.
- **Porte** : contrôle mécanique vert ou rouge (`python outils/portes.py`, exit 0 ou 1).
- **Preuve** : artefact regardé (capture, log, diff). Un exit 0 n'est pas une preuve de rendu.
- **Verdict** : décision humaine, Valide ou Rejete, avec motif écrit.
- **Lane** : verrou de périmètre de fichiers, un couloir d'exécution où un seul dev travaille à la fois.
- **Officiers** (Sonnet) jugent : `executant`, `banc`, `relecteur`.
- **Soldats** (Haiku) n'inventent rien, ne jugent pas : `fouilleur`, `photographe`. Un officier ne passe en Haiku qu'exceptionnellement, pour une tâche purement mécanique, et on le dit alors ainsi.

## Deux voies

- **Voie courte** : le diff se décrit en une phrase. L'orchestrateur le fait, le prouve (temps 4) et le
  commite, sans fiche ni agent.
- **Voie complète** : tout le reste, la marche ci-dessous.

## La marche en huit temps

1. **Reconnaissance et plan** : l'orchestrateur lit TODO, LESSONS et DECISIONS (`fouilleur` si la
   mémoire est grosse), puis écrit la tâche : critères vérifiables, périmètre, pièges connus. Le plan
   porte l'élégance (« existe-t-il plus simple ? », pas pour un fix trivial) ; `executant` écrit son
   `Implementation Plan` avant de coder, l'orchestrateur le relit.
2. **Exécution** : `executant`, changement minimal, bug corrigé en autonomie, Edit uniquement.
3. **DoD de l'exécutant** : tests, portes, `python -m py_compile` / `node --check` des fichiers touchés.
4. **Preuve rejouée par l'orchestrateur**, toujours : suite complète, portes, `py_compile` /
   `node --check`, et avant tout commit `git diff --cached --name-only` comparé à la liste attendue
   (sinon stop). Si un écran change : `banc` fait produire puis REGARDE les captures (recette).
5. **Relecture** : `relecteur`, qui n'a pas écrit le code, vérifie la correction.
6. **Verdict** : Yann tranche.
7. **Mise en service** : `/socle:livrer` (commit par chemins, déploiement, smoke).
8. **Capitalisation** : leçons L-NNN, décisions D-NNN, CHANGELOG, TODO.

Un temps échoue deux fois pour la même raison : on arrête et on replanifie (retour au temps 1).

## Statuts et transitions

`Todo → Ready → Dev → Recette → Relecture → Valide → Livre`, et `Rejete`.

| Transition | Propriétaire | Preuve exigée |
|---|---|---|
| Todo → Ready | orchestrateur | dépendances `Livre`, critères vérifiables |
| Ready → Dev | `executant` | `Implementation Plan` écrit et relu |
| Dev → Recette | `executant`, seulement si la tâche touche un écran | DoD cochée ; l'orchestrateur rejoue la preuve (temps 4) |
| Dev → Relecture | `executant`, tâche sans écran | portes vertes ; preuve rejouée par l'orchestrateur |
| Recette → Relecture | orchestrateur, sur le rendu de `banc` | seulement si un écran est touché : captures produites par `photographe` ET regardées ; sinon `Recette` est sautée |
| Relecture → Valide | orchestrateur, sur le rendu de `relecteur` + verdict de Yann | `## Relecture` sans BLOQUANT, preuve rejouée par l'orchestrateur, verdict écrit |
| Valide → Livre | `/socle:livrer` | commit, déploiement, smoke verts, ligne de CHANGELOG |
| tout → Rejete | orchestrateur | motif écrit dans `## Verdict` ; retour à `Dev` si reprise |
| clôture | orchestrateur | L/D versées, TODO à jour, fichier de la tâche déplacé de `backlog/tasks/` vers `backlog/completed/` (voir `/socle:tache`, section Clôturer), jamais réécrit |

C'est la seule table des transitions : `/socle:tache` y renvoie, il ne la recopie pas.

## Règles qui tiennent l'ensemble

- **L'orchestrateur : le cerveau d'abord, les mains si c'est moins cher.** Il cadre, relit, tranche,
  commite, déploie. Il code lui-même si le diff se décrit en une phrase, pour finir un Edit refusé à un
  agent, ou pour un correctif après un faux positif réel, et le dit dans son compte rendu. Sinon il
  délègue à `executant`.
- **Séquentiel par défaut, parallèle par exception** : deux tâches `Dev` en parallèle seulement si
  leurs périmètres de fichiers sont disjoints ET sans déplacement ni renommage (réservés à une seule
  tâche, lancée en premier ; `/socle:tache`, conflits). Sinon on enchaîne (`dependencies`) ou
  `isolation: worktree` (réserve : la base est la branche distante par défaut). 1 dev par lane.
- **Règle des deux usages** : pas de nouvel agent, skill ou hook tant que la procédure n'a pas
  servi deux fois à la main. Même règle pour le code : on extrait au 2e usage identique, jamais
  d'abstraction pour un usage hypothétique (règle `conception`).
- **Contre-avis** : une proposition de Yann se teste avant de s'exécuter (objection et alternative,
  ou « Rien à opposer »), sans complaisance ni contradiction gratuite (règle `contradicteur`).
- **Seuils de délégation** : 3 recherches ou plus, ou une sortie de plus de 100 lignes. Recherche
  vers `fouilleur`, preuve d'écran vers `photographe`. Sous le seuil, on le fait soi-même. Le rejeu
  des preuves n'est jamais délégué.
- **Un soldat** (toujours lancé avec `model: "haiku"`) ne juge, ne code, ne commite, ne déploie pas ;
  son rapport est un fait brut, vérifié avant usage ; il ne lance personne.
- **Convention plutôt que config** : trois commandes de projet, `python outils/portes.py`,
  `python outils/smoke.py`, `python outils/deployer.py`, plus `pytest` s'il y a `tests/`.
- **Outils de la machine** (navigateur, MCP, consoles) : doctrine dans `rules/outils-machine.md`.
- **Vérifier avant « fait »** : jamais de tâche finie sans preuve ; un livrable visuel s'ouvre.
- **Une correction humaine non gravée sera refaite** : la leçon est versée avant de clore.
- **Git** : commits par chemins listés, jamais `add -A`, `add .`, `commit -a`, et seulement le
  travail de la tâche en cours.
