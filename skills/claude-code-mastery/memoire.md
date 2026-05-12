# Memoire dans Claude Code — Guide complet

> Officiel Anthropic + extensions communautaires.
> Source principale : https://code.claude.com/docs/en/memory

---

## 1. Systeme natif (officiel Anthropic)

### 1.1 CLAUDE.md — Le coeur

| Fichier | Scope | Charge quand |
|---------|-------|-------------|
| `~/.claude/CLAUDE.md` | Global (tous projets) | Chaque message |
| `./CLAUDE.md` | Projet (racine repo) | Chaque message (surcharge global) |
| `CLAUDE.local.md` | Personnel (gitignore) | Chaque message |

**Principes officiels** :
- Court (< 200 lignes ideal)
- Tables > prose (3x plus dense en tokens)
- Actionnable ("DO X" pas "X is important")
- Lier vers `docs/` pour les details

**Anti-patterns** :
- \> 2000 lignes (Claude skimme, perd en precision)
- Prose explicative (tokens gaspilles)
- Secrets hardcodes
- Doc d'archi complete (lier vers `docs/`)
- Duplication avec `rules/`

### 1.2 Rules — Regles permanentes

| Aspect | Detail |
|--------|--------|
| Dossier | `~/.claude/rules/*.md` (global) ou `.claude/rules/*.md` (projet) |
| Chargement | **A CHAQUE MESSAGE** (comme CLAUDE.md) |
| Format | Markdown pur, pas de frontmatter |
| Path-scoping | Possible via YAML frontmatter (charge seulement pour certains fichiers) |

**Exemple path-scoped** :
```yaml
---
paths:
  - "src/api/**/*.ts"
  - "src/services/**"
---
# Regles API
- Toujours valider les inputs avec Zod
- Jamais de raw SQL
```

**Quand utiliser rules/ vs CLAUDE.md** :
- `CLAUDE.md` = profil, stack, conventions globales, URLs, commandes
- `rules/` = regles comportementales par domaine (securite, style, git, tests)

### 1.3 Auto-Memory — Claude ecrit tout seul

**Fonctionnement** :
- Claude capture automatiquement : decisions, patterns, bugs fixes, preferences
- Stocke dans `~/.claude/projects/{projet}/memory/`
- Fichier index : `MEMORY.md` (premieres 200 lignes ou 25KB charges auto)
- Fichiers thematiques : `{topic}.md` avec frontmatter (name, type, description)

**Types de memoire** :
- `user` — profil, preferences, expertise
- `feedback` — corrections, validations (ce qui marche / ne marche pas)
- `project` — decisions, deadlines, contexte metier
- `reference` — pointeurs vers ressources externes

**Commandes** :
| Commande | Effet |
|----------|-------|
| `/memory` | Ouvre le gestionnaire (voir/editer/toggle) |
| Desactiver | `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` ou toggle dans `/memory` |

### 1.4 Auto-Dream — Consolidation automatique

**Fonctionnement** :
- Lance un sub-agent de consolidation toutes les 24h (si 5+ enregistrements accumules)
- 4 etapes : Orient → Collect Signals → Consolidate (merge doublons) → Prune & Index
- Convertit dates relatives → absolues
- Tourne en arriere-plan (ne bloque pas)

**Commande** :
| Commande | Effet |
|----------|-------|
| `/dream` | Lancer manuellement la consolidation |

**Quand utiliser** :
- Apres une longue session avec beaucoup de decisions
- Quand MEMORY.md commence a avoir des doublons
- Avant de reprendre un projet apres une pause

---

## 2. claude-mem — Memoire persistante avancee (46.1k stars)

> Source : https://github.com/thedotmack/claude-mem
> Alternative communautaire pour projets multi-semaines.

### 2.1 Architecture

| Composant | Tech | Role |
|-----------|------|------|
| Hooks | TypeScript (5 lifecycle hooks) | Capture auto chaque interaction |
| Worker | Express + Bun (port 37777) | API HTTP pour stockage async |
| Database | SQLite3 (`~/.claude-mem/claude-mem.db`) | Stockage persistant sessions + observations |
| Vector DB | ChromaDB + ONNX (all-MiniLM-L6-v2) | Recherche semantique locale, zero API |

### 2.2 Recherche 3 couches (token economy)

| Couche | Fonction | Cout tokens |
|--------|----------|------------|
| 1. `search()` | Index compact (FTS5 + Chroma hybrid) | ~50-100 / resultat |
| 2. `timeline()` | Contexte chrono autour d'un resultat | Variable |
| 3. `get_observations()` | Details complets pour IDs filtres | ~500-1000 / observation |

**Economie** : ~10x reduction vs tout charger d'un coup. Pattern recommande : 2500-4000 tokens total vs 20000+ en approche naive.

### 2.3 Hooks lifecycle

| Hook | Trigger | Action |
|------|---------|--------|
| SessionStart | Demarrage | Injecte observations compressees dans contexte |
| UserPromptSubmit | Chaque prompt | Log du prompt |
| PostToolUse | Apres chaque tool | Envoie output au worker (async, ~8ms) |
| Stop | Session pause | Genere summary |
| SessionEnd | Fermeture | Nettoyage |

### 2.4 Installation

```bash
npx claude-mem install
# OU
/plugin install claude-mem
```

Auto-configure : hooks dans `~/.claude/hooks/`, worker Bun, SQLite + ChromaDB.

### 2.5 Configuration

Fichier : `~/.claude-mem/settings.json`

```json
{
  "MODEL": "sonnet",
  "WORKER_PORT": 37777,
  "SKIP_TOOLS": "ListMcpResourcesTool,SlashCommand",
  "FULL_OBSERVATIONS_N": 3,
  "LOG_LEVEL": "info"
}
```

Web UI : `http://localhost:37777` pour config interactive.

### 2.6 Quand utiliser quoi

| Contexte | Natif (CLAUDE.md + auto-memory) | claude-mem |
|----------|----|---|
| Projets < 3 jours | Suffisant | Overkill |
| Taches courtes | Suffisant | Non necessaire |
| Projets multi-semaines | Limite (200 lignes) | Recommande |
| Debugging multi-session | Perte de contexte | Historique complet |
| Refactors distribues | Coherence difficile | Architecture maintenue |
| Cout token critique | Injection simple | 10x savings via 3 couches |

**Approche recommandee** : complementaire. Natif pour les directives et regles. claude-mem pour l'archive et la recherche historique.

---

## 3. Patterns Boris Cherny (recommande, pas normatif)

| Fichier | Contenu | Officiel ? |
|---------|---------|------------|
| `tasks/todo.md` | Plan avec items cochables | Non — best practice |
| `tasks/lessons.md` | Lecons apprises (MAJ apres corrections) | Non — best practice |

**Workflow Boris** :
1. Ecrire le plan dans `tasks/todo.md`
2. Valider avant implementation
3. Cocher au fur et a mesure
4. MAJ `tasks/lessons.md` apres corrections
5. Relire les lecons au debut de la session suivante

---

## 4. Resume : ou mettre quoi

| Information | Ou la mettre | Charge quand |
|-------------|-------------|-------------|
| Profil, stack, conventions | `CLAUDE.md` | Chaque message |
| Regles code/git/securite | `rules/*.md` | Chaque message |
| Decisions projet, deadlines | Auto-memory (`memory/`) | SessionStart (200 lignes) |
| Historique debug, patterns | claude-mem (si installe) | SessionStart (compress) |
| Plan de taches en cours | `tasks/todo.md` (Boris pattern) | Quand invoque |
| Lecons apprises | `tasks/lessons.md` (Boris pattern) | Quand invoque |
