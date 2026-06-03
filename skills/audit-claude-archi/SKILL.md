---
name: audit-claude-archi
description: Audite l'architecture Claude d'un projet (CLAUDE.md, INDEX, skills, agents, rules, hooks) et propose une refonte alignée doc Anthropic officielle. Auto-trigger sur "audit claude.md", "challenger structure", "refonte claude", "trop de claude.md", "découpage CLAUDE", "où mettre", "claude.md vs index", "claude.md vs rules", "claude.md vs skill", "scope claude", "process auto", "hook agent". Toujours rafraîchit la doc en ligne avant d'analyser.
allowed-tools: WebFetch Read Glob Grep Bash
---

# Audit Claude Archi

Audit complet de l'architecture Claude d'un projet : challenger CLAUDE.md, INDEX.md, skills, agents, rules, hooks. Produit un CR pédagogique, un diagnostic projet, un plan de refonte aligné Anthropic, et un auto-challenge avant exécution.

## Principe directeur

**La doc Anthropic bouge.** Ne JAMAIS faire confiance à ce qui est gravé ici sur les chiffres précis (seuils, comportements de chargement, syntaxe frontmatter). Le skill REFETCH la doc à chaque exécution. Les "règles d'or" ci-dessous sont des repères, pas des sources de vérité.

**Boussole de fond = Context Engineering** (cadre officiel Anthropic). Tout l'audit sert un seul objectif : *trouver le plus petit ensemble de tokens à haut signal qui maximise le résultat — le contexte est une ressource finie.* Chaque mécanisme (CLAUDE.md, rule, skill, subagent, hook, auto-memory) est un levier pour charger **le bon contexte, au bon moment, au coût minimal**, et router le travail vers **le bon LLM au besoin** (ex. Haiku via subagent). Voir la *Lentille économie de tokens* plus bas.

**🏷️ Discipline OFFICIEL vs IDÉE (non négociable).** Chaque affirmation de l'audit est étiquetée :
- `[OFFICIEL ✓ <source>]` — appuyé sur une doc / cookbook / course / article Anthropic (cf. *canon officiel* ci-dessous). Citer la source.
- `💡 [IDÉE — non officiel]` — pattern maison ou communauté (backlog, PMO auto-déclenché, substrate…). **Ne JAMAIS le présenter comme une reco Anthropic.** À proposer comme option, pas comme règle.

## Étape 1 — Rafraîchir la doc officielle (OBLIGATOIRE)

Fetch en parallèle les 8 pages canoniques. Si une page redirige, suivre la redirection.

```
https://code.claude.com/docs/en/memory            ← CLAUDE.md, rules path-scoped, AUTO-MEMORY
https://code.claude.com/docs/en/best-practices    ← guidance générale
https://code.claude.com/docs/en/skills            ← skills, frontmatter, lifecycle
https://code.claude.com/docs/en/features-overview ← arbre de décision feature (« Extend Claude Code »)
https://code.claude.com/docs/en/sub-agents        ← subagents, héritage CLAUDE.md
https://code.claude.com/docs/en/hooks-guide       ← hooks, triggers, déterminisme
https://code.claude.com/docs/en/hooks             ← RÉFÉRENCE hooks (catalogue événements + schémas JSON)
https://code.claude.com/docs/en/context-window    ← « What survives compaction » (survie /compact)
```

### Le canon officiel Anthropic (seules sources autorisées pour un constat « OFFICIEL »)

Au-delà des docs ci-dessus, fetch ces ressources **officielles** si l'audit touche au coût contexte, aux skills, ou à un système multi-agents.

**Articles ingénierie** (`anthropic.com/engineering` & `/research`) :
```
effective-context-engineering-for-ai-agents  ← LE cadre token economy (« smallest set of high-signal tokens »)
building-effective-agents (research/)         ← Workflows vs Agents + les 5 patterns
code-execution-with-mcp                       ← MCP tool search (jusqu'à −98.7% tokens)
writing-tools-for-agents                      ← design d'outils token-efficient (pagination, filtres, ACI)
claude-code-best-practices                    ← bonnes pratiques Claude Code (workflow, contexte)
```

**Repos GitHub officiels** (`github.com/anthropics`) :
```
anthropic-cookbook  ← CODE des patterns : Patterns/Agents/ (implémente les 5 patterns), Skills/, Claude Agent SDK/
skills              ← skills officiels de référence (document skills PDF/DOCX/XLSX, mcp-builder…) = gabarit SKILL.md
courses             ← 5 cours : API fundamentals · prompt engineering · real-world prompting · prompt evals · tool use
claude-code         ← examples/hooks/ (ex. bash_command_validator)
```

**Les 5 patterns Workflow** (officiels, *Building Effective Agents*) : **prompt chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer**. Distinction officielle : *workflow* = chemins de code **prédéfinis** (déterministe, prévisible) ; *agent* = le **LLM dirige** son propre process. Philosophie officielle : *commencer simple, n'ajouter de la complexité que si ça améliore mesurablement.*

> Audit d'un système multi-agents maison (PMO/pipeline) → ce n'est PAS couvert par la doc officielle. Voir l'*Annexe — idées non officielles* + les skills `pmo-design` / `pmo-challenge`.

Extraire de cette lecture :
- Seuil de lignes recommandé pour CLAUDE.md
- Comportement de chargement ancestors vs subdirs (lazy / on-demand / persistance après /compact)
- **Auto-memory** : seuil chargé (`MEMORY.md` → 200 premières lignes OU 25KB), distinction CLAUDE.md (toi tu écris) vs auto-memory (Claude écrit)
- Frontmatter `paths:` des rules — syntaxe exacte du moment ; **rules SANS `paths:`** = chargées au launch, priorité = CLAUDE.md
- Comportement des `@path` imports (économise contexte ou pas ? → **non**, chargés au launch)
- Skills : `disable-model-invocation` (coût contexte = 0 si true), `user-invocable`, `context: fork`, `paths:` (skills aussi path-scopables maintenant), `model`/`effort`, lifecycle après /compact (re-attache ~5k tokens/skill, budget combiné 25k)
- Hooks : types `command` / `prompt` / `agent` / `http` (plus seulement du shell déterministe) + catalogue d'événements (au-delà de UserPromptSubmit/PreToolUse/SessionStart : `InstructionsLoaded`, `PreCompact`/`PostCompact`, `ConfigChange`, `SessionEnd`, `UserPromptExpansion`, `PermissionRequest`…)
- **Custom commands = Skills** (fusion : `.claude/commands/x.md` ≡ `.claude/skills/x/SKILL.md`)
- **HTML comments** `<!-- … -->` dans CLAUDE.md : strippés du contexte = notes mainteneur gratuites (0 token)

## Étape 2 — Scanner le projet

```bash
# Inventaire
find . -name "CLAUDE.md" -not -path "*/node_modules/*" -not -path "*/_archive/*"
find . -name "INDEX.md" -not -path "*/node_modules/*" -not -path "*/_archive/*"
ls .claude/rules/ 2>/dev/null
ls .claude/agents/ 2>/dev/null
ls .claude/skills/ 2>/dev/null
ls ~/.claude/projects/*/memory/ 2>/dev/null  # auto-memory du projet (MEMORY.md + topic files)
cat .claude/settings.json 2>/dev/null  # pour les hooks
wc -l <chaque CLAUDE.md trouvé>
wc -l <MEMORY.md>                      # >200 lignes = surplus NON chargé
```

Pour chaque CLAUDE.md, INDEX.md, rules, MEMORY.md : compter lignes, sampler contenu (15 premières lignes), identifier les sources de vérité dupliquées entre fichiers.

> 💡 Pour vérifier *factuellement* quels fichiers d'instructions se chargent (et pourquoi), proposer à l'utilisateur le hook `InstructionsLoaded` (log session_start / nested_traversal / path_glob_match). Plus fiable que de raisonner sur les globs à la main.

## Étape 3 — CR pédagogique (avant diagnostic)

Présenter à l'utilisateur, sous forme de **tableau de décision** issu de l'étape 1 :

| Mécanisme | Quand charge | Coût | Survit `/compact` | Usage |
|-----------|--------------|------|-------------------|-------|
| CLAUDE.md racine + ancestors | Session start, entier | Toujours | ✅ re-injecté | Règles transverses au projet |
| CLAUDE.md de subdir | On-demand quand fichier du subdir touché | 0 avant | ❌ pas re-injecté | Règles pôle/domaine |
| `.claude/rules/*.md` **avec** `paths:` | Quand fichier match glob | 0 avant | recharge à match | Règles très ciblées |
| `.claude/rules/*.md` **sans** `paths:` | Session start | Toujours | comme CLAUDE.md | Règles transverses modulaires |
| Auto-memory `MEMORY.md` | Session start (200 1ʳᵉˢ lignes / 25KB) | Toujours (plafonné) | ✅ relu du disque | Ce que **Claude** apprend (build cmds, prefs) |
| Auto-memory topic files | On-demand (Claude les lit) | 0 avant | n/a | Détail déchargé hors MEMORY.md |
| Skill (description) | Session start | Low | re-attaché (budget) | Workflow / reference |
| Skill (full content) | Quand invoqué | Variable | ~5k tok/skill, 25k total | idem |
| Skill `disable-model-invocation: true` | Seulement si TOI tu l'invoques | **0** | n/a | Action à side-effect (`/deploy`) |
| Subagent | Quand invoqué | Isolé | n/a | Tâche contexte séparé |
| Hook `command` | Événement lifecycle | 0 | n/a | **Déterministe forcé** |
| Hook `prompt` / `agent` | Événement lifecycle | 0 (LLM externe) | n/a | Décision avec jugement (firing garanti, verdict variable) |

Énoncer en 4 lignes les distinctions critiques :
- **INDEX.md ≠ CLAUDE.md** : INDEX = catalogue humain navigable (Read manuel) ; CLAUDE.md = règles auto-chargées par Claude.
- **Skill ≠ Rule path-scoped** : skill = workflow invocable + reference (on-demand) ; rule = règle imposée chaque session (ou à match). NB : les deux acceptent `paths:` désormais — la ligne se brouille, trancher sur *invocable vs imposé*.
- **CLAUDE.md ≠ Hook** : CLAUDE.md = advisory (Claude peut zapper) ; hook = enforced (l'événement déclenche **toujours**). Un hook `prompt`/`agent` garde un firing garanti mais délègue le *verdict* à un modèle.
- **Auto-memory ≠ CLAUDE.md** : auto-memory = ce que **Claude** s'écrit tout seul (corrections, prefs) ; CLAUDE.md = ce que **toi** tu imposes. Ne jamais dupliquer l'un dans l'autre.

## Lentille économie de tokens (Context Engineering)

Appliquer cette grille à **chaque** fichier de l'archi : *« ce contenu paie-t-il son loyer en tokens à chaque session, ou peut-il être chargé au besoin ? »*

### Leviers pour alléger le contexte permanent

| Levier | Gain | Mécanisme |
|--------|------|-----------|
| Subagent / skill `context: fork` | Sort recherche/logs du contexte principal → seul le résumé revient | isolation |
| LLM **au besoin** (Haiku via subagent, ou hook `prompt`) | Route les tâches simples vers un modèle moins cher (= pattern *routing*) | routing |
| `disable-model-invocation: true` | Description **non chargée** = coût 0 jusqu'à invocation manuelle | skill |
| Skill on-demand | Body chargé seulement à l'invocation (vs CLAUDE.md toujours présent) | skill |
| Rule `paths:`-scopée | Chargée seulement quand un fichier match le glob | rule |
| MCP tool search / code-execution MCP | Schémas JSON déférés jusqu'à usage (jusqu'à **−98.7 %**) | mcp |
| HTML comments `<!-- … -->` dans CLAUDE.md | Strippés du contexte = notes mainteneur à **0 token** | claude.md |
| Topic files auto-memory | Détail hors des 200 lignes de `MEMORY.md`, lu à la demande | auto-memory |
| ❌ `@imports` | **N'économisent RIEN** (chargés au launch) — piège classique | — |

Règle d'or : *si Claude n'en a pas besoin à CHAQUE session → ça ne doit pas être dans le contexte permanent (CLAUDE.md / rule sans paths / 200 lignes de MEMORY.md).*

### Où vivent les leçons & savoirs ? (guide de placement)

Question récurrente : une leçon (REX, savoir métier, règle) → CLAUDE.md, rule, skill, agent, auto-memory, ou fichier projet ?

| Type de leçon / savoir | Où le mettre | Pourquoi |
|------------------------|--------------|----------|
| Ce que **Claude découvre seul** (build cmd, prefs, REX session) | **Auto-memory** (`MEMORY.md` + topic files) | Claude l'écrit, relu chaque session, plafonné 200 lignes |
| Règle que **TOI tu imposes**, transverse ("toujours X") | **CLAUDE.md** (racine ou pôle) | advisory imposé, chaque session |
| Règle imposée mais **ciblée** à un type de fichier | **Rule `paths:`** | advisory, 0 token avant match |
| Règle qui **DOIT tenir à 100 %** (jamais zappable) | **Hook** (`command` déterministe, ou `prompt`/`agent` si jugement) | enforced, firing garanti |
| **Savoir métier** d'un domaine (ex. LESSONS LimeZu, catalogue tags) | **Skill** (`SKILL.md` + `reference.md`/`LESSONS.md`) | on-demand, ~0 coût avant usage |
| **État projet / décisions** (backlog, sprint-log…) | **Fichiers projet** 💡 *format maison, non officiel* | hors contexte, lus par les agents au besoin — s'inspire du *structured note-taking* (officiel) |
| **Procédure répétée** invocable (`/deploy`, pipeline) | **Skill** (souvent `disable-model-invocation: true`) | workflow déclenché, coût 0 sinon |

Anti-pattern transverse : la **même** leçon recopiée dans 3 endroits (CLAUDE.md + auto-memory + skill) → 1 seule source de vérité, les autres pointent (`[[lien]]` ou chemin).

## Étape 4 — Diagnostic projet

Pour chaque problème détecté, format :
```
🔴 CRITIQUE / 🟡 ATTENTION / 🟢 OK — <fichier ou pattern>
  Constat : <ce qui ne va pas>
  Source officielle : <citation doc Anthropic>
  Impact : <coût contexte / adhérence / maintenance>
```

Patterns à chasser systématiquement :
1. CLAUDE.md > seuil recommandé (consomme contexte permanent + adhérence dégradée)
2. Règles métier diluées dans INDEX.md (devraient être CLAUDE.md ou rules)
3. Détails spécifiques à un sous-pôle mélangés dans CLAUDE.md racine (gaspille contexte sessions autres pôles)
4. Process critique en prose ADVISORY dans CLAUDE.md (candidat hook ou rule path-scoped)
5. Duplication source-de-vérité entre fichiers (DRY cassé)
6. Skills user-level qui dupliquent rules project-level (ou inverse)
7. Agents définis sans triggers déclarés clairement (advisory uniquement)
8. Pas de hook `UserPromptSubmit` pour militariser des invocations critiques
9. `MEMORY.md` (auto-memory) > 200 lignes → le surplus n'est PAS chargé (fausse sécurité). Déplacer le détail en topic files
10. Duplication CLAUDE.md ⇄ auto-memory (Claude réécrit ce que tu imposes déjà, ou inverse)
11. Règle « advisory » qui demande un *jugement* (pas un simple shell) → candidat hook `prompt`/`agent`, pas seulement `command`
12. `AskUserQuestion` utilisé pour poser une question alors que le canal (bot Telegram) ne relaie que allow/deny → poser en TEXTE

## Étape 5 — Plan de refonte

Proposer une architecture cible en 3 niveaux quand le projet est multi-pôles :
```
PROJET/
├── CLAUDE.md                    ← routage + commun + signaux (< 80 lignes)
├── pôle-A/CLAUDE.md             ← pôle A on-demand (< 150 lignes)
├── pôle-B/CLAUDE.md             ← pôle B on-demand (< 150 lignes)
└── .claude/
    ├── rules/*.md               ← règles path-scoped très ciblées
    └── settings.json hooks      ← militarisation déterministe
```

Pour chaque fichier proposé : lister ligne par ligne ce qui va dedans, d'où ça vient (fichier source actuel), et ce qui en sort.

## Étape 6 — Auto-challenge

Avant de présenter le plan à l'utilisateur, le critiquer soi-même selon ces axes :

| Axe | Question |
|-----|----------|
| Simplicité | Combien de niveaux ? Un nouveau venu pige en 2 min ? |
| Efficacité | Quelle économie de contexte concrète (estimation %) ? |
| Rapidité | Adhérence améliorée ? Charge réduite ? |
| Intégrité | Aucune perte de matière ? Sources de vérité préservées ? |
| Qualité | 100 % conforme doc Anthropic ? Aucun anti-pattern ? |
| `/compact` | Routage critique reste à la racine ? Nested se rechargent ? |
| Réversibilité | Plan en phases avec commits séparés ? Revert possible ? |
| Hook nécessaire ? | Y a-t-il une règle critique qui DOIT être déterministe (donc hook obligatoire) ? |

Lister les risques identifiés + leur réponse.

## Étape 7 — Question à l'utilisateur

⚠️ **JAMAIS `AskUserQuestion`** (le picker natif ne se relaie pas sur le bot Telegram — seulement allow/deny). Poser la question **en TEXTE dans la réponse**, façon chatbot (règle machine-wide `~/.claude/rules/interaction-style.md`).

Proposer en texte plusieurs niveaux d'exécution, et laisser l'utilisateur répondre librement :
- Plan détaillé ligne par ligne d'abord (revue avant code)
- Exécution directe en commits séparés (revue par diff)
- Phase 1 seulement (CLAUDE.md), phase 2 plus tard (rules + hooks)
- Pilote sur un seul fichier d'abord (preuve de concept)

Ex. : « Tu préfères que je sorte d'abord le plan ligne par ligne, ou que j'exécute directement en commits séparés que tu revois par diff ? »

Ne JAMAIS toucher un fichier avant validation utilisateur.

## Anti-patterns à signaler à l'utilisateur

- **CLAUDE.md > 200 lignes** systématiquement, sans découpage path-scoped
- **`@imports` utilisés pour "économiser le contexte"** → ils n'économisent RIEN, juste de l'organisation visuelle
- **Règles critiques en prose advisory** quand un hook ferait le travail (ex : "toujours faire X avant commit" → PreToolUse hook)
- **INDEX.md utilisés comme CLAUDE.md** ou inverse
- **Skills project-level qui devraient être user-level** (réutilisables multi-projets)
- **Process militaire qui dépend de la mémoire humaine/Claude** sans rule path-scoped pour le rappeler
- **`MEMORY.md` (auto-memory) > 200 lignes** → le surplus n'est pas chargé ; déplacer le détail en topic files
- **Auto-memory qui duplique CLAUDE.md** (ou inverse) — l'un est écrit par Claude, l'autre imposé par toi
- **`AskUserQuestion`** pour poser une question → préférer le TEXTE (picker non relayable sur canaux distants)

## Format de réponse

1. **CR pédagogique** (tableau de décision + 4 distinctions critiques) — 1 écran
2. **Diagnostic** (liste classée 🔴🟡🟢) — concis
3. **Plan** (arborescence cible + répartition ligne par ligne) — clair
4. **Auto-challenge** (tableau risque → réponse) — court
5. **Question** posée **en TEXTE** (jamais `AskUserQuestion`), 3-4 niveaux d'exécution proposés

Pas de blabla. L'utilisateur veut un audit actionnable, pas un essai.

## Annexe — Idées NON OFFICIELLES (patterns avancés)

⚠️ **Rien dans cette annexe n'est une reco Anthropic.** Ce sont des pratiques maison/communauté qui *s'appuient* sur des briques officielles mais dont la **forme est inventée**. À proposer comme options, jamais comme « la doc dit ». Toujours préfixer `💡 [IDÉE — non officiel]`.

- 💡 **Coordination par fichiers (« substrate »)** — des agents qui se parlent via des fichiers partagés (`backlog.md`, `decisions.md`, `sprint-log.md`). *S'inspire* du **structured note-taking / agentic memory** (ça, c'est officiel — article context-engineering) mais le format backlog/PMO est 100 % maison.
- 💡 **PMO orchestrateur forcé avant/après** — un agent « chef de projet » déclenché à chaque tour via hook (`UserPromptSubmit` en amont, `Stop`/`SubagentStop` en aval) pour logger décisions et garder la cohérence. = deux briques officielles (subagent + hook) câblées en pattern maison.
- 💡 **Pipeline = patterns officiels chaînés** — `simplifier → designer → reviewer (boucle)` n'est que du *prompt chaining* + *evaluator-optimizer* (officiels). Seul le **câblage en sous-agents nommés** est maison.
- 💡 **Ressources communauté (non officielles)** — il n'existe **pas** de « liste de repos recommandés » signée Anthropic. Côté communauté : `awesome-claude-code` (GitHub) recense skills/hooks/agents tiers. Non maintenu par Anthropic → auditer avant d'adopter.

Pour auditer en profondeur cette couche multi-agents maison → skills `pmo-design` (conception) / `pmo-challenge` (audit).

---

_MAJ 2026-06-03 : refresh doc Anthropic. Ajouts — auto-memory (`MEMORY.md` 200 lignes/25KB), rules sans `paths:` (chargées au launch), skills `paths:`/`user-invocable`/`disable-model-invocation` (coût 0), hooks `prompt`/`agent` (firing garanti ≠ verdict déterministe) + catalogue d'événements élargi (`InstructionsLoaded`, `PreCompact`…), fusion commands=skills, HTML comments strippés. **Nouveau cadre de fond : Context Engineering** (boussole token economy) + section *Lentille économie de tokens* (leviers + guide « où vivent les leçons ») + références conceptuelles (context-engineering, code-execution-MCP, building-effective-agents : Workflows vs Agents + 5 patterns). Fix : suppression `AskUserQuestion` (conflit règle machine-wide → questions en texte). **Passe « tri OFFICIEL »** : canon officiel sourcé (docs + articles eng + cookbook + courses + skills repo), discipline d'étiquetage `[OFFICIEL ✓]` vs `💡 [IDÉE — non officiel]`, + Annexe non officielle (substrate/backlog, PMO forcé, awesome-claude-code communauté). Inchangé : seuil 200 lignes, `@imports` n'économisent rien, survie /compact racine vs subdir._
