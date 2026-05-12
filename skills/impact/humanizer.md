---
name: humanizer
description: "Détecter et corriger les marqueurs IA dans un texte francophone. Synthèse de Wikipedia:Signs of AI Writing, blader/humanizer v2.5.1, stop-slop et recherche FR. Auto-trigger sur : humaniser, non-robot, détection IA, tics IA, texte robot, sonner humain, réécrire IA, prose authentique, marqueurs IA, burstiness, anti-soulless, ouvertures robotiques, participe présent, rythme."
tags: [humanizer, non-robot, écriture, IA, texte, authentique]
version: 1.1.0
origin: Wikipedia-AISIGNS + blader/humanizer + stop-slop + recherche-francophone + anti-slop-fr
---

# Humanizer — Écriture non-robot

> Détecter les marqueurs IA · Réécrire · Calibrer · Scorer

---

## Pourquoi ce skill ?

Un LLM régresse vers la moyenne statistique de son corpus. Le résultat est un texte qui *semble* correct — bonne grammaire, bonne structure — mais qui sonne "fabriqué" : trop propre, trop poli, trop prévisible. Ce skill donne les outils pour identifier ces marqueurs et les supprimer.

**Principe de base** : l'IA infle le sens (tout est crucial, pivotal, transformational), évite les mots rares, répète les mêmes structures, préfère le générique au spécifique. Humaniser = inverser chaque tendance.

---

## DIAGNOSTIC RAPIDE

Avant de réécrire, scanner ces 5 symptômes cardinaux :

| Symptôme | Marqueur |
|----------|----------|
| **Inflation de signifiance** | crucial, pivotal, incontournable, transformationnel, constitue un tournant |
| **Structures formulaïques** | "Non seulement X, mais aussi Y" · "Malgré les défis, Y" · règle de 3 |
| **Générique vs spécifique** | "approche", "méthodologie", "enjeux", "paysage", "écosystème" |
| **Hedging** | "il est important de noter que", "il convient de préciser", "à cet égard" |
| **Format robot** | gras partout · tirets cadratin en série · listes à la place de la prose |

> **Seuil d'alerte** : 3+ symptômes dans un même paragraphe = réécriture obligatoire.

---

## PARTIE 1 — Marqueurs IA universels

### 1.1 Vocabulaire IA (mots à surveiller)

Ces mots n'interdisent pas le texte, mais leur **densité** est un signal. Un ou deux = acceptable. Cinq dans un paragraphe = IA.

**Génération GPT-4 / ChatGPT 2023-2024** (très fréquents)
additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key (adjectif), landscape (abstrait), meticulous/meticulously, pivotal, underscore, tapestry (abstrait), testament, valuable, vibrant

**Génération GPT-4o / 2024-2025**
align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant

**Équivalents français directs**
crucial · vital · pivot(al) · incontournable · intrinsèque · nuancé · paysage (abstrait) · tapisserie · témoignage vivant · souligner · renforcer · mettre en lumière · illustrer · favoriser · cultivar · englober · résonner avec · s'aligner avec · délivrer (au sens de livrer une valeur)

**Jargon corporate / startup (FR)**
optimiser · fluidifier · orchestrer · rationaliser · prioriser · résilience · agilité · transversalité · co-construction · gestion du changement · écosystème · synergie · paradigme · approche holistique · solution à 360° · end-to-end · valeur ajoutée · levier · roadmap · quick win · impact · déployer

---

### 1.2 Structures formulaïques à briser

**Contraste binaire surutilisé**
```
❌ "Ce n'est pas seulement un outil, c'est une révolution."
❌ "Non seulement il réduira les coûts, mais il améliorera aussi la qualité."
✅ Supprimer le premier membre ou reformuler avec une seule affirmation directe.
```

**Section Défis & Perspectives** (pattern quasi-automatique chez les LLM)
```
❌ "Malgré ses atouts indéniables, X fait face à plusieurs défis.
    L'avenir dépendra de sa capacité à s'adapter..."
✅ Supprimer ou transformer en observation factuelle concrète.
```

**Fausse agentivité / annonces**
```
❌ "Cette section explorera les principaux aspects de..."
❌ "Dans ce qui suit, nous verrons que..."
✅ Supprimer et commencer directement par le contenu.
```

**Listes à la place de la prose**
```
❌ Une liste à 7 items pour tout, même des idées qui se suivent naturellement.
✅ Regrouper en prose. Les listes sont pour des éléments réellement parallèles et discrets.
```

**Fragmentation dramatique** (whitespace artificiel)
```
❌ "L'IA change tout.
    Vraiment tout.
    Plus rien ne sera comme avant."
✅ Une phrase complète ou supprimer.
```

**Règle de trois systématique**
```
❌ "Ce projet est ambitieux, structuré et transformateur."
❌ "La formation couvre les fondamentaux, les cas pratiques et les perspectives futures."
✅ Choisir le qualificatif le plus précis, supprimer les autres.
```

**Variation élégante** (synonymes tournants)
```
❌ "L'IA... Le modèle... La technologie... L'algorithme... L'outil..." (= même chose)
✅ Répéter le même mot. La variation forcée est un signe IA.
```

---

### 1.3 Évitement des verbes simples ("est", "sont", "a")

Les LLM préfèrent les verbes marketing aux verbes d'état neutres.

| À éviter | Remplacer par |
|----------|--------------|
| "sert de", "joue le rôle de" | "est" |
| "présente", "offre", "propose" | "a", "comporte" |
| "constitue un exemple de" | "est un exemple de" |
| "témoigne de", "illustre" | "montre" |
| "permet de s'assurer que" | "garantit" / "assure" |

---

### 1.4 Ton promotionnel et inflation de sens

Les LLM traitent tout sujet comme s'il était de grande importance.

**Signes d'inflation** :
- Affirmer qu'un sujet mineur "marque un tournant", "incarne une vision", "reflète des tendances plus larges"
- Relier chaque fait à un contexte plus grand ("dans le paysage actuel de l'IA", "à l'ère du numérique")
- Qualifier des faits ordinaires de "remarquables", "notables", "significatifs"
- Clore avec une note vaguement positive même si le sujet ne le justifie pas

**Correction** : supprimer les couches d'importance. Écrire le fait. Laisser le lecteur juger.

---

### 1.5 Hedging excessif et disclaimers

```
❌ "Il est important de noter que..."
❌ "Il convient de préciser que..."
❌ "On pourrait dire que..."
❌ "Il est à noter que..."
❌ "Dans une certaine mesure..."
❌ "Selon certains experts..."
```

→ Supprimer ou reformuler en affirmation directe. Si l'incertitude est réelle, la nommer précisément ("d'après l'étude X de 2023").

---

### 1.6 Ton sycophante et collaboratif ("chatbot leaks")

```
❌ "Excellente question !"
❌ "Bien sûr, je serais ravi de..."
❌ "J'espère que cela vous aide."
❌ "N'hésitez pas à me dire si vous souhaitez approfondir..."
❌ "Voici une présentation détaillée de..."
```

→ Ces fragments s'infiltrent dans du contenu copié depuis un chatbot. Supprimer systématiquement.

---

### 1.7 Format et mise en forme

| Signe | Explication |
|-------|-------------|
| **Gras partout** | L'IA met en gras plusieurs mots par phrase "pour l'impact". Réserver le gras aux termes techniques et aux points pivots réels. |
| **Tirets cadratin en série** | L'IA abuse du — pour ponctuer. Remplacer par virgule, parenthèse ou point. |
| **Titres en Title Case** | "Les Enjeux De La Transition Numérique" → "Les enjeux de la transition numérique" |
| **Emojis comme bullets** | Signe quasi-certain d'IA. Supprimer. |
| **Listes inline gras + deux-points** | "**Avantage :** texte" répété × 5. Réécrire en prose ou en tableau simple. |
| **Sauts de niveau de titre** | L'IA saute souvent du H1 au H3 sans H2. |

---

## PARTIE 2 — Marqueurs IA spécifiques au français

### 2.0 Ouvertures robotiques

L'IA ouvre systématiquement par des formules spatiales ou temporelles sans valeur informative.

| IA | Humain |
|----|--------|
| "Dans un monde où..." | Commencer par le sujet directement |
| "À l'ère de..." | "Depuis 2023,..." ou "Depuis que X existe" |
| "Dans le paysage [actuel/numérique/concurrentiel] de..." | Nommer le domaine sans métaphore spatiale |
| "Plongeons dans..." | "Voici trois approches testées sur le terrain" |
| "À l'heure de..." | Supprimer, commencer par le fait |
| "Dans l'univers de..." | Supprimer ou reformuler directement |
| "Il est crucial/essentiel de noter que..." | "Attention :" ou directement l'affirmation |

**Règle** : si le texte commence par "Dans", "À l'ère", "À l'heure" → couper le premier segment.

---

### 2.1 Transitions surutilisées en FR

Ces connecteurs logiques apparaissent trop souvent, et souvent en début de paragraphe :

```
En outre · De plus · Par conséquent · Néanmoins · Toutefois
En résumé · Pour conclure · En conclusion · Il convient de souligner
À cet égard · Dans ce contexte · En effet · Ainsi · Dès lors
Dans le cadre de · Au regard de · À titre d'exemple · Notamment
```

**Règle** : si un connecteur commence 3 paragraphes consécutifs, le texte est probablement IA. Varier ou supprimer.

---

### 2.2 Vocabulaire générique impersonnel (FR)

L'IA préfère les mots qui couvrent le plus de cas possibles :

| Mot générique | Signe d'IA si... |
|--------------|-----------------|
| "cela", "ceci", "ce phénomène" | utilisé pour référer à quelque chose qui a un nom précis |
| "cette réalité", "cette dynamique" | en début de phrase, sans référent clair |
| "enjeux" | pluriel flou sans préciser lesquels |
| "problématique" | au lieu de "problème" ou du problème nommé |
| "démarche", "approche" | au lieu de décrire ce qui est fait concrètement |
| "acteurs", "parties prenantes" | sans les nommer |
| "utilisateurs", "collaborateurs" | sans qualifier qui exactement |

---

### 2.3 Clichés marketing et langue de bois (FR)

```
Déverrouiller le potentiel de · Révolutionner la façon dont
Passer au niveau supérieur · Solution qui change la donne
Répondre aux enjeux de · Accompagner la transformation
Porter un regard neuf sur · Repenser les fondamentaux
Placer l'humain au cœur de · Co-construire l'avenir
Créer de la valeur ajoutée · S'inscrire dans une démarche
Aller plus loin ensemble · Faire de X un levier de Y
```

---

### 2.4 Illusion d'exactitude francophone

Le Libération checknews note que les LLM "présentent avec assurance des informations comme vraies même si elles ne le sont pas". En français, se manifeste par :
- Statistiques sans source ("plus de 70% des entreprises...")
- Ordre de grandeur invraisemblable présenté comme fait
- Exemples génériques ("une PME de la région", "un utilisateur lambda")
- Absence totale de fautes de frappe (texte trop propre)

---

### 2.5 Structure textuelle IA (FR)

Le Projet Voltaire signale :
- Articulations logiques "sommaires" : tout est lié par des connecteurs, sans vraie tension
- Absence de mots rares, d'argot, d'humour, de registre familier
- Style plat : ni montées ni descentes de tension
- Introduction → développement → conclusion rigide, même pour des textes courts

---

### 2.6 Participe présent en fin de phrase

Tic syntaxique FR : l'IA finit les phrases par des -ant qui simulent une logique de cause ou de conséquence, sans vraiment l'établir.

```
❌ "ChatGPT aide à rédiger des textes, proposant des formulations adaptées, permettant ainsi de gagner du temps."
✅ "ChatGPT aide à rédiger. Il propose des formulations et réduit le temps passé sur chaque document."
```

**Signal** : 2+ participes présents dans la même phrase → réécrire avec des phrases séparées.

---

### 2.7 Simplifications lexicales (FR)

L'IA préfère les tournures longues et formelles. Remplacer par l'équivalent simple :

| IA | Humain |
|----|--------|
| "Afin de" | "Pour" |
| "Dans le but de" | "Pour" |
| "En raison du fait que" | "Parce que" / "Car" |
| "À ce stade" | "Maintenant" |
| "Il est important de souligner que" | (supprimer) |
| "Il convient de mentionner que" | (supprimer) |
| "À titre d'exemple" | "Par exemple" |
| "Dans le cadre de" | "Pour" / "Lors de" |
| "Au regard de" | "Selon" / "D'après" |
| "Dans cette optique" | (supprimer ou reformuler) |
| "Cela étant dit" | (supprimer) |

---

### 2.8 Métaphores creuses

L'IA abuse des métaphores spatiales et architecturales vidées de sens. Remplacer par le sens littéral ou supprimer.

```
Au cœur de · À la croisée des chemins · Pierre angulaire
Fil rouge · Tisser des liens · Naviguer dans (abstrait)
Feuille de route · Socle solide · Levier de croissance
À la hauteur des enjeux · Faire écho à
```

```
❌ "La formation est au cœur de notre stratégie de transformation."
✅ "La formation est notre priorité n°1 cette année."
```

---

## PARTIE 3 — Règles fondamentales (stop-slop)

Ces 8 règles s'appliquent à tout texte, IA ou non. Un texte qui les viole sonnera "robot" même s'il est humain.

### Règle 1 : Couper les phrases de remplissage
Toute phrase qui n'apporte pas d'information nouvelle ou ne fait que reprendre la précédente est à couper. "Introduction" qui explique ce qu'on va dire → couper. "Récapitulatif" de ce qui vient d'être dit → couper.

### Règle 2 : Voix active
Sujet → verbe → objet. La voix passive dilue la responsabilité et cache l'agent de l'action.
```
❌ "Une décision a été prise par l'équipe..."
✅ "L'équipe a décidé..."
```

### Règle 3 : Être spécifique
Chaque affirmation vague peut être rendue concrète. Si ce n'est pas possible, l'affirmation n'apporte rien.
```
❌ "Les résultats ont été significatifs."
✅ "Le taux de complétion a augmenté de 23% en 6 semaines."
```

### Règle 4 : Faire confiance au lecteur
Ne pas expliquer ce que le lecteur peut déduire. Ne pas résumer ce qu'on vient de dire. Ne pas justifier l'évident.

### Règle 5 : Varier le rythme
Alterner phrases courtes et longues. L'IA produit des phrases quasi-uniformes (20-25 mots). Un texte humain a des phrases de 4 mots et des phrases de 40 mots.

### Règle 6 : Mettre le lecteur dans la scène
Privilegier le concret, l'anecdote, le cas réel. L'IA reste en altitude ; un texte humain descend au sol.

### Règle 7 : Couper les "quotables"
Les phrases trop bien tournées, trop propres, trop symétriques sont souvent générées pour l'effet plutôt que pour l'information. Si la phrase semble faite pour être citée, la supprimer ou la simplifier.

### Règle 8 : Un point de vue, pas une liste de perspectives
L'IA présente "plusieurs points de vue" pour paraître équilibrée. Un humain a un point de vue et l'assume. Choisir une position et l'argumenter.

---

### Rythme et burstiness

**Burstiness** : les détecteurs IA mesurent la variance de longueur de phrases (perplexité + burstiness). L'IA produit des phrases quasi-uniformes (~20 mots). L'humain alterne naturellement entre 5 et 40 mots.

**Variation de structure** — alterner :
- Phrases très courtes (5-10 mots) pour l'impact
- Phrases longues (25-40 mots) pour le développement, avec subordonnées
- Fragment. (Incomplet. Intentionnel.)
- Question rhétorique ?

**Ponctuation expressive** (avec modération) :
- Parenthèses pour les apartés (pas plus de 2 par texte)
- Points de suspension pour la réflexion...
- Tirets pour les interruptions — quand le sens le justifie vraiment
- Points d'exclamation occasionnels (pas plus d'un par page)

**Imperfections contrôlées** — signes d'écriture humaine :
- Commencer une phrase par "Et" ou "Mais"
- Amorces conversationnelles : "Bon,", "Alors,", "En fait,", "Honnêtement,"
- "Ça" au lieu de "cela" (si le registre le permet)
- Omettre le "ne" expletif en contexte oral/informel ("Il sait pas", "J'y crois pas")
- Une digression assumée, une pensée à mi-chemin, une parenthèse qui part un peu loin

---

## PARTIE 3b — Personnalité et voix (Anti-Soulless)

### Signes d'écriture sans âme
- Toutes les phrases ont la même longueur (~20 mots)
- Aucune opinion, uniquement du reporting neutre
- Pas d'incertitude ni de doute ("peut-être", "je ne sais pas trop")
- Aucun "je" même quand c'est approprié
- Aucune digression ou tangente
- Pas de référence concrète à une expérience réelle
- Aucune référence culturelle, aucun humour, aucun registre familier

### Injecter de la voix
- **Avoir des opinions** : "Je ne sais pas trop quoi penser de..." / "Franchement, ça m'agace"
- **Varier le rythme** : une phrase courte. Puis une plus longue qui développe vraiment.
- **Reconnaître la complexité** : "C'est impressionnant — mais aussi un peu inquiétant"
- **Utiliser "je"** quand ça a du sens : "Ce qui me frappe, c'est..."
- **Être spécifique sur les sentiments** : pas "préoccupant" mais "ça donne la chair de poule"
- **Laisser entrer le désordre** : apartés, tangentes, pensées non finies
- **Questions rhétoriques** pour impliquer le lecteur : "Et pourquoi ça marche ? Personne ne sait vraiment."

---

## PARTIE 4 — Process en 2 passes (blader adapté)

### PASSE 1 — Diagnostic

Lire le texte et marquer chaque marqueur avec une catégorie :
- `[VOCAB]` — mot IA détecté
- `[STRUCT]` — structure formulaïque
- `[TONE]` — inflation de sens ou hedging
- `[FORMAT]` — problème de mise en forme

Compter. Si > 10 marqueurs pour 500 mots : réécriture profonde. Si 3-9 : réécriture ciblée. Si < 3 : révision légère.

### PASSE 2 — Réécriture

Pour chaque section marquée :
1. **Identifier l'intention** : qu'est-ce que cette phrase voulait dire, réellement ?
2. **Supprimer** tout ce qui ne sert que l'effet
3. **Concrétiser** : remplacer le générique par le spécifique
4. **Vérifier le rythme** : la phrase d'après est-elle de longueur différente ?
5. **Préserver le sens** : ne pas perdre l'information dans la réécriture

---

### TEST ORAL

Avant la passe finale, lire le texte réécrit à voix haute. Poser ces 3 questions :

1. **"Est-ce que je dirais ça à quelqu'un en face ?"** — si non, reformuler
2. **"Où est-ce que je bute ou je souffle ?"** — ces points indiquent une phrase trop longue ou mal rythmée
3. **"Quelle phrase me semble fausse ou trop lisse ?"** — c'est celle qui contient encore un tic IA

Si le texte sonne comme une présentation de start-up ou un copier-coller de plaquette commerciale → recommencer PASSE 2.

---

### PASSE FINALE — "Qu'est-ce qui sonne encore IA ?"

Relire le texte réécrit. Répondre en bullets :
- "La conclusion est encore trop lisse → supprimer la dernière phrase"
- "Le paragraphe 3 reste trop abstrait → ajouter un exemple"
- "Le tiret cadratin du 2e paragraphe est encore là → remplacer par virgule"

Puis réécrire les points identifiés.

---

## PARTIE 5 — Scoring

Évaluer le texte sur 5 dimensions, /10 chacune :

| Dimension | Description | /10 |
|-----------|-------------|-----|
| **Directness** | Chaque phrase porte son poids. Pas de remplissage. | |
| **Rythme** | Variation de longueur de phrases. Pas d'uniformité. | |
| **Confiance** | Ne pas expliquer l'évident. Faire confiance au lecteur. | |
| **Authenticité** | Ton propre, point de vue assumé. Pas de voix générique. | |
| **Densité** | Ratio idées/mots élevé. Pas de redondance. | |

**Interprétation** :
- 40-50 : texte humain assumé
- 30-39 : réécriture ciblée recommandée
- 20-29 : réécriture profonde nécessaire
- < 20 : réécriture complète

---

## PARTIE 6 — Exemples avant/après (FR)

### Exemple 1 : Email professionnel

```
AVANT (IA):
"Dans le cadre de notre démarche d'amélioration continue, il est important de noter
que notre équipe a mis en place plusieurs initiatives visant à optimiser nos processus.
Ces efforts témoignent de notre engagement envers l'excellence opérationnelle et
notre volonté de relever les défis de demain."

APRÈS (humain):
"On a revu nos processus de validation ce trimestre. Résultat : les délais de
traitement ont baissé d'une semaine. Si ça vous intéresse, je peux vous montrer
le détail jeudi."
```

### Exemple 2 : Documentation technique

```
AVANT (IA):
"Cette solution innovante permet d'orchestrer efficacement les différents flux de
données tout en garantissant une expérience utilisateur optimale. Elle s'inscrit
dans un écosystème robuste et évolutif, répondant aux enjeux contemporains de la
transformation numérique."

APRÈS (humain):
"Le pipeline collecte les données Snowflake toutes les 6h, les enrichit via
Cortex AI et les expose dans une API REST. La latence est < 200ms pour 95% des
requêtes."
```

### Exemple 3 : Présentation pédagogique

```
AVANT (IA):
"Au terme de cette formation enrichissante, les participants auront acquis les
compétences nécessaires pour naviguer dans un paysage technologique en constante
évolution. Ces apprentissages constitueront un socle solide pour relever les défis
de l'intelligence artificielle."

APRÈS (humain):
"Après cette session, vous saurez écrire un prompt qui donne des résultats
cohérents, et repérer quand l'IA hallucine. Ce sont les deux compétences les plus
utiles pour l'instant."
```

### Exemple 4 : Titre / accroche

```
AVANT (IA):
"Déverrouiller le plein potentiel de votre équipe grâce à l'intelligence artificielle"

APRÈS (humain):
"Comment notre équipe a réduit de moitié le temps de rédaction des comptes rendus"
```

---

### Exemple 5 : texte marketing (avec audit intégré)

**❌ AVANT (IA brut)**

> Dans le paysage numérique actuel, les entreprises font face à des défis sans précédent. Notre solution innovante permet de naviguer dans cet environnement complexe avec agilité et efficacité. Il est important de noter que nos clients bénéficient d'un accompagnement personnalisé, leur permettant d'optimiser leurs processus tout en maximisant leur retour sur investissement.

**🔍 AUDIT des marqueurs**
- `Dans le paysage numérique actuel` → ouverture robotique (§ 2.0)
- `défis sans précédent` → cliché de crédit (§ 1.4)
- `naviguer dans cet environnement complexe` → métaphore creuse (§ 2.8)
- `agilité et efficacité` → doublet vide (§ 2.3)
- `Il est important de noter que` → simplification à supprimer (§ 2.7)
- `leur permettant d'optimiser... tout en maximisant` → 2 participes présents empilés (§ 2.6)
- 3 phrases, longueur quasi-identique (≈ 22 mots) → 0 burstiness (§ 3.rythme)

**✅ APRÈS (humain)**

> Les entreprises reçoivent chaque jour plus de données qu'elles ne peuvent en traiter. C'est là qu'on intervient.
>
> On ne vend pas une plateforme. On vend du temps gagné : moins de tableaux, moins de réunions, moins d'angles morts. Nos clients réduisent en moyenne 30 % du temps passé sur le reporting — dès le premier mois.

**Changements appliqués** : ouverture concrète (chiffre) • structure courte/longue alternée • "on" à la place du définitif • chiffre réel à la place de "maximiser le ROI" • tiret cadratin pour le rythme • digression courte assumée ("C'est là qu'on intervient")

---

## PARTIE 7 — Calibration de voix (optionnel)

Quand on réécrit pour quelqu'un, ne pas effacer sa voix. Collecter 3 textes écrits par la personne (emails, posts, comptes rendus) et identifier :

1. **Longueur de phrase préférée** — courtes ou longues ?
2. **Niveau de registre** — formel, semi-formel, familier ?
3. **Tics positifs** — expressions récurrentes qui sonnent authentiques
4. **Ponctuation préférée** — tirets, parenthèses, deux-points ?
5. **Rapport à l'humour** — présent, absent, ironique ?

Ensuite réécrire en **préservant et amplifiant** ces traits, tout en supprimant les marqueurs IA.

---

## USAGE

### Demande simple
> "Humanise ce texte" → appliquer le process 2 passes + scoring

### Demande avec calibration
> "Humanise ce texte dans le style de ces exemples" → calibration voix → process 2 passes

### Audit uniquement
> "Identifie les marqueurs IA dans ce texte" → PASSE 1 seulement, liste annotée

### Réécriture d'un type de contenu spécifique
| Type | Focus prioritaire |
|------|------------------|
| Email professionnel | Supprimer hedging + ton sycophante + jargon corporate |
| Documentation tech | Supprimer inflation de sens + être spécifique + voix active |
| Slide / présentation | Supprimer règle de 3 + annonces + gras excessif |
| Post LinkedIn | Supprimer clichés marketing + fragmentation dramatique + emojis-bullets |
| Compte rendu | Supprimer transitions formulaïques + générique → spécifique |
| Fiche pédagogique | Supprimer ton sycophante + hedging + faire confiance au lecteur |

---

## SOURCES

- Wikipedia:Signs of AI Writing (2025) — taxonomie complète des marqueurs
- blader/humanizer v2.5.1 — 29 patterns + process 2 passes
- stop-slop (hardikpandya) — 8 règles + scoring 5 dimensions
- GPTHuman.ai — liste mots IA en français
- Projet Voltaire — indices FR (mots impersonnels, articulations logiques, mots rares)
- Libération CheckNews (jan. 2023) — illusion d'exactitude, homogénéité structurelle
- Stylométrie et burstiness — métriques de détection IA (variance de longueur)
- Blog du Modérateur, Redacteur.com — tics ChatGPT en français (participe présent, ouvertures)
- anti-slop-fr — simplifications lexicales FR, métaphores creuses, voix authentique
