# Token Economy — Audit & Bonnes Pratiques (Challengees)

> Sources : audit 926 sessions Claude Code + article "10 things I changed" + experience terrain.
> Chaque conseil est annote : **VALIDE**, **PARTIELLEMENT VALIDE**, ou **CLAUDE.AI ONLY** (pas applicable a Claude Code CLI).

---

## 1. Audit 926 sessions — les 4 decouvertes cles

### 1.1 ENABLE_TOOL_SEARCH — VALIDE

**Probleme** : Claude Code charge le schema JSON complet de TOUS les tools au demarrage. ~20K tokens de definitions d'outils a chaque tour, utilises ou non.

**Fix** : une ligne dans `settings.json` :
```json
{ "env": { "ENABLE_TOOL_SEARCH": "true" } }
```

**Impact** : contexte passe de ~45K a ~20K. Sur 858 sessions, ~264M tokens economises.

**Verdict : VALIDE.** C'est le quick win #1. A activer immediatement.

### 1.2 Cache expiry (5 min idle) — VALIDE

**Probleme** : 54% des tours venaient apres 5+ min d'inactivite. Chaque retour = re-traitement complet du contexte au prix fort (pas de cache hit). 12.3M tokens gaspilles sur les gaps.

**Strategie** :
- Travailler en sessions concentrees (25-45 min type Pomodoro)
- `/compact` AVANT de partir en pause
- Alternativement : `/clear` + coller un resume si la pause est longue

**Verdict : VALIDE.** Le cache prompt a bien un TTL de 5 min chez Anthropic.

### 1.3 Skills fantomes — VALIDE

**Probleme** : 42 skills chargees, 19 utilisees 2 fois ou moins sur 858 sessions. Chaque schema de skill dans le contexte = tokens brules pour rien.

**Strategie** :
- Auditer ses skills : `ls ~/.claude/skills/`
- Deplacer les rarement utilisees dans un dossier `~/.claude/skills-archive/`
- Garder en `skills/` uniquement celles utilisees > 1x/semaine
- Rappel : **rules/** = toujours charge. **skills/** = a la demande. Ne pas confondre.

**Verdict : VALIDE.** Moins on charge, moins on consomme.

### 1.4 Lectures de fichiers redundantes — VALIDE

**Probleme** : 1122 lectures redundantes (meme fichier lu 3+ fois). Un cas extreme : meme fichier lu 33 fois.

**Strategie** :
- Claude Code re-lit naturellement les fichiers modifies pour verifier — c'est normal
- Les vrais gaspillages viennent de contextes longs ou Claude "oublie" avoir lu
- `/compact` regulierement reduit ce phenomene
- Structurer les CLAUDE.md avec les chemins cles evite les recherches repetees

**Verdict : VALIDE mais nuance.** Certaines relectures sont intentionnelles (verification post-edit).

---

## 2. "10 regles" — Challenge

### Regle 1 : Editer le prompt au lieu de follow-up

**Conseil** : cliquer Edit sur le message original au lieu d'envoyer "non je voulais dire..."

**Verdict : CLAUDE.AI ONLY.** Dans Claude Code CLI, il n'y a pas de bouton Edit. En revanche, le principe est bon : reformuler clairement plutot qu'empiler des corrections. En CLI, ca se traduit par `/clear` + prompt reformule.

### Regle 2 : Nouveau chat tous les 15-20 messages

**Verdict : PARTIELLEMENT VALIDE.** Le principe est bon (cout quadratique). En Claude Code, utiliser `/compact` aux milestones (garde le resume) ou `/clear` entre taches independantes.

### Regle 3 : Grouper les questions en 1 message

**Verdict : VALIDE.** 3 prompts separes = 3 chargements de contexte. 1 prompt avec 3 taches = 1 seul. Toujours battre les taches independantes dans un seul message.

### Regle 4 : Uploader les fichiers recurrents dans Projects

**Verdict : CLAUDE.AI ONLY.** Pas de concept "Projects" dans Claude Code CLI. L'equivalent est CLAUDE.md (charge auto) ou skills/ (charge a la demande).

### Regle 5 : Configurer Memory & User Preferences

**Verdict : CLAUDE.AI ONLY pour l'UI.** En Claude Code, c'est exactement `~/.claude/CLAUDE.md` qui joue ce role. Ecrire une fois son profil, stack, preferences = economiser 3-5 messages de setup a chaque session.

### Regle 6 : Desactiver les features inutilisees

**Verdict : PARTIELLEMENT VALIDE.** En Claude Code :
- `ENABLE_TOOL_SEARCH=true` = ne charge que les tools necessaires
- Reduire les MCP servers actifs si inutilises
- Extended thinking : `MAX_THINKING_TOKENS=10000` pour limiter le budget reflexion
- Mais pas de toggle "web search" comme dans l'UI web

### Regle 7 : Haiku pour taches simples

**Verdict : VALIDE.** C'est la strategie officielle Anthropic :
- `CLAUDE_CODE_SUBAGENT_MODEL=haiku` pour les workers
- `/model haiku` pour taches simples directement
- Sonnet pour le dev quotidien, Opus pour archi complexe

### Regle 8 : Etaler le travail sur la journee

**Verdict : CLAUDE.AI ONLY.** Concerne les rate limits de l'UI web (fenetre glissante 5h). Claude Code via API n'a pas ce mecanisme — c'est du pay-per-token.

### Regle 9 : Travailler en heures creuses

**Verdict : CLAUDE.AI ONLY.** Idem — concerne l'UI web avec peak hours. L'API n'a pas de tarification horaire differentielle.

### Regle 10 : Activer Extra Usage

**Verdict : CLAUDE.AI ONLY.** Specifique aux abonnements Pro/Max de l'UI web.

---

## 3. Resume actionnable pour Claude Code

### Les 6 VRAIES regles qui comptent

| # | Regle | Impact | Effort |
|---|-------|--------|--------|
| 1 | `ENABLE_TOOL_SEARCH=true` | Enorme (14K/tour) | 1 ligne |
| 2 | `/compact` toutes les 15-20 interactions | Fort (cout quadratique) | Habitude |
| 3 | `/clear` entre taches independantes | Fort | Habitude |
| 4 | `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | Modere (3x par agent) | 1 ligne |
| 5 | Battre les taches en 1 prompt | Modere | Discipline |
| 6 | Sessions concentrees (eviter les gaps 5min+) | Modere (cache TTL) | Organisation |

### Les 3 a IGNORER (Claude.ai only, pas Claude Code)

- Edit prompt (pas de bouton en CLI)
- Peak hours / etaler la journee (API = pay-per-token)
- Extra Usage (UI web uniquement)

---

## 4. Mises a jour avril 2026

### 4.1 1M tokens context (GA)

La fenetre de contexte est maintenant de 1M tokens (~200-350 fichiers, ~750K mots).
vs Cursor ~200K, Windsurf ~128K.

**Impact** : plus de place, mais le cout quadratique reste. `/compact` toujours critique.
Regle : 80% du contexte atteint → exit session, restart pour du travail multi-fichier complexe.

### 4.2 Context Editing (nouveau)

Claude supprime automatiquement les outputs tools obsoletes du contexte.
**Reduction** : -84% du contexte sans perte de coherence.

### 4.3 Skills < 2000 tokens

Etude communaute : 80% des skills publiques **nuisent** a la qualite (trop longues, trop generiques).
Les 20% restantes (iterees par experts domaine, < 2000 tokens) surpassent le modele generique.

### 4.4 claude-mem : 10x token savings

Plugin memoire (46.1k stars) avec recherche 3 couches :
- search() ~100 tokens → timeline → get_observations() ~1000 tokens
- vs approche naive : 20000+ tokens
- Detail dans `memoire.md`

### 4.5 Tableau recapitulatif actualise

| Action | Economie | Effort |
|--------|----------|--------|
| `ENABLE_TOOL_SEARCH=true` | ~14K/tour | 1 ligne |
| `/compact` toutes les 15-20 interactions | Fort (cout quadratique) | Habitude |
| `/clear` entre taches independantes | Fort | Habitude |
| `CLAUDE_CODE_SUBAGENT_MODEL=haiku` | 3x par agent | 1 ligne |
| Battre les taches en 1 prompt | Modere | Discipline |
| Sessions concentrees (eviter gaps 5min+) | Modere (cache TTL) | Organisation |
| Skills < 2000 tokens chacune | Modere | Audit skills |
| Context Editing (auto) | -84% contexte | Automatique |
| claude-mem (si installe) | 10x reduction | Install plugin |
