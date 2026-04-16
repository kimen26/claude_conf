---
name: prompt-craft
description: "L'art d'écrire un prompt efficace — template humanisé, frameworks de marché, few-shot, chain-of-thought, anti-patterns, évaluation. Inclut une variante complète pour Snowflake Cortex Agent (Orchestration vs Response instructions). Active dès que l'utilisateur veut créer, améliorer ou debugger un prompt, ou configurer un agent Snowflake."
family: impact
origin: Domaine
---

# SKILL : prompt-craft

> Écrire des prompts qui fonctionnent — génériques et adaptés à Snowflake Cortex Agent.

---

## Quand activer ce skill

- L'utilisateur veut créer ou améliorer un prompt pour une IA (Claude, GPT, Gemini, Mistral...)
- Il configure un agent Snowflake (Cortex Agent / Snowflake Intelligence)
- Il se plaint qu'un modèle "ne comprend pas" ou donne de mauvaises réponses
- Il veut un template de prompt réutilisable
- Mots-clés : "prompt", "instruction", "system message", "agent Snowflake", "Cortex Agent"

---

## PC.1 — Pourquoi la qualité du prompt change tout

Un LLM résout un problème dans un **espace de solution**. La qualité du prompt détermine la taille et la pertinence de cet espace.

### L'équation de base

```
Qualité de la sortie = f(Qualité du modèle × Qualité du prompt × Qualité des données)
```

- Un bon modèle + mauvais prompt → mauvais résultat
- Un bon prompt + modèle modeste → résultat souvent acceptable
- **Garbage in, garbage out** s'applique aux instructions autant qu'aux données

### Ce qui dégrade un prompt

| Problème | Symptôme | Cause racine |
|----------|----------|--------------|
| Trop vague | Réponse générique, sans angle | Le modèle "comble le vide" avec des moyennes statistiques |
| Rôle sans contexte | Réponse correcte mais hors-sol | Le modèle ignore la situation réelle |
| Format implicite | Réponse bien écrite mais inutilisable | Le modèle choisit un format par défaut |
| Instructions négatives | L'interdit est accompli | Les LLM traitent mal "ne pas faire X" |
| Trop de contraintes | Réponse rigide ou vide | Le modèle ne peut pas satisfaire toutes les règles |

---

## PC.2 — Le template humanisé (ordre validé)

### Structure canonique

```markdown
## Contexte
[Situation, background, ce que l'IA doit savoir pour comprendre la demande.
Qui, quoi, pourquoi, quel environnement, quelles contraintes extérieures.]

## Rôle
[Persona / expertise de l'IA. "Tu es un X spécialisé en Y."
Définit le ton, le niveau d'expertise, le point de vue.]

## Objectifs
[Ce que le prompt doit produire. Résultat attendu, pas la méthode.
Peut être une liste numérotée si plusieurs livrables.]

## Règles
[Contraintes obligatoires. Ce qu'il faut faire / ne pas faire.
Formuler en positif quand possible : "Toujours inclure..." plutôt que "Ne pas oublier..."]

## Format
[Structure de la réponse attendue. Longueur, style (Markdown / prose / liste),
titres, langue, longueur max, unités, etc.]

## Exemples
[Few-shot si nécessaire. Format : INPUT → OUTPUT.
1 exemple = minimum, 3 = recommandé pour les tâches complexes.]
```

### Règles d'or sur l'ordre
1. **Contexte avant Rôle** — le rôle prend sens dans un contexte
2. **Objectifs avant Règles** — ce qu'on veut avant les contraintes
3. **Format avant Exemples** — les exemples illustrent le format

### Exemple complet

```markdown
## Contexte
Je suis responsable formation chez Infopro Digital. Je prépare un email
à envoyer à 50 managers qui n'ont pas encore inscrit leurs équipes à la
formation IA obligatoire. La date limite est dans 10 jours.

## Rôle
Tu es un expert en communication interne et en conduite du changement.
Ton ton est professionnel, direct, bienveillant et légèrement urgent.

## Objectifs
Rédiger un email de relance qui provoque l'inscription.
L'email doit lever les 3 principales résistances : manque de temps,
doute sur la pertinence, peur du changement.

## Règles
- Toujours personnaliser avec [Prénom Manager]
- Ne pas utiliser de jargon technique IA
- Ne pas culpabiliser — créer une urgence positive
- Maximum 200 mots

## Format
- Objet de l'email (1 ligne)
- Corps en 3 paragraphes
- Appel à l'action final avec lien [LIEN_INSCRIPTION]

## Exemples
N/A (contexte suffisamment clair)
```

---

## PC.3 — Frameworks de marché comparés

| Framework | Acronyme | Origine | Forces | Limites |
|-----------|---------|---------|--------|---------|
| **Notre template** | C-R-O-R-F-E | Infopro / usage terrain | Ordre logique, exhaustif, mémorisable | Plus long à rédiger |
| **CO-STAR** | Context·Objective·Style·Tone·Audience·Response | Communauté OpenAI | Couvre le style et l'audience | Rôle absent |
| **RISEN** | Role·Instructions·Steps·End goal·Narrowing | Blog prompting | Structuré par étapes | Verbeux pour tâches simples |
| **RTF** | Role·Task·Format | Minimaliste | Ultra-rapide | Insuffisant pour tâches complexes |
| **CROF** | Context·Role·Output·Format | Anthropic-inspired | Concis | Pas de règles/contraintes explicites |

### Règle de sélection

```
Tâche simple (< 2 min) → RTF
Tâche standard → CO-STAR ou notre template sans exemples
Tâche complexe ou réutilisable → Notre template complet avec exemples
Agent Snowflake → PC.10 (voir section dédiée)
```

---

## PC.4 — Few-shot prompting

**Source :** Brown et al. (2020), *Language Models are Few-Shot Learners* (GPT-3 paper)

Le few-shot consiste à donner au modèle des exemples de paires INPUT → OUTPUT pour lui "montrer" plutôt que "décrire" ce qu'on veut.

### Combien d'exemples ?

| Nombre | Quand l'utiliser |
|--------|-----------------|
| 0-shot | Format standard, tâche connue |
| 1-shot | Format inhabituel mais simple |
| 3-shot | Format complexe, style précis, classification |
| 5-shot+ | Tâche très spécialisée, peu de données de fine-tuning |

### Format des exemples

```markdown
## Exemples

Exemple 1 :
INPUT : "Résumé de réunion : long, informel, plein de digressions"
OUTPUT :
**Décisions** : [liste]
**Actions** : [qui / quoi / quand]
**Points ouverts** : [liste]

Exemple 2 :
INPUT : "Résumé de réunion : court, déjà structuré"
OUTPUT :
**Décisions** : [liste]
**Actions** : [liste]
```

### Erreurs classiques en few-shot
- Exemples contradictoires entre eux
- Exemples qui illustrent l'exception plutôt que la règle
- Format d'exemple non cohérent (certains en Markdown, d'autres en texte brut)

---

## PC.5 — Chain-of-Thought (Wei et al., 2022)

**Source :** Jason Wei et al. (2022), *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (Google Brain)

Le CoT force le modèle à "penser à voix haute" avant de répondre, ce qui améliore significativement les performances sur les tâches de raisonnement.

### Deux variantes

| Variante | Syntaxe | Quand |
|---------|---------|-------|
| **Zero-shot CoT** | Ajouter "Réfléchis étape par étape." en fin de prompt | Tâches inattendues, exploration |
| **Few-shot CoT** | Montrer des exemples incluant le raisonnement intermédiaire | Tâches complexes répétables |

### Zero-shot CoT

```markdown
## Objectifs
Calculer le coût total de formation pour 3 groupes de 12 personnes.
Tarif jour : 850€ HT. Durée : 2 jours. TVA : 20%.

Réfléchis étape par étape avant de donner le résultat final.
```

### Limites du CoT
- Ralentit la génération (plus de tokens)
- Ne compense pas un contexte ou des données erronées
- Peut "inventer" des étapes si le modèle n'a pas les connaissances

---

## PC.6 — Itération de prompt : méthode des 3 versions

Un bon prompt ne s'écrit pas en un coup. La méthode des 3 versions structure l'amélioration.

### Protocole

```
V1 — Prompt minimal
→ Écrire le prompt le plus simple possible
→ Observer : qu'est-ce qui manque dans la réponse ?

V2 — Ajout ciblé
→ Corriger l'un des problèmes identifiés
→ Ne modifier qu'une variable à la fois (pour savoir ce qui a changé)

V3 — Consolidation
→ Fusionner les améliorations qui fonctionnent
→ Nettoyer les redondances
```

### Diff structuré entre versions

Avant de passer de V1 à V2, documenter :
- Ce qui était dans V1
- Ce qui a changé
- Pourquoi (quelle observation)

### A/B test de prompts

Pour les prompts à fort volume ou usage récurrent :
1. Identifier la métrique de qualité (pertinence 1-5, format correct oui/non, etc.)
2. Tester les 2 versions sur 10-20 inputs représentatifs
3. Choisir le gagnant avant de déployer

---

## PC.7 — Anti-patterns classiques

| Anti-pattern | Exemple | Pourquoi ça échoue | Solution |
|-------------|---------|-------------------|---------|
| **Le vague absolu** | "Rédige quelque chose sur l'IA" | Le modèle satisfait n'importe quelle interprétation | Ajouter objectif + public + format |
| **Rôle sans contexte** | "Tu es un expert" | L'expert de quoi ? pour qui ? | Contexte + rôle ensemble |
| **Format implicite** | (aucune section Format) | Le modèle choisit prose ou liste par défaut | Toujours expliciter le format |
| **Instructions négatives** | "Ne pas utiliser de jargon" | LLM suit mieux les positifs | "Utiliser un langage accessible à un non-expert" |
| **Sur-contraindre** | 15 règles contradictoires | Le modèle ne peut pas tout satisfaire | Prioritiser : 3-5 règles max |
| **Demander la méthode** | "Fais une analyse SWOT" | Outil imposé, objectif oublié | "Identifie les forces, faiblesses, opportunités, menaces" |
| **Attendre de la créativité sans espace** | Contexte + rôle + règles + format très stricts | Aucun espace pour générer | Laisser 1 dimension ouverte |

---

## PC.8 — Prompt pour tâches récurrentes : templating

### Variables avec placeholder

```markdown
## Contexte
Je travaille chez {{NOM_ENTREPRISE}}, secteur {{SECTEUR}}.
Mon audience est {{AUDIENCE}} (niveau {{NIVEAU_EXPERTISE}}).

## Objectifs
Rédiger {{TYPE_CONTENU}} sur le sujet : {{SUJET}}.
Longueur cible : {{LONGUEUR}}.
```

### Prompt library : 3 niveaux

| Niveau | Description | Exemple |
|--------|-------------|---------|
| **Base** | Prompt générique adaptable | Template email de relance |
| **Variante** | Base + spécialisation pour un contexte | Relance formation / relance événement |
| **Instance** | Variante avec toutes les variables remplies | Email relance formation IA Infopro |

### Bonnes pratiques de versioning

```
prompt-lib/
  email-relance/
    v1-base.md        ← template générique
    v2-formation.md   ← variante formation
    v3-evenement.md   ← variante événement
    CHANGELOG.md      ← ce qui a changé + pourquoi
```

---

## PC.9 — Évaluer un prompt : 5 critères

Avant de valider un prompt comme "prêt à déployer", le passer à travers ces 5 critères.

| Critère | Question | Méthode de test |
|---------|----------|----------------|
| **Précision** | La réponse contient-elle les informations demandées ? | Comparer à un "gold standard" |
| **Cohérence** | En relançant 3 fois, les réponses sont-elles cohérentes ? | 3 runs, comparer |
| **Format** | La structure est-elle exactement celle demandée ? | Checklist format |
| **Ton** | Le registre correspond-il à la cible ? | Lecture à voix haute |
| **Robustesse** | Avec un input légèrement différent, le prompt tient-il ? | 5 inputs variés |

### Score de validation

```
5/5 → Déploiement production
3-4/5 → Iterer sur les critères qui échouent
< 3/5 → Reprendre le prompt depuis V1
```

---

## PC.10 — Snowflake Cortex Agent (variante spécifique)

> **Source :** Documentation officielle Snowflake — [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents) · [Best Practices](https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents)

### Architecture du Cortex Agent

Un Cortex Agent combine **4 couches d'instructions** :

```
[Semantic Views]            → Instructions dans la couche données (SQL/vues)
[Orchestration instructions] → Logique de raisonnement + routage outils
[Response instructions]      → Format, ton, style de réponse
[Tool descriptions]          → Ce que chaque outil fait / quand l'utiliser
```

> ⚠️ Ne pas confondre **Orchestration** (QUOI faire, QUEL outil, QUAND) et **Response** (COMMENT répondre, QUEL format).

---

### Champ 1 — Orchestration Instructions

**Définition :** Govern how the agent reasons, plans, and selects tools. The "brain" of the agent.

**Ce qui va ici :**
- Identité et périmètre de l'agent
- Contexte métier et terminologie du domaine
- Règles de sélection des outils (quel outil pour quelle question)
- Limites et frontières (ce que l'agent ne doit PAS faire)
- Règles métier et logique conditionnelle
- Workflows multi-étapes

**Matrice de décision Orchestration vs Response :**

| Instruction | Ici ou là ? | Exemples |
|------------|------------|---------|
| Quel outil sélectionner | **Orchestration** | "Use CustomerData for current metrics" |
| Quelles données récupérer | **Orchestration** | "Include last 90 days of usage data" |
| Comment interpréter l'intention | **Orchestration** | "When user says 'recent', use last 30 days" |
| Séquencer les appels outils | **Orchestration** | "Always call CustomerLookup before CustomerMetrics" |
| Logique conditionnelle | **Orchestration** | "If result > 100 rows, aggregate before displaying" |
| Gestion d'erreur outil | **Orchestration** | "If error code X occurs, try alternative tool Y" |
| Format de la réponse | **Response** | "Use tables for multi-row results" |
| Ton | **Response** | "Be concise and professional" |
| Structure texte | **Response** | "Lead with direct answer, then details" |
| Message d'erreur à l'utilisateur | **Response** | "Explain limitation and suggest alternative" |

**Template Orchestration Instructions :**

```
**Role:**
You are "[NOM_AGENT]", a [DESCRIPTION_COURTE] for [ORGANISATION].
Your Scope: You answer questions about [DOMAINE_1], [DOMAINE_2], [DOMAINE_3].
Your Users: [PROFIL_UTILISATEURS] who need [BESOIN_PRINCIPAL].

**Domain Context:**
- [TERME_METIER_1] : [Définition]
- [TERME_METIER_2] : [Définition]
- Data refresh: [FRÉQUENCE] at [HEURE] [TIMEZONE]
- Fiscal year: [DATES]

**Tool Selection Guidelines:**
- For questions about [SUJET_1]: Use "[NOM_OUTIL_1]"
    Examples: "[EXEMPLE_QUESTION]", "[EXEMPLE_QUESTION]"
- For questions about [SUJET_2]: Use "[NOM_OUTIL_2]"
    Examples: "[EXEMPLE_QUESTION]"
- When intent is ambiguous between Tool A and Tool B: [RÈGLE DE TIEBREAK]

**Limitations and Boundaries:**
- You do NOT have access to [DONNÉES_EXCLUES].
    If asked, respond: "[MESSAGE_REDIRECT]"
- You do NOT have real-time data. Data refreshes [FRÉQUENCE].
- Do NOT [ACTION_INTERDITE].

**Business Rules:**
- When a user asks about [CAS_1], ALWAYS [ACTION_A] before [ACTION_B]
- If a result returns more than [N] rows, [AGGREGATION_RULE]
- For [CAS_EDGE], [COMPORTEMENT_ATTENDU]

**Workflow — [NOM_WORKFLOW] :**
When user asks "[TRIGGER_PHRASE]":
1. Use [OUTIL_1] to get [DONNÉES_1]
2. Use [OUTIL_2] to get [DONNÉES_2]
3. Present results as [FORMAT]
```

---

### Champ 2 — Response Instructions

**Définition :** Control the final output format, tone, and communication style. The "voice" of the agent.

**Ce qui va ici :**
- Style et ton de communication
- Format de présentation des données (table, chart, prose)
- Structure des réponses selon type de question
- Messages d'erreur pour l'utilisateur final

**Template Response Instructions :**

```
**Style:**
- [ADJECTIF_TON] and [ADJECTIF_TON] — [EXPLICATION_CONTEXTE]
- Lead with [QUOI EN PREMIER] then [QUOI ENSUITE]
- [RÈGLE DE TON]
- Avoid [CE QUI EST INTERDIT DANS LE TON]

**Data Presentation:**
- Use tables for [CONDITION] (ex: multi-row data, > 3 items)
- Use charts for [CONDITION] (ex: comparisons, trends, rankings)
- For single values: [FORMAT] (ex: state directly without table)
- Always include [MÉTADONNÉE] (ex: units, data freshness, time period)

**Response Structure:**
For "[TYPE_QUESTION_1]" questions:
  → [TEMPLATE_RÉPONSE]
  Example: "[EXEMPLE_RÉPONSE_FORMATÉE]"

For "[TYPE_QUESTION_2]" questions:
  → [TEMPLATE_RÉPONSE]

**Error Handling:**
- When data unavailable: "[MESSAGE_TYPE]"
- When query ambiguous: "[MESSAGE_TYPE]"
- When results empty: "[MESSAGE_TYPE]"
```

---

### Descriptions d'outils (Tool Descriptions)

**Règle d'or :** "Tool descriptions are often the culprit for most agent quality problems."

**Structure d'une bonne description d'outil :**

```
Name: [DOMAINE][FONCTION]   ← ex: CustomerConsumptionAnalytics, SalesforcePipelineQuery

Description:
[CE QUE L'OUTIL FAIT] + [QUELLES DONNÉES IL ACCÈDE] + [QUAND L'UTILISER] + [QUAND NE PAS L'UTILISER]

Data Coverage:
- [PÉRIMÈTRE ET FRAÎCHEUR DES DONNÉES]
- Sources: [TABLES / SERVICES]

When to Use:
- [CAS_USAGE_1]
- [CAS_USAGE_2]

When NOT to Use:
- Do NOT use for [CAS_EXCLU_1] (use [OUTIL_ALTERNATIF] instead)
- Do NOT use for [CAS_EXCLU_2]

Key Parameters:
- [PARAM_1]: Type [TYPE]. Required: [OUI/NON]. Format: [FORMAT]. Example: "[EXEMPLE]"
- [PARAM_2]: Type [TYPE]. Optional (defaults to [VALEUR_DÉFAUT]).
```

**Anti-patterns à éviter :**
- ❌ Nom générique : "DataTool", "Tool1", "Query"
- ❌ Description vague : "Gets data."
- ❌ Pas de "When NOT to Use" → l'agent utilisera l'outil pour tout
- ❌ Paramètres non typés → l'agent passera des formats incorrects

---

### Best Practices Snowflake Cortex Agent

**Scope :**
- Un agent = un périmètre métier précis (pas un agent omniscient)
- Commencer avec 20 questions "golden" stakeholder → deviennent le scope initial

**Instructions :**
- Ne pas répéter les comportements de base de Snowflake (gestion des outils, validation) — déjà inclus
- Séparer strictement Orchestration (logique) et Response (style)
- Orchestration = modifier les comportements ; Response = le ton et format

**Outils :**
- Cortex Analyst (Text-to-SQL) → pour données structurées + semantic views
- Cortex Search → pour RAG / documents non structurés
- Custom tools (UDF/stored proc) → pour actions ou calculs custom
- "Generate with Cortex" dans l'UI = bon point de départ pour les descriptions

**Performance :**
- Budget : time limit + token limit portent sur l'orchestration uniquement (pas les outils)
- Threads : obligatoires pour conversations multi-tours
- Pré-définir des queries vérifiées dans les semantic views pour les questions fréquentes
- Traces dans le monitoring tab pour diagnostiquer latence et erreurs

**Évaluation :**
- Créer un "golden set" de questions + outil attendu + réponse attendue
- Utiliser le framework GPA (Goal-Plan-Action) pour évaluer la fiabilité
- Surveiller : taux de sélection outil correct, latence, feedbacks négatifs

---

## Matrice : type de tâche → framework recommandé

| Type de tâche | Framework | Pourquoi |
|--------------|-----------|---------|
| Email rapide | RTF | Simplicité, pas besoin de plus |
| Article / contenu long | Notre template complet | Contexte + format + exemples nécessaires |
| Analyse de données | CO-STAR ou template + exemples | Style + audience important |
| Prompt réutilisable (prod) | Template + variables {{}} | Versioning, maintenance |
| Raisonnement complexe | Template + "réfléchis étape par étape" | Zero-shot CoT |
| Classification répétée | Few-shot 3 exemples | Montrer > décrire |
| Agent Snowflake | PC.10 (Orchestration + Response + Tools) | Architecture spécifique Cortex |

---

## Références

- Brown et al. (2020). *Language Models are Few-Shot Learners* (GPT-3 / NeurIPS)
- Wei et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in LLMs* (Google Brain)
- Snowflake Documentation — [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents)
- Snowflake — [Best Practices for Building Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents)
- Snowflake — [Cortex Agents Manage](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-manage)
