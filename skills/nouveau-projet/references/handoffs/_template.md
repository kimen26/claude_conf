---
id: HO-NNN
titre: <verbe + objet, résultat observable>
statut: brouillon          # brouillon | pret | en_cours | fait | abandonne
ouvert: AAAA-MM-JJ
fichiers:                  # ownership EXHAUSTIF — deux briefs actifs ne partagent jamais un fichier
  - src/<module>.py
  - tests/test_<module>.py
---

# HO-NNN — <titre>

## Objectif
<Une phrase. Ce qu'on observe quand c'est fait.>

## Contexte utile
<Pointeurs : décision D-NNN, leçon L-NNN, fichier à lire d'abord. Pas de prose.>

## Portes de vérification
| Commande | Attendu |
|---|---|
| `<lint / tests>` | 0 erreur |
| `python recette-visuelle.py <url> --wait "<sel>"` | exit 0 + captures ouvertes |

## Hors périmètre
<Ce qu'on ne touche PAS, même si « ça irait avec ». Transverses gelés.>

## Rapport d'exécution (rempli par l'exécutant)
- Commit(s) :
- Sortie des portes (collée, pas résumée) :
- Doutes / questions remontés au cerveau :
