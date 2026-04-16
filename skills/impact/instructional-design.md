---
name: impact-instructional-design
description: Ingénierie pédagogique — concevoir, structurer et évaluer une formation de A à Z. ADDIE, SAM, Backward Design, Bloom verbs, Kirkpatrick 4 niveaux, Mayer Multimedia, 70-20-10, microlearning. Active sur instructional design, ingénierie pédagogie, ADDIE, objectifs pédagogiques, évaluation formation, e-learning.
family: impact
origin: Formations-Infopro
version: 1.0.0
---

# Impact — Instructional Design & Ingénierie Pédagogique

## Quand activer ce skill

- Concevoir une formation de A à Z (objectifs → livrable → évaluation)
- Écrire des objectifs pédagogiques clairs et mesurables
- Choisir entre ADDIE, SAM ou Backward Design pour son contexte
- Évaluer l'impact réel d'une formation (au-delà du "c'était bien")
- Adapter un cours présentiel en e-learning ou blended
- Décider quoi mettre en microlearning vs session longue

---

# ID. Ingénierie Pédagogique

> "Designing instruction is not about making beautiful slides. It's about engineering the conditions under which learning occurs." — Robert Gagné

## ID.1 ADDIE vs SAM — Choisir son modèle

**Source** :
- ADDIE : Florida State University (années 1970), popularisé par l'armée américaine
- SAM : Michael Allen, *Leaving ADDIE for SAM* (2012)

**Principe** :

```
ADDIE — Séquentiel
────────────────────────────────────────────
Analyze → Design → Develop → Implement → Evaluate
   │         │         │          │          │
   └──────────── Phase suivante ──────────────┘
   Avantage : rigoureux, documenté
   Inconvénient : lent, rigide, feedback tard

SAM — Itératif (Successive Approximation Model)
────────────────────────────────────────────────
Preparation → Iterative Design → Iterative Development
     ↑                ↕                   ↕
     └──── Prototype rapide → Test → Amélioration ────┘
   Avantage : prototype rapide, feedback tôt, agile
   Inconvénient : moins documenté, demande un client impliqué
```

**Quand utiliser quoi** :

| Contexte | Modèle recommandé |
|----------|------------------|
| Formation réglementaire, grande organisation, approbations multiples | ADDIE |
| Startup, formation interne, deadline courte, client itératif | SAM |
| Projet IA/tech évolutif comme Duolingo de l'IA | **SAM** — le contenu change vite |

---

## ID.2 Backward Design (Conception à Rebours)

**Source** : Grant Wiggins & Jay McTighe, *Understanding by Design* (1998, ASCD)

**Citation** : *"Begin with the end in mind: what should students know, understand, and be able to do?"*

**Principe** : Ne pas commencer par "que vais-je enseigner ?" mais par "qu'est-ce que l'apprenant saura faire à la fin ?"

```
ORDRE CLASSIQUE (mauvais)    BACKWARD DESIGN (Wiggins)
──────────────────────        ──────────────────────
1. Contenu disponible    →    1. Résultats attendus (what can they DO?)
2. Activités             →    2. Preuves d'apprentissage (comment mesurer?)
3. Évaluation            →    3. Activités d'apprentissage (design backward)
```

**Les 3 questions de Wiggins avant tout contenu** :
1. Quel est le **résultat durable** espéré ? (pas "ils auront entendu parler de X")
2. Quelle **preuve** montrerait qu'ils l'ont acquis ?
3. Quelles **activités** permettront cette acquisition ?

**Application** :
- Avant d'écrire une slide : "Si cette session s'arrête là, qu'est-ce que l'apprenant doit pouvoir FAIRE ?"
- Concevoir le **quiz final avant les slides** → discipline radicale contre le cours encyclopédique
- Lien avec Kirkpatrick Niveau 3 : Backward Design force à penser au transfert réel dès le début

---

## ID.3 Taxonomie de Bloom & Verbes d'Action

**Source** : Benjamin Bloom et al., *Taxonomy of Educational Objectives* (1956) ; révision par Lorin Anderson & David Krathwohl (2001)

**Citation** : *"Not all cognitive objectives are created equal. Remembering a fact is not the same as applying it."*

**Principe** : 6 niveaux cognitifs, du plus simple au plus complexe. Chaque objectif pédagogique doit commencer par un **verbe d'action** qui situe le niveau visé.

```
          ┌─────────────┐
          │  CRÉER       │← Produire, concevoir, formuler, planifier
          ├─────────────┤
          │  ÉVALUER    │← Juger, défendre, critiquer, sélectionner
          ├─────────────┤
          │  ANALYSER   │← Différencier, distinguer, organiser, relier
          ├─────────────┤
          │  APPLIQUER  │← Utiliser, exécuter, implémenter, résoudre
          ├─────────────┤
          │  COMPRENDRE │← Expliquer, résumer, paraphraser, classer
          ├─────────────┤
          │  MÉMORISER  │← Réciter, identifier, nommer, reconnaître
          └─────────────┘
```

**Verbes précis par niveau** :

| Niveau | Verbes | Exemple formation IA |
|--------|--------|---------------------|
| Mémoriser | Définir, lister, réciter, identifier | "Définir ce qu'est un token" |
| Comprendre | Expliquer, résumer, illustrer, comparer | "Expliquer pourquoi le contexte influence la réponse" |
| Appliquer | Utiliser, exécuter, résoudre, démontrer | "Utiliser les 6 éléments du prompt pour une tâche réelle" |
| Analyser | Différencier, distinguer, organiser, relier | "Analyser pourquoi ce prompt produit une hallucination" |
| Évaluer | Juger, défendre, critiquer, sélectionner | "Sélectionner la meilleure approche RAG pour ce cas" |
| Créer | Concevoir, planifier, produire, formuler | "Concevoir un agent pour automatiser ce workflow" |

**Règle pratique** :
- Éviter les verbes vagues : "comprendre", "connaître", "maîtriser" → non mesurables
- Un objectif bien formé = **Verbe Bloom + Conditions + Critère** (formule Mager, voir ID.4)

---

## ID.4 Objectifs Pédagogiques (Mager)

**Source** : Robert Mager, *Preparing Instructional Objectives* (1962, 1984)

**Citation** : *"If you're not sure where you're going, you're liable to end up someplace else."*

**Principe** : Un objectif pédagogique bien formé comporte 3 éléments (formule ABC) :
- **A**udience : pour qui ?
- **B**ehavior : que fera-t-il ? (verbe observable, Bloom)
- **C**ondition + **D**egree : dans quelles conditions ? avec quel niveau de performance ?

```
MAUVAIS OBJECTIF :
"Les participants comprendront les fondamentaux du prompting"
→ "comprendre" = non mesurable

BON OBJECTIF (Mager) :
"À l'issue de la session, le participant sera capable de
rédiger un prompt en 6 éléments [Behavior] pour une situation
professionnelle réelle [Condition] sans aide [Condition] avec
un taux de réussite ≥4/5 sur les critères de complétude [Degree]"
```

**Application** :
- Rédiger les objectifs AVANT le contenu (Backward Design)
- Maximum 3 objectifs par module de 90 min — au-delà = contenu surchargé
- Partager les objectifs avec les apprenants dès le début ("Voici ce que vous saurez faire")

---

## ID.5 Modèle Kirkpatrick — 4 Niveaux d'Évaluation

**Source** : Donald Kirkpatrick, *Evaluating Training Programs* (1959, 1994) ; James Kirkpatrick (fils), version New World Kirkpatrick (2016)

**Citation** : *"The only way to truly know if a training program is working is to measure it at all four levels."*

**Principe** : 4 niveaux d'évaluation, du plus facile au plus impactant.

```
Niveau 4 : RÉSULTATS        ← Business impact (ROI, chiffre d'affaires, qualité)
    ↑ causé par
Niveau 3 : COMPORTEMENT     ← Est-ce qu'ils font différemment au travail ?
    ↑ causé par
Niveau 2 : APPRENTISSAGE    ← Est-ce qu'ils savent faire ? (compétence)
    ↑ causé par
Niveau 1 : RÉACTION         ← Est-ce qu'ils ont aimé ? (satisfaction J+0)
```

**Réalité** : 80% des organisations ne mesurent que le Niveau 1 (questionnaire à chaud).

| Niveau | Outil de mesure | Timing |
|--------|----------------|--------|
| 1 Réaction | Questionnaire satisfaction | J+0 (fin de session) |
| 2 Apprentissage | Quiz avant/après, démonstration | J+0 à J+7 |
| 3 Comportement | Observation, entretien manager | J+30 à J+90 |
| 4 Résultats | KPIs business définis en amont | J+90 à J+180 |

**Application** :
- Définir les indicateurs Niveau 3 et 4 **avant** la formation (Backward Design + Kirkpatrick)
- Quiz à J+7 = Niveau 2 différé — bien plus fiable que le quiz à chaud
- "Est-ce que vos équipes promptent différemment depuis la formation ?" = Niveau 3 en 1 question

---

## ID.6 Principes Multimédia de Mayer

**Source** : Richard Mayer, *Multimedia Learning* (2001, 2009) — 20 ans d'expériences en laboratoire

**Citation** : *"People learn more deeply from words and pictures than from words alone."*

**Principe** : Le cerveau traite les informations visuelles et verbales via 2 canaux séparés (Dual Coding, Paivio). Chaque canal a une capacité limitée. Un bon design multimédia coordonne les canaux sans les surcharger.

**12 Principes** (les 6 essentiels) :

| Principe | Ce qu'il dit | Application pratique |
|----------|-------------|---------------------|
| **Cohérence** | Supprimer le contenu non essentiel | Pas de musique de fond pendant l'explication |
| **Signalisation** | Mettre en évidence les éléments clés | Flèches, couleurs, surlignage dans la slide |
| **Redondance** | Ne pas ajouter du texte complet sur une slide avec narration audio | Slide minimaliste + voix off OU texte complet SANS voix off |
| **Contiguïté spatiale** | Placer texte et image correspondants proches | Légendes juste à côté des éléments, pas en bas de page |
| **Segmentation** | Diviser en petits segments avec contrôle du rythme | Pause entre chaque concept, bouton "suivant" |
| **Pré-formation** | Enseigner les concepts clés avant la leçon principale | Glossaire avant le module, mini-lexique en amont |

**Application** :
- La règle "1 slide = 1 idée" vient directement de Mayer (éviter la surcharge cognitive canal visuel)
- Les vidéos pédagogiques > 6 min perdent l'attention → segmenter (Philip Guo, edX study, 2014)
- Texte + image coordonnés > texte seul (Cohen's d = 0.72, effet fort)

---

## ID.7 Modèle 70-20-10

**Source** : Morgan McCall, Robert Lombardo & Michael Eichinger, *The Career Architect Development Planner* (1996, Centre for Creative Leadership)

**Citation** : *"Development is primarily about stretch, experiences and challenges."*

**Principe** : Les compétences professionnelles se développent via 3 sources :

| Source | % | Type |
|--------|---|------|
| **Expériences terrain** | 70% | Faire pour de vrai, projets, erreurs |
| **Apprentissage social** | 20% | Feedback, mentoring, observation de pairs |
| **Formation formelle** | 10% | Cours, e-learning, conférences |

**Attention** : Ce ne sont pas des prescriptions strictes — des études récentes (Clardy, 2018) montrent des variations selon le contexte.

**Application** :
- Une formation présentielle de 2 jours = 10% du développement seulement
- Le vrai apprentissage se passe dans les 70% → concevoir des missions terrain post-formation
- DIGI comme filet de sécurité post-formation = activation du 20% (aide de l'IA comme mentor)
- "Plan d'action individuel" en fin de session = pont vers les 70%

---

## ID.8 Microlearning

**Source** : Theo Hug, *Micro Learning and Narration* (2005) ; Nick Shackleton-Jones, *How People Learn* (2019)

**Citation** : *"Microlearning is not about making training shorter. It's about making the unit of change smaller."*

**Principe** : Unité d'apprentissage courte (2-7 min), autonome, axée sur **une seule compétence**.

**Comparaison** :

| | Formation longue | Microlearning |
|-|-----------------|---------------|
| Durée | 1-2 jours | 2-7 min |
| Scope | Large | 1 concept, 1 skill |
| Contexte | Planifié | Juste-à-temps (Just-in-Time) |
| Rétention | Élevée pendant, décroît vite | Répétée → très élevée |
| Usage | Acquisition initiale | Rappel, practice, troubleshooting |

**Formats microlearning** :
- Vidéo < 5 min (règle Guo/edX)
- Infographie 1 concept
- Quiz 3-5 questions
- Podcast 5 min (concept + exemple + application)
- "One-pager" imprimable

**Application** :
- Ne pas micro-learner les compétences complexes qui requièrent du contexte → garder en formation longue
- Microlearning idéal pour : révision post-formation (Ebbinghaus J+7, J+30), glossaire, FAQ
- Les fiches formation (F1-F9) sunt des microlearning documents — chargeables dans DIGI

---

## Combinaisons recommandées

| Situation | Skills à combiner |
|-----------|------------------|
| Concevoir une formation complète de A à Z | `instructional-design.md` + `adaptive-learning.md` + `structure.md` |
| Écrire des objectifs percutants | `instructional-design.md` + `action.md` |
| Design de slides efficaces | `instructional-design.md` + `storytelling.md` + `simplifier.md` |
| Évaluer l'impact d'une formation existante | `instructional-design.md` + `feedback.md` |
| Transformer une formation en e-learning | `instructional-design.md` + `adaptive-learning.md` + `gamification.md` |
