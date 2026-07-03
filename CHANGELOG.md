# CHANGELOG — claude_conf

Journal des skills partagés via ce passe-plat **perso ⇄ taff**. À mettre à jour à **chaque push** (règle imposée dans le skill `Sync-Skills-github-ProPerso`).

**Format :** `- AAAA-MM-JJ (perso|taff) — <changement>`
La machine d'origine `(perso|taff)` indique d'où vient la version la plus à jour → en cas de delta, on garde la plus récente et on ne committe que le fichier optimisé.

---

## claude-infra
- 2026-07-03 (taff) — **Ajout. Mégaskill fusion de 4 skills** : `cycle` (routeur) + `audit-claude-archi` + `roborock-challenge` + `challenge-local` → SKILL.md routeur + 12 `references/`. Délègue aux plugins officiels (claude-md-management, claude-code-setup, skill-creator, hookify). Section Maintenance intégrée (version + changelog interne + règles de propagation). **Côté perso : pull puis archiver les 3 anciens skills locaux** (retirés du repo).

## claude-code-mastery
- 2026-07-03 (taff) — `repos.md` : veille 02/07 (ECC renommé, section D compression tokens rtk/headroom/context-mode/caveman, index récap A→D). Nouveau `plugins.md` : bonnes pratiques plugins officiels (actifs/désactivés + règles).

## audit-claude-archi
- 2026-07-03 (taff) — **Retiré du repo** : fusionné dans `claude-infra/references/audit-archi.md`.
- 2026-06-03 (perso) — Ajout. Audit archi Claude aligné doc Anthropic officielle (auto-memory, Context Engineering, discipline `[OFFICIEL]` vs `💡 [IDÉE]`, annexe non-officielle).

## pmo-design
- 2026-06-04 (perso) — Ajout. **Version générique** (exemples projet → placeholders neutres `pole-a-*` / `pole-b-*`).

## pmo-challenge
- 2026-06-04 (perso) — Ajout. **Version générique** (jumeau de `pmo-design`).

## roborock-challenge
- 2026-07-03 (taff) — **Retiré du repo** : fusionné dans `claude-infra/references/nettoyage.md` + `checks-*.md`.
- 2026-06-04 (perso) — Ajout. Renommé depuis `challenge-roborock` (convention `<métier>-<tâche>`). **Version générique** (SKILL.md + `references/`).

## challenge-local
- 2026-07-03 (taff) — **Retiré du repo** : fusionné dans `claude-infra/references/setup-wizard.md`.

## cheikh — famille (architecte / sentinelle / stratege)
- (taff, date à confirmer) — Refonte en **3 sous-skills** : `architecte` (setup·design), `sentinelle` (audit lecture-seule), `stratege` (post-mortem·optim). Stocké sous `skills/CheiKh/`. **À récupérer côté perso** (remplace l'ancien `cheikh` mono-fichier).

---

> ⚠️ Convention de nommage en cours de standardisation : `<métier>-<tâche>` (ex. `pmo-design`, `pmo-challenge`, `roborock-challenge`). Le dossier `CheiKh/` (casse + imbrication) reste à reconcilier en `cheikh-architecte` / `cheikh-sentinelle` / `cheikh-stratege` lors d'une prochaine passe.
