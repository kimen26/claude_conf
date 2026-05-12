# Multi-Agent — Patterns d'orchestration Claude Code

> Comment utiliser les sous-agents et Agent Teams efficacement.

---

## 1. Concepts fondamentaux

### 1.1 Parent vs sous-agent

- Le sous-agent **ne voit PAS** la conversation parent
- Son prompt doit etre **auto-suffisant** (comme briefer un collegue qui vient d'arriver)
- Chaque agent = contexte frais = CLAUDE.md recharge

### 1.2 Foreground vs background

| Mode | Quand | Comportement |
|------|-------|-------------|
| Foreground (defaut) | Tu as besoin du resultat pour continuer | Bloque jusqu'a completion |
| Background (`run_in_background: true`) | Taches independantes en parallele | Notifie quand fini |

### 1.3 Types de sous-agents disponibles

| Type | Specialite |
|------|-----------|
| `general-purpose` | Recherche, taches multi-etapes |
| `Explore` | Exploration codebase rapide (glob, grep, read) |
| `Plan` | Planification d'implementation |
| `code-reviewer` | Revue de code |
| `security-reviewer` | Analyse securite |
| `build-error-resolver` | Fix erreurs de build |
| `database-reviewer` | SQL, schemas, performance |
| `python-reviewer` | Code Python |
| `tdd-guide` | Test-driven development |
| `refactor-cleaner` | Nettoyage code mort |
| `doc-updater` | Documentation |

---

## 2. Patterns d'orchestration

### 2.1 Fan-out / Fan-in (parallele)

Lancer N agents en parallele, collecter les resultats, synthetiser.

**Cas d'usage** : review multi-perspective avant commit

```
Agent 1: security-reviewer  ─┐
Agent 2: code-reviewer       ├─→ Synthese parent
Agent 3: database-reviewer   ─┘
```

**Regle** : tous les `Agent()` dans UN SEUL message = parallele. Sequentiel sinon.

### 2.2 Pipeline sequentiel

Agent 1 output → Agent 2 input.

```
planner (plan) → tdd-guide (tests) → code-reviewer (validation)
```

**Regle** : attendre le resultat de chaque etape avant de lancer la suivante.

### 2.3 Multi-perspective

Meme question, roles differents :
- Agent "factual reviewer" — verifie les faits
- Agent "senior engineer" — qualite du code
- Agent "security expert" — vulnerabilites

### 2.4 Worktree isolation

```
Agent(isolation: "worktree")
```

- Cree un git worktree temporaire (branche separee)
- L'agent ecrit du code sans toucher la branche principale
- Cleanup auto si aucun changement
- Retourne le chemin et la branche si des changements existent

**Cas d'usage** : experimentation de code, feature branches paralleles

---

## 3. Agent Teams (experimental)

> Feature flag : `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`

### 3.1 Principe

Multi-instance Claude Code avec coordination :
- 1 team lead + N teammates
- Worktrees isoles (zero conflit git)
- Shared task list + peer messaging

### 3.2 Quand utiliser

- 3-5 agents optimal (> 5 = overhead > gain)
- Modules independants en parallele
- Debugging (hypotheses concurrentes)
- Cross-layer coordination (frontend + backend + DB)

### 3.3 Docs

https://code.claude.com/docs/en/agent-teams

---

## 4. Ecrire un bon prompt de sous-agent

### Bon prompt

```
"Review migration 0042_user_schema.sql for safety.
Context: adding NOT NULL column to 50M-row table.
Existing rows get a backfill default.
I want independent verification on locking behavior.
Report: is this safe, and if not, what breaks?"
```

**Inclure** :
- QUOI faire
- POURQUOI (contexte)
- Ce qu'on a deja verifie / ecarte
- Format de reponse souhaite

### Mauvais prompt

```
"Based on your findings, fix the bug"
```

**Probleme** : delegue la synthese a l'agent au lieu de la faire toi-meme.

---

## 5. Gestion des couts

| Strategie | Impact |
|-----------|--------|
| `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | 3x moins cher par agent worker |
| Ne pas spawner un agent pour un simple `Read` | Utiliser le tool directement |
| Parallele dans UN message (pas sequentiel) | 1 chargement contexte au lieu de N |
| `Explore` au lieu de `general-purpose` pour les recherches codebase | Plus rapide et moins cher |

---

## 6. Anti-patterns

| Anti-pattern | Alternative |
|-------------|------------|
| Agent pour lire 1 fichier | `Read` directement |
| Agents sequentiels quand independants | Parallele dans 1 message |
| Prompt vague sans contexte | Brief complet auto-suffisant |
| "Based on research, implement" | Faire la synthese soi-meme, donner des instructions precises |
| > 5 agents simultanes | 3-5 optimal |
| Deleguer la comprehension | Comprendre d'abord, deleguer l'execution |

---

## 7. Memoire — les 4 couches (vue agent-centric)

| Couche | Ou | Charge quand | Qui voit |
|--------|-----|-------------|---------|
| **Conversation** | RAM contexte courant | Pendant la session | Bot actif uniquement |
| **Globale** | `~/.claude/CLAUDE.md` + `~/.claude/memory/MEMORY.md` + `skills/`, `rules/` | Auto a chaque message | Tous bots (parent + sub) |
| **Projet** | `./CLAUDE.md` + `./.claude/` | Auto si lance depuis le repo | Tous bots dans le repo |
| **Agent** | `~/.claude/agent-memory/{name}/` via `memory: user` dans frontmatter | Auto pour CET agent a chaque invocation | Cet agent uniquement, cross-conversation |

**Implication critique** : un sub-agent ne voit PAS la conversation parent. Il voit globale + projet + sa propre couche agent. Tout ce que le parent a "appris" dans la conversation courante doit etre **passe explicitement** dans le prompt d'invocation.

---

## 8. Consolidation — parent ou sub-agent dedie ?

**Critere de decision** :

| Cas | Qui consolide | Pourquoi |
|-----|--------------|----------|
| Synthese simple (concat, dedup, pick best) | Parent | Il a le contexte de mission, c'est 1 tour de plus |
| Synthese lourde (relecture, scoring, rerank de 50 resultats) | Sub-agent dedie `consolidator` | Ne pas saturer le contexte parent avec le detail |
| Synthese qui demande la mission complete | Parent OBLIGATOIREMENT | Le sub ne connait pas les vraies attentes |
| Plusieurs vagues de recherche prevues | Sub-agent dedie | Garde le parent leger pour orchestrer la suite |

**Regle pratique** :
- *"Prends ce qui est utile, jette le reste"* → parent.
- *"Comprends ces 2 outputs en profondeur et produis un nouveau document"* → sub-agent dedie.
Sinon le parent finit avec 100k tokens de transcripts dans son contexte.

---

## 9. Hierarchie a 3 niveaux — limite officielle et workaround

**Limite** : par defaut, un sub-agent **ne dispose pas** du tool `Agent`. Donc un "parent intermediaire" ne peut PAS spawner ses propres workers, sauf via **Agent Teams** (experimental, v2.1.32+).

⇒ En mode classique, on est bloque a **2 niveaux** : Main → workers.

**Workaround sans Agent Teams** :

```
Main (parent)
 |
 +-- Tour 1 : Agent worker_A || Agent worker_B (parallele dans 1 message)
 |          chacun ecrit dans .claude-tmp/research/{ts}-{id}.md
 |          chacun retourne PATH + resume court (~500 tokens)
 |
 +-- Tour 2 : Agent consolidator
              prompt : "lis A.md et B.md, ecris docs/final.md"
              retourne "done + 1 paragraphe takeaway"
```

Le `consolidator` joue le role du "parent intermediaire" sans avoir besoin de spawner. Equivalent fonctionnel, sans la limite.

---

## 10. Bus filesystem — conventions

Des que les outputs depassent quelques k tokens, communication via filesystem :

```
.claude-tmp/                         # gitignored
├── research/
│   ├── 20260426-1430-A.md           # timestamp + ID worker
│   └── 20260426-1430-B.md
├── synth/
│   └── 20260426-1430-final.md
└── lessons/
    └── ...
```

**Regles d'or** :
1. **1 fichier par worker** (jamais 2 workers qui ecrivent au meme endroit → race conditions).
2. **Timestamp + ID dans le nom** pour debug et rejouabilite.
3. **Le worker retourne le PATH + un resume court**, pas le contenu (sinon le parent re-pollue son contexte).
4. **Cleanup explicite** : `.claude-tmp/` dans `.gitignore`, rappel dans `tasks/cleanup.md`.
5. **Frontmatter coherent** : si l'agent doit deposer un fichier, `tools` doit inclure `Write` (piege classique : oublier `Write` dans la allowlist).

---

## 11. Arbre de decision — recherche multi-source

```
Tache de recherche multi-source ?
│
├── Sortie tient en <5k tokens par worker ?
│   └── OUI → Fan-out simple, parent consolide directement.
│             Pas de fichiers temp, retours en string.
│
└── Sortie volumineuse (transcripts, dumps, listings) ?
    │
    ├── Synthese mecanique (concat, filtrer) ?
    │   └── Bus filesystem + parent consolide en 1 tour.
    │
    └── Synthese qui demande "comprendre" les outputs ?
        └── Bus filesystem + sub-agent CONSOLIDATOR dedie.
            Parent ne voit que le resume final + path.
```
