# Tips Avances — Boris Cherny & Power Users

> Boris Cherny = developpeur officiel de Claude Code chez Anthropic.
> Ses conseils sont de la source directe, pas de l'interpretation communautaire.

---

## 1. Boris Cherny — Tips CLI (mars 2026)

### 1.1 `--bare` : startup 10x plus rapide

Par defaut, `claude -p` (et les SDKs TypeScript/Python) cherchent les CLAUDE.md locaux, settings, et MCPs. Pour un usage non-interactif (scripts, CI), ca ralentit pour rien.

```bash
# Sans --bare : charge CLAUDE.md + settings + MCP + skills
claude -p "genere un resume de ce fichier"

# Avec --bare : skip tout, prompt brut
claude -p "genere un resume de ce fichier" --bare
```

**Quand utiliser** : scripts automatises, SDK calls, CI/CD pipelines, benchmarks.
**Quand NE PAS utiliser** : dev interactif (on veut le contexte CLAUDE.md).

### 1.2 `--add-dir` : multi-repo

Quand on travaille sur plusieurs repos simultanment :

```bash
# Demarrer dans repo A, donner acces a repo B
claude --add-dir ../other-repo

# En cours de session
/add-dir ../docs-repo
```

**Effet** : Claude voit les fichiers ET a les permissions de lire/ecrire dans le dossier ajoute. Utile pour monorepos ou repos de documentation adjacents.

### 1.3 `--agent` : agents custom

```bash
# Lancer un agent specifique defini dans .claude/agents/
claude --agent=code-reviewer

# L'agent charge son propre system prompt, tools, et skills
```

**Attention** : l'agent ne voit PAS la conversation en cours. C'est un contexte frais avec ses propres instructions.

### 1.4 `/voice` : input vocal

```bash
# Dans le CLI : activer le mode vocal
/voice
# Puis maintenir la barre d'espace pour parler

# Dans Desktop : bouton microphone
# Dans iOS : activer dictation dans les settings systeme
```

**Anecdote Boris** : "I do most of my coding by speaking to Claude, rather than typing."

---

## 2. CLAUDE.md de reference (Boris Cherny)

6 principes operationnels extraits de son CLAUDE.md public :

### 2.1 Plan mode par defaut

- Entrer en mode plan pour toute tache 3+ etapes ou decision d'archi
- Si ca derape : **STOP et replanifier** — ne pas continuer a pousser
- Utiliser le mode plan pour les etapes de verification aussi, pas juste pour construire
- Ecrire des specs detaillees des le depart pour reduire l'ambiguite

### 2.2 Strategie sous-agents

- Utiliser les sous-agents **liberalement** pour garder le contexte principal propre
- Deleguer recherche, exploration, et analyse parallele aux sous-agents
- Pour les problemes complexes : jeter plus de compute via sous-agents
- **1 tache = 1 sous-agent** pour une execution concentree

### 2.3 Boucle d'auto-amelioration

- Apres TOUTE correction utilisateur : mettre a jour `tasks/lessons.md`
- Ecrire des regles pour soi-meme qui empechent la meme erreur
- Iterer sans pitie sur ces lecons jusqu'a ce que le taux d'erreur baisse
- Relire les lecons au debut de la session pour le projet concerne

### 2.4 Verification avant "done"

- Ne JAMAIS marquer une tache complete sans prouver qu'elle marche
- Comparer le comportement entre main et la branche quand pertinent
- Se demander : "Un staff engineer approuverait-il ca ?"
- Executer tests, verifier logs, demontrer la correction

### 2.5 Exiger l'elegance (equilibre)

- Pour les changements non-triviaux : pause et "existe-t-il une maniere plus elegante ?"
- Si un fix semble bricole : "sachant tout ce que je sais maintenant, implementer la solution elegante"
- **Ignorer** pour les corrections simples et evidentes — ne pas sur-concevoir
- Remettre en question son propre travail avant de le presenter

### 2.6 Bug fixing autonome

- Rapport de bug = le corriger. Ne pas demander d'accompagnement.
- Pointer logs, erreurs, tests echoues — puis resoudre
- Zero context switching requis de l'utilisateur
- Aller corriger les tests CI defaillants sans qu'on dise comment

---

## 3. Gestion des taches (pattern Boris)

```
tasks/
├── todo.md        # Plan avec items cochables
└── lessons.md     # Lecons apprises (auto-MAJ apres corrections)
```

**Workflow** :
1. **Plan First** : ecrire le plan dans `tasks/todo.md` avec items verifiables
2. **Verify Plan** : valider avant de commencer l'implementation
3. **Track Progress** : cocher au fur et a mesure
4. **Explain Changes** : resume haut niveau a chaque etape
5. **Document Results** : ajouter une section review dans todo.md
6. **Capture Lessons** : MAJ `tasks/lessons.md` apres corrections

---

## 4. Patterns avances (communaute)

### 4.1 Multi-perspective analysis

Pour les problemes complexes, lancer plusieurs sous-agents avec des roles differents :
- Agent "factual reviewer" — verifie les faits
- Agent "senior engineer" — qualite du code
- Agent "security expert" — vulnerabilites
- Agent "consistency reviewer" — coherence avec l'existant

### 4.2 Skeleton projects

Avant d'implementer from scratch :
1. Chercher des projets existants (`gh search repos`, `gh search code`)
2. Evaluer en parallele (securite, extensibilite, pertinence)
3. Cloner le meilleur comme fondation
4. Iterer dans la structure prouvee

### 4.3 Context window hygiene

- Eviter les derniers 20% de la fenetre de contexte pour du travail complexe
- Taches "basse sensibilite au contexte" (single-file edit, doc update) = OK en fin de fenetre
- Taches "haute sensibilite" (refacto multi-fichier, debug complexe) = /compact d'abord

### 4.4 Autocompact

```json
{ "env": { "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50" } }
```

Declenche le compactage automatique quand le contexte atteint 50% de la fenetre. Evite de se retrouver dans les derniers 20% sans s'en rendre compte.

---

## 5. Patterns a eviter (anti-patterns)

| Anti-pattern | Pourquoi c'est mauvais | Alternative |
|-------------|----------------------|-------------|
| Charger 40+ skills | Tokens brules a chaque tour | Garder < 15 skills actives |
| Hooks lourds (> 500ms) | Ralentit chaque interaction | Scripts legers, exit fast |
| CLAUDE.md > 2000 lignes | Contexte sature | Extraire dans skills/ ou docs/ |
| Tout dans rules/ | Charge a chaque message | Deplacer le domaine-specifique dans skills/ |
| Pas de /compact | Cout quadratique | /compact toutes les 15-20 interactions |
| Amend au lieu de nouveau commit | Risque de perdre du travail si hook echoue | Toujours nouveau commit |
| `--no-verify` pour skipper hooks | Contourne les gardes-fous | Corriger la cause du blocage |
| Skills > 2000 tokens | Nuisent a la qualite (80% du marche = bruit) | Skills courtes, iterees par expert domaine |

---

## 6. Features recentes (mars-avril 2026)

### 6.1 Auto-Dream (`/dream`)

Consolidation memoire automatique toutes les 24h (si 5+ enregistrements accumules).
4 etapes : Orient → Collect Signals → Consolidate → Prune & Index.
Lancer manuellement : `/dream`. Detail dans `memoire.md`.

### 6.2 Worktrees (isolation git)

```bash
claude --worktree    # Cree branche + worktree isole
```

Claude travaille dans un worktree pendant que tu reviews un autre. Cleanup auto si pas de changements. +18% throughput rapporte par les equipes.

### 6.3 `claude --chrome` (browser integre)

Integration Chrome DevTools officielle (beta). Navigation, click, form fill, console logs, GIF recording. Detail dans `ui-frontend.md`.

### 6.4 Agent Teams (experimental)

Multi-instance Claude Code coordonnees. Feature flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. 1 team lead + N teammates, worktrees isoles, shared task list. Detail dans `multi-agent.md`.

### 6.5 Auto Mode

Reduit les prompts d'approbation (93% deja approuves). Moins de friction.

### 6.6 Scheduled Tasks

Jobs recurrents sur infra cloud Anthropic (pas sur ton laptop). GA mars 2026.

### 6.7 Context Editing

Supprime automatiquement les outputs tools obsoletes du contexte. Reduction 84% du contexte sans perte de coherence.

### 6.8 1M tokens context (GA)

Fenetre de contexte complete : ~200-350 fichiers, ~750K mots. vs Cursor ~200K, Windsurf ~128K.

---

## 7. Stats adoption (mars 2026)

- Claude Code = outil #1 (depasse Cursor/Copilot en 8 mois)
- ~4% des commits GitHub generes par Claude Code
- 17 releases en 30 jours (mars 2026)
- 112k stars sur le repo claude-code
