---
name: claude-infra
description: "Infra Claude Code complete — audit d'architecture (CLAUDE.md, skills, agents, hooks, rules, memory vs doc officielle Anthropic), nettoyage GED (orphelins, liens morts, frontmatters casses, doublons semantiques, knowledge rot), application post-audit (corbeille manuelle, double aval), setup/wizard de config, routage vers plugins officiels. Auto-trigger sur : audit claude.md, challenger structure, refonte claude, ou mettre, claude.md vs skill/rules/index, passe le Roborock, nettoie la GED, fichiers orphelins, liens morts, knowledge rot, audite ma config, challenge-local, setup claude, applique le nettoyage, quel skill utiliser, quel outil pour, cycle de vie config, cartographie claude, etat des lieux config."
allowed-tools: WebFetch Read Glob Grep Bash
---

# Claude Infra — audit, nettoyage, setup, routage

Skill parapluie. Identifier le besoin dans la table, charger UNIQUEMENT le module concerné (`references/`). Ne jamais empiler deux modules d'audit sur la même question.

## Routage

| Besoin | Module / outil | Charge |
|---|---|---|
| Auditer l'archi Claude vs doc officielle ("où mettre X", "claude.md vs skill") | `references/audit-archi.md` | + `refresh-doc.md` obligatoire |
| Nettoyer / Roborock (orphelins, liens morts, doublons, rot) | `references/nettoyage.md` | checks-*.md à la demande |
| **Appliquer un rapport d'audit validé** (suppression, archivage) | `references/application.md` | uniquement après rapport + validation explicite |
| Setup / wizard config perso | `references/setup-wizard.md` | manuel, questionnaire |
| **Hygiène d'un CLAUDE.md** (qualité, sync codebase) | → plugin officiel `claude-md-management` ("audit my CLAUDE.md") | délégué |
| **Capturer apprentissages fin de session** | → `/revise-claude-md` (même plugin) | délégué |
| **Recommander automations pour UN repo** | → plugin officiel `claude-code-setup` ("recommend automations") | délégué |
| **Créer/tester un skill** | → plugin officiel `skill-creator` | délégué |
| **Créer un hook** | → plugin officiel `hookify` | délégué |
| Veille écosystème (repos, outils) | → skill `claude-code-mastery` (`repos.md`) | délégué |
| Process projet IA (hors infra Claude) | → skill `CheiKh` (architecte/sentinelle/stratege) | hors périmètre |
| Multi-agents / PMO | → skills `pmo-design` / `pmo-challenge` | hors périmètre |
| Sync pro↔perso | → skill `Sync-Skills-github-ProPerso` | hors périmètre |

## Règles non négociables

1. **Audits = lecture seule.** `audit-archi.md`, `nettoyage.md`, `setup-wizard.md` (phase audit) n'écrivent jamais. Seul `application.md` écrit — et seulement après un rapport existant + validation explicite (double aval, corbeille manuelle pour le risqué, traçabilité obligatoire).
2. **Refresh doc avant audit archi.** La doc Anthropic bouge — `references/refresh-doc.md` d'abord, jamais confiance aux chiffres gravés.
3. **Étiquetage OFFICIEL vs IDÉE** (voir audit-archi.md) : toute reco est sourcée `[OFFICIEL ✓]` ou marquée `💡 [IDÉE — non officiel]`.
4. **Un besoin = un module.** Doute entre deux → demander à l'utilisateur, pas cumuler.
5. Rapport final : suivre `references/report-template.md` pour les audits/nettoyages.

## Canon officiel (source unique)

- Doc live : URLs canoniques dans `references/refresh-doc.md`
- Repos de référence : `~/.claude/skills/claude-code-mastery/repos.md` (catalogue A/B/C/D + veille datée)

## Maintenance du skill (procédure MAJ)

**Version : 2026-07-03b** (v1 fusion 4 skills ; v2 intègre grille de décision + triage orphelins + module application repris de CheiKh).

3 niveaux de fraîcheur, 3 mécanismes distincts :

| Quoi | Peut pourrir ? | Mécanisme |
|---|---|---|
| Doc officielle Anthropic | Non | **Auto** — `refresh-doc.md` refetch live à CHAQUE audit. Rien de gravé |
| Table de routage + checks | Oui | **Semi-auto** — le module nettoyage détecte lui-même le drift (skill listé dans le routeur mais absent du disque, plugin délégué désinstallé…). Tout audit qui trouve un écart routeur/réalité DOIT proposer la correction du SKILL.md |
| Propagation pro ↔ perso | Oui | **Manuel discipliné** — règles ci-dessous |

### Règles de propagation (non négociables)

1. **Source de vérité = GitHub** (`kimen26/claude_conf`). Jamais éditer claude-infra sur les 2 PC sans sync entre les deux — `status` avant toute modif.
2. Toute modif → **bump la ligne Version** (date) + 1 ligne au changelog ci-dessous → push immédiat via `Sync-Skills-github-ProPerso`.
3. Sur l'autre PC : premier réflexe de session infra = `sync status` ; si GitHub plus récent → pull avant usage.
4. Modif de structure (ajout/retrait d'un module references/) → mettre à jour la table de routage DANS LE MÊME commit.
5. Nouveau plugin officiel installé/retiré → vérifier les lignes "délégué" du routeur.

### Changelog

- 2026-07-03b : ajout `references/application.md` (module d'écriture, seul du skill) + grille de décision 3-questions et triage orphelins dans `nettoyage.md`. Repris de `CheiKh` (sentinelle/stratège) après comparaison — CheiKh reste séparé (scope pipeline métier, hors config Claude).
- 2026-07-03a : création (fusion 4 skills, délégation plugins officiels claude-md-management / claude-code-setup / skill-creator / hookify).
