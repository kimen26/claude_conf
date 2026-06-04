---
name: pmo-design
description: Concevoir un PMO (Project Management Officer) en système multi-agent Claude Code - hiérarchie parent/enfant, scope strict, classification d'inputs, coordination via fichiers (substrate pattern), gestion du memory isolation des sous-agents. Template normé 12 sections + anti-patterns issus de cas réels. Skill jumeau de `pmo-challenge` (audit d'un système PMO existant).
---

# PMO Design — Pattern de conception multi-agent

> Skill capitalisé après deepsearch des bonnes pratiques Claude Code subagents Feb-May 2026 + audit de 2 PMO réels (pole-b-pmo mature + pole-a-pmo/pole-a-tile-pmo hiérarchique).

## Quand utiliser ce skill

Tu charges ce skill **avant** de créer ou refondre un agent qui gère de la **persistance, du backlog, de la traçabilité, du sprint-log** dans un projet multi-fichiers. Triggers typiques :

- « Crée un PMO pour [pôle X] »
- « Mon agent oublie tout au reboot »
- « Comment on fait une hiérarchie parent/enfant entre agents ? »
- « Les sous-agents se marchent dessus / écrivent dans les mêmes fichiers »
- « Je veux normer mes agents PMO entre eux »
- « Quelle est la différence entre PMO et sachant ? »

## Principe fondamental — PMO vs Sachant

**Distinction critique à graver :**

| Rôle | Verbe-clé | Exemple |
|------|-----------|---------|
| **PMO** | *trace, log, alerte, synchronise* | pole-a-pmo, pole-b-pmo |
| **Sachant** | *crée, conçoit, exécute le métier* | pole-a-dev, pole-b-architecte, pole-b-conseiller |

Un PMO **ne crée pas de contenu métier**. Un sachant **ne tient pas le backlog**. Confondre les deux produit soit un PMO bloat (qui écrit du code), soit un sachant qui oublie tout (pas de trace).

**Règle dure** : pour chaque domaine structuré, prévois les **deux rôles**. Sinon il manque un côté de l'équation.

---

## 5 trouvailles deepsearch (Feb-May 2026)

### 1. 🚨 Memory isolation problem (Hindsight, mai 2026)

> *"Subagents do not share memory with the coordinator or each other. By default, every subagent invocation starts fresh — whatever the subagent figures out vanishes the moment it returns."*

**Implication design** : un PMO **ne peut PAS porter la mémoire en RAM**. Il **doit graver dans fichiers** que le main agent ou un autre tour peut relire. Même la feature `~/.claude/agent-memory/` (v2.1.33+, fév 2026) ne sert pas comme source de vérité projet — elle est **silotée par subagent**.

→ **Pattern obligatoire** : tout PMO écrit ses outputs dans des fichiers du projet (substrate). La synthèse remontée au parent doit être **formattée pour copier-coller** dans la source de vérité.

### 2. 🗂️ Coordination substrate pattern

> *"The shared progress file acts as the coordination substrate — each agent reads it at startup and writes to it at completion."*

**Implication design** : désigner **1-2 fichiers source de vérité** par pôle (ex : `state.md` + `BACKLOG.md`) que **tous** les agents du pôle lisent au startup. Pas de mémoire orale, pas de "je me souviens du tour d'avant".

→ **Pattern obligatoire** : la fiche PMO commence par `## Première action OBLIGATOIRE (lecture ordonnée)` listant ces fichiers.

### 3. 🌳 Hierarchical decomposition (Google ADK + Anthropic)

> *"Parent → child only. Child returns synthesis to parent. Never child ↔ child."*

**Implication design** :
- Un sous-agent ne peut **invoquer** que son parent (jamais un agent d'un autre pôle direct)
- Un sous-agent **remonte une synthèse formatée** au parent, qui l'intègre
- Un parent n'écrit pas dans le scope strict du sous-agent (séparation des concerns)

→ **Pattern obligatoire** : si `pole-a-tile-pmo` veut alerter `pole-b-pmo`, il passe par `pole-a-pmo` (parent). Jamais en direct.

### 4. 📋 « 1 goal, 1 input, 1 output, 1 handoff » (Anthropic engineering blog)

Chaque fiche d'agent commence par cette section, à 4 lignes max :
```
- Goal : <unique objectif mesurable>
- Input : <ce qui te déclenche>
- Output : <ce que tu produis>
- Handoff : <à qui tu rends la main, sous quel format>
```

→ **Pattern obligatoire** : un agent sans ces 4 lignes claires est scope-creep en puissance.

### 5. 🧠 Opus orchestrator + Haiku worker

> *"Production pattern: Opus as orchestrator, Haiku as worker inside sub-agents."*

**Implication design** : PMO = Haiku (log structuré rapide, ~5x cheaper). Sachant créatif = Sonnet ou Opus. Orchestrateur principal = Sonnet/Opus.

→ **Pattern obligatoire** : modèle dans le frontmatter cohérent avec le rôle. Ne mets pas Opus sur un PMO Haiku-equivalent.

---

## Template PMO normé (12 sections)

Copier-coller cette structure. Adapter le contenu, garder l'ordre.

```markdown
---
name: <pôle>-pmo (ou <pôle>-<spé>-pmo pour sous-agent)
description: PMO <pôle> <projet> - <verbe action-oriented>. <quand l'invoquer>. Haiku pour log structuré rapide.
model: haiku
---

Tu es le **PMO du <pôle/sous-domaine>**.

**Tu n'es pas un secrétaire.** Tu es **garant**. <conséquence si tu échoues>

---

## 🎯 1 goal, 1 input, 1 output, 1 handoff

- Goal : <unique objectif mesurable>
- Input : <ce qui te déclenche>
- Output : <fichiers que tu écris OU synthèse que tu remontes>
- Handoff : <à qui, sous quel format>

---

## 📚 Première action OBLIGATOIRE (lecture ordonnée)

1. <fichier 1>
2. <fichier 2>
3. ...

---

## 🗺️ TA CARTOGRAPHIE (fichiers de ton scope)

| Fichier | Rôle | Tu y notes |
|---------|------|------------|
| ... | ... | ... |

⚠️ **Si tu ne mets à jour QUE [fichier le plus facile], tu as ÉCHOUÉ.** Les autres aussi doivent être synchros.

---

## 🤝 Sous-spécialistes (que tu délégues) OU 🤝 Parent (qui te délègue)

| Sous-agent | Scope | Quand déléguer |
|------------|-------|---------------|
| ... | ... | ... |

OU pour un sous-agent :

**Parent** : `<pôle>-pmo`. Tu ne touches pas à son scope (`state.md`, `BACKLOG.md`). Tu remontes une synthèse.

---

## 🤖 Autonomie — ce que tu peux faire SANS être invité

### Décisions opérationnelles
- ...

### Interroger un autre agent
- ...

### Alerter l'auteur
- ...

---

## 🚫 Ce que tu NE fais PAS

- ...

---

## 🧭 Classification d'un input utilisateur (6 catégories)

| Catégorie | Signal | Action PMO |
|-----------|--------|-----------|
| **DÉCISION** | « Je décide… » / arbitrage tranché | → entrée datée dans <fichier décisions> |
| **LEÇON** | Pattern observé / piège identifié | → L-xxx dans <fichier leçons> |
| **TODO** | Chantier identifié, pas exécuté dans le tour | → ticket dans <backlog> |
| **QUESTION OUVERTE** | Arbitrage nécessaire, pas tranché | → section dédiée |
| **INFO** | Contexte/rapport, rien à acter | → ignored ou sprint-log |
| **TRAITEMENT IMMÉDIAT** | Correction à exécuter dans le tour | → action + log |

Un message peut être plusieurs catégories à la fois.

---

## ⏱️ Timing déclenchement

- À chaque tour main agent où signal <pôle> apparaît
- Mi-tour si décision prise (ne pas attendre la fin)
- Avant remise main à l'auteur : checklist complète
- Pas attendre "fin de session" explicite

---

## 🚨 SLA et alertes

| Trigger | Action |
|---------|--------|
| User signale 2x le même bug sans correction | Alerte + ticket bloqué |
| Ticket ouvert > 1 session sans note | Alerte clarification |
| ... | ... |

---

## ⚙️ Checklist avant remise main (obligatoire)

```
[ ] 1. ...
[ ] 2. ...
```

---

## 📝 Format rapport

```
## <agent> — capture session du <date>

### Contexte tour
### Classification inputs
### Checklist persistance
### Alertes
### Fichiers modifiés
```

---

## ❌ ANTI-PATTERNS À FUIR

1. **« J'ai noté dans 1 fichier, ça suffit »** → NON
2. **« Pas de demande explicite de fin de session »** → NON
3. **...**

---

## 🧭 MNÉMONIQUE

> Une phrase qui résume le rôle en 1 ligne mémorable.
```

---

## Patterns hiérarchie multi-PMO (parent + sous-spé)

Quand un pôle a plusieurs domaines structurés, **NE PAS** créer un méga-PMO qui gère tout. Préférer :

```
main agent (Sonnet/Opus)
  └─ <pôle>-pmo (Haiku) [PMO niveau pôle]
      • scope : source de vérité projet (state.md + BACKLOG.md)
      • DÉLÈGUE à <pôle>-<spé>-pmo si signal sous-domaine détecté
              └─ <pôle>-<spé>-pmo (Haiku) [sous-spé]
                  • scope : fichiers techniques du sous-domaine
                  • REMONTE 1 synthèse 5-10 lignes au parent
```

**Règle d'or** : le sous-spé ne touche PAS state.md ni BACKLOG.md du pôle. C'est le parent qui intègre la synthèse.

**Exemple concret :**
- Pôle A : `pole-a-pmo` (parent) + `pole-a-tile-pmo` (sous-spé pipeline assets)
- Pôle B : `pole-b-pmo` seul (pas encore besoin de sous-spé)

---

## Format synthèse sous-spé → parent

Quand un sous-spé doit remonter au parent, il utilise **toujours** ce format :

```markdown
## <sous-spé> → <parent> — session du <date>

### Fait dans mon scope
- <fichier 1> : <action ou "rien">
- <fichier 2> : ...

### Découvertes capturées
- L-xxx (proposé) : <1 ligne synthétique POUR le backlog parent>

### Alertes
- <alerte ou "aucune">

### À intégrer par <parent>
→ Ajouter L-xxx dans <backlog parent> : "<1 ligne>"
→ Ajouter au <state parent> Session YYYY-MM-DD : "<résumé>"

### Fichiers modifiés (mon scope strict)
- Liste
```

Le parent **copie-colle** dans state.md + BACKLOG.md. Pas de paraphrase, pas de perte d'info.

---

## Frontmatter — les pièges qui font disparaître un agent silencieusement

Le harness Claude Code parse le YAML strict. Dans `description:` **non quotée** :

| Interdit | Symptôme | Remplacer par |
|----------|----------|---------------|
| `:` interne (`Foo : bar`) | Agent disparaît de la liste, pas d'erreur | `-` ou `(parenthèses)` |
| Em-dash `—` (U+2014) | Idem | `-` (tiret simple) |
| `×` (U+00D7) | Idem | `x` |

**OK :** accents (é è à ç), apostrophes typographiques ('), virgules, points, parenthèses, tirets simples.

**Diagnostic 30s** :
```bash
grep -P '[—×]|: .* :' .claude/agents/*.md
```

**Alternative** : quoter la description.
```yaml
description: "Foo : bar — baz"
```

---

## Anti-patterns globaux (issus de cas réels)

1. **PMO qui ne grave que dans 1 fichier** → "journal intime" invisible au reboot
2. **Sous-spé qui touche au scope du parent** → double-écriture, perte de cohérence
3. **PMO sans classification d'inputs** → tout devient "info", rien n'est tickété
4. **PMO sans SLA chiffrés** → blocages invisibles, plus de garde-fou
5. **PMO confondu avec sachant** → soit code médiocre, soit aucune trace
6. **Frontmatter `description: PMO : tile - foo — bar`** → agent disparaît sans erreur
7. **Pas de mnémonique** → la fiche ne se grave pas, pas reprise au reboot
8. **Pas de "Ce que tu NE fais PAS"** → scope creep garanti

---

## Checklist création nouveau PMO

Avant de pousser ton agent PMO en prod, vérifier :

```
[ ] Frontmatter sans : / — / × dans description non quotée
[ ] Section "1 goal, 1 input, 1 output, 1 handoff" présente
[ ] Section "Première action OBLIGATOIRE" liste les fichiers source de vérité
[ ] Cartographie en table (Fichier / Rôle / Tu y notes)
[ ] Classification 6 catégories d'inputs présente
[ ] Section "Ce que tu NE fais PAS" explicite
[ ] SLA chiffrés (jours, tickets)
[ ] Checklist avant remise main
[ ] Format rapport spécifié
[ ] Mnémonique 1 ligne
[ ] Anti-patterns 3-5 explicités
[ ] Si sous-spé : section synthèse au parent + parent référencé
[ ] Si parent avec sous-spés : section "Sous-spécialistes" + délégation explicite
[ ] Modèle Haiku (sauf cas justifié)
[ ] Existe un sachant correspondant pour le métier ? (sinon créer en parallèle)
```

---

## Sources deepsearch (Feb-May 2026)

- [Claude Code & Agent Memory: Best Practices for 2026 — orchestrator.dev, avril 2026](https://orchestrator.dev/blog/2026-04-06--claude-code-agent-memory-2026/)
- [Your Claude Code Subagents Don't Share What They Learn — Hindsight, mai 2026](https://hindsight.vectorize.io/blog/2026/05/06/claude-code-subagents-shared-memory)
- [Claude Code's 'Tasks' update lets agents work longer and coordinate across sessions — VentureBeat](https://venturebeat.com/orchestration/claude-codes-tasks-update-lets-agents-work-longer-and-coordinate-across)
- [How Agents Manage Other Agents: Four Subagents Patterns in 2026 — philschmid.de](https://www.philschmid.de/subagent-patterns-2026)
- [Multi-agent patterns in ADK — Google Developers, 2026](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [Building agents with the Claude Agent SDK — Anthropic engineering](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Best Practices with Claude Code Subagents Part II: From Prompts to Pipelines — PubNub](https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/)
- [Claude Code Agent Teams, Subagents, and MCP: The 2026 Playbook — Developers Digest](https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026)
- [Anthropic Managed Agents (avril 2026) — InfoQ](https://www.infoq.com/news/2026/04/anthropic-managed-agents/)
- [Create custom subagents — Claude Code Docs officiels](https://code.claude.com/docs/en/sub-agents)

---

## Les 3 niveaux de mémoire d'un système multi-agent

Une erreur classique : ne distinguer qu'**un seul** journal. Conséquence : soit il devient illisible (mélange tile + design d'agent + retours user), soit il oublie une dimension.

**Toujours penser 3 niveaux** :

| Niveau | Fichier type | Contenu | Qui écrit | Qui lit |
|---|---|---|---|---|
| **1. Technique métier** | `LESSONS.md` du skill | Connaissances du domaine (ex cartographie tile, règles d'or) | PMO sous-spé + sachants | Sachants à chaque session, PMO sous-spé |
| **2. Méta-process pipeline** | `PIPELINE-MEMORY.md` | Décisions de design des agents, frictions résolues, patterns user, hypothèses à tester | PMO sous-spé (garant) | Main agent au reboot avant toute refonte |
| **3. Collaboration user** | Auto-memory `feedback_*.md` | Tics du user, préférences ton, anti-patterns relationnels | Main agent | Main agent cross-sessions |

**Pourquoi 3 ?** Parce qu'un PMO qui écrit "user préfère propositions concrètes" dans LESSONS.md technique pollue le journal. Et une refonte d'agent gravée dans LESSONS.md technique est invisible au reboot pour le main agent qui n'ouvre pas un skill technique.

**Template `PIPELINE-MEMORY.md` recommandé (7 sections)** :

```
1. Architecture actuelle (snapshot)
2. Décisions de design (chronologique, daté)
3. Frictions résolues (F-xxx avec symptôme/cause/résolution/pattern gravé)
4. Patterns user observés (P-xxx)
5. Hypothèses à tester (table avec critère)
6. Sources externes & inspirations
7. Comment alimenter ce fichier
```

**Exemple concret** : un fichier `PIPELINE-MEMORY.md` maintenu par un sous-PMO de pipeline.

---

## Études de cas — PMO de référence

### PMO mono-pôle (mature)
- Force : classification en ~6 catégories, autonomie sur 3 niveaux, SLA défini, suivi d'un PROCESS multi-étapes
- Pattern : PMO seul au niveau pôle (pas de sous-spé nécessaire)

### PMO hiérarchique (parent + sous-spé)
- Force : hiérarchie explicite, format de synthèse remontée standardisé
- Pattern : PMO parent au niveau pôle + sous-PMO pour un pipeline technique borné
