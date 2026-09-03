# Protocole handoffs — l'usine de dev (version générique)

> À dégainer quand plusieurs sessions travaillent en parallèle sur le même repo.
> Avant ça : inutile. Ceci est le squelette portable : chaque projet le décline
> dans `docs/handoffs/README.md` (protocole adapté), `_template.md` (brief) et un
> check anti-collision (`handoff-check.py` ou équivalent) — voir la liste en bas.

## Le principe

Un chat **cerveau** (conception, arbitrages, revue) + des sous-chats **exécutants**
lancés à la demande, chacun sur UN brief. Le cerveau ne code pas les chantiers ;
l'exécutant ne décide pas hors de son brief.

## Le brief (HO-NNN)

Un fichier `docs/handoffs/HO-NNN-<titre>.md` par chantier, avec au minimum :

1. **Objectif** — une phrase, résultat observable
2. **Fichiers autorisés** — la liste EXHAUSTIVE de ce que l'exécutant peut toucher (ownership par fichier : deux briefs actifs ne partagent jamais un fichier)
3. **Portes de vérification** — les commandes à jouer, sortie = preuve dans le rapport
4. **Hors périmètre** — ce qu'on ne touche PAS (transverses gelés)
5. **Statut** — `brouillon → pret → en cours → fait` (mis à jour dans le brief)

## Les règles qui tiennent l'ensemble

- **Rien ne dépasse des fichiers autorisés.** Un doute = on bloque et on demande, jamais « je corrige au passage ».
- **L'index git est partagé** entre sessions : commits ciblés (`git add <chemins>`, jamais `-A`), et vérifier `git show --stat HEAD` après CHAQUE commit — un add ciblé emporte quand même ce qu'une autre session a stagé.
- **Le registre est dérivé, jamais tenu à la main** : `handoff-check.py` le construit depuis les frontmatters et échoue sur collision (cf. principe : une règle sans commande n'est pas une règle).
- **Revue par le cerveau** avant `fait` : rejouer les portes, ouvrir les captures, graver dans memory/ (décision, leçon, TODO) dans le même commit de revue.
- **Briefs terminés = archives** : ils gardent leur syntaxe d'époque, on ne les recontrôle pas.

## Ce qu'il faut construire pour démarrer (dans l'ordre)

Tout est livré dans `handoffs/` à côté de ce fichier — voir `handoffs/README.md` :

1. `docs/handoffs/_template.md` — le gabarit de brief (frontmatter `id` / `statut` / `fichiers` lu par la machine)
2. `scripts/handoff-check.py` — le registre dérivé + anti-collision (fichier revendiqué par deux briefs actifs, statut hors vocabulaire, id en doublon) → dans la table des portes
3. `docs/handoffs/README.md` — ce protocole adapté au projet
4. Optionnel : agents `dev-handoff` (exécute) et `recette-livraison` (vérifie, lecture seule, ne répare jamais)
