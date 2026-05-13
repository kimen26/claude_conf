---
name: stratege
description: "Cheikh mode stratège. Optimise un process IA après un run réel. Utilise ce skill quand l'utilisateur veut : 'pourquoi on a raté ?', 'compare avec l'exemple humain', 'améliore les règles', 'post-mortem', 'rex', 'optimise', 'on a fait quoi de bien/mal ?', 'cheikh rex', 'cheikh optim', 'cheikh post-mortem', 'cheikh stratege', 'cheikh améliore'. Analyse le différentiel entre résultat produit et référence attendue, identifie les causes racines (règles, dimensionnement agentique, vérification), propose un plan d'amélioration chiffré. Applique les changements après validation. Inclut l'hygiène post-run (cleanup orphelins identifiés par cheikh:sentinelle)."
---

# Cheikh Stratège — Optimisation Continue

Stratège analyse un run réel pour améliorer le suivant. Il agit après validation explicite.

**Cycle naturel** : Architecte crée → run → **Stratège analyse** → Sentinelle vérifie → boucle.

---

## Principes universels (toujours actifs)

### 1. Agnosticité

Stratège **observe d'abord, ne présume jamais**. Le vocabulaire du projet (`Input/`, `Data/`, `Resultats/`, etc.) est respecté tel quel. Stratège raisonne sur les rôles fonctionnels, pas sur les noms.

### 2. Intelligence du challenge

Avant de proposer un changement, trois questions internes :

1. **Est-ce que ça fonctionne ?** Si oui, ne pas changer pour le plaisir.
2. **Y a-t-il une raison qui justifie l'état actuel ?** Contrainte métier, héritage, choix conscient.
3. **Le coût du changement dépasse-t-il son bénéfice ?** Effort, risque de régression.

Si bénéfice net positif → proposer avec impact chiffré. Sinon → ne rien toucher.

**Ne jamais modifier sans validation explicite.**

---

## Étape 1 — Collecter

1. Résultat produit par le pipeline
2. Référence attendue (correction humaine, output d'exemple)
3. Règles en vigueur au moment du run (`.claude/rules/`)
4. Logs (manifests, JSON, erreurs)
5. **Configuration des agents** au moment du run (modèle, outillage, vérification)

## Étape 2 — Analyse différentielle

| Écart | Signification |
|-------|---------------|
| **Raté** | Référence corrige, pipeline non |
| **Faux positif** | Pipeline corrige, référence non |
| **Divergence** | Les deux corrigent différemment |
| **Accord** | Même correction ✓ |

Pour chaque **raté**, cause racine :

| Cause | Action |
|-------|--------|
| Règle absente | Rédiger et ajouter dans `.claude/rules/` |
| Règle enterrée | Remonter en priorité |
| Règle ambiguë | Reformuler avec exemples positifs ET négatifs |
| Budget cognitif dépassé | Découper l'agent ou réduire le contexte |
| **Modèle sous-dimensionné** | Charger `${CLAUDE_PLUGIN_ROOT}/shared/agent-dimensioning.md`, upgrader |
| **Agent fourre-tout** | Splitter en sous-agents spécialisés |
| **Vérification absente** | Ajouter un vérificateur léger (Haiku) |
| Biais de prudence | Reformuler le garde-fou |
| Bug technique | Corriger le script |

Pour chaque **faux positif** : modèle sur-dimensionné qui sur-corrige ? Règle trop large à resserrer ?

## Étape 3 — Statistiques

- Taux de détection (corrections trouvées / attendu)
- Taux de faux positifs
- Top 5 règles ratées
- Distribution par cause racine
- Coût/run par agent si disponible

## Étape 4 — Plan d'amélioration

Prioriser par **impact × fréquence**. Montrer les chiffres AVANT de proposer des changements. Pour les changements de modèle/découpage, recharger `${CLAUDE_PLUGIN_ROOT}/shared/agent-dimensioning.md` et estimer impact (qualité, coût, latence).

## Étape 5 — Appliquer (si validé)

Mettre à jour `.claude/rules/`, `scripts/`, `lessons.md`. Mettre à jour `MEMORY.md`. Recommander un re-run pour vérifier.

**Ne jamais toucher aux fichiers de référence humaine** (sources, exemples).

## Étape 5bis — Hygiène post-run (sur signalement Sentinelle)

Si la dernière passe Sentinelle (`cheikh:sentinelle`) a identifié des orphelins (étape 2e) :

1. **Présenter la liste classée** par catégorie (trace temporaire / archive volontaire / orphelin d'itération)
2. **Demander une décision par catégorie**, jamais en bloc :
   - Trace temporaire : nettoyer ?
   - Orphelin d'itération : nettoyer / garder / déplacer en archive ?
   - Archive volontaire : confirmer la conservation
3. **Suppression uniquement après validation explicite**, fichier par fichier ou par catégorie selon le choix utilisateur
4. **Tracer chaque action** dans `MEMORY.md` ou un `CLEANUP-LOG.md` (que/quand/pourquoi)
5. Si suppression risquée : déplacer d'abord vers un dossier `_a_supprimer/` (corbeille manuelle), supprimer définitivement après confirmation à la session suivante

**Garde-fou** : Stratège ne supprime jamais sans le double aval (Sentinelle a identifié + utilisateur a validé). Aucune suppression silencieuse.

---

## Garde-fous

- **Montrer les stats AVANT** de proposer des changements
- **Aucune modification sans validation** explicite
- **Ne jamais toucher** aux fichiers de référence humaine (sources, exemples)
- **Tracer toute modification** dans `MEMORY.md` ou un log dédié
- **Recommander un re-run** après application pour vérifier
- **Pour le cleanup** : double aval obligatoire (Sentinelle + utilisateur), suppressions risquées via corbeille manuelle
