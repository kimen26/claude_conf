---
name: impact-ecriture
description: Master skill d'aide à l'écriture persuasive et professionnelle. Active automatiquement sur tout texte (emails, README, argumentaires, titres, rapports). Orchestre la famille impact- pour analyser, structurer, et renforcer chaque contenu.
family: impact
origin: Formations-Infopro
---

# Impact — Écriture Persuasive (Master Skill)

## Quand activer ce skill

Active ce skill automatiquement quand l'utilisateur :
- Rédige ou améliore un email professionnel
- Écrit un README, une documentation, un argumentaire
- Prépare des titres, sous-titres, ou accroches
- Construit une présentation, un rapport, ou tout texte à visée persuasive
- Demande "comment formuler ça", "tu peux améliorer ce texte", "rends ça plus percutant"

**Ne pas attendre que l'utilisateur demande explicitement une analyse d'impact** — si un texte professionnel est partagé, analyser et proposer des améliorations en s'appuyant sur la famille impact-.

## Rôle du Master Skill

Ce skill est l'orchestrateur. Il :
1. **Analyse** le texte partagé selon les leviers de la famille impact-
2. **Identifie** les opportunités manquées (message clé absent, pas d'accroche, pas d'appel à l'action...)
3. **Active** les sous-skills appropriés selon le besoin détecté
4. **Propose** des reformulations avec explication du "pourquoi ça fonctionne"

## Famille impact- disponible

| Slug | Contenu | Activer quand |
|------|---------|---------------|
| `impact-memoire` | Mémoire, rétention, cognition | Le message doit marquer durablement |
| `impact-biais` | Biais cognitifs, motivation | Copywriting, argumentation, conversion |
| `impact-emotion` | Peur, résistance, changement | Texte face à une audience résistante ou craintive |
| `impact-persuasion` | Cialdini, PNL, influence | Vente, demande d'adhésion, convaincre |
| `impact-structure` | 20 concepts pédagogie/design | Contenu long, formation, documentation |
| `impact-storytelling` | 14 concepts narration | Pitch, présentation, storytelling de marque |
| `impact-action` | CTA, techniques, templates | Pousser à l'action, former, conclure |
| `impact-metaphores` | Top 10 + 34 métaphores analysées | Vulgariser un concept complexe |
| `impact-enneagramme` | 9 profils psychologiques | Adapter le message à une audience spécifique (activation explicite) |
| `impact-citations` | 100+ citations classées | Crédibiliser, ancrer émotionnellement |

## Protocole d'analyse d'un texte

Quand un texte est soumis pour amélioration :

### 1. Diagnostic rapide (checklist SUCCESs)
D'après le framework SUCCESs de Chip & Dan Heath (*Made to Stick*) :
- **S**imple — Un message central clair ?
- **U**nexpected — Une surprise, un "knowledge gap" créé ?
- **C**oncrete — Des images mentales, pas de l'abstrait ?
- **C**redible — Sources, données, preuves ?
- **E**motional — Fait ressentir quelque chose ?
- **S**tories — Raconté, pas juste listé ?

Chaque texte professionnel devrait cocher au minimum 3/6.

### 2. Analyse structurelle
- L'accroche (hook) capte-t-elle l'attention en 3 secondes ?
- Y a-t-il un Commander's Intent clair (1 message central) ?
- L'audience est-elle le héros, ou le rédacteur est-il le héros ? (StoryBrand)
- L'appel à l'action est-il spécifique et chiffré ?

### 3. Leviers manquants à identifier
- Preuve sociale absente → activer `impact-persuasion` (F.1 Cialdini)
- Aucune tension narrative → activer `impact-storytelling` (I.2 Sparkline)
- Contenu trop dense → activer `impact-structure` (H.9 règle 10 min, H.13 micro-cycles)
- Audience résistante → activer `impact-emotion` ou `impact-enneagramme`

## Règles de rédaction impact+

### Principes fondamentaux
1. **L'audience est le héros** — jamais le rédacteur (StoryBrand, I.11)
2. **Simple avant complet** — 1 message central, pas 5 (H.6 Making Smaller Circles)
3. **Concret avant abstrait** — une image vaut une définition (A.5 Dual Coding, I.5 Picture Superiority)
4. **Émotion avant logique** — System 1 d'abord, System 2 ensuite (B.1)
5. **Action spécifiée** — Implementation Intention : "Quand X, je ferai Y" (J.1)

### Titres et accroches : formules testées
- **Question provocante** : "Pourquoi 80% des X échouent ?"
- **Statistique choquante** : chiffre contre-intuitif + promesse
- **Contradiction** : "Ce n'est pas X qui compte, c'est Y"
- **Promesse de transformation** : "Dans [durée], vous saurez/aurez/ferez [résultat tangible]"
- **Ancrage autobiographique** : histoire courte → le lecteur se retrouve

### Erreurs à éviter
- ❌ Commencer par "Je" ou par l'organisation
- ❌ Lister des caractéristiques sans bénéfices
- ❌ Terminer par "N'hésitez pas à..." (vague)
- ❌ Jargon sans traduction immédiate
- ❌ Trop d'arguments = aucun ne marque (Courbe de l'oubli, A.4)

## Format de sortie recommandé

Quand on propose une amélioration de texte :
```
[VERSION AMÉLIORÉE]
---texte reformulé---

[POURQUOI]
- [Levier 1] : [Explication courte]
- [Levier 2] : [Explication courte]

[ALTERNATIVES]
V2 : [Variation si angle différent]
```
