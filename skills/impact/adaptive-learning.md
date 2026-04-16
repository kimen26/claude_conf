---
name: impact-adaptive-learning
description: Concevoir des parcours d'apprentissage qui s'adaptent au rythme, au niveau et aux lacunes de chaque apprenant. Spaced repetition, Mastery Learning, Testing Effect, Desirable Difficulties, Learning Analytics. Active sur adaptive learning, parcours personnalisé, répétition espacée, rétention long terme, évaluation formative, SuperMemo, Anki.
family: impact
origin: Formations-Infopro
version: 1.0.0
---

# Impact — Adaptive Learning & Parcours Personnalisés

## Quand activer ce skill

- Concevoir un parcours qui s'adapte au niveau ou au rythme de l'apprenant
- Maximiser la rétention sur le long terme (pas seulement pendant la session)
- Choisir quand faire réviser, re-tester, ou avancer
- Analyser pourquoi des apprenants oublient rapidement après la formation
- Construire la mécanique pédagogique du projet "Duolingo de l'IA"

---

# AL. Apprentissage Adaptatif

> L'apprentissage adaptatif n'est pas l'IA qui "personnalise tout" — c'est aligner le bon contenu, au bon niveau, au bon moment.

## AL.1 Courbe de l'Oubli & Répétition Espacée (Spaced Repetition)

**Source** : Hermann Ebbinghaus, *Über das Gedächtnis* (1885) ; Piotr Wozniak, algorithme SM-2 (SuperMemo, 1987) ; Sebastian Leitner, *So lernt man lernen* (1972)

**Citation** : *"The relearning of forgotten material is much quicker than the original learning."* — Ebbinghaus

**Principe** :
Sans révision, on oublie exponentiellement : ~50% en 1 heure, ~70% en 24h, ~90% en 7 jours.
La répétition espacée exploite l'**effet d'espacement** : réviser juste *avant* l'oubli consolide bien plus qu'une révision immédiate.

```
Rétention
100% ─┐
      │\         ← Sans révision
      │  \
 50% ─┤    \──────┬────── ← Avec révision espacée
      │           │\
      │           │  \───────┬──────────
      └───────────┴──────────┴─────────→ Temps
      0     1h  24h  7j    30j
```

**Algorithme Leitner (version low-tech)** :
- Boîte 1 : réviser chaque jour
- Boîte 2 : réviser tous les 2 jours
- Boîte 3 : réviser tous les 4 jours
- Si réponse fausse → retour en Boîte 1
- Si réponse juste → avancer d'une boîte

**Application** :
- Ne jamais "voir le concept une seule fois en formation" → prévoir une capsule de rappel J+1, J+7, J+30
- Quiz de rappel à J+7 = intervention la plus rentable par rapport au temps passé (source : Cepeda et al., 2006 — méta-analyse 254 études)
- Anki, Duolingo, Babbel = tous basés sur SM-2

---

## AL.2 Mastery Learning & Problème des 2 Sigma

**Source** : Benjamin Bloom, *The 2 Sigma Problem* (1984, Educational Researcher)

**Citation** : *"The average tutored student performed two standard deviations better than the average conventionally taught student."*

**Principe** :
Bloom a prouvé expérimentalement que le tutorat individuel produit des résultats **2 écarts-types supérieurs** à l'enseignement collectif standard. Dans une classe normale, un élève moyen devient "exceptionnel" avec un tutorat 1-to-1.

Le **Mastery Learning** propose de répliquer cet effet sans tutorat individuel :
1. Définir un seuil de maîtrise explicite (ex : 80% de réussite)
2. Permettre à l'apprenant de progresser **seulement** s'il maîtrise l'étape précédente
3. Proposer des voies alternatives pour ceux qui n'ont pas atteint le seuil

**Application** :
- Parcours adaptatif = "tu ne passes au prompt avancé que si tu maîtrises les 6 éléments de base"
- Le quiz formateur n'est pas une évaluation — c'est un **diagnostic de déviation**
- L'IA peut approcher le 2 Sigma via feedback immédiat + adaptation automatique du contenu

---

## AL.3 Zone Proximale de Développement (ZPD)

**Source** : Lev Vygotsky, *Mind in Society* (1978) ; complété par Wood, Bruner & Ross sur le *Scaffolding* (1976)

**Citation** : *"What a child can do with assistance today, she will be able to do by herself tomorrow."* (adapté adulte : "à l'apprenant guidé")

**Principe** : Distance entre ce que l'apprenant peut faire **seul** et ce qu'il peut faire **avec aide**. La ZPD est la zone d'apprentissage optimale.

```
         ┌──────────────────────┐
         │   ZPD (zone de      │← Ici se passe l'apprentissage réel
         │   développement)    │
    ─────┼──────────────────────┼─────
    Sait │                      │ Hors portée
    déjà │                      │ (même avec aide)
         └──────────────────────┘
              ↑ Scaffolding ↑
```

**Scaffolding (Bruner)** : L'enseignant/formateur ou l'IA fournit un support temporaire exactement dans la ZPD, puis le retire progressivement (fading).

**Application** :
- Toujours évaluer le niveau *avant* pour positionner dans la ZPD (pré-test ou questionnaire)
- Pas assez difficile → ennui (Flow channel). Trop difficile → anxiété (Csikszentmihalyi, cf. `structure.md`)
- En pratique : "prompt 0-shot" → "prompt avec contexte" → "prompt multi-step" = scaffolding progressif

---

## AL.4 Testing Effect (Retrieval Practice)

**Source** : Henry Roediger III & Jeffrey D. Karpicke, *Test-Enhanced Learning* (2006, Psychological Science) — étude sur 120 étudiants

**Citation** : *"Practicing recall helps retention far more effectively than studying the material again."*

**Principe** : Essayer de se rappeler une information (retrieval) consolide la mémoire **bien plus** que relire le contenu, même si on échoue à se rappeler.

| Méthode | Rétention à 1 semaine |
|---------|----------------------|
| Étudier 4 fois | ~40% |
| Étudier 3 fois + 1 test | ~55% |
| Étudier 1 fois + 3 tests | **~67%** |

**Application** :
- Chaque module doit finir par **"Récite ce que tu as appris"** plutôt que "Voilà le résumé"
- Les quiz ne sont pas que de l'évaluation — ce sont des **activités d'apprentissage** en eux-mêmes
- "Ferme ton écran et explique ce que tu viens d'apprendre à ton voisin" = retrieval practice gratuit

---

## AL.5 Interleaving vs Blocking

**Source** : Robert Bjork, *Desirable Difficulties* (1994, UCLA) ; Nicholas Cepeda et al., revue méta-analytique (2006)

**Citation** : *"Conditions that make practice more difficult, and lead to more errors, often produce better long-term learning."*

**Principe** : L'**interleaving** (mélanger les sujets) produit plus de confusion pendant l'apprentissage mais une meilleure rétention à long terme que le **blocking** (bloc thématique).

| Méthode | Expérience immédiate | Rétention J+30 |
|---------|---------------------|----------------|
| **Blocking** (AAABBBCCC) | Confort, sentiment de maîtrise | Faible |
| **Interleaving** (ABCABCABC) | Difficile, frustrant | Forte |

**Autres Desirable Difficulties** :

| Difficulté désirable | Description |
|---------------------|-------------|
| **Spacing** (voir AL.1) | Réviser espacé plutôt que massé |
| **Generation Effect** | Trouver la réponse avant de la voir (génération active > lecture passive) |
| **Disfluency** | Légère difficulté de lecture → meilleure mémorisation (police difficile, reformulation) |

**Application** :
- Ne pas enseigner "Prompting" puis "RAG" puis "Agents" en blocs — entremêler les questions
- Quiz final = questions mélangées de tous les modules
- "Devine d'abord avant que je t'explique" = Generation Effect

---

## AL.6 Learning Analytics & Mesure de l'apprentissage

**Source** : George Siemens & Phil Long, *Penetrating the Fog: Analytics in Learning and Education* (2011) ; George Siemens, fondateur du concept de Learning Analytics

**Citation** : *"Learning analytics is the measurement, collection, analysis and reporting of data about learners and their contexts, for purposes of understanding and optimizing learning."*

**Principe** : Utiliser les données comportementales (temps passé, erreurs, séquences) pour diagnostiquer les lacunes et adapter le parcours.

**Indicateurs clés** :

| Indicateur | Ce qu'il révèle | Action |
|-----------|-----------------|--------|
| **Temps par module** | Difficultés cachées ou démotivation | Revoir le module/scinder |
| **Taux d'erreur par question** | Concept mal enseigné ou mal formulé | Réviser l'explication |
| **Abandon point X** | Pic de complexité ou de friction (Fogg) | Réduire la friction à ce point |
| **Score à J+7 vs J+0** | Rétention réelle vs rétention à chaud | Ajuster la répétition espacée |
| **Ordre des erreurs** | Prérequis manquants | Revoir le prerequisite mapping |

**Application** :
- Définir **avant le lancement** les 3 indicateurs qu'on suivra — pas les 30 disponibles
- Le dropout rate à un point précis est une information actionnable (pas juste une stat)
- En présentiel : lever de main, tour de table, Mentimeter = analytics basse technologie

---

## AL.7 Prerequisite Mapping (Graphe de Dépendances)

**Source** : John Carroll, *The Carroll Model* (1963) ; ALEKS (Assessment and Learning in Knowledge Spaces), Université d'Arizona

**Principe** : Certains concepts ne peuvent être compris qu'après d'autres. Cartographier les prérequis évite de construire sur du vide.

```
       ┌─────────┐     ┌─────────────────┐
       │ Token   │────→│ Fenêtre contexte│
       └─────────┘     └────────┬────────┘
                                 │
       ┌──────────┐              ↓
       │ LLM      │────→  ┌─────────────┐
       └──────────┘        │ RAG         │
                           └──────┬──────┘
       ┌──────────┐               ↓
       │ Embedding│────→  ┌──────────────┐
       └──────────┘        │ Agent        │
                           └──────────────┘
```

**Application** :
- Cartographier les prérequis avant de séquencer le parcours (pas l'inverse)
- Si un apprenant échoue → remonter le graphe pour identifier où est la lacune réelle
- ALEKS (mathématiques) a réduit le temps d'apprentissage de 30% avec ce modèle seul

---

## Combinaisons recommandées

| Situation | Skills à combiner |
|-----------|------------------|
| Design complet d'un parcours adaptatif | `adaptive-learning.md` + `instructional-design.md` + `gamification.md` |
| Maximiser la rétention après une session | `adaptive-learning.md` + `memoire.md` |
| Comprendre pourquoi les apprenants oublient | `adaptive-learning.md` + `structure.md` |
| Bâtir un quiz formatif efficace | `adaptive-learning.md` + `feedback.md` |
