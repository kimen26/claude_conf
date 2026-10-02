---
name: recette-ecran
description: "Recette d'un écran en une commande : lance python outils/smoke.py via le soldat photographe, liste les captures à ouvrir et exige qu'elles soient regardées. À utiliser dès que l'utilisateur demande une recette, « capture l'écran », « montre-moi la page », ou veut voir un écran avant de le déclarer réparé. Ne sert pas à écrire de l'outillage Playwright (skill preuve-navigateur)."
argument-hint: "<page ou scénario>"
---

# /socle:recette-ecran : voir avant de dire « réparé »

Un code retour 0 ne prouve **rien** sur des pixels : un écran peut être cassé avec toutes les
portes vertes. Ce skill force le geste qui compte : produire les captures, puis **les ouvrir**.

## Déroulé

1. `python outils/smoke.py --help` pour connaître les scénarios et options du projet. Gabarit non
   rempli (il affiche « AUCUNE CAPTURE », exit 0) : le dire à Yann, pointer `SCENARIOS` dans
   `outils/smoke.py` (gabarit `gabarits/outils/smoke.py` du plugin), s'arrêter : rien n'est prouvé.
2. Lancer `socle:photographe` (Agent avec `model: "haiku"`) avec le scénario, la largeur et le
   dossier de sortie. Il rend : COMMANDE, CAPTURES (chemins), MESURES (s'il y en a), EXCEPTIONS.
   Il ne regarde rien.
3. **Ouvrir chaque capture avec Read** et la décrire en une phrase. Qui regarde : l'orchestrateur,
   ou `banc` (temps 6 de la marche). Jamais un soldat Haiku.
4. Chercher : texte qui chevauche ou touche un autre, texte rogné, élément hors écran, bouton
   recouvert, contraste, accent manquant, cadratin affiché.
5. Rendre par critère : **tenu** / **non tenu** / **non prouvé**, avec le chemin de la capture.

## Règles

- Ne jamais déclarer un écran réparé sans avoir ouvert **toutes** les captures demandées (toutes
  les largeurs du scénario). Une capture non ouverte est « non prouvé ».
- Un nombre de défauts à 0 ne dit rien ; un nombre élevé peut être du rognage voulu : lire l'image
  tranche.
- Les mesures éventuelles complètent le regard, elles ne le remplacent pas.
- Un cas difficile nouveau (libellé long, réponse longue, état vide) s'ajoute au scénario de
  `outils/smoke.py` du projet, pas à un script jetable hors dépôt.
- Un seul navigateur à la fois sur le profil partagé de la machine : si le verrou est pris, attendre,
  c'est attendu.
