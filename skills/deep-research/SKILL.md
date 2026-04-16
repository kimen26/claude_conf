---
name: deep-research
description: "Méthodologie de recherche profonde et plurielle pour apprendre un nouveau sujet : sources académiques, philosophiques, praticiens, voix non-conventionnelles. Multi-culturelle (USA, France, Europe, Asie). Protocole de synthèse et critères de qualité épistémologique."
family: methodology
origin: Formations-Infopro
version: "2.0"
---

# Deep Research — Apprendre un Sujet en Profondeur

> "The test of a first-rate intelligence is the ability to hold two opposed ideas in mind at the same time and still retain the ability to function." — F. Scott Fitzgerald

> "Celui qui ne connaît qu'une seule chose ne connaît rien." — Khalil Gibran

---

## ⚡ Principe fondateur : Pluralisme épistémologique

Une vérité robuste résiste à plusieurs types d'éclairage. Avant de conclure, consulter **au moins 4 types de sources différents** sur un même sujet. La convergence entre sources hétérogènes est un signal fort. La divergence est une invitation à creuser.

**Règle d'or** : Si toutes vos sources disent la même chose de la même façon, vous êtes probablement dans une chambre d'écho.

---

## ⚠️ AVANT DE COMMENCER — Phase 0 : Cadrage

**Ne jamais foncer sans avoir répondu à ces 5 questions.** Si les réponses ne sont pas claires, les poser à l'utilisateur.

```
Questions de cadrage obligatoires :

1. PÉRIMÈTRE
   "Sur quel sujet exactement ? Y a-t-il un angle particulier
    (pratique / théorique / historique / comparatif) ?"

2. PROFONDEUR SOUHAITÉE
   "Quel niveau de profondeur ? Comprendre les bases / Maîtriser /
    Créer un contenu / Prendre une décision ?"

3. USAGE FINAL
   "Pour quoi faire ? Formation / Article / Prise de décision /
    Curiosité personnelle ? Le livrable attendu ?"

4. CONTRAINTES
   "Y a-t-il une deadline ? Des sources à exclure ?
    Des angles déjà explorés à ne pas répéter ?"

5. CONNAISSANCES ACTUELLES
   "Qu'est-ce qui est déjà connu sur le sujet ? Ce qu'on cherche
    à AJOUTER ou CONFIRMER, pas reformuler ce qu'on sait."
```

**Règle** : Une recherche sans cadrage produit des notes volumineuses et inutiles. 10 minutes de cadrage économisent 3 heures de bruit.

---

## 📁 Système de Fichiers de Travail

### Structure à créer au début de chaque recherche

```
research/[sujet]/
├── 00-cadrage.md          ← Questions de la Phase 0 + réponses
├── 01-plan.md             ← Plan initial + axes priorisés
├── 02-brut.md             ← Capture RAW au fil de la recherche
├── 03-sources.md          ← Sources avec métadonnées + validation
├── 04-insights.md         ← Insights distillés, quotes retenues
└── 05-synthese.md         ← Livrable final structuré
```

### Règle de capture

- **02-brut.md** : TOUT noter sans filtrer en temps réel (paraphrase + lien + quote exacte si mémorable)
- **Ne jamais modifier le brut**. Le filtrage vient après, dans 04-insights.
- **Une source = une ligne dans 03-sources.md** — pas de source non listée
- Si la recherche dure > 1 session : le fichier 02-brut.md permet de reprendre sans perte

### Template 03-sources.md

```markdown
| Source | Auteur | Date | Type | Lien/Ref | Validé | Fiabilité (1-5) | Note |
|--------|--------|------|------|----------|--------|-----------------|------|
| Titre  | Nom    | 2024 | Académique | URL | ✅ | 4 | Insight clé |
```

Types : `académique` / `philosophique` / `praticien` / `entrepreneur` / `non-conventionnel` / `littéraire` / `culturel` / `données`

---

## Taxonomie des Sources — 8 Couches

### Couche 1 — Académique (fondation)

**Ce qu'on cherche** : ce qui est démontrable, réplicable, peer-reviewed

**Bases de données** :
- **Google Scholar** : point d'entrée universel, gratuit
- **PubMed** : sciences de la vie, psychologie, neurosciences
- **JSTOR** : sciences humaines et sociales, archives historiques
- **arXiv** : sciences dures, IA, mathématiques (preprints)
- **SSRN** : économie, droit, sciences sociales (preprints)
- **Cairn.info** : sciences humaines francophones (SHS)
- **OpenDOAR / CORE** : accès libre aux repositories institutionnels

**Thèses et mémoires** :
- **ProQuest Dissertations** : thèses américaines et canadiennes
- **TEL (theses.fr)** : thèses françaises en ligne
- **EThOS** : thèses britanniques
- **DART-Europe** : thèses européennes

**Comment chercher** :
- Commencer par les **méta-analyses** et **revues systématiques** (titre contient "meta-analysis", "systematic review", "literature review")
- Remonter aux **articles originaux** cités dans les synthèses
- Chercher l'auteur qui domine le domaine → lire toute sa bibliographie
- Chercher aussi les **articles de critique** ("critique of", "replication failure", "limits of")

---

### Couche 2 — Philosophie & Histoire des Idées

**Ce qu'on cherche** : les fondements conceptuels, les questions que personne ne pose plus

**Philosophes anciens à consulter par domaine** :

| Domaine | Anciens incontournables |
|---------|------------------------|
| Apprentissage / connaissance | Socrate (maïeutique), Platon (allégorie de la caverne), Aristote (catégories) |
| Action / décision | Épictète (stoïcisme pratique), Marc Aurèle, Sénèque |
| Rhétorique / persuasion | Aristote (*Rhétorique*), Cicéron (*De Oratore*), Quintilien |
| Éthique / comportement | Kant, Hume, Mill (utilitarisme), Nietzsche (valeurs) |
| Épistémologie | Descartes, Bacon (méthode expérimentale), Hume (causalité), Popper (falsifiabilité) |
| Changement / transformation | Héraclite ("panta rei"), Hegel (dialectique), Marx |
| Nature humaine | Hobbes, Locke, Rousseau (contrat social) |

**Penseurs modernes à chercher** :
- William James (pragmatisme américain)
- John Dewey (éducation par l'expérience)
- Michel Foucault (pouvoir, discours)
- Pierre Bourdieu (habitus, capital culturel)
- Hannah Arendt (action, pensée politique)
- Paul Ricœur (herméneutique, récit)

**Ressources** :
- **Stanford Encyclopedia of Philosophy** (SEP) : référence académique accessible
- **Internet Archive** : textes anciens libres de droits
- **Gallica (BNF)** : textes philosophiques français numérisés

---

### Couche 3 — Praticiens & Experts du Domaine

**Ce qu'on cherche** : ce qui marche dans le monde réel, pas seulement en laboratoire

**Formats à chercher** :
- Livres de praticiens (pas académiques) — chercher les 10 livres les plus cités dans le domaine
- **TED Talks** et conférences filmées (YouTube, Vimeo) — pour les idées fortes condensées
- **Podcasts longs** (Lex Fridman, Tim Ferriss, Huberman Lab, France Culture...) — les praticiens y parlent différemment que dans leurs livres
- **Interviews longues** : un expert perd sa garde après 1-2h, dit ce qu'il pense vraiment
- **Newsletters de spécialistes** — souvent plus à jour et moins filtrés que les livres

**Qui chercher** :
- Les **fondateurs** du champ — qui a eu l'idée originale ?
- Les **dissidents** — qui s'est fâché avec le consensus et pourquoi ?
- Les **traducteurs** — qui a pris l'idée abstraite et l'a rendue pratique ?
- Les **critiques** — qui dit que tout ça ne marche pas, et avec quels arguments ?

---

### Couche 4 — Entrepreneurs Visionnaires & Penseurs "First Principles"

**Ce qu'on cherche** : la pensée par simplification radicale, les modèles mentaux de terrain, les frameworks issus de l'action à grande échelle

Ces profils ne sont ni académiques ni praticiens classiques. Ce sont des gens qui ont construit des choses impossibles en refusant les conventions de leur secteur. Leurs idées sont souvent moins rigoureuses que la recherche académique mais **plus puissantes que n'importe quelle théorie** pour mobiliser, décider, simplifier.

**Profils types** :

| Penseur | Ce qu'il apporte spécifiquement |
|---------|--------------------------------|
| **Elon Musk** | First principles thinking ("raisonnez depuis la physique, pas par analogie"), Boîte à Idioties, MVPs extrêmes, tolérance au risque absurde |
| **Jeff Bezos** | Day 1 mentality, Customer Obsession, Working Backwards (lettre d'annonce avant le produit), Long-term thinking, Regret Minimization Framework |
| **Steve Jobs** | Simplicité comme résistance ("dire non à mille choses"), Intersection arts/technologie, vision du produit fini comme point de départ |
| **Warren Buffett** | Circle of Competence, Inversion (penser en erreurs à éviter), Mr. Market, pensée probabiliste |
| **Charlie Munger** | Latticework of mental models (100+ modèles), Inversion systématique, Lollapalooza effect (effets combinés) |
| **Jensen Huang (Nvidia)** | "Pain + Reflection = Progress", culture de franchise radicale, impossibilité assumée comme moteur |
| **Reed Hastings** | No Rules Rules, densité de talent, contexte plutôt que contrôle |
| **Ray Dalio** | Principes explicites, mécanisme de la réalité, radical transparency, idea meritocracy |
| **Paul Graham** | Conseils à contre-courant (Do Things That Don't Scale, Keep Your Identity Small...) |
| **Naval Ravikant** | Leverage spécifique, knowledge + code + capital, wealth vs. money |

**Sources à consulter** :
- **Lettres aux actionnaires** (Bezos → Amazon Letters, Buffett → Berkshire) : condensé de pensée sur 20-30 ans
- **Interviews longues** sur Lex Fridman, How I Built This, Invest Like the Best
- **Podcasts/writings** de Paul Graham (paulgraham.com essays), Naval (blog + podcast)
- **Biographies autorisées** : *Steve Jobs* (Isaacson), *The Everything Store* (Stone)
- **Transcriptions de talks** (All In Podcast, Acquired podcast pour les deep dives)

**Comment utiliser cette couche** :
- Ne pas citer comme preuve empirique — ces gens n'ont souvent pas de données au sens académique
- Utiliser pour **formuler**, **simplifier**, **tester une idée contre le réel**
- Ce qu'ils ont **fait** compte plus que ce qu'ils **disent** — chercher les décisions, pas les discours

---

### Couche 5 — Voix Non-Conventionnelles

**Ce qu'on cherche** : les angles morts du consensus, les idées hétérodoxes bien argumentées

**Principe** : Une idée non-conventionnelle n'est pas nécessairement fausse. Elle peut être en avance, supprimée, ou simplement ignorée par inertie institutionnelle. Critère d'inclusion : **cohérence interne + base empirique ou logique solide**, quelle que soit la popularité.

**Où trouver** :
- **Substack** : chercher les auteurs qui remettent en question le consensus de leur domaine
- **LessWrong** : raisonnement rationnel appliqué à des sujets non conventionnels
- **Edge.org** : questions annuelles aux meilleurs penseurs mondiaux
- **Blogs académiques personnels** : souvent plus libres que les publications officielles
- **Reddit r/science, r/slatestarcodex, r/philosophy** : débats de fond entre gens informés
- **Heterodox Academy** : voix académiques alternatives (sciences sociales)
- **INET (Institute for New Economic Thinking)** : économie alternative
- **Revues hétérodoxes** : *Real-World Economics Review*, *Journal of Post-Keynesian Economics*...

**Penseurs marginaux influents par domaine** :
- **Psychologie** : Nassim Taleb (antifragilité), Jonathan Haidt (fondements moraux)
- **Éducation** : John Holt (unschooling), Sugata Mitra (école dans le nuage)
- **Leadership** : Bob Sutton (no asshole rule), Ricardo Semler (démocratie en entreprise)
- **Économie** : E.F. Schumacher (Small is Beautiful), Mariana Mazzucato
- **Sciences cognitives** : Francisco Varela (enaction), Mark Johnson (embodied cognition)

**Critères d'inclusion pour une source non-conventionnelle** :
- [ ] L'auteur maîtrise le domaine mainstream avant de s'en éloigner
- [ ] L'argument est falsifiable (peut être contredit par des faits)
- [ ] Les données/exemples sont vérifiables
- [ ] L'auteur reconnaît les limites de son approche
- [ ] La position n'est pas simplement motivée par la provocation ou l'intérêt commercial

---

### Couche 6 — Arts, Littérature & Poésie

**Ce qu'on cherche** : ce que la raison seule ne peut pas saisir — les vérités émotionnelles, incarnées, symboliques

La littérature et la poésie atteignent des vérités psychologiques avant la science. Dostoïevski a décrit la souffrance mentale avec une précision que la psychiatrie du XIXe siècle n'avait pas encore.

**Approches** :
- Pour un sujet humain (peur, transformation, pouvoir, apprentissage...) : chercher le **roman canonique** qui traite ce thème
- Chercher les **essais d'auteurs** (Montaigne, Emerson, Baldwin, Virginia Woolf) — souvent plus profonds que les articles
- **Poésie comme condensé conceptuel** : un poème réussit ce qu'un article de 50 pages rate
- **Mythologie** (Campbell, Graves) : les archétypes narratifs révèlent des structures psychologiques universelles

**Auteurs-penseurs à consulter** :
| Thème | Auteurs suggérés |
|-------|-----------------|
| Nature humaine | Dostoïevski, Tolstoï, Kafka, Camus |
| Pouvoir & résistance | Orwell, Hannah Arendt, James Baldwin |
| Transformation | Hermann Hesse, Rainer Maria Rilke |
| Mémoire & identité | Proust, Borges, Toni Morrison |
| Éducation & croissance | Goethe (*Wilhelm Meister*), Rousseau (*Émile*) |
| Action & courage | Seneca, Marcus Aurelius, Épictète |

---

### Couche 7 — Diversité Géographique & Culturelle

**Ce qu'on cherche** : les angles culturels qui n'existent pas dans le cadre de référence dominant

**Pourquoi c'est important** : La majorité des sources académiques en gestion, psychologie et pédagogie sont anglo-saxonnes, WEIRD (Western, Educated, Industrialized, Rich, Democratic). Elles représentent ~12% de la population mondiale mais ~80% des publications en sciences du comportement.

**Grille de diversification** :

| Zone | Apport spécifique | Sources type |
|------|-------------------|--------------|
| **France** | Philosophie sociale, dialectique, rôle de l'État | Bourdieu, Foucault, Sartre, Derrida, les Annales |
| **Allemagne** | Phenomenologie, hermeneutique, philosophie du travail | Hegel, Nietzsche, Heidegger, Habermas, Freud |
| **Japon** | Kaizen, Ikigai, Esthétique du vide (Wabi-sabi), long terme | Toyota Way, Mishima, Zen |
| **Chine** | Collectif vs individuel, harmonie, pensée systémique | Confucius, Sun Tzu, Taoïsme, Lao Tseu |
| **Inde** | Non-dualité, conscience, praxi spirituelle | Upanishads, Gandhi, Krishnamurti, Amartya Sen |
| **Amérique Latine** | Libération, pensée critique, colonialité | Paulo Freire (pédagogie des opprimés), Borges |
| **Afrique** | Ubuntu ("je suis parce que nous sommes"), communauté | Desmond Tutu, Achille Mbembe, Ubuntu philosophy |
| **Anglo-Saxon (USA)** | Pragmatisme, innovation, empirisme, scale | James, Dewey, Silicon Valley thought leaders |
| **Scandinavie** | Confiance, flat hierarchy, codesign | Nordic model, Lars Kolind |

**Conseil** : Pour un sujet donné, chercher explicitement "X [sujet] japanese approach", "X french perspective", "X ubuntu philosophy" — souvent les résultats sont surprenants et enrichissants.

---

### Couche 8 — Données Empiriques & Terrain

**Ce qu'on cherche** : ce que les gens font vraiment, pas ce qu'ils disent faire

**Sources** :
- **Rapports d'organisations** : McKinsey, Harvard Business Review, Gallup, OCDE, INSEE, Eurostat
- **Études de cas** : Harvard Business School Cases, INSEAD cases
- **Données ouvertes** : data.gouv.fr, Eurostat, World Bank Open Data, Our World in Data
- **Entretiens qualitatifs** : chercher des thèses qualitatives, des études ethnographiques
- **Observation participante** : si possible, aller sur le terrain

---

## 🔄 Protocole Adaptatif en 6 Phases

> Le protocole n'est PAS linéaire. Il peut boucler. Phase 3 peut ramener à Phase 1.

```
Phase 0 → Phase 1 → Phase 2 ─→ Phase 3 ──→ Phase 4 → Phase 5 → Phase 6
                        ↑            │
                        └──── PIVOT ─┘ (si nouveau filon découvert)
```

---

### Phase 0 — Cadrage (10-15 min)

*(Déjà décrit en tête de document — obligatoire)*

**Livrable** : `00-cadrage.md` complété. Si réponses manquantes → poser les questions à l'utilisateur. Ne pas démarrer sans réponses claires.

---

### Phase 1 — Cartographie rapide (30-45 min)

**Objectif** : comprendre la forme du territoire avant d'explorer

```
1. Chercher "[sujet] overview / introduction" sur Google Scholar → lire les abstracts des 5 premiers
2. Wikipedia (EN + FR) → lire References uniquement, pas le contenu
3. Perplexity ou Elicit : "[sujet] state of the art 2024" → identifier les auteurs qui reviennent
4. Identifier :
   - 3-5 auteurs INCONTOURNABLES
   - 2-3 CONTROVERSES principales
   - Ce qu'on ne sait PAS encore (limites du champ)
   - Les SOURCES EXISTANTES sur le sujet qui semblent déjà bien faites
```

**Livrable** : Plan dans `01-plan.md` → axes prioritaires, sources cibles, ordre d'exploration

**Règle** : **Chercher ce qui existe avant d'aller plus loin**. Si un guide, une revue ou un travail existant couvre 80% du besoin → s'appuyer dessus, ne pas réinventer.

---

### Phase 2 — Capture Brute (durée variable)

**Objectif** : noter TOUT sans filtrer, sans reformuler, sans juger

```
Pour chaque source consultée :
- Rédiger dans 02-brut.md : source + date + quote exacte si mémorable + paraphrase courte
- Ajouter dans 03-sources.md : une ligne par source (cf. template)
- NE PAS chercher à synthétiser en temps réel — juste capturer
```

**Format de capture brute** :
```markdown
## [Auteur, Titre, Date]
- TYPE: académique / entrepreneur / philosophique / ...
- Insight : [ce qui est dit EN MES MOTS]
- Quote : "[citation exacte si forte]" (p.XX ou timestamp)
- Lien : [URL ou référence]
- À approfondir ? oui/non
```

**Règle** : Ne noter que ce qui est **utile pour le cadrage défini en Phase 0**. Si c'est intéressant mais hors sujet → une ligne dans une section "Hors-sujet Potentiellement Utile Plus Tard" dans le brut, pas dans les insights.

---

### Phase 3 — Check de Re-planification (après chaque sous-domaine exploré)

**C'est le cœur du protocole adaptatif. S'arrêter et se poser ces questions** :

```
QUESTIONS DE PIVOT :

1. "Est-ce que j'ai trouvé un FILON inattendu qui vaut plus que mon plan initial ?"
   → Si oui : noter dans 01-plan.md la découverte + re-prioriser les axes suivants

2. "Est-ce que j'accumule des notes sur quelque chose qui est HORS PÉRIMÈTRE ?"
   → Si oui : couper. Reporter dans "Hors-sujet" ou créer une note séparée.

3. "Est-ce que je cherche encore à CONFIRMER ce que je savais déjà ?"
   → Si oui : chercher explicitement une source qui CONTREDIT.

4. "Ai-je consulté au moins 3 types de sources différents ?"
   → Si non : diversifier avant de continuer.

5. "Combien de sources ai-je validées vs. notées sans vérifier ?"
   → Si ratio < 50% validé : faire la Phase 4 maintenant, pas à la fin.
```

**Triggers de PIVOT immédiat** :
- Découverte d'un auteur/concept qui change le cadre initial → noter dans 01-plan.md et ré-orienter
- Constatation que la bonne question n'est pas celle de départ → mettre à jour 00-cadrage.md
- Constatation que quelque chose de mieux que le livrrabl ciblé existe déjà → signaler à l'utilisateur

---

### Phase 4 — Validation des Sources

**Pour chaque source dans 03-sources.md** :

```
Test 1 — Existence
  → La source est-elle accessible et réellement publiée ?
  → L'auteur existe-t-il ? (éviter les confabulations d'IA)

Test 2 — Autorité
  → Qui est l'auteur ? Quelle est son institution ? Sa spécialité ?
  → A-t-il des raisons cachées de dire ce qu'il dit ? (Intérêt financier, idéologique...)

Test 3 — Cohérence interne
  → Les données citées dans la source sont-elles sourçables ?
  → Les conclusions suivent-elles des prémisses correctes ?

Test 4 — Recoupement
  → Au moins 1 autre source indépendante confirme-t-elle le fait central ?
  → Des sources opposées ? Pourquoi s'opposent-elles ?

Test 5 — Récence / Pertinence
  → Pour les sciences dures : < 10 ans sauf référence fondatrice
  → Pour les sciences humaines : la date importe moins que le raisonnement
```

**Mettre à jour** : colonne "Validé" et "Fiabilité 1-5" dans `03-sources.md`.

**Règle** : Une source non-validée peut aller dans les notes brutes mais **jamais dans le livrable final**.

---

### Phase 5 — Distillation (1-2h)

**Objectif** : passer de la capture brute (02) au condensé utile (04)

```
1. Relire 02-brut.md en entier une seule fois sans noter
2. Ouvrir 04-insights.md
3. Demander : "Qu'est-ce que je saurais que je ne savais pas avant ?"
4. Ne noter dans 04-insights.md QUE les réponses à cette question
```

**Structure de 04-insights.md** :
```markdown
# Insights — [Sujet]

## Insights qui changent ma compréhension (max 5)
1.
2.

## Tensions & Contradictions trouvées
- [Source A] dit X ↔ [Source B] dit Y → [Mon interprétation de la divergence]

## Convergences fortes (dit par des gens qui ne s'apprécient pas)
- X est vrai selon [auteur libéral + auteur conservateur + praticien + académique]

## Ce que personne ne dit mais qui semble évident
-

## Questions ouvertes (ce que je ne sais toujours pas)
1.
2.

## Quotes à conserver (verbatim)
> "[Quote exacte]" — Auteur, Source, Date
```

---

### Phase 6 — Synthèse & Livrable (`05-synthese.md`)

**Règle Feynman** : Si vous ne pouvez pas l'expliquer sans jargon à quelqu'un d'intelligent qui n'est pas du domaine, vous n'avez pas encore compris.

```
Structure du livrable :

1. RÉSUMÉ EXÉCUTIF (5-10 lignes)
   → Ce qu'on sait maintenant qu'on ne savait pas avant de commencer

2. CORPS (selon besoin : article / slide / note de formation / skill...)

3. LIMITES & INCERTITUDES
   → Ce qui reste flou, contesté, non résolu

4. SOURCES CLÉS (top 5-10 depuis 03-sources.md)

5. SI CONVERSION EN SKILL :
   - Retirer tout ce qui est "notes de recherche" → garder uniquement le savoir distillé
   - Reformater selon le standard SKILL.md
   - Relire en se demandant : "Est-ce que quelqu'un qui n'a pas fait la recherche comprend tout ?"
```

---

## ✅ Validation des Sources — Checklist Rapide

### Signaux positifs ✅
- L'auteur cite ses sources et les limites de son travail
- La position peut être falsifiée (il dit ce qui lui donnerait tort)
- Des gens qui ne s'apprécient pas arrivent à la même conclusion
- La source a été critiquée ET a répondu aux critiques
- Elle distingue corrélation et causalité
- Elle précise le contexte de validité ("ça marche dans ce contexte, pas dans celui-là")

### Signaux d'alerte ⚠️
- La source ne cite que des auteurs qui pensent pareil
- Aucune limite n'est mentionnée
- Les chiffres ne sont pas sourcés
- L'auteur a un intérêt financier non déclaré dans la conclusion
- La certitude est totale sur un sujet naturellement complexe
- Le ton est polémique plus qu'analytique
- **Source générée par IA sans vérification humaine**

---

## 🛠️ Outils Pratiques

| Outil | Usage |
|-------|-------|
| **Connected Papers** | Visualiser le graphe de citations d'un article |
| **Semantic Scholar** | Moteur de recherche académique avec IA |
| **Unpaywall** | Accéder gratuitement aux articles payants (légal) |
| **Zotero** | Gestionnaire de bibliographie open source |
| **Perplexity AI** | Recherche avec sources citées (point de départ, jamais point final) |
| **Elicit.org** | IA pour revue de littérature académique — cherche des papers spécifiquement |
| **Consensus.app** | État du consensus académique sur une question — très utile pour Phase 1 |
| **paulgraham.com** | Essays de Paul Graham — idées contre-intuitives bien argumentées |
| **Edge.org** | Questions annuelles aux meilleurs penseurs mondiaux |
| **Substack** | Voix hétérodoxes et experts de niche qui ne publient pas en académique |

---

## ❌ Anti-Patterns à Éviter

- **La bulle Wikipedia** : Lire Wikipedia puis s'arrêter. Wikipedia est un début, jamais une fin.
- **L'autorité unique** : Lire le livre LE PLUS CONNU et s'estimer informé.
- **La confirmation rapide** : Chercher des sources qui confirment ce qu'on croit déjà.
- **Le biais de langue** : Ne lire que les sources en anglais (ou qu'en français).
- **L'actualité chronique** : Ne lire que ce qui a été publié dans les 2 dernières années.
- **La profondeur sans largeur** : Devenir ultra-expert d'un sous-sous-domaine sans voir l'image globale.
- **La largeur sans profondeur** : Survoler 50 sources sans en avoir compris une seule.
- **Foncer sans cadrer** : Commencer à chercher sans avoir défini l'usage final.
- **Noterr pour noter** : Capturer tout ce qui semble intéressant sans filtre → bruit.
- **Ignorer les pivots** : Trouver un filon inattendu et continuer le plan initial par inertie.
- **Valider à la fin seulement** : Construire toute une synthèse sur des sources non vérifiées.
- **Confondre quote entrepreneuriale avec preuve** : Ce que dit Musk est une hypothèse, pas un fait démontré.

---

## 📋 Quand Utiliser Quelle Couche

| Besoin | Couches prioritaires |
|--------|---------------------|
| Comprendre un concept scientifique | 1 → 7 |
| Préparer une formation | 1 + 3 + 4 + 6 |
| Nourrir une prise de décision stratégique | 4 + 5 + 8 |
| Écrire un article de fond | 1 + 2 + 5 + 7 |
| Créer un nouveau skill | 1 + 3 + 4 + 5 |
| Comprendre un phénomène humain/culturel | 2 + 6 + 7 + 8 |
| Challenger une idée reçue | 5 + 4 + 2 |

**Règle** : La profondeur minimale = **3 couches différentes** pour toute recherche sérieuse.

