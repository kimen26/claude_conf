---
name: info-architecture
description: "L'art de catégoriser, indexer, ranger et nommer intelligemment. Taxonomie, MECE, Diátaxis, PARA, facettes, card sorting. Active dès que l'utilisateur structure une documentation, une base de connaissance, un dossier, un système de tags ou une arborescence de fichiers."
family: impact
origin: Domaine
---

# SKILL : info-architecture

> Organiser l'information pour qu'on la trouve, qu'on la comprenne et qu'on la maintienne — sans effort visible.

---

## Quand activer ce skill

- "Comment structurer ma documentation / ma base de connaissances ?"
- "Quelles grandes sections pour ce projet / ce dossier ?"
- "Je crée un système de tags, comment les nommer ?"
- "Mon arborescence de fichiers est devenue un chaos"
- "Je dois indexer / catégoriser un corpus de contenus"
- Mots-clés : "ranger", "classer", "catégoriser", "indexer", "lotir", "nommer les dossiers"

---

## IA.1 — L'architecture de l'information : définition et enjeux

**Source :** Peter Morville & Louis Rosenfeld, *Information Architecture for the World Wide Web* (1998, O'Reilly)

L'architecture de l'information (AI) est l'art de **structurer et étiqueter** un contenu pour que les gens puissent le **trouver, comprendre et utiliser**.

### Les 3 cercles de Morville

```
       [UTILISATEURS]
           ↕
[CONTEXTE] ↔ [CONTENU]
```

Une bonne architecture répond simultanément à :
- **Qui** cherche ? (utilisateurs, niveau d'expertise, vocabulaire)
- **Quoi** est stocké ? (type de contenu, volume, dynamisme)
- **Dans quel contexte ?** (organisation, outil, usage mobile/web/print)

### Pourquoi l'organisation échoue souvent

| Erreur | Conséquence |
|--------|-------------|
| L'auteur classe selon sa logique de production | Le lecteur cherche selon son besoin de consommation |
| Une seule dimension de classement | Impossible de retrouver quelque chose par un autre angle |
| Nommage instable (synonymes, abréviations) | Doublon silencieux, contenu introuvable |
| Granularité incohérente | Des dossiers à 1 fichier à côté de dossiers à 500 |

---

## IA.2 — MECE : la base de la catégorisation propre

**Source :** McKinsey & Company — principe fondateur de leur structure analytique

**MECE = Mutually Exclusive, Collectively Exhaustive**

- **Mutuellement Exclusif** : chaque élément appartient à une et une seule catégorie
- **Collectivement Exhaustif** : toutes les catégories ensemble couvrent 100% du corpus

### Test MECE

```
□ Si je prends n'importe quel élément de mon corpus,
  peut-il entrer dans DEUX catégories ? → Non = ✅ ME
□ Si je prends n'importe quel élément de mon corpus,
  y a-t-il une catégorie pour lui ? → Oui = ✅ CE
```

### Anti-MECE fréquents

| Problème | Exemple | Correction |
|----------|---------|-----------|
| Overlap | "Formations" + "Formations Management" | "Management" est un sous-type de "Formations" |
| Fourre-tout | Catégorie "Divers" ou "Autres" | Forcer une catégorie propre ou accepter un 4e niveau |
| Niveaux mélangés | "PDF", "Vidéos", "RH", "Finance" | PDF/Vidéo = format ; RH/Finance = domaine → 2 axes différents |

### MECE en pratique : l'arbre

```
Méthode :
1. Lister tous les éléments à classer
2. Trouver le critère de découpage (domaine ? format ? audience ? maturité ?)
3. Créer les catégories du même niveau d'abstraction
4. Tester ME → tester CE → itérer
```

---

## IA.3 — Diátaxis : le meilleur framework pour la documentation

**Source :** Daniele Procida — *Diátaxis* (2021) — utilisé par Django, NumPy, Ubuntu, Linux Kernel docs

Diátaxis distingue **4 types de documentation** selon deux axes :
- Axe vertical : **Apprentissage** (apprendre) vs **Travail** (faire)
- Axe horizontal : **Pratique** (action) vs **Théorique** (connaissance)

### Le carré Diátaxis

```
                  PRATIQUE (action)
                        │
        TUTORIAL ───────┼─────── HOW-TO
   (apprendre            │              (faire)
    en faisant)          │
─────────────────────────┼─────────────────────
   EXPLANATION           │          REFERENCE
   (comprendre           │           (consulter)
    les concepts)        │
                  THÉORIQUE (connaissance)
                        │
                  APPRENTISSAGE ←→ TRAVAIL
```

### Les 4 types en détail

| Type | Question | Format | Exemple |
|------|----------|--------|---------|
| **Tutorial** | "Comment je commence ?" | Étapes guidées, résultat garanti | Quickstart, premier pas |
| **How-To** | "Comment je fais X ?" | Recette, présuppose un contexte | "Comment créer un agent Snowflake" |
| **Reference** | "C'est quoi exactement ?" | Exhaustif, neutre, stable | API, glossaire, liste des paramètres |
| **Explanation** | "Pourquoi ça fonctionne comme ça ?" | Conceptuel, narratif | Architecture, décisions de design |

### Erreurs classiques

```
❌ Mélanger tutorial et how-to dans "Guides"
   → Le débutant se perd dans des guides qui supposent trop
   → L'expert doit chercher dans des tutoriels trop basiques

❌ Mettre les explications dans les références
   → Les refs deviennent trop longues à lire d'une traite
   → L'explication n'est pas retrouvable seule

❌ Pas de section Reference
   → Oblige à relire tout le guide pour retrouver un paramètre
```

### Structure de dossiers Diátaxis

```
docs/
  tutorials/       ← Apprenez en faisant (séquentiels)
  how-to/          ← Guides pratiques (tâches spécifiques)
  reference/       ← API, glossaire, config (complet)
  explanation/     ← Concepts, background, "pourquoi"
```

---

## IA.4 — Taxonomie, Ontologie, Folksonomie

Trois niveaux de sophistication pour l'indexation et le tagging.

| Concept | Définition | Contrôle | Exemple |
|---------|-----------|---------|---------|
| **Folksonomie** | Tags libres, créés par les utilisateurs | Aucun | Tags libres Notion, hashtags Twitter |
| **Taxonomie** | Hiérarchie de termes contrôlés, mono-axe | Fort | Arborescence de dossiers Windows |
| **Ontologie** | Relations sémantiques entre concepts (pas seulement hiérarchiques) | Très fort | Wikidata, Knowledge Graph Google |

### Quelle approche choisir ?

```
Petits corpus, usage perso, croissance rapide → Folksonomie
Documentation équipe, wiki interne → Taxonomie
Searchabilité avancée, recommandations, IA → Ontologie
```

### Thésaurus : le compromis entre folksonomie et taxonomie

Un thésaurus vocabulaire contrôlé avec :
- **Termes préférés** (terme officiel)
- **Termes non-préférés** (synonymes → redirigent vers le term préféré)
- **Relations** : terme plus large / plus étroit / associé

```
Exemple :
Terme préféré : "Formation présentielle"
Termes non-préférés : "formation en salle", "cours en face-à-face", "formation physique"
Terme plus large : "Formation"
Terme plus étroit : "Formation présentielle inter-entreprises"
```

---

## IA.5 — PARA : organiser sa base personnelle

**Source :** Tiago Forte, *Building a Second Brain* (2022)

PARA est un système d'organisation des fichiers et notes en 4 catégories universelles :

| Lettre | Catégorie | Définition | Durée de vie |
|--------|-----------|-----------|-------------|
| **P** | Projects | Objectif avec une deadline | Court terme |
| **A** | Areas | Responsabilité continue sans deadline | Long terme |
| **R** | Resources | Intérêts, références, matière | Permanent |
| **A** | Archives | Tout ce qui n'est plus actif | Permanent |

### Exemples PARA

```
Projects/          ← Ce sur quoi je travaille EN CE MOMENT
  - Refonte_Documentation_Q1_2026/
  - Formation_IA_Lancement_Mars/

Areas/             ← Mes responsabilités continues
  - Management_Équipe/
  - Budget_Formation/
  - Gouvernance_Données/

Resources/         ← Ce qui m'intéresse mais sans projet actif
  - Pédagogie/
  - IA_Outils/
  - Architecture_Information/

Archives/          ← Projets terminés, références obsolètes
  - Formation_Leadership_2024/
  - Projet_Intégration_Snowflake_2023/
```

### La règle de déplacement PARA

```
Un projet terminé → Archives/
Un projet qui démarre → Projects/
Une ressource utilisée dans un projet → reste dans Resources
  (ne pas copier dans Projects — créer un lien/référence)
```

---

## IA.6 — Classification facettée

**Source :** Shiyali Ramamrita Ranganathan, *Colon Classification* (1933) — bibliothéconomie

La classification facettée permet de décrire un même objet selon **plusieurs axes indépendants** (facettes), contrairement à une hiérarchie rigide.

### Principe

```
OBJET → intersection de N facettes

Exemple : un document de formation
  Facette 1 (domaine) : Management
  Facette 2 (type contenu) : Étude de cas
  Facette 3 (niveau) : Avancé
  Facette 4 (format) : PDF
  Facette 5 (date) : 2025
```

### Avantage vs hiérarchie

| Approche | Limite |
|----------|--------|
| **Hiérarchie** `Management/Études de cas/Avancé` | Un seul chemin d'accès → introuvable si vous pensez "Avancé" d'abord |
| **Facettes** | Retrouvable par n'importe quelle combinaison de facettes |

### Implémenter des facettes

En pratique dans Notion, Airtable, SharePoint :
```
Champ "Domaine" : Management / Finance / RH / Tech
Champ "Type" : Tutoriel / Référence / Étude de cas / Outil
Champ "Niveau" : Débutant / Intermédiaire / Avancé
Champ "Statut" : Brouillon / Validé / Archivé
```

---

## IA.7 — Card Sorting : valider une architecture avec les utilisateurs

**Source :** Méthode UX — Jakob Nielsen, Don Norman

Le card sorting est une technique pour découvrir comment les **utilisateurs** (pas l'auteur) organisent mentalement un corpus.

### Types

| Type | Description | Quand |
|------|-------------|-------|
| **Ouvert** | L'utilisateur crée lui-même les catégories | Pour créer une architecture from scratch |
| **Fermé** | Les catégories sont données, l'utilisateur place les cartes | Pour valider une architecture existante |
| **Hybride** | Catégories données + possibilité d'en créer | Le plus courant |

### Protocole simplifié (version équipe)

```
1. Écrire 1 contenu = 1 post-it / carte
2. Réunir 5-10 utilisateurs représentatifs
3. Demander de regrouper les cartes selon leur logique
4. Nommer les groupes (en ouvert)
5. Identifier les patterns : quels groupes reviennent ?
   Quelles cartes créent du désaccord ?
6. Utiliser ces patterns comme base de l'architecture
```

### Insight clé

> "L'architecture intuitive pour l'auteur est rarement l'architecture intuitive pour le lecteur."

---

## IA.8 — Johnny Decimal : numéroter ses dossiers

**Source :** John Noble, *Johnny.Decimal* (2019)

Johnny Decimal est un système de numérotation hiérarchique pour les fichiers et dossiers :

```
[AIRE 10-19] Gestion
  [10] Administration
    10.01 — Contrat de travail
    10.02 — Fiches de paie
  [11] Budget
    11.01 — Budget formation 2026
    11.02 — Factures

[AIRE 20-29] Projets
  [20] Formation IA
    20.01 — Programme
    20.02 — Supports participants
  [21] Refonte Documentation
    21.01 — Arborescence cible
    21.02 — Migration en cours
```

### Règles

```
- Maximum 10 "aires" (00-09, 10-19, etc.)
- Maximum 10 "catégories" par aire
- Chaque fichier a un identifiant unique XX.YY
- Le numéro est stable dans le temps (ne pas renommer les IDs)
```

### Avantages
- Retrouvable par numéro même sans moteur de recherche
- Identifiant court pour référencer dans les emails/Slack : "c'est en 20.02"
- Résiste aux réorganisations (le numéro reste, le contenu bouge dans sa catégorie)

---

## IA.9 — Anti-patterns de l'organisation qui échoue

| Anti-pattern | Symptôme | Cause | Correction |
|-------------|----------|-------|-----------|
| **Le fourre-tout "Divers"** | Dossier "Divers" grossit indéfiniment | Paresse de catégorisation | Forcer une catégorie propre ou créer "À traiter" avec deadline |
| **L'arborescence ego** | Structure = organigramme de l'équipe | On classe selon QUI produit, pas QUI cherche | Restructurer selon les besoins utilisateurs (card sorting) |
| **La granularité folle** | 50 sous-dossiers avec 1 fichier chacun | Sur-segmentation | Regrouper si moins de 5 fichiers dans une catégorie |
| **Les synonymes silencieux** | "Supports", "Fiches", "Ressources", "Outils" dans le même niveau | Nommage non contrôlé | Choisir 1 terme par concept, créer un glossaire |
| **L'archive oubliée** | Vieux fichiers mélangés aux actifs | Pas de convention d'archivage | Convention : préfixe `ARCHIVE_` ou dossier dédié + date |
| **La hiérarchie profonde** | 6+ niveaux de dossiers | Arborescence = pensée complexe externalisée | Max 3-4 niveaux + facettes ou tags pour la profondeur |
| **La duplication fantôme** | Même fichier avec des noms légèrement différents | Pas de "source de vérité" définie | Single Source of Truth + liens vers des copies |

---

## IA.10 — Checklist avant de structurer une base de connaissance

```
Analyse préalable
□ Qui va utiliser cette base ? (profils, vocabulaire naturel)
□ Quels sont les 10 types de contenu principaux ?
□ Quelle est la fréquence de mise à jour prévue ?
□ Quel outil d'hébergement ? (contraintes techniques)
□ La base sera-t-elle publique, interne ou personnelle ?

Choix du framework
□ Documentation technique → Diátaxis
□ Gestion personnelle / PKM → PARA
□ Fichiers d'entreprise → Johnny Decimal + MECE
□ Tagging / recherche → Facettes + Thésaurus
□ Validation avec utilisateurs → Card sorting d'abord

Construction
□ Max 4 niveaux de profondeur
□ Nommage MECE pour chaque niveau
□ Glossaire des termes de catégorisation créé
□ Convention de nommage des fichiers documentée
□ Processus d'archivage défini

Validation
□ Tester : "Où est X ?" avec 3 utilisateurs différents
□ Tester : "Où mettre Y ?" (un nouveau contenu)
□ Identifier les raccourcis utilisés spontanément
□ Réviser au bout de 3 mois d'usage réel
```

---

## Synthèse : quel framework pour quel besoin ?

| Besoin | Framework | Pourquoi |
|--------|-----------|---------|
| Structure une documentation produit/projet | **Diátaxis** | Séparation tutorial/how-to/ref/explication |
| Organise ses fichiers personnels | **PARA** | 4 catégories universelles, simple à maintenir |
| Range des dossiers d'équipe avec IDs | **Johnny Decimal** | Identifiants stables, retrouvabilité |
| Crée un système de tags cohérent | **Facettes + Thésaurus** | Multi-dimensionnel, sans ambiguïté |
| Vérifie la cohérence d'un niveau | **MECE** | Exclusivité + exhaustivité |
| Valide l'architecture avec les utilisateurs | **Card sorting** | Découvrir la logique mentale des lecteurs |
| Documente les relations complexes entre concepts | **Ontologie** | Au-delà de la hiérarchie simple |

---

## Références

- Morville, P. & Rosenfeld, L. (1998). *Information Architecture for the World Wide Web*. O'Reilly.
- Ranganathan, S.R. (1933). *Colon Classification* — fondateur de la classification facettée
- Procida, D. (2021). *Diátaxis Documentation Framework* — diataxis.fr
- Forte, T. (2022). *Building a Second Brain*. Atria. — Méthode PARA
- Noble, J. (2019). *Johnny.Decimal* — johnnydecimal.com
- Nielsen, J. & Norman, D. — *NN/g Card Sorting* — nngroup.com
- Minto, B. (1987). *The Pyramid Principle* — McKinsey MECE
