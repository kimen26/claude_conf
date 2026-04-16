---
name: impact-gamification
description: Concevoir des expériences d'apprentissage engageantes par les mécaniques de jeu. Octalysis, BJ Fogg, Self-Determination Theory, boucles de progression, Variable Reward. Active sur gamification, engagement, motivation, badges, points, progression, rétention.
family: impact
origin: Formations-Infopro
version: 1.0.0
---

# Impact — Gamification & Engagement

## Quand activer ce skill

- Concevoir un parcours de formation qui doit motiver sur la durée
- Augmenter la complétion d'un module e-learning ou d'une app
- Récompenser des comportements d'apprentissage sans créer de dépendance extrinsèque
- Analyser pourquoi un système de badges/points ne fonctionne pas
- Relier au projet "Duolingo de l'IA" (VISION_ADAPTIVE_LEARNING.md)

---

# GA. Motivation & Core Drives

> La gamification mal appliquée = PBL (Points, Badges, Leaderboards) sans sens = pression sans plaisir.
> La bonne gamification touche les core drives intrinsèques.

## GA.1 Octalysis Framework (8 Core Drives)

**Source** : Yu-kai Chou, *Actionable Gamification* (2015) — framework validé sur Foursquare, Twitter, StackOverflow

**Citation** : *"Games are fun not because they ARE games, but because they have good game design. And good game design is always about motivation."*

**Principe** : 8 motivations fondamentales qui poussent les gens à agir. Chaque mécanique de jeu active un ou plusieurs drives.

| # | Core Drive | Exemples mécaniques | Quadrant |
|---|-----------|-------------------|----------|
| 1 | **Epic Meaning & Calling** | Mission narrative, lore, "tu fais partie de quelque chose" | Blanc (intrinsèque) |
| 2 | **Development & Accomplishment** | Points, badges, niveaux, progression visible | Blanc (extrinsèque) |
| 3 | **Empowerment of Creativity** | Builder libre, personnalisation, combos | Blanc (intrinsèque) |
| 4 | **Ownership & Possession** | Inventaire, collection, customisation d'avatar | Noir (extrinsèque) |
| 5 | **Social Influence & Relatedness** | Leaderboard, guildes, gifting, équipes | Blanc (intrinsèque) |
| 6 | **Scarcity & Impatience** | Timer, slots limités, "disponible demain" | Noir (extrinsèque) |
| 7 | **Unpredictability & Curiosity** | Boîte mystère, quête cachée, easter egg | Noir (intrinsèque) |
| 8 | **Loss & Avoidance** | Streak à ne pas perdre, vies, countdown | Noir (extrinsèque) |

**Quadrants** :
- **Blanc (Right Brain)** = motivation créative, sociale, intrinsèque → engagement durable
- **Noir (Left Brain)** = motivation orientée résultat ou peur → engagement court terme, peut créer de l'anxiété

**Application** :
- Un parcours formation doit activer au moins **3 drives Blancs**
- Duolingo active 1 (tu apprends une langue = mission), 2 (streak, XP), 5 (leagues), 6 (streak freeze — scarcité), 8 (perdre son streak)
- Ne jamais baser un système uniquement sur le Drive 8 → burnout et abandon

---

## GA.2 BJ Fogg Behavior Model (B=MAP)

**Source** : BJ Fogg, *Tiny Habits* (2019) ; Stanford Persuasive Technology Lab

**Citation** : *"If someone is not doing what you want them to do, either they lack motivation, ability, or a prompt. Those are the only three reasons."*

**Principe** : Un comportement se produit quand Motivation + Ability + Prompt convergent au même moment.

```
B = MAP
Behavior = Motivation × Ability × Prompt

             Motivation
                 ↑
                 |        ★ Action Zone
                 |      /
                 |    /
    ────────────|──/──────── Ligne d'action
                | /
                |/
                ──────────→ Ability (Facilité)
                                    Prompt
```

**Les 3 leviers** :

| Levier | Réduire la friction signifie... | En formation |
|--------|--------------------------------|--------------|
| **Motivation** | Relier au "Pourquoi moi" personnel | Ennéagramme, HOOK session |
| **Ability** | Rendre le premier pas trivial | Microlearning, "5 min" |
| **Prompt** | Déclencher au bon moment | Push notif, email J+3 |

**Règle d'or Fogg** : "If you want to change behavior, make it easier first, not more motivating." → La friction tue même la bonne motivation.

**Application** :
- Avant d'augmenter la motivation → chercher où est la friction (ability)
- Un module "à faire en 5 min" est un prompt en soi
- Le streak Duolingo = Prompt (notification) + Ability (1 leçon = 3 min)

---

## GA.3 Self-Determination Theory (SDT) — Intrinsèque vs Extrinsèque

**Source** : Edward Deci & Richard Ryan, *Self-Determination Theory* (1985, 2000)

**Citation** : *"The question is not whether to use rewards, but how to use them without undermining intrinsic motivation."*

**Principe** : La motivation durable repose sur 3 besoins psychologiques fondamentaux :

| Besoin | Définition | Brisé par... |
|--------|-----------|--------------|
| **Autonomie** | Sentiment de choisir | Obligation, surveillance excessive |
| **Compétence** | Sentiment de progresser | Trop facile ou trop difficile |
| **Relation** | Sentiment d'appartenir | Apprentissage isolé, pas de pairs |

**Échelle de motivation** (du moins au plus autonome) :

```
Extrinsèque ←─────────────────────────────→ Intrinsèque
Contrainte    Récompense   Identification   Intégration   Plaisir pur
(punition)    (badge/XP)   (≪j'y vois l'utilité≫)       (curiosité)
```

**Règle de Deci & Ryan** : Les récompenses tangibles (argent, badges) **diminuent** la motivation intrinsèque sur les tâches déjà intéressantes. Les récompenses informationnelles (feedback, score) l'**augmentent**.

**Application** :
- Badge ≠ récompense si mal utilisé → transformer en **feedback** ("Tu maîtrises les prompts de base")
- Proposer des chemins au choix dans le parcours (autonomie)
- Groupes de pairs, forums, défi en équipe → besoin de relation

---

## GA.4 Variable Reward (Récompense Variable)

**Source** : B.F. Skinner, Operant Conditioning (1938) ; Nir Eyal, *Hooked* (2014)

**Citation** : *"Variable schedules of reinforcement produce the highest rate of behavior and are most resistant to extinction."* — Skinner

**Principe** : Une récompense incertaine est plus addictive qu'une récompense certaine. Le cerveau libère plus de dopamine *en anticipant* une récompense variable qu'en la recevant.

**Les 3 types (Eyal)** :

| Type | Exemple jeu / formation |
|------|------------------------|
| **Variable of the Tribe** | Likes sociaux, réactions des pairs, classement changeant |
| **Variable of the Hunt** | Boîte mystère, question aléatoire, défi surprise |
| **Variable of the Self** | Succès inattendus, découverte de sa propre progression |

**Application** :
- "Défi du jour" tiré aléatoirement > "Exercice 3 de la semaine 2"
- Révéler un badge de façon surprenante (pas annoncé à l'avance)
- ⚠️ À doser : trop de variable reward = dark pattern (casino). Éthique : la surprise doit rester bénéfique.

---

## GA.5 Bartle Player Types

**Source** : Richard Bartle, *Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs* (1996)

**Principe** : 4 types de joueurs avec des motivations différentes. Chaque type est alienated par les mécaniques des autres.

| Type | Motivation | Mécanique idéale | % typique |
|------|-----------|-----------------|-----------|
| **Achiever** | Progresser, collecter, finir | XP, niveaux, 100% completion | ~40% |
| **Explorer** | Découvrir, comprendre le système | Contenu caché, easter eggs, lore | ~10% |
| **Socialiser** | Connexions avec les autres | Guildes, chat, collaboration | ~40% |
| **Killer** | Compétition, dominer | Leaderboard, PvP, classement | ~10% |

**Application** :
- Un parcours formation doit satisfaire Achiever (progression visible) et Socialiser (pairs) en priorité
- Explorer = bonus content, articles avancés, "pour aller plus loin"
- Attention Killer : le leaderboard public peut démotiver 90% des apprenants non-compétitifs

---

## GA.6 Progress Principle

**Source** : Teresa Amabile & Steven Kramer, *The Progress Principle* (2011), Harvard Business Review

**Citation** : *"Of all the things that can boost emotions, motivation, and perceptions during a workday, the single most important is making progress in meaningful work."*

**Principe** : Le simple fait de progresser — même un petit pas — est le moteur motivationnel le plus puissant en contexte de travail/apprentissage.

**Application** :
- Rendre la progression visible immédiatement et constamment (barre de progression, "tu en es à 3/7")
- Découper en micro-victoires : mieux vaut 10 étapes visibles que 3 grandes invisibles
- Célébrer les micro-progrès verbalement en formation ("vous venez de faire quelque chose que 90% des gens ne savent pas faire")

---

## GA.7 PBL et ses limites (Points, Badges, Leaderboards)

**Source** : Juho Hamari, Jonna Koivisto et Harri Sarsa, *Does Gamification Work?* (2014, revue de 24 études)

**Citation** : *"Gamification does not always improve user experience or engagement. Effects are highly context-dependent."*

**Principe** : PBL (Points/Badges/Leaderboards) est la gamification la plus répandue et souvent la moins efficace seule.

**Résultats de la méta-analyse** :
- Points → augmentent la quantité de contenu produit mais **pas la qualité**
- Leaderboards → motivent les **top 10%**, démotivent les **90% restants**
- Badges → efficaces uniquement si **informationnels** (feedback de compétence) pas seulement décoratifs

**Application** :
- Ne pas implémenter PBL seul → y ajouter des Core Drives intrinsèques (Octalysis CD1, CD3, CD5)
- Leaderboard → privilégier relatif (vs ses propres scores) ou par équipe vs public global
- Badge utile : "Maîtrise du prompt zéro-shot" (compétence spécifique) vs "Actif pendant 7 jours" (temps = peu de valeur)

---

## Combinaisons recommandées

| Situation | Skills à combiner |
|-----------|------------------|
| Design d'un parcours gamifié | `gamification.md` + `adaptive-learning.md` + `structure.md` |
| Augmenter la complétion e-learning | `gamification.md` + `biais.md` (aversion perte, IKEA effect) |
| Motiver sans créer de dépendance | `gamification.md` + `emotion.md` (sécurité psychologique) |
| Récompenses verbales en présentiel | `gamification.md` + `corps-voix.md` + `action.md` |
