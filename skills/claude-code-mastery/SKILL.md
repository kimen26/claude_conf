---
name: claude-code-mastery
description: "Bonnes pratiques Claude Code officielle Anthropic : architecture ~/.claude, nomenclature (agents, skills, hooks, MCP), CLAUDE.md ideal, economie de tokens, CLI avance. Active des que l'utilisateur demande : config claude code, best practice, architecture ~/.claude, nommer un agent/skill/hook, optimiser tokens, CLAUDE.md, settings.json, MCP server, ou veut la norme officielle."
family: dev
origin: Anthropic Official + Community Best Practices
---

# SKILL : claude-code-mastery

> La reference quotidienne pour configurer, nommer et optimiser Claude Code selon les normes Anthropic.

---

## Quand activer ce skill

- L'utilisateur configure ou restructure son `~/.claude/`
- Il cree un agent, skill, hook ou MCP server et veut la norme
- Il veut optimiser sa consommation de tokens
- Il demande "c'est quoi la vraie norme ?" ou "best practices Claude Code"
- Mots-cles : `CLAUDE.md`, `settings.json`, `hooks`, `agents`, `skills`, `MCP`, `tokens`, `~/.claude`

---

## A. Architecture officielle ~/.claude/

### A.1 Arborescence canonique

```
~/.claude/                          # CONFIG GLOBALE (tous projets)
|-- CLAUDE.md                       # Memoire persistante globale (profil, stack, regles)
|-- settings.json                   # Env vars, hooks, MCP servers, preferences
|-- keybindings.json                # Raccourcis clavier
|-- agents/                         # Sous-agents reutilisables
|   |-- code-reviewer.md            # YAML frontmatter + instructions MD
|   |-- architect.md
|   `-- tdd-guide.md
|-- skills/                         # Knowledge documents par domaine
|   |-- python/
|   |   `-- SKILL.md
|   |-- security/
|   |   `-- SKILL.md
|   `-- {domain}/
|       `-- SKILL.md                # + fichiers .md annexes optionnels
|-- hooks/                          # Scripts evenementiels
|   |-- session-start.js
|   |-- sql-guard.js
|   `-- pre-tool-use.py
|-- rules/                          # Regles comportementales (optionnel)
|   |-- coding-style.md
|   |-- git-workflow.md
|   `-- security.md
|-- contexts/                       # Contextes specialises (optionnel)
|   `-- about-me.md
`-- .mcp.json                       # MCP servers (alternatif a settings.json)

./                                  # CONFIG PROJET (racine du repo git)
|-- CLAUDE.md                       # Instructions projet (surcharge le global)
|-- .claude/
|   |-- settings.json               # Env vars + hooks specifiques projet
|   |-- agents/                     # Agents specifiques projet
|   `-- .mcp.json                   # MCP servers specifiques projet
```

### A.2 Ordre de chargement (priorite croissante)

1. `~/.claude/settings.json` (global)
2. `~/.claude/CLAUDE.md` (global)
3. `~/.claude/rules/*.md` (global)
4. `./.claude/settings.json` (projet)
5. `./CLAUDE.md` (projet) -- **SURCHARGE le global**
6. Skills actives (a la demande)
7. Agents (quand invoques)

**Important** : `CLAUDE.md` est injecte dans le contexte a CHAQUE message. Il doit rester court et synthetique.

---

## B. Nomenclature officielle

### B.1 Agents

| Aspect | Norme |
|--------|-------|
| Fichier | `~/.claude/agents/{name}.md` |
| Nommage | `kebab-case` lowercase (ex: `code-reviewer`, `tdd-guide`) |
| Suffixes courants | `-reviewer`, `-guide`, `-assistant`, `-resolver` |
| Frontmatter | YAML obligatoire : `name`, `description`, `model`, `tools` |

**Frontmatter agent :**

```yaml
---
name: Code Reviewer
description: Reviews code for quality and security. Use after writing code.
model: claude-sonnet-4-6          # sonnet|opus|haiku
temperature: 0.3                   # 0.0 (deterministe) a 1.0 (creatif)
maxTurns: 3                        # iterations max
permissionMode: allow-all          # allow-all|block-all|prompt
tools:                             # Tools autorises
  - Bash
  - Read
  - Edit
  - Grep
  - Glob
disallowedTools:                   # Tools bloques
  - Write
  - RemoteTrigger
skills:                            # Skills a charger avec l'agent
  - python
  - security
mcpServers:                        # MCP servers a connecter
  - github
effort: high                       # low|medium|high
---
```

**Activation :** `claude --agent=code-reviewer` ou via le parent qui lance `Agent(subagent_type="code-reviewer")`

### B.2 Skills

| Aspect | Norme |
|--------|-------|
| Dossier | `~/.claude/skills/{domain}/SKILL.md` |
| Nommage domaine | `kebab-case` lowercase (ex: `prompt-craft`, `ipd-snowflake`) |
| Fichier principal | Toujours `SKILL.md` |
| Fichiers annexes | `{sous-domaine}.md` dans le meme dossier |

**Frontmatter skill :**

```yaml
---
name: prompt-craft
description: "Description courte (1-2 lignes) pour le matching auto."
family: impact                     # Famille logique (optionnel)
origin: Domaine                    # Provenance (optionnel)
---
```

**Activation auto :** Claude matche la `description` avec le prompt utilisateur.

### B.3 Hooks

| Aspect | Norme |
|--------|-------|
| Dossier | `~/.claude/hooks/` |
| Nommage | `{suffixe-descriptif}.js` ou `.py` (ex: `sql-guard.js`) |
| Config | Dans `settings.json` > `hooks` |
| Langage | JS (Node) ou Python (avec shebang) |

**Evenements principaux :**

| Evenement | Quand | Peut bloquer ? |
|-----------|-------|----------------|
| `SessionStart` | Demarrage session | Non |
| `UserPromptSubmit` | Avant traitement prompt | **OUI** (exit 2) |
| `PreToolUse` | Avant execution d'un tool | **OUI** (exit 2) |
| `PostToolUse` | Apres execution reussie | Non |
| `SubagentStart/End` | Cycle sous-agent | Non |
| `PreCompact` | Avant compaction contexte | Non |
| `Stop` | Session terminee | Non |

**Exit codes :** `0` = OK | `1` = Erreur non-bloquante | `2` = **BLOCK**

### B.4 MCP Servers

| Aspect | Norme |
|--------|-------|
| Config | `settings.json` > `mcpServers` ou `.mcp.json` |
| Nommage | lowercase, max 32 chars (ex: `github`, `cobalt-docs`) |
| Transport | `http` (recommande) ou `stdio` |
| Secrets | Toujours `${VAR_NAME}` -- jamais en dur |

**Scopes :** Global (`~/.claude/`) | Projet (`.claude/`) | Local (`~/.claude/.mcp-local.json`)

### B.5 Rules vs Skills

| | Rules (`~/.claude/rules/`) | Skills (`~/.claude/skills/`) |
|---|---|---|
| Chargement | **Toujours** (chaque message) | **A la demande** (matching description) |
| Format | MD pur, pas de frontmatter | MD avec YAML frontmatter |
| Usage | Regles universelles (style, git, securite) | Connaissances domaine specifiques |

---

## C. CLAUDE.md ideal

### C.1 Principes

1. **Court** : charge a chaque message = chaque token compte
2. **Synthetique** : tableaux et listes, pas de prose
3. **Actionnable** : des regles, pas des descriptions
4. **Hierarchise** : global = profil + regles ; projet = stack + conventions + pieges

### C.2 Template Global (~/.claude/CLAUDE.md)

```markdown
# Profil
- Nom, entreprise, role
- Langue par defaut (FR/EN)

## Stack
| Outil | Usage | Config |
|-------|-------|--------|

## Regles operationnelles
- Code : lire avant editer, changements minimaux
- SQL : confirmer DROP/DELETE
- Git : conventional commits
- Securite : secrets en .env uniquement

## Agents actifs
(liste avec quand les utiliser)
```

### C.3 Template Projet (./CLAUDE.md)

```markdown
# Projet {Nom}
- Stack, statut, URLs

## Structure
(arborescence cle)

## Conventions
- IDs, nommage, tags

## Commandes courantes

## Pieges connus
```

### C.4 Anti-patterns CLAUDE.md

| A eviter | Pourquoi |
|----------|----------|
| > 2000 lignes | Depasse le budget contexte utile |
| Prose explicative | Tokens gaspilles, preferer tableaux |
| Secrets (tokens, creds) | Securite -- utiliser `${VAR}` |
| Doc exhaustive d'archi | Lien vers `docs/` plutot |
| Historique des changements | C'est le job de git |
| Duplication avec rules/ | Si dans rules/, pas dans CLAUDE.md |

### C.5 Reference : CLAUDE.md de Boris Cherny (dev officiel Claude Code)

6 principes cles (applicable a tout projet) :

1. **Plan mode par defaut** -- mode plan pour toute tache 3+ etapes ou decision d'archi
2. **Strategie sous-agents** -- deleguer recherche/exploration, garder le contexte principal propre
3. **Boucle auto-amelioration** -- apres correction, ecrire dans `tasks/lessons.md` pour ne pas repeter
4. **Verification avant "done"** -- prouver que ca marche (tests, logs, diff)
5. **Exiger l'elegance (equilibre)** -- "existe-t-il une maniere plus elegante ?" sauf fix trivial
6. **Bug fixing autonome** -- corriger sans demander d'accompagnement, zero context switch pour l'user

---

## D. Economie de tokens -- Quick Reference

> Detail complet dans `token-economy.md`

### D.1 Quick wins

| Action | Economie | Comment |
|--------|----------|---------|
| `ENABLE_TOOL_SEARCH=true` | ~14K tokens/tour | `settings.json` > `env` |
| Reduire skills inutilises | ~2-5K/tour par skill | Supprimer ou sortir de `rules/` |
| `/compact` aux milestones | Reset contexte partiel | Habituer a taper regulierement |
| `/clear` entre taches | Reset total | Nouveau contexte propre |
| `--bare` pour SDK/scripts | Startup 10x rapide | Skip CLAUDE.md + settings + MCP |
| `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | 3x moins cher par agent | Pour workers simples |

### D.2 Cout quadratique des messages

```
Cout message N = (tous les precedents) + message N
Total ~ S x N(N+1) / 2
```

Message 30 coute **31x** message 1. Conclusion : `/compact` ou `/clear` regulierement.

### D.3 Cache prompt (5 min TTL)

Apres 5 min d'inactivite, le cache expire. Le message suivant re-traite TOUT au prix fort. Travailler en sessions concentrees.

---

## E. CLI avance

| Flag/Commande | Usage |
|---------------|-------|
| `--bare` | SDK/scripts non-interactifs, skip config |
| `--add-dir ../repo` | Acces a un 2e repo |
| `--agent=name` | Lancer un agent custom |
| `/voice` | Input vocal (hold spacebar en CLI) |
| `/add-dir` | Ajouter dossier en cours de session |
| `/compact` | Compacter le contexte |
| `/clear` | Reset complet |
| `/model opus` | Changer de modele |
| `/fast` | Toggle mode rapide (meme modele) |

---

## F. Modeles -- quand utiliser quoi

| Modele | Cas d'usage | Cout relatif |
|--------|------------|--------------|
| **Haiku 4.5** | Agents frequents, taches simples | 1x |
| **Sonnet 4.6** | Dev quotidien, code complexe | 3x |
| **Opus 4.6** | Architecture, raisonnement profond | 15x |

---

## G. Plugins (officiel Anthropic — 2026)

### G.1 Systeme de plugins

Claude Code a un systeme de plugins officiel avec marketplace integree.

| Commande | Effet |
|----------|-------|
| `/plugin` | Ouvre le gestionnaire de plugins |
| `/plugin install {name}@claude-plugins-official` | Installer un plugin |
| `/plugin marketplace add {owner/repo}` | Ajouter une marketplace tierce |

### G.2 Structure d'un plugin

```
my-plugin/
├── .claude-plugin/plugin.json      # Manifest (nom, version, description)
├── agents/                          # Agents du plugin
├── skills/                          # Skills du plugin
├── hooks/                           # Hooks du plugin
├── commands/                        # Slash commands
├── .mcp.json                        # MCP servers (optionnel)
└── README.md
```

### G.3 Plugin vs Skill (distinction)

| | Plugin | Skill |
|---|---|---|
| **Nature** | Package distributable complet | Fichier de connaissance |
| **Contient** | Skills + agents + hooks + MCP | Instructions MD |
| **Installation** | `/plugin install` | Copier dans `skills/` |
| **Partage** | Via marketplace GitHub | Copier-coller |

### G.4 Plugins officiels notables (33 dans claude-plugins-official)

| Plugin | Ce qu'il fait |
|--------|--------------|
| `frontend-design` | UI production-ready (auto-invoque) — 277k+ installs |
| `code-review` | Review avec 5 agents paralleles |
| `pr-review-toolkit` | Analyse PR (6 agents specialises) |
| `security-guidance` | Warnings securite (9 patterns, hook PreToolUse) |
| `feature-dev` | 7 phases feature dev (3 agents) |
| `skill-creator` | Creer ses propres skills en conversationnel |
| `ralph-wiggum` | Boucles iteratives autonomes |
| `commit-commands` | Helpers commit/push/PR |
| 12x LSP plugins | Support langages (C/C++, Go, Java, Python, Rust, TS...) |

Ref : https://github.com/anthropics/claude-plugins-official (16.6k stars)

---

## H. Features 2026 (recentes)

| Feature | Quoi | Statut |
|---------|------|--------|
| **Auto-Memory** | Claude ecrit ses propres observations dans `memory/` | GA |
| **Auto-Dream** (`/dream`) | Consolidation memoire auto toutes les 24h | GA |
| **`/memory`** | Gestionnaire de memoire (voir, editer, toggle) | GA |
| **Plugins** (`/plugin`) | Marketplace + installation + creation | GA |
| **`claude --chrome`** | Browser integre (DevTools Chrome) | Beta |
| **Agent Teams** | Multi-instance, shared task list | Experimental |
| **Worktrees** (`--worktree`) | Isolation git par agent/feature | GA |
| **Scheduled Tasks** | Jobs recurrents sur infra cloud Anthropic | GA |
| **Auto Mode** | Reduit les prompts d'approbation | GA |
| **Context Editing** | Supprime outputs tools obsoletes du contexte (-84%) | GA |
| **1M tokens context** | Fenetre de contexte complete | GA |

---

## Fichiers annexes

| Fichier | Contenu |
|---------|---------|
| `courses.md` | 5 cours officiels Anthropic + cookbooks + quickstarts |
| `token-economy.md` | Audit 926 sessions + 10 regles challengees |
| `tips-avances.md` | Boris Cherny, patterns avances |
| `repos.md` | Catalogue repos Git officiels + communautaires (MAJ avril 2026) |
| `memoire.md` | Systeme memoire natif + claude-mem (46.1k stars) |
| `multi-agent.md` | Patterns orchestration, worktrees, Agent Teams |
| `methodologies.md` | Spec-driven (spec-kit 86.8k) + TDD (superpowers 145k) |
| `ui-frontend.md` | frontend-design officiel, chrome, Obsidian, repomix |
