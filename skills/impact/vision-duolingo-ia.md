---
name: impact-vision-duolingo-ia
description: Vision stratégique complète du "Duolingo de l'IA" — formation IA adaptative et gamifiée propulsée par agents et base de connaissances. Architecture, pipeline de génération, univers visuels par métaphore, gamification, adaptive learning. Active sur Duolingo de l'IA, formation IA adaptative, génération dynamique contenu, univers métaphore, charte graphique formation.
family: impact
origin: Formation-Infopro — VISION_ADAPTIVE_LEARNING.md
version: 1.0.0
---

# Vision : Le "Duolingo de l'IA"

> Formation IA personnalisée, propulsée par nos agents et notre base de connaissances pédagogiques.
> Contenu "froid" (humain) + Couche "chaude" (agent génère) = Expérience apprenant unique.

---

## Architecture Générale

```
┌─────────────────────────────────────────────────────────────────┐
│  CONTENU FROID (Humain écrit)      COUCHE CHAUDE (Agent génère) │
│                                                                 │
│  • Concepts IA                     • Métaphores adaptées        │
│  • Infos entreprise (DIGI)         • QCM personnalisés          │
│  • Contacts, ressources            • Feedback Growth Mindset    │
│  • Cas d'usage Chainsnow           • Gamification               │
│  • Structure modules               • Rythme adaptatif           │
│                                                                 │
│         ↓                                    ↓                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │           EXPÉRIENCE APPRENANT UNIQUE                   │  │
│   └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Modules de Formation (Contenu Froid)

| Module | Contenu | Cas Chainsnow |
|--------|---------|---------------|
| **M0 — Onboarding** | Profiling (ennéagramme/VAKOG), attentes, peurs, choix métaphore | — |
| **M1 — C'est quoi l'IA ?** | LLM = prédiction, hallucinations, Chatbot vs Agent vs Copilote | DIGI : À quoi sert notre chatbot interne |
| **M2 — Le Prompt** | Anatomie (Rôle + Contexte + Contraintes + Output), erreurs classiques | Exemples de prompts métier |
| **M3 — La Data** | GIGO, préparation données, formats, qualité, volume | Nos pipelines de données |
| **M4 — Le RAG / VectorStore** | Embeddings, chunks, similarité, retrieval, RAG vs Text2SQL | Architecture de nos agents |
| **M5 — Évaluation & Guardrails** | Métriques, tests, benchmarks, sécurité | Notre monitoring |
| **M6 — Déploiement** | De l'idée à la prod, rôles équipe, maintenance | — |

---

## Gamification : Le Modèle "Duolingo"

### Éléments Core

| Élément | Description | Implémentation |
|---------|-------------|----------------|
| **Streak quotidien** | "5 jours consécutifs ! 🔥" — pousse à revenir | Notification + visuel |
| **XP (Points d'expérience)** | Gagnés à chaque leçon/quiz complété | Barre de progression |
| **Niveaux** | Débutant → Initié → Praticien → Expert → Maître | Seuils définis par compétence |
| **Badges/Achievements** | "Premier prompt réussi", "Chasseur de biais" | Débloqués sur critères objectifs |

### Carte Compétence (Style Panini/FIFA)

```
┌─────────────────────────────────────────┐
│  🃏 CARTE COMPÉTENCE                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  [Avatar]           YANN PONAIRE        │
│                     Niveau: Expert      │
│                     XP: 2,450           │
│                                         │
│  Prompting      ████████░░ 80%          │
│  Data           ████░░░░░░ 40%          │
│  RAG            █████████░ 90%          │
│  Évaluation     ██░░░░░░░░ 20%          │
│  Architecture   ██████░░░░ 60%          │
│                                         │
│  🏆 Badges: [🎯] [🔥] [🧠] [📚]         │
└─────────────────────────────────────────┘
```

### Toile d'Araignée des Compétences (Radar Chart)

```
                    Prompting
                       ██
                      ████
                     ██████
        Architecture ████████ Data Prep
                    ██████████
                   ████████████
        Évaluation ████████████ RAG/Retrieval
                    ██████████
                     ████████
                      ████
                   Déploiement
```

### Micro-Sessions (3-5 min)

| Type | Durée | Fréquence | Exemple |
|------|-------|-----------|---------|
| **Leçon concept** | 3-5 min | À la demande | "Le RAG en 3 min" |
| **Quiz rapide** | 2 min | Quotidien | Rappel streak |
| **Défi pratique** | 5-10 min | Hebdo | Prompt à construire |
| **Boss fight** | 15-20 min | Fin de module | Évaluation intégrée |

### Rappels Intelligents (Spacing Effect)

```
Jour 1:  Apprend le concept "Hallucinations"
Jour 2:  Quiz rapide (1 question)
Jour 4:  Quiz rapide (2 questions)
Jour 7:  Quiz + nouveau contenu lié
Jour 14: Révision intégrée
Jour 30: Test de rétention
```

L'agent gère le calendrier selon la courbe d'oubli de chaque apprenant.

---

## Parcours Types

### Découverte (COMEX/Direction)
```
Module 0 → Module 1 → Quiz Boss → Carte "Initié"
Durée: ~30 min répartis sur 1 semaine
```

### Utilisateur (Chefs de produit, Métiers)
```
Module 0 → 1 → 2 → 3 (light) → Quiz Boss → Carte "Praticien"
Durée: ~2h réparties sur 2 semaines
```

### Builder (Tech, Data)
```
Tous les modules → Défis pratiques → Projet final → Carte "Expert"
Durée: ~5h réparties sur 1 mois
```

---

## Univers Visuels par Métaphore

Chaque métaphore = un **thème graphique complet** (couleurs, icônes, images, analogies visuelles). L'apprenant est immergé dans SON univers.

### 🧳 Métaphore Valise (Module Data)

**Concept** : Préparer ses données = préparer sa valise

**Étape 1** : Trier ce qu'on emmène
> "Vos données c'est comme vos vêtements. Tout prendre = valise qui explose. Bien choisir = voyage serein."

**Quiz contextualisé** :
> Vous partez 3 jours. Que mettez-vous ?
> ○ Toute votre garde-robe (= toute la BDD)
> ● 3 tenues adaptées (= données filtrées)
> ○ Rien, j'achète sur place (= API live)

**Charte graphique** : Bleu voyage, sable, terracotta | Stamps, stickers | Ambiance aventure, exploration

### 👨‍🍳 Métaphore Cuisine (Module Data)

**Concept** : Préparer ses données = mise en place du chef

**Étape 1** : La mise en place
> "Un chef ne commence jamais à cuisiner sans avoir tout préparé, lavé, coupé, pesé. Vos données c'est pareil."

**Quiz contextualisé** :
> Avant de cuisiner un risotto, vous...
> ○ Jetez tout dans la casserole (= data brute)
> ● Préparez chaque ingrédient (= data clean)
> ○ Commandez en livraison (= API)

**Charte graphique** : Rouge, crème, vert basilic | Ustensiles | Ambiance chaleureuse, gourmande

### 🔩 Métaphore IKEA (Module Data)

**Concept** : Préparer ses données = inventaire des pièces IKEA

**Étape 1** : Inventaire des pièces
> "Avant de monter le meuble, on ouvre le carton, on trie les pièces, on vérifie qu'il ne manque rien. Sinon on se retrouve avec 3 vis en trop à la fin."

**Quiz contextualisé** :
> Vous ouvrez le carton KALLAX. D'abord...
> ○ On visse direct (= query sans prépa)
> ● On trie et on compte (= data profiling)
> ○ On appelle un pote (= consultant externe)

**Charte graphique** : Bleu IKEA, jaune, bois naturel | Schémas techniques | Ambiance méthodique, DIY

### Charte Graphique Récapitulative

| Métaphore | Palette | Style icônes | Ambiance |
|-----------|---------|--------------|----------|
| 🧳 Valise | Bleu voyage, sable, terracotta | Stamps, stickers | Aventure |
| 👨‍🍳 Cuisine | Rouge, crème, vert basilic | Ustensiles | Chaleureux |
| 🔩 IKEA | Bleu IKEA, jaune, bois | Schémas techniques | Méthodique |
| 🐕 Chien | Vert prairie, marron, ciel | Pattes, os, balles | Fun, loyal |
| 🏟️ Match | Vert terrain, blanc, noir | Sifflet, carton | Compétitif |

---

## Pipeline de Génération Dynamique

```
1. REQUÊTE
   User: "Je veux apprendre le module Data"
   + Profil: Type 6 (Loyaliste), VAKOG Visuel

2. GÉNÉRATION (Agent)
   → Sélectionne métaphore "Valise" (adaptée au profil)
   → Génère HTML/JS du module
   → Inclut quiz personnalisé
   → Ajoute visuels (diagrammes, animations)

3. VALIDATION (Automated)
   → HTMLHint / ESLint (syntax)
   → Lighthouse (perf, a11y)
   → Security scan (XSS, injections)
   → Preview sandbox

4. DÉPLOIEMENT
   → Si OK: Push vers CDN/Vercel
   → Si KO: Agent corrige et reboucle

5. TRACKING
   → Progression enregistrée
   → Analytics comportement
   → Feedback pour améliorer
```

### Validator : Ce qu'on Check

| Check | Outil | Critère |
|-------|-------|---------|
| **Syntax HTML** | HTMLHint | 0 erreurs |
| **Syntax JS** | ESLint | 0 erreurs |
| **Accessibilité** | axe-core / Lighthouse | Score > 90 |
| **Performance** | Lighthouse | Score > 80 |
| **Sécurité** | Custom + OWASP | Pas de XSS, injections |
| **Responsive** | Playwright | OK mobile/tablet/desktop |

### Architecture Cible

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SNOWFLAKE                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │   Cortex    │  │  Learner    │  │  Content    │                     │
│  │   Agents    │  │  Profiles   │  │   Store     │                     │
│  └──────┬──────┘  └─────────────┘  └─────────────┘                     │
│         │                                                               │
└─────────┼───────────────────────────────────────────────────────────────┘
          │
          ▼ Génère HTML
┌─────────────────────┐
│    n8n / GitHub     │◄─── Validation Pipeline
│    Actions          │
└─────────┬───────────┘
          │
          ▼ Si OK
┌─────────────────────┐     ┌─────────────────────┐
│   Vercel / CDN      │────▶│   formation.ipd.com │
│   (Static Deploy)   │     │   (Site public)     │
└─────────────────────┘     └─────────────────────┘
```

---

## Stack Technique Envisagée

| Composant | Option 1 (Full Snowflake) | Option 2 (Hybride) | Option 3 (Web-First) |
|-----------|---------------------------|---------------------|----------------------|
| **Backend** | Cortex Agents | n8n + Cortex | n8n + Cortex |
| **Frontend** | Streamlit in Snowflake | Next.js / Vercel | Site statique généré |
| **Génération** | Agent → Streamlit | Agent → n8n → Deploy | Agent → Validate → CDN |
| **Data** | Snowflake tables | Snowflake | Snowflake |
| **Auth** | Snowflake SSO | Auth0 / SSO entreprise | SSO entreprise |
| **Validation** | N/A (Streamlit géré) | GitHub Actions | n8n + Lighthouse |
| **Notifications** | Email / Slack webhook | n8n automations | n8n automations |

---

## Idées Avancées (Easter Eggs)

- **Questions bonus cachées** : Déclenchées par des chemins non-standard
- **Achievements secrets** : "A posé la question qui a fait bugger l'IA"
- **Mode "Hard"** : Pour les téméraires, sans aide
- **Défier un collègue** : Sur un quiz spécifique
- **Leagues** : Classement par équipe/département

---

## Questions Ouvertes (À Décider)

1. **Obligatoire ou volontaire ?** La formation est-elle imposée ou opt-in ?
2. **Temps alloué ?** Les collaborateurs ont-ils du temps dédié ?
3. **Incentives ?** Récompenses réelles (pas que virtuelles) ?
4. **Intégration RH ?** Lien avec les entretiens annuels ?
5. **Multi-langue ?** Besoin EN/FR ?

---

## Références Croisées

| Besoin | Skills Impact |
|--------|---------------|
| Gamification détaillée | `gamification.md` (Octalysis, Fogg, SDT, Variable Reward) |
| Adaptive Learning | `adaptive-learning.md` (Spaced Repetition, Mastery Learning, ZPD) |
| Design pédagogique | `instructional-design.md` (ADDIE, Bloom, Kirkpatrick) |
| Profils psychologiques | `enneagramme.md` (Types 1-9 face à l'IA) |
| Quiz & évaluation | `quiz-design.md` (Distracteurs, Hypercorrection, Bloom) |

---

*Document issu de VISION_ADAPTIVE_LEARNING.md — Formation Infopro Digital — Février 2026*
