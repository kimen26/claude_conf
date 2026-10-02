# Mémoire projet : la convention

Un projet qui dure oublie. Pas le code : le code se relit. Ce qui s'oublie, c'est **pourquoi**
on a tranché comme ça, **quelle erreur** on a déjà payée, et **où on en était** avant la coupure.

D'où cinq fichiers dans `memory/`, un par question. Choisir où écrire ne doit demander aucune
réflexion : on se demande à quelle question la chose répond, et le fichier tombe tout seul.

| Fichier | Répond à | On y écrit quand | Numérotation |
|---|---|---|---|
| `memory/DECISIONS.md` | **pourquoi** c'est comme ça | à chaque arbitrage non évident | `D-NNN` |
| `memory/TODO.md` | **quoi ensuite** | ouverture / fermeture de chantier | aucune |
| `memory/LESSONS.md` | **quelle erreur ne pas refaire** | après CHAQUE correction humaine, chaque piège payé | `L-NNN` |
| `memory/MEMORY.md` | **où on en est** | fin de session, fin de chantier | aucune |
| `memory/CHANGELOG.md` | **ce qui est sorti** | à chaque livraison, une ligne ; à la release, regroupé sous `vX.Y` | `vX.Y` |

Le socle stable (vision produit, profil utilisateur, contexte métier) vit aussi dans `memory/`
mais hors de ce quintette : il ne se met pas à jour au fil de l'eau, il se réécrit rarement.

## Les règles qui tiennent l'ensemble

**La convention du projet prime.** Un repo qui a déjà sa mémoire (`memoire/decisions.md`,
`docs/adr/`, un `AGENTS.md` qui dit où écrire…) garde la sienne : on n'y crée jamais un
second système. Le quintette ci-dessus s'applique aux projets neufs et à ceux qui n'ont rien.

**Une correction humaine non gravée sera refaite.** C'est la seule règle vraiment non
négociable. Graver AVANT de clore la session, jamais « je le noterai plus tard » : plus tard,
le contexte est parti. Une leçon coûte deux lignes à écrire et une demi-journée à réapprendre.

**`D-NNN` et `L-NNN` sont des compteurs partagés.** Comme l'index git, comme un numéro de
version : plusieurs sessions écrivent dans le même fichier. Le numéro se prend en **relisant le
fichier au moment d'écrire**, jamais au moment de décider. Sinon deux sessions gravent le même
numéro le même jour et « L-053 » désigne deux choses. Un script qui vérifie l'unicité vaut mieux
qu'une promesse.

**Une archive ne se réécrit pas.** `DECISIONS`, `LESSONS`, `MEMORY` racontent le passé : ils
gardent leur syntaxe et leur vocabulaire d'époque. Les corriger pour qu'ils « collent » à la
réalité d'aujourd'hui, c'est réécrire l'histoire du projet et perdre l'information la plus
utile : ce qu'on croyait à ce moment-là. Seuls les documents **normatifs** (ceux qui prescrivent)
doivent dire vrai en permanence.

**Les tâches ne sont pas de la mémoire.** Une tâche est jetable : elle décrit un travail à
faire, elle meurt une fois fait. Elle vit dans `backlog/tasks/`, et descend dans
`backlog/completed/` une fois livrée. Sinon les tâches mortes noient l'état courant : le dossier
de travail doit se lire d'un coup d'œil et ne montrer que les chantiers vivants.

**Lane ≠ epic.** Lane : verrou de périmètre de fichiers, un couloir d'exécution où un seul dev
travaille à la fois. Un *epic* est un résultat métier qui se découpe.
Un chantier de 3+ tâches avec un critère de fin métier mérite d'être annoncé comme tel, ses
tâches listées dessous. En dessous de 3, une lane suffit, sinon on réinvente Jira en markdown.

**Le CHANGELOG n'est pas un journal de commits.** `/socle:livrer` y ajoute une ligne par
livraison ; la release les regroupe sous `vX.Y`, en capacités livrées. Une ligne = ce que
l'utilisateur voit de plus, écrit de son point de vue (« les photos partent dans la bonne
fiche », pas « refactor du module de ciblage »).

## Ce qui ne va PAS dans la mémoire

- Ce que le code dit déjà (structure, signatures, dépendances) : ça se relit.
- Ce que git dit déjà (qui, quand, quel diff) : l'historique est là pour ça.
- Le détail d'exécution d'un chantier : il vit dans sa tâche, et meurt avec elle.
- Ce qui n'a d'intérêt que dans la conversation en cours.

En cas de doute : si la chose sera **fausse dans trois mois**, elle n'a rien à faire dans une
archive. Si elle sera **encore vraie et encore utile**, elle mérite ses deux lignes.
