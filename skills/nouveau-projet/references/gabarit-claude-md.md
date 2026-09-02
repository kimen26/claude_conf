# Gabarit CLAUDE.md racine (< 100 lignes, à trous)

```markdown
# <NomProjet> — <mission en une phrase>

<2-3 phrases max : quoi, pour qui, où on en est.>

## ACTION OBLIGATOIRE — avant toute réponse

| Mots dans la demande | Pôle | Charger |
|---|---|---|
| <mots-clés métier A> | <PÔLE A> | <skill ou fichier> |
| <mots-clés métier B> | <PÔLE B> | <skill ou fichier> |
| dump · idée brute | INBOX | déposer dans inbox/, demander en texte |

Annoncer avant d'agir : « Mode [X] — je charge [Y] puis j'agis. »

## Invariants (non négociables)

1. <invariant métier n°1 — le plus important du projet>
2. Questions en TEXTE dans la réponse, jamais de formulaire.
3. <…>

## Workflow

Plan → TodoWrite → Exécution → Vérification → Commit → memory/ gravé

## Portes de vérification

| Commande | Quand |
|---|---|
| <check syntaxe/lint> | tout changement de code |
| <check métier> | <déclencheur> |

## Fichiers transversaux

| Fichier | Rôle |
|---|---|
| memory/MEMORY.md | état courant |
| memory/TODO.md | file d'attente (lanes) |
| memory/DECISIONS.md | arbitrages datés D-NNN |
| memory/LESSONS.md | leçons gravées L-NNN |
```

**Règles de croissance** : chaque nouvelle règle arrive AVEC sa porte de vérification.
Quand la racine dépasse ~150 lignes, extraire le détail vers un fichier routé.
