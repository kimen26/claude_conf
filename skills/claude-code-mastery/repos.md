# Repos de Reference — Claude Code (juillet 2026)

> Catalogue maintenu. Organise par valeur, pas par date.
> Derniere veille : 02/07/2026.
> Pour checker une MAJ : `gh api repos/{owner}/{repo}/commits?per_page=5`
> ou (si `gh` indispo) : `curl -s https://api.github.com/repos/{owner}/{repo}/commits`

---

## Index — ou chercher quoi

4 sections, 4 usages differents. "Interet" = a quel point ca vaut le detour pour toi aujourd'hui.

| # | Section | Repo | Stars | Interet | Exemple concret dedans |
|---|---------|------|-------|---------|--------------------------|
| A.1 | Officiels Anthropic | [anthropics/skills](https://github.com/anthropics/skills) | 157.5k | TRES ELEVE | Skill `frontend-design` (277k+ installs) — reference structure SKILL.md |
| A.2 | Officiels Anthropic | [anthropics/courses](https://github.com/anthropics/courses) | 22k | TRES ELEVE | Notebook `Prompt Engineering` — curriculum officiel en Jupyter |
| A.3 | Officiels Anthropic | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 31.4k | ELEVE | Plugin `skill-creator` — `/plugin install skill-creator@claude-plugins-official` |
| A.4 | Officiels Anthropic | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 46.3k | TRES ELEVE | Notebook `CMA_coordinate_specialist_team` — 1 coordinateur + 3 specialistes |
| A.5 | Officiels Anthropic | [anthropics/claude-quickstarts](https://github.com/anthropics/claude-quickstarts) | 17.2k | ELEVE | Projet `Autonomous Coding Agent` — 2-agent avec persistence git |
| B.1 | Outils fonctionnels | [github/spec-kit](https://github.com/github/spec-kit) | 117.3k | TRES ELEVE | Commande `/speckit.specify` — Spec-Driven Development |
| B.2 | Outils fonctionnels | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 85.4k | TRES ELEVE (multi-semaines) | `npx claude-mem install` — memoire persistante SQLite + ChromaDB |
| B.3 | Outils fonctionnels | [yamadashy/repomix](https://github.com/yamadashy/repomix) | 26.8k | MODERE | Pack tout un repo en 1 fichier XML/Markdown pour coller dans un LLM |
| C.1 | Sources d'inspiration | [affaan-m/ECC](https://github.com/affaan-m/ECC) | 224.8k | A cherry-pick | Skill `loop-design-check` — review de boucles agent orientees objectif |
| C.2 | Sources d'inspiration | [obra/superpowers](https://github.com/obra/superpowers) | 243.8k | A cherry-pick | Skill TDD `RED-GREEN-REFACTOR` — discipline phase gates |
| C.3 | Sources d'inspiration | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 47.8k | Discovery ponctuel | Index curate en 9 categories — "je cherche un skill pour X" |
| C.4 | Sources d'inspiration | [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | 61.8k | A cherry-pick | 84 best practices — patterns workflow/orchestration/memory/security |
| D | Compression tokens | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | 67.9k | Si contexte trop bruyant | Proxy CLI Rust — compresse git/npm/pytest/docker avant contexte |
| D | Compression tokens | [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom) | 55.6k | Si contexte trop bruyant | Lib+proxy+MCP server — compresse logs/RAG/fichiers/historique |
| D | Compression tokens | [mksglu/context-mode](https://github.com/mksglu/context-mode) | 18.5k | Si sessions longues MCP | MCP server — sandbox tool output + memoire de session |
| D | Compression tokens | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 79.7k | Si reponses trop bavardes | Skill de style — reponses ultra compactes (-65% tokens) |

**Comment lire ce tableau** : A = va chercher la verite chez Anthropic. B = va installer un outil qui resout un probleme precis (memoire, spec-driven, packaging repo). C = va piocher des idees/patterns sans tout copier. D = va reduire la facture en tokens si ton contexte est bruyant.

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
- **Detail** : voir `plugins.md` dans ce skill (setup Yann : actifs/desactives + regles)

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

---

## C. Sources d'inspiration (pour cherry-pick, pas copier)

### C.1 affaan-m/ECC (ex-everything-claude-code) — 224.8k stars
- **URL** : https://github.com/affaan-m/ECC — **RENOMME** depuis mai 2026 (redirect 301 depuis l'ancienne URL `everything-claude-code`)
- **Contenu** : Systeme d'optimisation de performance de harness agentique — skills, instincts, memoire, securite, research-first dev. Multi-harness : Claude Code, Codex, Opencode, Cursor
- **Ce qu'on en tire** : Patterns orchestration multi-agent, architecture agents a grande echelle
- **Attention** : Enorme projet, cherry-pick ce qui est pertinent. Verifier `full_name` via l'API si l'URL casse encore (repo tres actif, renommages possibles)

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

## D. Compression de contexte / tokens

Quatre outils qui attaquent le meme probleme (le cout en tokens du contexte) a des couches differentes du pipeline. Se chevauchent partiellement — pas forcement a cumuler tous les 4.

| Outil | Couche principale | Ce qu'il optimise | Entree / sortie | Overlap avec les autres | Usage ideal | Limite principale |
|-------|-------------------|--------------------|------------------|--------------------------|-------------|--------------------|
| **rtk-ai/rtk** (67.9k★) | Proxy / preprocesseur CLI | La sortie terminal avant qu'elle entre dans le contexte | Entree : commandes shell — Sortie : texte compresse | Fort overlap avec headroom sur la compression de sorties CLI ; faible avec Caveman | Logs bruyants : git, npm, pytest, docker, etc. | Ne traite pas les gros artefacts hors CLI et ne gere pas la memoire de session |
| **headroomlabs-ai/headroom** (55.6k★) | Couche de compression de contexte (lib + proxy + MCP server) | Le pipeline de contexte dans son ensemble | Entree : sorties d'outils, logs, RAG, fichiers, historique — Sortie : contexte compacte | Overlap partiel avec RTK sur les logs/CLI, partiel avec context-mode sur les tool outputs | Quand plusieurs sources de bruit alimentent le LLM en meme temps | Plus large, donc moins specialise ; la valeur depend de la stack autour |
| **mksglu/context-mode** (18.5k★) | MCP server / couche de gestion de contexte | Les gros outputs d'outils et la continuite de session | Entree : appels d'outils — Sortie : resumes + indexation locale | Overlap partiel avec headroom sur les tool outputs ; quasi aucun avec Caveman ; complementaire de RTK | Workflows Claude Code / MCP avec beaucoup de sorties a conserver et retrouver | Pas un simple compresseur : ajoute une couche d'indexation et de memoire, donc plus de complexite |
| **JuliusBrussee/caveman** (79.7k★) | Skill / style de generation | Le texte genere par l'agent lui-meme | Entree : instructions de reponse — Sortie : formulation ultra compacte | Overlap surtout conceptuel avec les autres sur la reduction de tokens ; peu de chevauchement technique direct | Quand les reponses de l'agent sont trop bavardes et qu'on veut une communication tres dense | Ne remplace pas la gestion du contexte ni la compression des outils ; agit sur la forme du message |

**Lecture** : RTK et headroom se chevauchent le plus (compression CLI/logs) — probablement redondant d'installer les deux. context-mode est complementaire (memoire de session + indexation, pas juste de la compression). Caveman est orthogonal aux 3 autres : il agit sur la sortie du modele, pas sur son entree.

**A tester en priorite si le sujet t'interesse** : `headroom` (le plus complet, MCP server + proxy + lib, et couvre large) ou `rtk` (le plus simple, binaire Rust unique, zero dependance) selon si tu veux une solution large ou minimaliste.

---

## E. Verifier les MAJ d'un repo

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

## F. Derniere verification : 02/07/2026

| Repo | Stars (delta mai) | Derniere MAJ | Statut |
|------|---------------------|--------------|--------|
| anthropics/skills | 157.5k (+28.5k) | 01/07/2026 | TRES ACTIF — claude-api sync Sonnet 5 + Managed Agents |
| anthropics/courses | 22k | 13/11/2025 | GELE depuis 8 mois |
| anthropics/claude-plugins-official | 31.4k (+12.7k) | 02/07/2026 | TRES ACTIF — `idmp-plugin` ajoute, bump continu des starter packs (data-agent-kit, migration-to-aws, carta-investors, convex) |
| anthropics/claude-cookbooks | 46.3k (+4k) | 30/06/2026 | ACTIF — `roadtrip_planner` managed agent, benchmark agentic search reproduit sur Messages API |
| anthropics/claude-quickstarts | 17.2k (+0.7k) | 28/05/2026 | GELE depuis ~5 semaines |
| github/spec-kit | 117.3k (+24.3k) | 01/07/2026 | TRES ACTIF — support script type `py`, extension Analytics catalog communautaire |
| thedotmack/claude-mem | 85.4k (+12.4k) | 01/07/2026 | TRES ACTIF. Toujours NON installe localement → `npx claude-mem install` si besoin |
| yamadashy/repomix | 26.8k (+2.4k) | 02/07/2026 | ACTIF |
| affaan-m/ECC (ex-everything-claude-code) | 224.8k (+49.8k) | 01/07/2026 | **RENOMME** (redirect depuis l'ancien nom) — TRES ACTIF, `loop-design-check`, Stop hook qualite thinking, `growth-log`, pack React Native/Expo |
| obra/superpowers | 243.8k (+62.8k) | 01/07/2026 | TRES ACTIF — v6.1.0 : bootstrap allege, install marketplace Codex, support Gemini retire |
| hesreallyhim/awesome-claude-code | 47.8k (+5k) | 29/06/2026 | ACTIF |
| shanraisshan/claude-code-best-practice | 61.8k (+10.3k) | 02/07/2026 | TRES ACTIF |

### Decouvertes interessantes (juin-juillet 2026)

**1. `github/spec-kit`** — franchit les 100k stars (117k, +24k en 2 mois) : devient un standard incontournable. Nouveau support `py` script type + resolution interpreteur Python.

**2. `obra/superpowers` v6.1.0** — evolution vs v5.1.0 (mai) :
- Simplification du bootstrap par session (plus leger)
- Ajoute l'installation via marketplace Codex (multi-harness)
- Retire le support Gemini CLI — recentrage sur l'ecosysteme Claude Code + Codex

**3. `affaan-m/ECC` — changement de nom** : `everything-claude-code` → `ECC`. L'ancienne URL redirige (301) mais **verifier `gh api` en cas d'echec silencieux** (les clients non-suiveurs de redirect peuvent planter). Nouveautes : `loop-design-check` (design/review de boucles agent orientees objectif), Stop hook de verification qualite du thinking en fin de session, `growth-log` (methodologie de capture d'apprentissage).

**4. `anthropics/claude-cookbooks`** — nouveau notebook `roadtrip_planner` dans managed_agents, et un cookbook de reproduction du benchmark agentic search officiel directement via l'API Messages (utile pour eval interne).

**5. `anthropics/claude-plugins-official`** — franchit 31k stars (+12.7k en 2 mois), rythme de bump tres soutenu sur les starter packs (quasi-quotidien). Nouveau plugin `idmp-plugin`.

### Historique (mai 2026, pour reference)

**1. `anthropics/claude-cookbooks/managed_agents/`** — 12 notebooks dont :
- `CMA_coordinate_specialist_team.ipynb` : 1 coordinateur + 3 specialistes avec toolsets scopes (parfait pour archi PMO)
- `CMA_remember_user_preferences.ipynb` : memory stores read/write par user + read-only partage
- `CMA_verify_with_outcome_grader.ipynb` : grade-and-revise itere jusqu'a passage rubrique
- `CMA_orchestrate_issue_to_pr.ipynb` : issue → fix → PR → CI → review → merge
- `CMA_gate_human_in_the_loop.ipynb` : HITL via outils custom decide/escalate

**2. `anthropics/claude-plugins-official` nouveaux plugins (mai)** :
- `snowflake-cortex-code` : plugin officiel Snowflake (a tester en priorite)
- `oracle-data-platform` : pattern data platform
- `skill-creator` (officiel) : `/plugin install skill-creator@claude-plugins-official` — workflow iteratif intent → draft → tests subagents → eval-viewer → benchmark → optimisation description

**3. ECC skills potentiellement utiles** (a explorer ponctuellement) :
- `agent-harness-construction`, `autonomous-loops`, `continuous-agent-loop`, `agent-introspection-debugging`
- `context-budget`, `cost-aware-llm-pipeline`
- `agent-eval`, `benchmark`, `canary-watch`
- `data-scraper-agent`, `dashboard-builder`
- `documentation-lookup`, `codebase-onboarding`

### Repos NON ajoutes (volonte explicite Yann mai 2026)

Cette liste est **fermee** : ne pas ajouter de nouveau repo sans validation explicite.
