---
name: markdown-lisibilite
description: "Expert en lisibilité visuelle Markdown. Utilise ce skill dès que tu crées ou révises du contenu Markdown : documentation technique, fiches pédagogiques, README, wikis Confluence, prompts, SKILL.md, réponses longues. Couvre : typographie, hiérarchie visuelle, patterns listes/tableaux/gras, anti-patterns, structure cognitive du lecteur scanneur, contenu pédagogique (chunking, progressive disclosure), citations et dialogues."
---

# Lisibilité Visuelle en Markdown

## Quand utiliser ce skill

- Écrire ou réviser un README, SKILL.md, fiche pédagogique, wiki, documentation
- Réponses longues dans un chat (structurer pour le scan)
- Détecter des anti-patterns dans un document existant
- Formater des citations, dialogues, tableaux de comparaison
- Contenu pédagogique (formations, tutoriels, explications)

---

## 1. Lois typographiques fondamentales

### Longueur de ligne (CPL — Characters Per Line)
- **Optimal** : 60–80 caractères par ligne (Butterick's Practical Typography)
- **Maximum** : 100 caractères. Au-delà, l'œil perd le début de la ligne suivante
- **Minimum** : 45 caractères. En dessous, trop de sauts, lecture hachée
- En Markdown rendu (HTML), CSS `max-width: 65ch` est la règle d'or
- Dans un terminal / éditeur, préférer les paragraphes courts à la prose étalée

### Interligne et espacement
- Une ligne vide entre chaque paragraphe (règle absolue en Markdown)
- Une ligne vide **avant** chaque titre (sauf début de fichier)
- Ne jamais empiler deux titres sans contenu entre eux (`## A` suivi direct de `### B`)
- Espacement cohérent : ne pas mélanger des blocs aérés et des blocs serrés dans le même document

### Hiérarchie visuelle (H1 → H6)
- **H1** : Titre unique du document. Un seul par fichier.
- **H2** : Sections principales (max 5–7 par document)
- **H3** : Sous-sections. Ne pas descendre sous H3 sauf nécessité absolute
- **H4+** : signal d'alerte — le document est probablement trop dense, envisager de le scinder
- Règle : chaque titre introduit **au moins 2–3 lignes** de contenu avant le titre suivant

### Contraste et lisibilité
- Jamais de texte light-grey sur white en production (ratio WCAG AA : 4.5:1 minimum)
- En Markdown brut : le gras signale l'importance, pas la décoration
- Les titres créent du "white space" visuel par leur hauteur — c'est leur rôle respiratoire

---

## 2. Patterns Markdown : quand et pourquoi

### Liste à puces vs paragraphe

**Utiliser une liste quand :**
- Les items sont **parallèles** (même structure grammaticale)
- Il y a **3 items ou plus**
- Les items peuvent être **lus dans n'importe quel ordre**
- Chaque item est **court** (< 1 ligne idéalement, < 2 lignes max)

**Utiliser un paragraphe quand :**
- Les idées s'**enchaînent logiquement** (cause/effet, séquence narrative)
- Il y a moins de 3 éléments ("d'abord X, puis Y" = prose, pas liste)
- Le contenu est **argumentatif** (raisonnement, nuances)

```markdown
❌ ANTI-PATTERN — liste de phrases complètes narrative :
- Premièrement, nous avons analysé les données.
- Ensuite, nous avons identifié les anomalies.
- Finalement, nous avons corrigé le pipeline.

✅ BON — prose fluide :
Nous avons d'abord analysé les données, identifié les anomalies,
puis corrigé le pipeline.

✅ BON — liste d'items parallèles :
Outils utilisés :
- dbt (transformations)
- Airflow (orchestration)
- Snowflake (stockage)
```

### Listes numérotées vs à puces
- **Numérotées** : quand l'ordre compte (procédure, étapes séquentielles)
- **À puces** : quand l'ordre est indifférent (caractéristiques, exemples, options)

### Séparateur horizontal `---`
Utiliser **uniquement** pour marquer une **rupture thématique forte** — changement de contexte, fin de section majeure avant une nouvelle partie totalement distincte.

Ne **jamais** utiliser pour décorer ou "aérer". Chaque `---` doit avoir une signification editoriale.

```markdown
✅ BON : séparer deux sections conceptuellement distinctes
## Concepts théoriques
[contenu]

---

## Exercices pratiques
[contenu]

❌ MAUVAIS : utiliser --- entre chaque sous-section
### Étape 1
[2 lignes]
---
### Étape 2
```

### Tableaux vs listes

| Utiliser un tableau quand… | Utiliser une liste quand… |
|---------------------------|--------------------------|
| Comparaison multi-dimensionnelle (≥2 propriétés) | Énumération simple (1 propriété) |
| Données structurées (API, config) | Items sans relation entre eux |
| Le lecteur doit cross-référencer | L'ordre ou la relation n'importe pas |
| ≥ 3 lignes ET ≥ 2 colonnes | < 3 éléments à comparer |

```markdown
❌ MAUVAIS — pseudo-tableau en liste :
- Snowflake : data warehouse
- dbt : transformations
- Airflow : orchestration

✅ BON — tableau si 3+ attributs à comparer :
| Outil | Rôle | Langage |
|-------|------|---------|
| Snowflake | Data warehouse | SQL |
| dbt | Transformations | SQL/Jinja |
| Airflow | Orchestration | Python |

✅ BON — liste si 1 attribut seulement :
Stack utilisée : Snowflake, dbt, Airflow
```

### Gras `**text**` vs italique `*text*`

| Usage | Format | Règle |
|-------|--------|-------|
| Terme clé, point critique, IMPORTANT | `**gras**` | Sparingly — max 1–2 par paragraphe |
| Titre de livre, mot étranger, emphasis léger | `*italique*` | Pour nuance sémantique |
| Terme technique à définir | `*italique*` au premier usage | Puis sans formatage |
| Avertissement ou mise en garde | **Gras** en début de phrase | "**Attention :** …" |

**Règle absolue :** si tout est en gras, rien n'est en gras. Le gras perd son pouvoir au-delà de 10–15% du texte.

```markdown
❌ MAUVAIS — gras décoratif saturé :
**Pour configurer** le projet, **ouvrir** le fichier **config.yaml**
et **modifier** les **paramètres** de **connexion**.

✅ BON — gras uniquement sur ce qui mérite d'être scanné :
Pour configurer le projet, ouvrir `config.yaml` et modifier
les paramètres de connexion. **Ne jamais commiter ce fichier.**
```

### Blockquotes `>`

Utiliser pour :
1. **Citations directes** d'une source externe (auteur, documentation officielle)
2. **Callouts importants** — note, avertissement, tip (si pas de syntaxe dédiée disponible)
3. **Dialogue** ou parole attribuée à un locuteur
4. Mettre en **relief un principe** dans un contexte pédagogique

Ne **pas** utiliser pour indenter visuellement du contenu "normal" ou comme décoration.

```markdown
> "Perfection is achieved not when there is nothing more to add,
> but when there is nothing left to take away."
> — Antoine de Saint-Exupéry

> **Note :** Cette configuration est requise uniquement en production.
```

### Code blocks `` ` `` et ` ``` `

- **Inline** `` `code` `` : noms de fichiers, commandes courtes, valeurs, variables, chemins
- **Bloc** ` ```lang ` : tout code > 1 ligne, toujours avec **spécification du langage**
- Ne jamais mettre du texte "non-code" dans un bloc code pour l'indenter
- Les exemples "avant/après" ou "bon/mauvais" méritent TOUJOURS un bloc de code

```markdown
❌ MAUVAIS — langue non spécifiée :
```
SELECT * FROM table
```

✅ BON — langue et contexte :
```sql
SELECT page_id, title FROM doc_pages WHERE state = 'ENRICHED';
```
```

---

## 3. Anti-patterns nommés

### Le Mur de Texte
**Définition** : Paragraphe > 6 lignes sans aucun élément visuel (titre, liste, gras).  
**Effet** : Le lecteur scanneur décroche immédiatement. Taux de lecture chute.  
**Remède** : Couper en 2–3 paragraphes, ajouter un titre intermédiaire, ou extraire une liste.

### La Liste Monstre (> 7 items)
**Définition** : Liste à puces de 8 items ou plus sans regroupement.  
**Effet** : Surcharge cognitive. Le lecteur ne retient que les 3 premiers et les 2 derniers (effet de primauté/récence).  
**Remède** : Regrouper en sous-listes avec titres. Seuil psychologique de Miller : 7±2 chunks.

```markdown
❌ MAUVAIS — 10 items sans structure :
- Airflow
- dbt
- Snowflake
- Streamlit
- n8n
- Python
- SQL
- VS Code
- Git
- Docker

✅ BON — regroupé par catégorie :
**Orchestration & Pipeline**
- Airflow, dbt, n8n

**Data & BI**
- Snowflake, Streamlit, SQL

**Dev**
- Python, VS Code, Git, Docker
```

### Le Gras Décoratif
**Définition** : Gras sur > 15% du texte, souvent sur des mots grammaticaux sans importance.  
**Effet** : Plus rien ne ressort. Rend le scan inutile.  
**Remède** : Ne garder en gras que 1–2 éléments par paragraphe, uniquement ce que le lecteur doit voir en 3 secondes.

### Le Titre Orphelin
**Définition** : `### Titre` suivi immédiatement d'un autre `#### Sous-titre` sans contenu intermédiaire.  
**Effet** : Hiérarchie confuse, document qui ressemble à un plan vide.  
**Remède** : Toujours au moins une phrase de contexte sous un titre avant de descendre dans la hiérarchie.

### La Liste de Phrases Complètes
**Définition** : Liste où chaque item est une phrase de 2+ lignes avec verbe conjugué.  
**Effet** : Pire que la prose : ni la fluidité du paragraphe, ni la scannabilité de la liste.  
**Remède** : Soit condenser les items (< 1 ligne, structure parallèle), soit réécrire en prose.

### Le Tableau Inutile (2 colonnes, 2 lignes)
**Définition** : Tableau avec 2 colonnes et 2–3 lignes pour remplacer une phrase.  
**Effet** : Overhead visuel pour zéro gain.  
**Remède** : "X fait A, Y fait B" = phrase. Tableau = 3+ lignes ET 2+ dimensions de comparaison.

### La Hiérarchie Plate
**Définition** : Tout le document en H2, sans H3 ni H4, ou tout en H1.  
**Effet** : Pas d'entrée visuelle dans le document. Pas de chemin de navigation.  
**Remède** : Utiliser H2 pour les grandes sections, H3 pour les sous-thèmes.

### La Ponctuation Anglaise / Tiret Oublié
**Définition** : `"guillemets anglais"` au lieu de `«guillemets français»`, manque d'espace insécable avant `:` `;` `!` `?` en français.  
**Effet** : Document en français avec rendu bâclé.  
**Remède** : `«texte»`, ` : `, ` ; `, ` !`, ` ?` avec espace insécable (ou au moins espace simple si Markdown ne supporte pas `&nbsp;`).

---

## 4. Structure cognitive du lecteur scanneur

### Le F-Pattern (Nielsen Norman Group, 2006 + 2017)
L'œil parcourt un document textuel selon un F :
1. **Bande horizontale haute** : lecture de la première ligne quasi complète
2. **Bande horizontale médiane** : lecture partielle d'une ligne dans le premier tiers
3. **Colonne verticale gauche** : scan des débuts de ligne descend rapidement

**Implication** : Les **3–4 premiers mots de chaque ligne** sont les plus lus. Mettre l'information critique à gauche, jamais enfouie à droite.

### Le Layer-Cake Pattern
Utilisé sur les **documents bien structurés** (titres + corps alternés) : l'œil saute de titre en titre, lit quelques lignes, resaute. C'est le comportement idéal à construire.

**Comment y parvenir :**
- Titres H2/H3 comme **ancres de navigation** (pas de titres vagues : "Introduction", "Contenu")
- Titres **descriptifs et autonomes** — compréhensibles hors contexte
- Premier paragraphe de chaque section = **résumé** de la section (top-loading)

### Les ancres visuelles
Par ordre d'efficacité pour capter le regard :
1. **Titres** (H1 > H2 > H3)
2. **Listes à puces / numérotées**
3. **Gras** dans la prose
4. **Tableaux**
5. **Blocs de code**
6. **Images / diagrammes**
7. *Italique*

Le regard saute d'ancre en ancre. La prose est lue **entre** les ancres, pas avant.

### Règle de la première phrase (top-loading)
La première phrase de chaque paragraphe/section doit contenir **l'essentiel** de l'information. Les phrases suivantes approfondissent.

```markdown
❌ MAUVAIS — bottom-loading :
En 2006, Nielsen a mené une étude avec des trackers oculaires
sur plusieurs milliers d'utilisateurs. Les résultats, très
interessants, ont montré que les gens lisaient en F.

✅ BON — top-loading :
Les lecteurs scannent les pages web en F (Nielsen, 2006).
L'œil lit la première ligne, puis descend en scannant
uniquement la gauche. Implication : l'info critique va à gauche.
```

---

## 5. Mise en forme des dialogues et citations

### Citations courtes (< 1 ligne)
Inline dans la prose avec guillemets français : `«texte»`

```markdown
Comme le note Butterick : «La typographie est le son visuel du texte.»
```

### Citations longues (> 1 ligne)
Blockquote `>` avec attribution en dessous :

```markdown
> Le texte bien composé disparaît. Le lecteur n'est pas
> conscient de la mise en forme — il est seulement conscient
> du sens.
>
> — Matthew Butterick, *Practical Typography*
```

### Dialogue entre locuteurs
Option 1 — Gras sur le locuteur + tiret cadratin :

```markdown
**Utilisateur** — Comment activer le mode Training ?  
**Assistant** — Saisir votre prénom et l'ID `2026-04` dans le formulaire.
```

Option 2 — Blockquote imbriqué (locuteur secondaire en réponse) :

```markdown
— Qu'est-ce qu'un agent IA ?

> Un agent IA est un système capable de planifier et d'exécuter
> des actions de façon autonome pour atteindre un objectif.
```

Option 3 — Tableau (pour FAQ ou Q&A pédagogique) :

```markdown
| Question | Réponse |
|----------|---------|
| Qu'est-ce qu'un LLM ? | Un modèle de langage entraîné sur du texte à grande échelle. |
| Quelle est la différence entre GPT et Claude ? | Architecture et prestataire différents ; comportement similaire. |
```

### Règles typographiques françaises en Markdown
| Cas | Correct | Incorrect |
|-----|---------|-----------|
| Guillemets | `«texte»` | `"texte"` |
| Tiret de dialogue | `—` (cadratin) | `-` (trait d'union) |
| Espace avant `:` | `mot :` | `mot:` |
| Espace avant `!` `?` | `Vraiment ?` | `Vraiment?` |
| Points de suspension | `…` (1 caractère) | `...` (3 points) |

---

## 6. Contenu pédagogique : règles spécifiques

### Chunking — Miller (1956), 7 ± 2
- Ne jamais dépasser **7 items** dans une liste sans regroupement
- Regrouper par **catégories sémantiques** (pas arbitrairement)
- Chaque "chunk" = un concept ou une tâche unitaire
- Appliquer au niveau des sections : max **5–7 sections H2** par document

### Progressive Disclosure
Révéler l'information par **couches de complexité croissante** :
1. Vue d'ensemble (ce que c'est, à quoi ça sert)
2. Utilisation basique (comment faire le cas standard)
3. Options avancées (configurations, cas limites)
4. Référence complète (tout, pour les experts)

```markdown
✅ BON — progressive disclosure :
## Vue d'ensemble
dbt transforme vos données SQL en pipeline versionné.

## Utilisation basique
```bash
dbt run --select mon_modele
```

## Configuration avancée
Voir `profiles.yml` pour les connexions multi-environnements.
```

### Exemple avant règle (Concrete-before-Abstract)
Le cerveau comprend mieux un exemple concret **avant** la règle abstraite. Auteurs : Sweller (Cognitive Load Theory), Brown/Roediger (Make It Stick).

```markdown
❌ MAUVAIS — règle d'abord :
Les chunked prompts divisent les instructions complexes
en segments atomiques pour réduire la charge cognitive.

✅ BON — exemple d'abord :
Au lieu de : "Analyse ce texte, identifie les entités, classe-les
par type, génère un résumé et propose des tags."

Faire : une instruction à la fois, dans des messages séparés.
C'est le **chunked prompting** — diviser pour réduire la charge cognitive.
```

### Les 4 C du contenu pédagogique (Merrill, 2002)
1. **Concret** : exemples réels, pas abstraits
2. **Connecté** : lié à ce que l'apprenant sait déjà
3. **Contrasté** : montrer les anti-patterns, pas seulement les bonnes pratiques
4. **Challengé** : poser une question, créer une attente avant de donner la réponse

### Callouts structurés
```markdown
> **💡 Concept clé :** Le fine-tuning modifie les poids du modèle.
> Le prompt engineering guide le modèle sans le modifier.

> **⚠️ Piège fréquent :** Ne pas confondre temperature (créativité)
> et top_p (diversité du vocabulaire). Modifier les deux simultanément
> rend le débogage impossible.

> **✅ Bonne pratique :** Tester avec temperature=0 d'abord,
> puis monter progressivement.
```

---

## 7. Références — Sources et auteurs

| Source | Domaine | Règles clés couvertes |
|--------|---------|----------------------|
| **Butterick's Practical Typography** (butterick.com/practical-typography) | Typographie web | CPL, interligne, hiérarchie, gras/italique |
| **Nielsen Norman Group** (nngroup.com) | UX Research | F-Pattern, Layer-cake, Progressive disclosure |
| **GOV.UK Content Design Guide** (gov.uk/guidance/content-design) | Plain language, accessibilité | Phrases courtes, top-loading, listes |
| **Google Material Design — Writing** | Design system | Tone, concision, hiérarchie |
| **Apple HIG — Writing** | Design system | Clarté, économie de mots |
| **Cognitive Load Theory** — Sweller (1988) | Pédagogie | Chunking, contenu intrinsèque vs extrinsèque |
| **Make It Stick** — Brown, Roediger, McDaniel (2014) | Apprentissage | Concrétude, interleaving, retrieval practice |
| **Merrill's First Principles** (2002) | Instructional design | Concret avant abstrait, résolution de problèmes |
| **Miller's Law** — Miller (1956) | Psychologie cognitive | 7 ± 2 chunks en mémoire de travail |
| **The Elements of Typographic Style** — Bringhurst | Typographie | Rythme, proportion, hiérarchie |

---

## 8. Checklist de révision rapide

Avant de livrer un document Markdown, vérifier :

```
STRUCTURE
[ ] Un seul H1 par document
[ ] H2 ≤ 7 sections
[ ] Chaque titre a au moins 2 lignes de contenu dessous
[ ] Pas de titres empilés sans contenu intermédiaire

LISTES
[ ] Chaque liste ≤ 7 items ou sous-groupes
[ ] Items structurellement parallèles (même forme grammaticale)
[ ] Liste numérotée si et seulement si l'ordre compte

FORMATAGE
[ ] Gras ≤ 1-2 par paragraphe, sur info critique uniquement
[ ] Italique pour termes techniques/étrangers seulement
[ ] Langue spécifiée sur tous les blocs de code

CONTENU
[ ] Première phrase de chaque section = essentiel (top-loading)
[ ] Exemples concrets avant règles abstraites
[ ] Pas de mur de texte (paragraphe > 6 lignes sans ancre visuelle)

TYPOGRAPHIE FRANÇAISE
[ ] Guillemets «français»
[ ] Espaces avant : ; ! ?
[ ] Tirets cadratins — pour les dialogues

TABLEAUX
[ ] Tableau = min 3 lignes ET 2+ dimensions de comparaison
[ ] Sinon : liste ou phrase
```

---

## 9. Patterns de révision — Avant/Après complet

### Cas 1 : Révision d'une section documentation

```markdown
❌ AVANT (mur de texte + gras décoratif) :
**Pour installer** le projet, vous devez d'abord **cloner** le dépôt
avec git clone, puis **installer les dépendances** en exécutant
pip install -r requirements.txt dans votre terminal. Ensuite vous
devez **configurer** les variables d'environnement en copiant le
fichier .env.example vers .env et en **remplissant** les valeurs.
Finalement, vous pouvez **lancer** l'application avec streamlit run app.py.

✅ APRÈS (top-loading + liste séquentielle + code inline) :
## Installation

Quatre étapes pour démarrer :

1. Cloner le dépôt : `git clone https://github.com/…`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer l'environnement : copier `.env.example` → `.env` et compléter les valeurs
4. Lancer : `streamlit run app.py`

**Prérequis :** Python 3.10+, accès réseau pour les requêtes Snowflake.
```

### Cas 2 : Révision d'une liste pédagogique

```markdown
❌ AVANT (liste monstre de phrases complètes) :
Les avantages de dbt sont nombreux :
- dbt permet de versionner vos transformations SQL dans Git comme du code
- dbt génère automatiquement la documentation de vos modèles et leurs dépendances
- dbt teste la qualité des données via des assertions configurables en YAML
- dbt gère les dépendances entre modèles et les exécute dans le bon ordre
- dbt est compatible avec de nombreux data warehouses dont Snowflake, BigQuery, Redshift
- dbt permet le développement en environnements multiples (dev, staging, prod)
- dbt dispose d'un écosystème de packages réutilisables (dbt Hub)
- dbt facilite la collaboration entre data engineers et data analysts

✅ APRÈS (chunking par catégorie, items courts) :
dbt offre trois apports majeurs :

**Qualité & gouvernance**
- Versionning Git des transformations SQL
- Tests de qualité des données (YAML)
- Documentation auto-générée

**Productivité**
- Gestion des dépendances entre modèles
- Multi-environnements (dev / staging / prod)
- Écosystème de packages (dbt Hub)

**Compatibilité**
- Snowflake, BigQuery, Redshift, et autres
```
