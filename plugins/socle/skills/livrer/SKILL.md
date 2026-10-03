---
name: livrer
description: "Met en service des tâches Backlog au statut Valide : commit par chemins listés, push, déploiement, smoke, passage en Livre, ligne de CHANGELOG. Argument = numéros de tâche, par exemple `/socle:livrer 85 86`. À invoquer dès que Yann demande de livrer en langage naturel (« livre », « livre tout », « commit push deploy »)."
argument-hint: "<numéros de tâche>"
---

# /socle:livrer : la mise en service (temps 7)

Argument : les numéros de tâche (`$ARGUMENTS`). Une demande de Yann en langage naturel (« livre »)
VAUT lancement : Claude invoque ce skill lui-même, il ne demande pas à Yann de taper la commande.

**Règles dures** : arrêt au **premier rouge non mécanique**, motif dit à l'utilisateur ; jamais
`git add -A`, `git add .` ni `git commit -a` ; jamais `push --force` ; jamais de commit d'un fichier
hors du `## Périmètre` des tâches citées ; **refus net si une porte est rouge**.

**Rouge mécanique** (test devenu faux parce qu'une tâche validée a changé volontairement un
comportement, `.pyc` oublié, cliquet à abaisser) : reprise par `executant`, diff relu, commit par
chemins, la livraison repart de l'étape qui a échoué. Tout autre rouge (régression, comportement non
voulu, smoke rouge) reste un arrêt.

## 1. Contrôler
Pour chaque numéro : `status: Valide` dans le frontmatter et un bloc daté dans `## Verdict`. Sinon stop.
Lire `## Périmètre` : c'est la liste blanche du commit. Puis `python outils/portes.py` : **exit 0
exigé**. Rouge : refuser de livrer, rapporter la fin de sortie, ne rien committer.

## 2. Commit par chemins
- `git status` : aucun fichier de conflit de synchronisation (copie de conflit, suffixe de nom de machine) ; s'il y en a, stop.
- Fichiers du commit = **périmètre de la tâche ∩ `git status`**, ajoutés un par un (`git add <chemin>`).
  Tout fichier modifié hors périmètre reste dehors et se signale. Un doute : `git diff <fichier>`,
  des lignes que la session n'a pas écrites ne se commitent pas.
- Avant de commiter : `git diff --cached --name-only` comparé à la liste attendue ; un écart, stop.
- Un fichier partagé entre deux tâches ne part qu'une fois, dans un seul commit : le dire.
- Un commit par tâche. Message Conventional Commits `type(scope): description (task-NNN)`, terminé
  par la ligne `Co-Authored-By` demandée par le contexte de session.

## 3. Pousser
`git push` simple. Refus (non fast-forward) : stop, dire pourquoi, ne jamais forcer. Si Yann n'a
pas demandé le push, s'arrêter avant et le lui proposer.

## 4. Déployer et prouver
```bash
python outils/deployer.py        # met HEAD en service ; --help pour les options
python outils/smoke.py           # APRÈS le déploiement, via socle:photographe
```
Un échec de connexion juste après le déploiement : le service redémarre, relancer **une** fois.
Deuxième échec : stop. Les captures du smoke s'**ouvrent et se regardent** (voir
`/socle:recette-ecran`), un exit 0 ne suffit pas. Ne jamais diffuser une URL interne de service.
Squelette `outils/deployer.py` non implémenté (exit 1 « non implémenté ») : le dire, ne pas inventer. Un
`outils/smoke.py` qui affiche « AUCUNE CAPTURE » n'a rien prouvé : le dire aussi.

## 5. Clôturer
- Statut `Livre` : `backlog task edit task-NNN --status Livre` (ou le frontmatter à la main si
  l'outil est absent).
- `memory/CHANGELOG.md` : **une ligne par livraison**, en tête, **du point de vue de l'utilisateur** (ce
  qu'il voit de plus : « les photos partent dans la bonne fiche », pas « refactor du module »), sans
  cadratin. La release regroupe ensuite ces lignes en capacités sous `vX.Y`.
- `memory/TODO.md` : lignes concernées en `[x]`. Garder le style de fin de ligne (CRLF ou LF) du fichier.
- Leçons, décisions, déplacement de la tâche vers `backlog/completed/` et board : voir `/socle:tache`, section Clôturer.
- Commit de ces notes, par chemins, après le déploiement.

## 6. Rendre compte
Commits (hash court par tâche), résultat du déploiement, résultat du smoke, tâches passées en
`Livre`, fichiers laissés dehors et pourquoi.
