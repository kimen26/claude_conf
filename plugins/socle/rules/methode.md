# La méthode du socle

Norme de travail de tout projet qui active le plugin `socle`. Elle prescrit : elle doit dire vrai
en permanence.

## Vocabulaire (un mot, un sens)

- **Tâche** : un fichier Backlog.md du projet, `backlog/tasks/task-NNN - titre.md`.
- **HO** : une tâche machine hors projet, un fichier de `%LOCALAPPDATA%\socle\taches\`, hors Backlog.
- **Porte** : contrôle mécanique vert ou rouge (`python outils/portes.py`, exit 0 ou 1).
- **Preuve** : artefact regardé (capture, log, diff). Un exit 0 n'est pas une preuve de rendu.
- **Verdict** : décision humaine, Valide ou Rejete, avec motif écrit.
- **Lane** : verrou de périmètre de fichiers, un couloir d'exécution où un seul dev travaille à la fois.
- **Officiers** (Sonnet) jugent : `eclaireur`, `executant`, `banc`, `relecteur`.
- **Soldats** (Haiku) n'inventent rien, ne jugent pas : `fouilleur`, `greffier`, `photographe`.

## La marche en dix temps

1. **Reconnaissance** : `eclaireur` lit la mémoire, cite les L-NNN et D-NNN utiles.
2. **Plan** : la tâche est écrite avec critères vérifiables, périmètre, pièges connus.
3. **Élégance** : « existe-t-il plus simple ? » (pas pour un fix trivial). `executant` écrit son
   `Implementation Plan` avant de coder, l'orchestrateur le relit.
4. **Exécution** : `executant`, changement minimal, bug corrigé en autonomie.
5. **DoD mécanique** : portes vertes APRÈS la dernière écriture, prouvées par `greffier`.
6. **Recette** : `banc` fait produire puis REGARDE les captures (obligatoire si un écran change).
7. **Relecture** : `relecteur`, qui n'a pas écrit le code, cherche le bug.
8. **Verdict** : l'orchestrateur rejoue les portes et ouvre les captures, Yann tranche.
9. **Mise en service** : `/socle:livrer` (commit par chemins, déploiement, smoke).
10. **Capitalisation** : leçons L-NNN, décisions D-NNN, CHANGELOG, TODO.

Un temps échoue deux fois pour la même raison : on arrête et on replanifie (retour au temps 2).

## Statuts et transitions

`Todo → Ready → Dev → Recette → Relecture → Valide → Livre`, et `Rejete`.

| Transition | Propriétaire | Preuve exigée |
|---|---|---|
| Todo → Ready | orchestrateur | dépendances `Livre`, critères vérifiables |
| Ready → Dev | `executant` | `Implementation Plan` écrit et relu |
| Dev → Recette | `executant` | portes vertes prouvées par `greffier`, DoD cochée |
| Recette → Relecture | `banc` | captures produites par `photographe` ET regardées (obligatoire si un écran est touché ; sinon saut documenté) |
| Relecture → Valide | `relecteur` + Yann | `## Relecture` sans BLOQUANT, portes rejouées par l'orchestrateur, verdict écrit |
| Valide → Livre | `/socle:livrer` | commit, déploiement, smoke verts, ligne de CHANGELOG |
| tout → Rejete | orchestrateur | motif écrit dans `## Verdict` ; retour à `Dev` si reprise |
| clôture | orchestrateur | L/D versées, TODO à jour, fichier de la tâche déplacé de `backlog/tasks/` vers `backlog/completed/` (voir `/socle:tache`, section Clôturer), jamais réécrit |

C'est la seule table des transitions : `/socle:tache` y renvoie, il ne la recopie pas.

## Règles qui tiennent l'ensemble

- **L'orchestrateur est le cerveau, pas les mains** : il cadre la tâche, relit, tranche, commite, déploie. Il
  ne code pas. Exceptions : une commande de lecture, une correction d'une ligne qu'il vient de
  relire, l'écriture de `memory/` et des tâches.
- **1 dev par lane** : deux tâches `Dev` en parallèle seulement si leurs périmètres de fichiers
  sont disjoints (`/socle:tache`, conflits). Sinon on enchaîne via `dependencies`.
- **Règle des deux usages** : pas de nouvel agent, skill ou hook tant que la procédure n'a pas
  servi deux fois à la main. Même règle pour le code : on extrait au 2e usage identique, jamais
  d'abstraction pour un usage hypothétique (règle `conception`).
- **Contre-avis** : une proposition de Yann se teste avant de s'exécuter (objection et alternative,
  ou « Rien à opposer »), sans complaisance ni contradiction gratuite (règle `contradicteur`).
- **Seuils de délégation** : 3 recherches ou plus, ou une sortie de plus de 100 lignes. Recherche
  vers `fouilleur`, rejeu de commandes vers `greffier`, preuve d'écran vers `photographe`. Sous le
  seuil, on le fait soi-même.
- **Un soldat** (toujours lancé avec `model: "haiku"`) ne juge, ne code, ne commite, ne déploie pas ;
  son rapport est un fait brut, vérifié avant usage ; il ne lance personne.
- **Convention plutôt que config** : trois commandes de projet, `python outils/portes.py`,
  `python outils/smoke.py`, `python outils/deployer.py`, plus `pytest` s'il y a `tests/`.
- **Outils de la machine** (navigateur, MCP, consoles) : doctrine dans `rules/outils-machine.md`.
- **Vérifier avant « fait »** : jamais de tâche finie sans preuve ; un livrable visuel s'ouvre.
- **Une correction humaine non gravée sera refaite** : la leçon est versée avant de clore.
- **Git** : commits par chemins listés, jamais `add -A`, `add .`, `commit -a`, et seulement le
  travail de la tâche en cours.
