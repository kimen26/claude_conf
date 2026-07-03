# Application — transformer un rapport d'audit validé en actions

> Les modules `audit-archi.md` et `nettoyage.md` sont **lecture seule**. Ce module est le SEUL de
> `claude-infra` qui écrit — et seulement après un rapport existant + validation explicite. Jamais
> d'application "à la volée" pendant un audit.

## Quand invoquer

- Un rapport `nettoyage.md` (Roborock) ou `audit-archi.md` vient d'être produit et validé par l'utilisateur
- L'utilisateur dit : "applique", "nettoie ce qui a été trouvé", "go sur les recommandations"

## Garde-fou d'entrée

**Double aval obligatoire** : (1) l'audit a identifié l'item, (2) l'utilisateur valide l'action. Aucune suppression silencieuse, aucune application en bloc sans passer par les catégories ci-dessous.

## Décision par catégorie, jamais en bloc

Pour les orphelins triés (voir `nettoyage.md` § Triage) :

| Catégorie | Question à poser | Action si "oui" |
|---|---|---|
| Trace temporaire | "Nettoyer ces N traces temporaires ?" | Suppression directe (faible risque) |
| Orphelin d'itération | "Nettoyer / garder / déplacer en archive ?" | Selon réponse — jamais de défaut implicite |
| Archive volontaire | "Confirmer la conservation ?" | Aucune action, juste tracer la confirmation |

Ne jamais fusionner ces 3 questions en une seule "je nettoie tout ?".

## Suppressions risquées — corbeille manuelle

Si une suppression touche un fichier référencé ailleurs de façon incertaine, ou si le doute persiste après l'audit :

1. Déplacer vers `_a_supprimer/` (ou équivalent local au projet) — **jamais de `rm` direct**
2. Suppression définitive seulement à la **session suivante**, après confirmation que rien n'a cassé
3. Si le projet a un `.gitignore`, s'assurer que `_a_supprimer/` n'est pas versionné par erreur

## Traçabilité obligatoire

Chaque application (suppression, archivage, correction de lien) se logue :
- Dans `MEMORY.md` du projet si le mécanisme existe (voir `checks-claude-memory.md`)
- Sinon dans un `CLEANUP-LOG.md` à la racine du périmètre audité

Format minimal : `AAAA-MM-JJ — <fichier/action> — <quoi> — <pourquoi> — <validé par>`.

## Après application

- Recommander une vérification rapide (le skill/agent/lien corrigé se déclenche-t-il toujours ?)
- Si le nettoyage touchait un skill partagé pro/perso (cf. `Sync-Skills-github-ProPerso`) → propager via sync, pas seulement en local
- Ne jamais toucher aux fichiers de référence humaine (sources, exemples de validation) même si signalés en audit

## Anti-patterns

- ❌ Appliquer pendant l'audit (mélange détection/action → confusion sur ce qui a été vérifié)
- ❌ "Je nettoie tout ce qui est orphelin" sans distinguer les 3 catégories
- ❌ `rm` direct sur un doute — toujours la corbeille manuelle si risque
- ❌ Suppression sans entrée de traçabilité
