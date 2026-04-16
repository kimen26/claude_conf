---
name: impact-quiz-design
description: Concevoir des quiz QCM formatifs efficaces. Distracteurs clairement faux, exploitation des biais/peurs via Hypercorrection Effect, 1 reponse fun obligatoire, coverage par section, niveaux Bloom. Active sur quiz, QCM, distracteur, question formation, evaluer, tester connaissances.
family: impact
origin: Formations-Infopro + retour terrain avril 2026
version: 1.0.0
---

# Impact -- Quiz Design & Distracteurs Efficaces

## Quand activer ce skill

- Creer ou reviser des quiz QCM pour une formation
- Analyser pourquoi un quiz est ambigu ou frustrant
- Verifier la couverture (coverage) des quiz par rapport au contenu
- Concevoir des distracteurs qui enseignent au lieu de pieger

---

# QD. Principes de Quiz Formatif

> Un quiz formatif n'est pas une evaluation -- c'est une **activite d'apprentissage** (Testing Effect, AL.4).
> Chaque question doit renforcer un concept cle, pas mesurer une performance.

## QD.1 Le Quiz comme Outil d'Apprentissage (pas d'evaluation)

**Source** : Henry Roediger III & Jeffrey D. Karpicke, *Test-Enhanced Learning* (2006)

**Principe** : Essayer de se rappeler une information consolide la memoire **bien plus** que relire le contenu.

| Methode | Retention a 1 semaine |
|---------|----------------------|
| Etudier 4 fois | ~40% |
| Etudier 1 fois + 3 tests | **~67%** |

**Implication** : Le quiz n'est pas la pour "noter" -- il est la pour **ancrer**. L'apprenant qui se trompe et se fait corriger retient mieux que celui qui n'a jamais ete teste.

---

## QD.2 L'Hypercorrection Effect -- Debunking Actif par les Distracteurs

**Source** : Andrew Butler, Lisa Fazio & Elizabeth Marsh, *The Hypercorrection Effect Is Robust* (2011, Memory & Cognition) ; Butterfield & Metcalfe (2001)

**Citation** : *"High-confidence errors are more likely to be corrected than low-confidence errors."*

**Principe** : Quand un apprenant croit fortement a une fausse croyance et decouvre qu'il a tort, il retient la bonne reponse **mieux** que s'il n'avait jamais eu le biais. La surprise emotionnelle de l'erreur cree un ancrage memoriel fort.

**Application au quiz** :
- Mettre les **biais courants, peurs et idees recues** sur l'IA dans les distracteurs
- L'apprenant qui choisit un distracteur-biais se fait corriger -> il retient
- L'apprenant qui hesite entre le biais et la bonne reponse -> il reflechit activement
- Meme l'apprenant qui repond juste voit les biais listes -> il est vaccine

**Exemples de biais/peurs exploitables en formation IA** :

| Biais / Peur | Distracteur possible |
|-------------|---------------------|
| "L'IA sait qu'elle ne sait pas" | "Le modele refuse de repondre quand il detecte un manque d'info" |
| "L'IA apprend de moi en temps reel" | "Le modele memorise vos conversations pour s'ameliorer" |
| "Plus c'est cher, mieux c'est" | "L'agent est plus capable car il utilise un modele plus intelligent" |
| "Le MCP c'est magique" | "Le MCP donne 10x plus de fonctionnalites que l'API" |
| "L'IA a une intention" | "Le modele change volontairement de style pour ne pas se repeter" |
| "L'IA comprend comme un humain" | "Le modele analyse le sens profond de votre question avant de chercher" |
| "Nouveau = forcement mieux" | "Les modeles recents ne font plus jamais d'hallucinations" |
| "Open source = gratuit et sans risque" | "Les modeles open source n'ont aucun cout car ils sont gratuits" |
| "L'IA remplace les devs" | "L'agent n'a pas besoin de configuration technique, il s'adapte tout seul" |

---

## QD.3 Anatomie d'une Question QCM Efficace

### Structure obligatoire (4 choix)

| Slot | Role | Critere |
|------|------|---------|
| **Bonne reponse** | Le concept cle a ancrer | Claire, sans ambiguite, correspond au contenu enseigne |
| **Distracteur 1** | Biais/peur/idee recue | Exploite l'Hypercorrection Effect (QD.2) |
| **Distracteur 2** | Mauvais mecanisme | Utilise le bon vocabulaire mais decrit un fonctionnement faux |
| **Reponse fun** | Absurde mais memorable | Humour, clin d'oeil, reference pop culture |

### Regles des distracteurs

**Un bon distracteur est :**
- Clairement **faux** quand on connait le contenu (pas une demi-verite)
- Formulairement **credible** en surface (meme structure grammaticale, meme longueur)
- Pedagogiquement **utile** (il enseigne ce que ce n'est PAS)

**Un mauvais distracteur est :**
- Une **demi-verite** ou un fait partiellement correct (frustre au lieu d'enseigner)
- **Trop evidemment faux** (n'oblige pas a reflechir)
- Un fait **vrai dans un autre contexte** (cree de la confusion sans resoudre)

### Patterns de distracteurs efficaces

| Pattern | Description | Exemple |
|---------|-------------|---------|
| **Inverse du mecanisme** | Decrit l'exact oppose du fonctionnement reel | "Le modele garde un historique" (alors qu'il est stateless) |
| **Faux prerequis** | Invente une condition qui n'existe pas | "Les linguistes devaient d'abord cataloguer toutes les langues" |
| **Faux plafond/plancher** | "Maximum" au lieu de "minimum", ou l'inverse | "Deux fois maximum" au lieu de "deux fois minimum" |
| **Confusion de niveau** | Melange deux concepts proches | "L'agent utilise un modele plus intelligent" (meme LLM) |
| **Biais de magie** | Attribue des pouvoirs surnaturels a la techno | "Le MCP donne 10x plus de fonctionnalites" |
| **Anachronisme** | Date ou fait historique faux | "Le texte informatique n'existe que depuis 2005" |
| **Faux acronyme** | Invente une expansion d'acronyme | "MCP = Master Certified Protocol" |

---

## QD.4 La Reponse Fun -- Obligatoire, pas Optionnelle

**Source** : Zeigarnik Effect + emotion = ancrage (memoire.md A.4)

**Principe** : L'humour cree une **emotion positive** qui :
1. Relache la tension du quiz (securite psychologique)
2. Cree un ancrage emotionnel sur la question (Peak-End Rule)
3. Rend le quiz partageable ("t'as vu la reponse D ?")

**Regles** :
- 1 reponse fun par question, toujours en position D (convention)
- Doit etre clairement absurde (pas de risque de confusion)
- Peut contenir une reference culturelle, un jeu de mots, une anthropomorphisation
- Ne doit jamais etre meprisant envers l'apprenant

**Exemples reussis** :
- "Personne n'avait pense a brancher le WiFi"
- "Le modele s'ennuie et improvise pour se distraire"
- "42 fois -- c'est la reponse a tout dans l'univers (Douglas Adams approuve)"
- "C'est vendredi, l'agent fait greve"

---

## QD.5 Coverage -- Verifier la Couverture

**Principe** : Chaque section significative du contenu doit etre testee par au moins 1 question. Les sections sans quiz sont des "angles morts" de retention.

**Methode** :
1. Lister toutes les sections (## level) du contenu principal
2. Mapper chaque question quiz a sa section (via `<!-- #sXX -->`)
3. Identifier les sections non couvertes
4. Prioriser : sections avec concepts cles > sections descriptives

**Criteres de couverture** :
- Sections **obligatoirement couvertes** : celles qui introduisent un concept nouveau ou une distinction cle
- Sections **optionnellement couvertes** : intro/accroche, bilan/takeaway, listes descriptives
- **2 questions par section** = densite ideale pour une formation courte (Testing Effect x2)

---

## QD.6 Niveaux de Bloom dans les Quiz

**Source** : Benjamin Bloom, *Taxonomy of Educational Objectives* (1956, revision Anderson & Krathwohl 2001)

| Niveau Bloom | Type de question | Exemple |
|-------------|-----------------|---------|
| 1. Se souvenir | "Quel est le nom de..." | Factuel, rappel direct |
| 2. Comprendre | "Quelle est la difference entre..." | Distinction, reformulation |
| 3. Appliquer | "Pour repondre a X, quel outil..." | Mise en situation |
| 4. Analyser | "Qu'est-ce qui s'est probablement passe..." | Diagnostic, raisonnement |

**Recommandation** :
- Formation decouverte (F1) : majorite niveaux 1-2, quelques niveaux 3-4
- Formation pratique (F3, F4) : majorite niveaux 3-4
- Eviter le niveau 1 pur (rappel factuel) sauf pour les definitions cles

---

## QD.7 Checklist de Revue Quiz

Avant de valider un quiz, verifier :

- [ ] **Bonne reponse** : claire, sans ambiguite, fidele au contenu enseigne
- [ ] **Distracteur 1** : exploite un biais ou une peur courante (Hypercorrection)
- [ ] **Distracteur 2** : mauvais mecanisme, clairement faux, pas une demi-verite
- [ ] **Reponse fun** : en position D, clairement absurde, cree un sourire
- [ ] **Aucun distracteur n'est partiellement vrai** (test : "est-ce que quelqu'un de competent pourrait argumenter que c'est juste ?")
- [ ] **Niveau Bloom** identifie (1-4)
- [ ] **Section cible** identifiee (tag `<!-- #sXX -->`)

---

## Combinaisons recommandees

| Situation | Skills a combiner |
|-----------|------------------|
| Creer des quiz pour une formation | `quiz-design.md` + `adaptive-learning.md` + `structure.md` |
| Identifier les biais a exploiter | `quiz-design.md` + `biais.md` + `emotion.md` |
| Calibrer la difficulte | `quiz-design.md` + `structure.md` (Flow, ZPD) |
| Rendre le quiz memorable | `quiz-design.md` + `memoire.md` (SUCCESs, Peak-End) |
| Gamifier le quiz | `quiz-design.md` + `gamification.md` (Variable Reward, Progress Principle) |
