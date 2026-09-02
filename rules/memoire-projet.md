# Mémoire projet — la convention

Un projet qui dure oublie. Pas le code — le code se relit. Ce qui s'oublie, c'est **pourquoi**
on a tranché comme ça, **quelle erreur** on a déjà payée, et **où on en était** avant la coupure.

D'où cinq fichiers dans `memory/`, un par question. Choisir où écrire ne doit demander aucune
réflexion : on se demande à quelle question la chose répond, et le fichier tombe tout seul.

| Fichier | Répond à | On y écrit quand | Numérotation |
|---|---|---|---|
| `memory/DECISIONS.md` | **pourquoi** c'est comme ça | à chaque arbitrage non évident | `D-NNN` |
| `memory/TODO.md` | **quoi ensuite** | ouverture / fermeture de chantier | — |
| `memory/LESSONS.md` | **quelle erreur ne pas refaire** | après CHAQUE correction humaine, chaque piège payé | `L-NNN` |
| `memory/MEMORY.md` | **où on en est** | fin de session, fin de chantier | — |
| `memory/CHANGELOG.md` | **ce qui est sorti** | à la release, en vidant les lanes terminées | `vX.Y` |

Le socle stable (vision produit, profil utilisateur, contexte métier) vit aussi dans `memory/`
mais hors de ce quintette : il ne se met pas à jour au fil de l'eau, il se réécrit rarement.

## Les règles qui tiennent l'ensemble

**Une correction humaine non gravée sera refaite.** C'est la seule règle vraiment non
négociable. Graver AVANT de clore la session, jamais « je le noterai plus tard » — plus tard,
le contexte est parti. Une leçon coûte deux lignes à écrire et une demi-journée à réapprendre.

**`D-NNN` et `L-NNN` sont des compteurs partagés.** Comme l'index git, comme un numéro de
version : plusieurs sessions écrivent dans le même fichier. Le numéro se prend en **relisant le
fichier au moment d'écrire**, jamais au moment de décider. Sinon deux sessions gravent le même
numéro le même jour et « L-053 » désigne deux choses. Un script qui vérifie l'unicité vaut mieux
qu'une promesse.

**Une archive ne se réécrit pas.** `DECISIONS`, `LESSONS`, `MEMORY` racontent le passé : ils
gardent leur syntaxe et leur vocabulaire d'époque. Les corriger pour qu'ils « collent » à la
réalité d'aujourd'hui, c'est réécrire l'histoire du projet et perdre l'information la plus
utile — ce qu'on croyait à ce moment-là. Seuls les documents **normatifs** (ceux qui prescrivent)
doivent dire vrai en permanence.

**Les briefs de chantier ne sont pas de la mémoire.** Un brief est jetable : il décrit un
travail à faire, il meurt une fois fait. Il vit dans `docs/`, et descend dans un
`archives/` une fois terminé. Sinon les briefs morts noient l'état courant — le dossier de
travail doit se lire d'un coup d'œil et ne montrer que les chantiers vivants.

**Lane ≠ epic.** Une *lane* est un couloir d'exécution : un verrou anti-collision quand
plusieurs sessions travaillent en parallèle. Un *epic* est un résultat métier qui se découpe.
Un chantier de 3+ briefs avec un critère de fin métier mérite d'être annoncé comme tel, ses
briefs listés dessous. En dessous de 3, une lane suffit — sinon on réinvente Jira en markdown.

**Le CHANGELOG est un exutoire, pas un journal.** On n'y écrit pas en continu : on y vide
`TODO.md` au moment d'une release, en capacités livrées. Une ligne = ce que l'utilisateur voit
de plus, écrit de son point de vue — « les photos partent dans la bonne fiche », pas « refactor
du module de ciblage ».

## Ce qui ne va PAS dans la mémoire

- Ce que le code dit déjà (structure, signatures, dépendances) — ça se relit.
- Ce que git dit déjà (qui, quand, quel diff) — l'historique est là pour ça.
- Le détail d'exécution d'un chantier — il vit dans son brief, et meurt avec lui.
- Ce qui n'a d'intérêt que dans la conversation en cours.

En cas de doute : si la chose sera **fausse dans trois mois**, elle n'a rien à faire dans une
archive. Si elle sera **encore vraie et encore utile**, elle mérite ses deux lignes.
