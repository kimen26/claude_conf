# Repos de Reference — Claude Code (mai 2026)

> Catalogue maintenu. Organise par valeur, pas par date.
> Derniere veille : 07/05/2026.
> Pour checker une MAJ : `gh api repos/{owner}/{repo}/commits?per_page=5`
> ou (si `gh` indispo) : `curl -s https://api.github.com/repos/{owner}/{repo}/commits`

---

## A. Officiels Anthropic (source de verite)

### A.1 anthropics/skills — 65.8k stars
- **URL** : https://github.com/anthropics/skills
- **Contenu** : Depot officiel des skills Anthropic (dont `frontend-design`, 277k+ installs)
- **Usage** : Reference pour la structure SKILL.md, frontmatter, et skills production-ready
- **Interet** : TRES ELEVE — c'est LA reference pour creer ses propres skills

### A.2 anthropics/courses — 5 cours officiels
- **URL** : https://github.com/anthropics/courses
- **Contenu** : Curriculum officiel (API Fundamentals → Prompt Engineering → Real World → Evals → Tool Use)
- **Format** : Jupyter Notebooks interactifs (Claude Haiku pour cout minimal)
- **Usage** : Comprendre comment Claude fonctionne, pas juste comment l'utiliser
- **Interet** : TRES ELEVE — le fondement theorique
- **Detail** : voir `courses.md` dans ce skill

### A.3 anthropics/claude-plugins-official — 16.6k stars
- **URL** : https://github.com/anthropics/claude-plugins-official
- **Contenu** : 33 plugins officiels (12 LSP langages, skill-creator, frontend-design, ralph-wiggum, security-guidance)
- **Structure** : `.claude-plugin/plugin.json` + `commands/` + `agents/` + `skills/` + `.mcp.json`
- **Installation** : `/plugin install {name}@claude-plugins-official`
- **Interet** : ELEVE — marketplace officielle + reference pour creer ses propres plugins

### A.4 anthropics/claude-cookbooks — 37.8k stars
- **URL** : https://github.com/anthropics/claude-cookbooks
- **Contenu** : 40+ Jupyter Notebooks (RAG, sub-agents, tool use, JSON mode, prompt caching, extended thinking, vision)
- **Format** : 95% Jupyter Notebooks, copy-pastable
- **Usage** : Patterns concrets pour integrer Claude dans des projets
- **Interet** : TRES ELEVE — recettes de cuisine officielles

### A.5 anthropics/claude-quickstarts — 16k stars
- **URL** : https://github.com/anthropics/claude-quickstarts
- **Contenu** : 5 projets deployables (Customer Support, Financial Analyst, Computer Use, Browser Automation, Autonomous Coding Agent)
- **Pattern cle** : Autonomous Coding Agent = 2-agent (initializer + coding) avec git persistence multi-session
- **Interet** : ELEVE — modeles d'apps completes

---

## B. Outils fonctionnels (font un truc precis)

### B.1 github/spec-kit — 86.8k stars
- **URL** : https://github.com/github/spec-kit
- **Contenu** : Toolkit officiel GitHub pour Spec-Driven Development
- **CLI** : `specify init`, `specify check` + slash commands Claude Code (`/speckit.specify`, `/speckit.tasks`, `/speckit.implement`)
- **Structure** : `constitution.md` → `spec.md` → `plan.md` → `tasks.md`
- **Ecosysteme** : 60+ extensions communautaires, VS Code extension
- **Interet** : TRES ELEVE — LE standard pour du spec-driven
- **Detail** : voir `methodologies.md` dans ce skill

### B.2 thedotmack/claude-mem — 46.1k stars
- **URL** : https://github.com/thedotmack/claude-mem
- **Contenu** : Plugin memoire persistante automatique pour Claude Code
- **Architecture** : 5 hooks lifecycle + SQLite + ChromaDB (embeddings ONNX locaux, zero API)
- **Recherche 3 couches** : search (~100t) → timeline → get_observations (~1000t) = 10x token savings
- **Install** : `npx claude-mem install`
- **Interet** : TRES ELEVE pour projets multi-semaines
- **Detail** : voir `memoire.md` dans ce skill

### B.3 yamadashy/repomix — 23.3k stars
- **URL** : https://github.com/yamadashy/repomix
- **Contenu** : Pack un repo entier en 1 fichier XML/Markdown optimise LLM
- **Features** : Token count, compression Tree-sitter, detection secrets, respect .gitignore
- **Usage** : Partager tout un codebase avec Claude sans copier-coller
- **Interet** : MODERE — utile pour onboarding ou review cross-repo

### B.4 YishenTu/claudian — 4.5k stars
- **URL** : https://github.com/YishenTu/claudian
- **Contenu** : Integration Claude Code dans Obsidian (COMMUNAUTAIRE, pas officiel Anthropic)
- **Features** : Read/write/edit natif dans Obsidian, conversations persistantes
- **Interet** : MODERE — si tu utilises Obsidian

---

## C. Sources d'inspiration (pour cherry-pick, pas copier)

### C.1 affaan-m/everything-claude-code — 150k stars
- **URL** : https://github.com/affaan-m/everything-claude-code
- **Contenu** : 36 agents, 150+ skills, hooks, NanoClaw v2 orchestration, Rust control-plane (ECC 2.0 alpha)
- **Ce qu'on en tire** : Patterns orchestration multi-agent, architecture agents a grande echelle
- **Attention** : Enorme projet, cherry-pick ce qui est pertinent

### C.2 obra/superpowers — 145k stars
- **URL** : https://github.com/obra/superpowers
- **Contenu** : Framework TDD/methodologie agentic. Philosophie "think before code"
- **Skills** : Brainstorming, planning, TDD (RED-GREEN-REFACTOR), debugging, verification, code review, git worktrees
- **Ecosysteme** : superpowers-marketplace, superpowers-lab, superpowers-chrome
- **Ce qu'on en tire** : Discipline methodologique, phase gates, quality-first
- **Detail** : voir `methodologies.md` dans ce skill

### C.3 hesreallyhim/awesome-claude-code — 37.9k stars
- **URL** : https://github.com/hesreallyhim/awesome-claude-code
- **Contenu** : Index curate (skills, hooks, commands, agents, plugins) en 9 categories
- **Usage** : Discovery ponctuel — "je cherche un skill pour [X]"

### C.4 shanraisshan/claude-code-best-practice — 35.3k stars
- **URL** : https://github.com/shanraisshan/claude-code-best-practice
- **Contenu** : 84 best practices structurees, living document (MAJ v2.1.97 avril 2026)
- **Ce qu'on en tire** : Patterns workflow, orchestration, memory, security

---

## D. Verifier les MAJ d'un repo

```bash
# Derniers 5 commits
gh api repos/anthropics/skills/commits?per_page=5 \
  --jq '.[].commit | "\(.committer.date[:10]) \(.message | split("\n")[0])"'

# Audit rapide tous les repos cles
for repo in anthropics/skills anthropics/courses anthropics/claude-plugins-official \
  anthropics/claude-cookbooks github/spec-kit thedotmack/claude-mem obra/superpowers \
  affaan-m/everything-claude-code; do
  echo "=== $repo ==="
  gh api "repos/$repo/commits?per_page=3" \
    --jq '.[].commit | "\(.committer.date[:10]) \(.message | split("\n")[0])"' 2>/dev/null || echo "(erreur)"
done
```

---

## E. Derniere verification : 07/05/2026

| Repo | Stars (delta avril) | Derniere MAJ | Statut |
|------|---------------------|--------------|--------|
| anthropics/skills | 129k (+63k) | 06/05/2026 | TRES ACTIF — claude-api + Managed Agents + webhooks |
| anthropics/courses | 21k | 13/11/2025 | GELE depuis 6 mois |
| anthropics/claude-plugins-official | 18.7k (+2k) | 06/05/2026 | TRES ACTIF — `snowflake-cortex-code`, `oracle-data-platform`, `speakai`, `twilio-developer-kit` ajoutes |
| anthropics/claude-cookbooks | 42.3k (+4.5k) | 06/05/2026 | TRES ACTIF — managed_agents (multiagent, outcomes, memory), vulnerability-detection-agent |
| anthropics/claude-quickstarts | 16.5k | 05/02/2026 | GELE depuis 3 mois |
| github/spec-kit | 93k (+6k) | 06/05/2026 | TRES ACTIF — extensions communautaires + trigger sur nouveau chantier (cf memoire `reference_spec_kit_trigger.md`) |
| thedotmack/claude-mem | 73k (+27k) | 07/05/2026 | TRES ACTIF — v12.7.5, multi-harness Codex/Claude. NON installe localement → `npx claude-mem install` recommande |
| yamadashy/repomix | 24.4k | 07/05/2026 | ACTIF — Dart query coverage |
| YishenTu/claudian | 10.4k (+5.9k) | 05/05/2026 | TRES ACTIF — v2.0.11, support Codex |
| affaan-m/everything-claude-code (ECC) | 175k (+25k) | 03/05/2026 | TRES ACTIF — `gateguard`, `loop-status`, `autonomous-loops`, `agent-harness-construction` |
| obra/superpowers | 181k (+36k) | 06/05/2026 | TRES ACTIF — v5.1.0, methodologie TDD systematique |
| hesreallyhim/awesome-claude-code | 42.8k (+4.9k) | 27/04/2026 | ACTIF — ToC ajoutee, ticker auto |
| shanraisshan/claude-code-best-practice | 51.5k (+16k) | 07/05/2026 | TRES ACTIF — v2.1.128 (matche dernier Claude Code), slides LLM intro |

### Decouvertes interessantes (mai 2026)

**1. `anthropics/claude-cookbooks/managed_agents/`** — 12 notebooks dont :
- `CMA_coordinate_specialist_team.ipynb` : 1 coordinateur + 3 specialistes avec toolsets scopes (parfait pour archi PMO)
- `CMA_remember_user_preferences.ipynb` : memory stores read/write par user + read-only partage
- `CMA_verify_with_outcome_grader.ipynb` : grade-and-revise itere jusqu'a passage rubrique
- `CMA_orchestrate_issue_to_pr.ipynb` : issue → fix → PR → CI → review → merge
- `CMA_gate_human_in_the_loop.ipynb` : HITL via outils custom decide/escalate

**2. `anthropics/claude-plugins-official` nouveaux plugins** :
- `snowflake-cortex-code` : plugin officiel Snowflake (a tester en priorite)
- `oracle-data-platform` : pattern data platform
- `skill-creator` (officiel) : `/plugin install skill-creator@claude-plugins-official` — workflow iteratif intent → draft → tests subagents → eval-viewer → benchmark → optimisation description

**3. `obra/superpowers` v5.1.0** — comparaison vs setup Yann :
- 4 piliers : TDD, Systematic, Complexity reduction, Evidence over claims
- 6 hooks sequentiels : design socratique → branche isolee → micro-tasks (2-5min) → impl 2-phase review → RED-GREEN-REFACTOR strict → merge avec decisions explicites
- Subagent-driven-development : delegue chaque tache a un agent fraichement contextualise
- Differenciation : force spec validee + archi explicite AVANT code (vs Claude Code standard qui saute direct au code)
- → A cherry-pick : le pattern "subagent fraichement contextualise" pour ton orchestration agents PMO

**4. ECC skills potentiellement utiles** (a explorer ponctuellement) :
- `agent-harness-construction`, `autonomous-loops`, `continuous-agent-loop`, `agent-introspection-debugging`
- `context-budget`, `cost-aware-llm-pipeline`
- `agent-eval`, `benchmark`, `canary-watch`
- `data-scraper-agent`, `dashboard-builder`
- `documentation-lookup`, `codebase-onboarding`

### Repos NON ajoutes (volonte explicite Yann mai 2026)

Cette liste est **fermee** : ne pas ajouter de nouveau repo sans validation explicite.
