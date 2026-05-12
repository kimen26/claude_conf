# Cours Officiels Anthropic — Reference

> Source : https://github.com/anthropics/courses
> Format : Jupyter Notebooks interactifs (Claude Haiku pour cout minimal)
> Progression recommandee : 1 → 2 → 3 → 4 → 5

---

## Vue d'ensemble

| # | Cours | Sujet | Prerequis |
|---|-------|-------|-----------|
| 1 | **API Fundamentals** | SDK, params modele, multimodal, streaming | Aucun |
| 2 | **Prompt Engineering Interactive** | Techniques core prompting step-by-step | Cours 1 |
| 3 | **Real World Prompting** | Prompts en contexte production | Cours 2 |
| 4 | **Prompt Evaluations** | Metriques qualite, test suites, eval en prod | Cours 3 |
| 5 | **Tool Use** | Workflows avec outils externes, function calling | Cours 1 |

---

## 1. API Fundamentals

**Objectif** : Maitriser les bases du SDK Anthropic.

**Concepts cles** :
- API keys et authentification
- Parametres modele (temperature, max_tokens, top_p)
- Prompts multimodaux (texte + images)
- Streaming de reponses
- Gestion des erreurs et retries

**Takeaway** : Tout part de la. Si tu ne comprends pas comment l'API fonctionne, les couches au-dessus (Claude Code, agents, MCP) restent magiques.

---

## 2. Prompt Engineering Interactive

**Objectif** : Apprendre les techniques de prompting par la pratique.

**Concepts cles** :
- Role du system prompt vs user prompt
- Techniques : few-shot, chain-of-thought, XML tags, role assignment
- Controle du format de sortie
- Gestion de la longueur et du style
- Prompt chaining (decomposer en etapes)

**Takeaway** : Le prompting n'est pas de la magie — c'est de l'ingenierie. Chaque technique a un cas d'usage precis. La version AWS Workshop existe aussi (meme contenu, infra differente).

---

## 3. Real World Prompting

**Objectif** : Appliquer les techniques en contexte reel.

**Concepts cles** :
- Prompts complexes multi-etapes
- Gestion du contexte long
- Extraction d'information structuree
- Classification et categorisation
- Summarization avec contraintes
- Prompts pour agents et workflows

**Takeaway** : Le pont entre theorie et production. Les exemples sont des vrais cas d'usage (support client, analyse de documents, generation de code). Version Google Vertex aussi disponible.

---

## 4. Prompt Evaluations

**Objectif** : Mesurer et ameliorer la qualite des prompts en production.

**Concepts cles** :
- Pourquoi evaluer (drift, regression, edge cases)
- Types d'evaluation (exact match, semantic, LLM-as-judge)
- Construction de test suites
- Metriques : precision, recall, F1 pour prompts
- CI/CD pour prompts (evaluation automatique avant deploy)
- A/B testing de prompts

**Takeaway** : Le cours le plus sous-estime. Sans evaluation, tu ne sais pas si ton prompt s'ameliore ou se degrade. Indispensable pour la production.

---

## 5. Tool Use

**Objectif** : Etendre Claude avec des outils externes (function calling).

**Concepts cles** :
- Definition de tools (JSON schema)
- Workflow : Claude decide quand appeler un outil → tu executes → Claude integre le resultat
- Tools multiples et orchestration
- Gestion des erreurs tool (timeout, mauvais input)
- Patterns : search, calculation, API calls, database queries
- Bonnes pratiques : descriptions claires, types precis, exemples dans la description

**Takeaway** : C'est le fondement de tout l'ecosysteme Claude Code. Skills = instructions. Tools = actions. MCP = protocole pour distribuer des tools. Comprendre tool use = comprendre Claude Code.

---

## Complement : Cookbooks (anthropics/claude-cookbooks — 37.8k stars)

Les cookbooks sont le **complement pratique** des cours. Pas de progression lineaire — on pioche ce dont on a besoin.

### Patterns cles

| Pattern | Notebook | Ce qu'on en tire |
|---------|----------|-----------------|
| **RAG** | `capabilities/retrieval_augmented_generation/` | Augmenter Claude avec connaissances externes |
| **Sub-agents** | `multimodal/using_sub_agents.ipynb` | Composition agents hierarchiques (Haiku sous Opus) |
| **Tool Use** | `tool_use/` | Customer service, calculator, SQL queries |
| **JSON Mode** | `misc/how_to_enable_json_mode.ipynb` | Structured outputs garanti |
| **Prompt Caching** | `misc/prompt_caching/` | Optimisation tokens (5 min TTL) |
| **Extended Thinking** | `misc/extended_thinking/` | Raisonnement profond (31K tokens) |
| **Vision** | `multimodal/` | Analyse images, graphiques, formulaires |
| **Agents SDK** | `agents/claude_agent_sdk/` | Construire des agents avec le SDK |

### Quickstarts (anthropics/claude-quickstarts — 16k stars)

5 projets deployables comme point de depart :

| Projet | Ce que ca demontre |
|--------|-------------------|
| **Customer Support Agent** | NLP + knowledge base |
| **Financial Data Analyst** | Chat + visualisation |
| **Computer Use Demo** | Automation desktop (GUI) |
| **Browser Automation** | Navigation web, Playwright |
| **Autonomous Coding Agent** | Pattern 2-agent + git persistence multi-session |

Le plus interessant : **Autonomous Coding Agent** — montre comment un agent lit son propre historique git pour s'ameliorer entre sessions.

---

## Quand consulter quoi

| Besoin | Source |
|--------|--------|
| Comprendre les bases Claude | Cours 1-2 |
| Ecrire de meilleurs prompts | Cours 2-3 |
| Mettre en prod | Cours 4 (evals) |
| Ajouter des outils/MCP | Cours 5 + cookbooks tool_use |
| Pattern RAG | Cookbooks RAG |
| Optimiser les tokens | Cookbooks prompt_caching |
| Construire un agent | Quickstart Autonomous Coding Agent + Cookbooks agents |
