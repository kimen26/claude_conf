---
id: task-042
title: Afficher le nombre de résultats sous la barre de recherche
status: Dev
assignee:
  - executant
labels:
  - ecran
  - recherche
priority: medium
dependencies:
  - task-038
created_date: '2026-10-01'
---

## Description

Aujourd'hui, après une recherche, l'utilisateur ne sait pas si la liste est complète ou tronquée.
On affiche sous la barre « 24 résultats » (ou « 1 résultat », « Aucun résultat ») pour qu'il sache
s'il doit affiner. Hors sujet : pagination, tri, export.

## Acceptance Criteria

- [ ] #1 Le compteur s'affiche sous la barre avec le bon accord (0, 1, plusieurs)
- [ ] #2 Un libellé de 300 caractères dans la barre ne déplace pas le compteur (capture à 1440 px)
- [ ] #3 `python outils/portes.py` exit 0 et `pytest -q` sans rouge
- [ ] #4 Un test couvre les trois cas d'accord (0, 1, N)

## Périmètre

- Autorisés : `app/vues/recherche.py`, `app/core/ui.py`, `tests/test_compteur.py`
- Interdits : `app/core/config.py`, tout fichier sous `outils/`
- Lane : recherche

## Pièges connus

- L-031 : une clé de widget ne dépend jamais d'un état (le clic serait perdu entre deux rendus)
- D-012 : tout le style vit dans `core/ui.py`, jamais dans une vue

## Implementation Plan

1. Ajouter `libelle_compteur(n)` pur dans `core/ui.py` (accord 0 / 1 / N), testé seul.
2. L'appeler dans `vues/recherche.py` sous la barre, dans un conteneur à hauteur fixe.
3. Test des trois cas, puis smoke à 1440 px avec un libellé de 300 caractères.

## Implementation Notes

(rempli par l'exécutant en rendant : fichiers touchés avec +x -y, écarts assumés, preuves)

## Verdict

(rempli après la relecture : `AAAA-MM-JJ · Valide | Rejete · motif`)
