# Phase 0bis — Refresh doc Anthropic

## Objectif

Vérifier que les règles auditées par Roborock sont toujours conformes à la **doc Anthropic officielle actuelle**, pas à un snapshot périmé.

## URLs canoniques à WebFetch

À chaque invocation de Roborock, fetcher ces 4 URLs et extraire les règles à jour :

### 1. Skills — vue d'ensemble
```
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
```
**Extraire** : structure dossier skill, fichiers obligatoires/optionnels, progressive disclosure, limites token.

### 2. Skills — best practices
```
https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
```
**Extraire** :
- Contraintes `name` : longueur max, regex autorisée, mots réservés
- Contraintes `description` : longueur max, third person, contenu requis
- Limite body SKILL.md (lignes)
- Anti-patterns (paths Windows, nested references, etc.)

### 3. Repo officiel skills
```
https://github.com/anthropics/skills
```
**Extraire** : nouveaux skills publiés, conventions de structure, fichiers optionnels récents (evals/, etc.).

### 4. Memory / CLAUDE.md
```
https://code.claude.com/docs/en/memory
```
**Extraire** : hiérarchie CLAUDE.md, auto-loading, scope path-based, taille recommandée racine.

## URLs secondaires (au besoin)

Si l'audit révèle des doutes spécifiques :

- **Hooks** : `https://code.claude.com/docs/en/hooks` — 12+ lifecycle events, format settings.json
- **Subagents** : `https://code.claude.com/docs/en/sub-agents` — frontmatter agents
- **Slash commands** : `https://code.claude.com/docs/en/slash-commands` — format custom commands
- **Settings** : `https://code.claude.com/docs/en/settings` — schéma settings.json

## Méthode de diff

Pour chaque URL fetched :

1. **Demander à WebFetch d'extraire** les contraintes structurées :
   > "Extract: max length of `name` field, allowed regex for `name`, reserved words, max length of `description`, max body lines for SKILL.md, any new required fields added recently."

2. **Comparer** aux règles locales :
   - `references/checks-frontmatters.md` (Phase 1)
   - `references/checks-skills.md` (Phase 2)
   - `references/checks-agents.md` (Phase 3)
   - `references/checks-claude-memory.md` (Phase 5)

3. **Si divergence détectée**, marquer dans le rapport :

```
### Phase 0bis — Doc Anthropic
✅ Frontmatter name regex : conforme (lowercase + digits + hyphens, ≤ 64 chars)
✅ Description max chars : conforme (1024)
⚠️ DIVERGENCE — Anthropic mentionne désormais un champ `disable-model-invocation` optionnel.
   → references/checks-frontmatters.md à mettre à jour (proposer diff à l'humain)
❌ DIVERGENCE CRITIQUE — limite body SKILL.md passée de 500 à 300 lignes.
   → Plusieurs skills locaux > 300 lignes → re-classifier en HAUTE Phase 2.
```

## Échecs de fetch

Si une URL échoue (timeout, 404, redirect non géré) :

```
### Phase 0bis — Doc Anthropic
⚠️ URL https://... non accessible ce run. Audit poursuivi avec règles locales (snapshot YYYY-MM-DD).
```

**Ne JAMAIS** bloquer l'audit complet sur un échec de Phase 0bis. La doc locale reste utilisable, juste possiblement périmée.

## Auto-update des references/

**Par défaut** : Roborock ne touche PAS aux `references/`. Il **propose** un diff dans le rapport, l'utilisateur valide.

**Si l'utilisateur dit explicitement** : "Roborock, refresh tes references/" ou "applique les màj de la Phase 0bis" → là Roborock peut éditer les `checks-*.md` correspondants avec les nouvelles règles.

## Date du dernier refresh

Pour traçabilité, en fin de chaque rapport Roborock, noter :

```
_Phase 0bis exécutée le YYYY-MM-DD HH:MM. URLs fetched: 4/4 (ou 3/4 si une a failed). Divergences détectées: N._
```

Cela permet à l'humain de savoir quand la doc Anthropic a été confrontée pour la dernière fois.
