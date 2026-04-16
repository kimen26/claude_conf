---
name: cheikh
description: "Outil complet d'audit, conception et optimisation de process IA. Utilise ce skill dès que l'utilisateur veut : (1) AUDITER un process existant — 'challenge le process', 'vérifie la cohérence', 'audit', 'check', 'y a des trous ?', contradictions, doublons, REX obsolètes ; (2) CONCEVOIR un nouveau process — 'setup', 'init', 'configure', 'nouveau projet', 'crée l'architecture', 'comment organiser mes dossiers', bootstrap, installer un pipeline ; (3) OPTIMISER après un run — 'pourquoi on a raté ?', 'compare avec l'exemple humain', 'améliore les règles', 'post-mortem', 'rex', 'optimise'. Couvre tout le cycle de vie d'un process IA : création → exécution → analyse → amélioration → audit."
---

# Cheikh — Audit, Architecture & Optimisation de Process IA

Cheikh est ton conseiller process. Il intervient sur **3 modes** :

| Mode | Quand | Ce qu'il fait |
|------|-------|---------------|
| **Sentinelle** | "challenge", "audit", "vérifie" | Scanne tout, détecte les problèmes, ne touche à rien |
| **Architecte** | "setup", "init", "nouveau projet" | Installe un process adapté — minimaliste d'abord |
| **Stratège** | "pourquoi raté ?", "améliore", "compare" | Analyse un run réel, optimise les règles |

Le cycle naturel : **Architecte** crée → tu fais un run → **Stratège** analyse → **Sentinelle** vérifie → boucle.

---

## MODE ARCHITECTE — Setup & Design

L'Architecte observe d'abord, installe ensuite. Il ne crée jamais de structure complexe avant de savoir si la complexité est justifiée.

### Étape 1 — Observation silencieuse

Scanner ce qui existe déjà sans rien dire à l'utilisateur :

1. `ls -R` pour voir l'arborescence complète
2. Lire les fichiers présents (exemples, règles, inputs existants)
3. S'il y a un exemple input ET output : comparer automatiquement pour déduire les transformations
4. Détecter l'existant : y a-t-il déjà un `CLAUDE.md` ? Un `.claude/` ? Si oui, enrichir, ne pas repartir de zéro.

**Sur les dossiers Input/Output** : ne jamais les créer si des fichiers ou dossiers de travail existent déjà à la racine. L'utilisateur a peut-être `Data/`, `Résultats/`, `Fichiers/` — ce sont ses Input/Output de fait. Les adopter tels quels, les renommer seulement si l'utilisateur le demande explicitement. Créer `Input/` et `Output/` uniquement si le dossier est vide ou sans structure apparente.

Produire mentalement un rapport d'observation : type de fichiers, volumétrie, complexité estimée, hypothèses sur le besoin, **noms des dossiers existants à conserver**.

### Étape 2 — Une seule question d'abord

Avant toute installation, poser **une seule question** :

> "J'ai exploré ton dossier. Je peux installer une base légère en silence (CLAUDE.md + structure minimale) et tu affines au fur et à mesure, ou on construit ensemble maintenant. Tu préfères quoi ?"

- **Base légère** → installer silencieusement, livrer un résumé de ce qui a été créé
- **Affiner ensemble** → passer à l'interview (Étape 3)

Ne poser d'autres questions que si l'observation n'a pas suffi à répondre.

### Étape 3 — Interview ciblée (si l'utilisateur veut affiner)

Seulement les questions dont l'observation n'a pas donné la réponse. Maximum 4 questions, en conversation — pas un formulaire.

Focus : intention métier, fréquence d'usage, niveau technique de l'utilisateur, priorités.

### Étape 4 — Proposition (si affinage)

Montrer le schéma **avant** d'installer quoi que ce soit :

```
PHASE 1 (nom) → PHASE 2 (nom) → OUTPUT
```

Pour chaque phase : ce qu'elle fait, qui l'exécute (LLM ou code), entrée/sortie.

Attendre la validation. C'est le moment le moins cher pour changer d'avis.

### Étape 5 — Installation

#### Structure minimale (base légère ou projet simple)

```
projet/
├── CLAUDE.md               ← Instructions permanentes (<200 lignes)
├── Input/                  ← Fichiers à traiter (jamais modifiés)
└── Output/                 ← Livrables finaux
```

Ajouter `.claude/` seulement si la complexité le justifie :

```
.claude/
├── rules/
│   ├── lessons.md          ← Règles extraites des erreurs (validées par toi)
│   └── [domaine].md        ← Règles métier par domaine si nécessaire
├── memory/
│   ├── MEMORY.md           ← Index vivant : todo, plans actifs, état du projet
│   └── [topic].md          ← Notes détaillées chargées à la demande
└── skills/
    └── [nom-skill]/
        ├── SKILL.md        ← Orchestrateur du workflow
        └── scripts/        ← Code Python/bash (exécuté, pas lu par le LLM)
```

> **Pourquoi cette structure ?** Elle suit les conventions officielles Claude Code :
> - `CLAUDE.md` = instructions permanentes lues à chaque session
> - `.claude/rules/` = règles modulaires, chargées selon le contexte
> - `.claude/memory/` = état vivant du projet, mis à jour par Claude au fil des sessions
> - `scripts/` = code exécutable séparé du contexte LLM

#### CLAUDE.md installé par défaut

Utiliser le template bundlé dans `assets/CLAUDE.md.template` — copier son contenu et remplacer les `[placeholders]` par les informations du projet observées à l'étape 1. Ne pas régénérer le template de zéro à chaque fois.

#### MEMORY.md installé par défaut

```markdown
# Mémoire du projet [Nom]

## En cours
- [ ] [Tâche active]

## Plans actifs
[Rien pour l'instant]

## État du projet
[Initialisation]

## Notes
[Vide — Claude enrichit au fil des sessions]
```

> **Important sur la mémoire** : Claude met à jour ce fichier activement. Il ajoute ce qui est pertinent, supprime ce qui est obsolète. Une mémoire qui grossit sans être élaguée devient du bruit.

#### lessons.md installé par défaut (si `.claude/rules/` créé)

```markdown
# Leçons apprises

## Format
**Erreur rencontrée** : [décrire ce qui s'est mal passé]
**Règle** : [la règle qui l'évite à l'avenir]

## Exemple
**Erreur** : Le LLM a ignoré une règle au milieu d'un prompt de 3000 mots
**Règle** : Garder chaque agent sous 2000 mots de contexte. Découper si nécessaire.
```

### Étape 6 — Vérification post-installation

Passer rapidement en **mode Sentinelle** sur ce qu'on vient de créer :
- Tous les fichiers référencés existent ?
- CLAUDE.md < 200 lignes ?
- La structure est cohérente avec la complexité du projet ?

Livrer un résumé de 3-5 lignes de ce qui a été installé et pourquoi.

---

## MODE SENTINELLE — Audit & Challenge

Tu veux vérifier qu'un process existant tient la route. Sentinelle lit tout sans rien modifier.

### Étape 1 — Cartographie complète

**Lire CHAQUE fichier EN ENTIER.** Un audit partiel est un audit faux.

Ordre de lecture :
1. `CLAUDE.md` à la racine — c'est l'index
2. `.claude/rules/` — les règles actives
3. `.claude/memory/MEMORY.md` — l'état courant
4. Les skills référencés (chaque `SKILL.md`, puis `scripts/`)
5. Les fichiers de données/passes utilisés par les skills

Pour chaque fichier noter : rôle, taille, fichiers référencés, **injecté dans un prompt LLM ou exécuté par du code**.

Produire un **tableau de l'écosystème** :

| Fichier | Rôle | Taille | Injection LLM ? | Référence |
|---------|------|--------|-----------------|-----------|

### Étape 2 — Mesure du budget cognitif (agents LLM uniquement)

Pour chaque agent LLM :
- Quels fichiers sont injectés dans son prompt ?
- Volume total estimé (mots)
- Budget cible : ~2000 mots idéal, 4000 max
- Signaler tout dépassement

> Le code exécutable (`scripts/`) ne compte PAS dans le budget cognitif — c'est Python, pas du contexte LLM. Un LLM qui reçoit 7 guides de 500 lignes dans un seul prompt va en rater la moitié.

### Étape 2b — Simulation du pipeline

Simuler le déroulement complet pour un fichier hypothétique :
1. Tracer chaque étape : quelle fonction appelée, quels fichiers lus/écrits
2. Vérifier que les signatures matchent entre orchestrateur et scripts
3. Vérifier que les formats de données matchent entre producteurs et consommateurs
4. Identifier les points de cassure silencieux

### Étape 3 — Audit croisé

| Cherche | Comment |
|---------|---------|
| **Contradictions** | Règle X dans fichier A contredit règle Y dans fichier B |
| **Doublons** | Même règle formulée différemment à 2 endroits |
| **Trous** | Règle présente dans la référence humaine mais absente des agents |
| **Orphelines** | Règle dans les agents sans source de référence |
| **Mémoire obsolète** | `.claude/memory/` contient des plans/todos terminés non nettoyés |
| **Lessons non appliquées** | `lessons.md` décrit une erreur qui se répète encore |
| **Liens cassés** | `CLAUDE.md` pointe vers un fichier qui n'existe pas |

Classer chaque problème : **CRITIQUE** (erreur en production), **IMPORTANT** (dégrade la qualité), **MINEUR** (cosmétique).

### Étape 4 — Découpage & orchestration

- Chaque phase a un scope clair ? Pas de chevauchement ?
- Les données passent correctement entre phases ?
- Ce qui est parallélisable est-il parallélisé ?
- La mémoire est-elle propre (pas de todos complétés non supprimés) ?

### Livrable

Rapport Markdown : carte écosystème → critiques → importants → mineurs → recommandations.

**Garde-fou absolu** : ne modifier AUCUN fichier. Citer fichier + ligne pour chaque problème.

---

## MODE STRATÈGE — Optimisation Continue

Tu as fait un run et tu veux analyser les résultats pour améliorer le prochain.

### Étape 1 — Collecter

1. Résultat produit par le pipeline
2. Référence attendue (correction humaine, output d'exemple)
3. Règles en vigueur au moment du run (`.claude/rules/`)
4. Logs (manifests, JSON corrections, erreurs)

### Étape 2 — Analyse différentielle

| Écart | Signification |
|-------|---------------|
| **Raté** | La référence corrige, le pipeline non |
| **Faux positif** | Le pipeline corrige, la référence non |
| **Divergence** | Les deux corrigent différemment |
| **Accord** | Même correction des deux côtés ✓ |

Pour chaque **raté**, identifier la cause racine :

| Cause | Action corrective |
|-------|-------------------|
| Règle absente | Rédiger et ajouter dans `.claude/rules/` |
| Règle enterrée | Remonter en priorité |
| Règle ambiguë | Reformuler avec exemples positifs ET négatifs |
| Budget cognitif dépassé | Découper l'agent ou réduire le contexte |
| Biais de prudence | Reformuler le garde-fou |
| Bug technique | Corriger le script dans `scripts/` |

### Étape 3 — Statistiques

- **Taux de détection** : corrections trouvées / total attendu
- **Taux de faux positifs** : corrections hors référence / total pipeline
- **Top 5 règles ratées** par fréquence
- **Distribution par cause racine**

### Étape 4 — Plan d'amélioration

Prioriser par **impact × fréquence**. Montrer les chiffres AVANT de proposer des changements.

### Étape 5 — Appliquer (si validé)

Mettre à jour `.claude/rules/`, les scripts dans `scripts/`, et `.claude/rules/lessons.md`.

**Ne jamais toucher aux fichiers de référence humaine** (ex: `_Regles/`, fichiers source).

Mettre à jour `.claude/memory/MEMORY.md` : marquer les tâches terminées, supprimer les plans obsolètes, noter les améliorations appliquées.

Recommander un re-run pour vérifier.

---

## Principes de conception (rappel pour tous les modes)

| Principe | Pourquoi |
|----------|----------|
| **Minimaliste d'abord** | Ne pas créer de structure pour une structure qui n'existera que sur le papier |
| **LLM = lecteur, code = exécuteur** | Le LLM lit et comprend. Les scripts appliquent. |
| **Budget cognitif ~2000 mots/agent** | Au-delà, la qualité chute. Découper plutôt que surcharger. |
| **Mémoire vivante** | `MEMORY.md` s'enrichit ET s'élague — une mémoire qui grossit indéfiniment devient du bruit |
| **Règles validées** | `lessons.md` ne contient que des patterns que l'utilisateur a confirmés |
| **CLAUDE.md < 200 lignes** | Au-delà, Claude commence à ignorer des instructions |

---

## Garde-fous communs

- **Sentinelle** ne modifie rien — lecture seule absolue
- **Architecte** pose LA question (léger ou affiner) AVANT d'installer
- **Stratège** montre les stats AVANT de modifier quoi que ce soit
- Toujours citer fichier + ligne pour chaque constat
- Expliquer POURQUOI c'est un problème, pas juste le lister
- Adapter le langage au niveau de l'utilisateur — ne pas supposer qu'il connaît "budget cognitif" ou "manifest JSON"
