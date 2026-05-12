# Methodologies — Spec-Driven + TDD + Plan Mode

> Comment structurer le travail avec Claude Code. Trois approches complementaires.

---

## 1. Spec-Driven Development (SDD)

### 1.1 Principe

Ecrire les specs AVANT le code. L'IA genere a partir de specs, pas de prompts vagues.

```
Specs (quoi/pourquoi) → Design (comment) → Tasks (etapes) → Code (implementation)
```

### 1.2 Outil de reference : GitHub Spec Kit (86.8k stars)

- **URL** : https://github.com/github/spec-kit
- **Install** : `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- **Init** : `specify init my-app --ai claude`

### 1.3 Structure des fichiers

```
.kiro/specs/core/{feature-name}/
├── requirements.md     # User stories + criteres d'acceptation (notation EARS)
├── design.md           # Architecture, diagrammes sequence, considerations tech
└── tasks.md            # Plan d'implementation detaille, dependances
```

**Notation EARS** (Easy Approach to Requirements Syntax) :
- **When** [trigger], **the system shall** [behavior]
- **While** [state], **the system shall** [behavior]
- **If** [condition], **then the system shall** [behavior]

### 1.4 Commandes slash Claude Code

| Commande | Effet |
|----------|-------|
| `/speckit.constitution` | Definir les regles du projet |
| `/speckit.specify` | Generer requirements + criteres |
| `/speckit.plan` | Generer design technique |
| `/speckit.tasks` | Decomposer en taches atomiques |
| `/speckit.implement` | Implementer tache par tache |

### 1.5 Autres repos spec-driven

| Repo | Ce qu'il apporte |
|------|-----------------|
| `Pimzino/claude-code-spec-workflow` | 14 slash commands + steering docs + templates |
| `SpillwaveSolutions/sdd-skill` | Workflow 6-step greenfield, 7-step brownfield |

---

## 2. TDD — Test-Driven Development

### 2.1 Principe

Ecrire les tests AVANT le code. Le cycle :

```
RED (test echoue) → GREEN (implementation minimale) → REFACTOR (ameliorer)
```

### 2.2 Framework de reference : Superpowers (145k stars)

- **URL** : https://github.com/obra/superpowers
- **Philosophie** : "Ne pas sauter sur le code — d'abord se demander que essayez-vous VRAIMENT de faire ?"
- **Skills inclus** : brainstorming, planning, TDD, debugging, verification, code review, git worktrees

### 2.3 Workflow TDD avec Claude Code

1. **Ecrire le test** : decrire le comportement attendu
2. **Executer** : verifier qu'il echoue (RED)
3. **Implementer** : ecrire le minimum pour que le test passe (GREEN)
4. **Executer** : verifier que le test passe
5. **Refactorer** : ameliorer sans casser les tests (REFACTOR)
6. **Verifier couverture** : viser 80%+

### 2.4 Avec les agents existants

| Agent | Role dans le TDD |
|-------|-----------------|
| `tdd-guide` | Enforce le cycle RED-GREEN-REFACTOR |
| `code-reviewer` | Valide la qualite apres refactor |
| `build-error-resolver` | Fix les erreurs de build |

---

## 3. Plan Mode (officiel Claude Code)

### 3.1 Principe

Mode structure ou Claude propose un plan AVANT d'executer.

### 3.2 Activation

| Action | Comment |
|--------|---------|
| Entrer | **Shift+Tab** ou ecrire dans le prompt "planifie d'abord" |
| Quitter | Claude appelle ExitPlanMode apres validation |

### 3.3 Workflow

```
1. USER: "Refactor auth module" + Shift+Tab
2. CLAUDE: [plan mode] Propose 5 etapes
3. USER: Approuve / ajuste
4. CLAUDE: ExitPlanMode → execute etape par etape
```

### 3.4 Quand utiliser

- Taches > 3 etapes
- Refactoring avec dependances
- Nouvelles features architecturales
- PAS pour petits correctifs ou lectures simples

---

## 4. Combiner les trois

### Workflow optimal

```
Spec-Driven (QUOI)     → Requirements, design, tasks
    ↓
Plan Mode (COMMENT)     → Claude propose le plan d'execution
    ↓
TDD (VALIDATION)        → Tests d'abord, puis implementation
    ↓
Code Review              → Agent code-reviewer verifie
```

### Mapping sur les agents existants

| Etape | Methodologie | Agent |
|-------|-------------|-------|
| 1. Clarifier le besoin | SDD | `planner` |
| 2. Concevoir l'architecture | SDD | `architect` |
| 3. Decomposer en taches | SDD + Plan Mode | `planner` |
| 4. Ecrire les tests | TDD | `tdd-guide` |
| 5. Implementer | TDD | — (Claude direct) |
| 6. Reviewer | — | `code-reviewer` |
| 7. Securite | — | `security-reviewer` |

### Quand utiliser quoi

| Situation | Approche |
|-----------|----------|
| Nouvelle feature complexe | SDD complet (specs → design → tasks → TDD) |
| Bug fix | TDD seul (test qui reproduit → fix → verify) |
| Refactoring | Plan Mode + code-reviewer |
| Prototype rapide | Plan Mode seul |
| Production critique | SDD + TDD + security-reviewer |

---

## 5. Ressources

| Source | URL |
|--------|-----|
| GitHub Spec Kit | https://github.com/github/spec-kit |
| Superpowers | https://github.com/obra/superpowers |
| SDD avec Claude Code (Heeki Park) | https://heeki.medium.com/using-spec-driven-development-with-claude-code-4a1ebe5d9f29 |
| SDD vs TDD (Martin Fowler) | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| Kiro IDE (AWS) | https://kiro.dev/docs/specs/ |
