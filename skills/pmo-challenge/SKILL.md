---
name: pmo-challenge
description: Auditer et challenger un système multi-agent / PMO existant. Méthodologie en 6 étapes - cartographie, liens cassés, obsolescence, simulation de scénarios, top risques, recommandations actionnables. Produit un rapport structuré avec priorisation CRITIQUE/HAUTE/MOYENNE/BASSE. Skill jumeau de `pmo-design` (conception). À utiliser quand l'utilisateur dit "fais le tour", "audite", "rien d'obsolète ?", "tout est clair ?".
---

# PMO Challenge — Audit d'un système multi-agent existant

> Skill jumeau de [`pmo-design`](../pmo-design/SKILL.md) (conception). Ici on **audite**, on **challenge**, on **simule**. On ne crée pas.

## Quand utiliser ce skill

Triggers utilisateur typiques :
- *"Fais un audit complet de [pôle X]"*
- *"Fais le tour de l'existant, rien d'obsolète ?"*
- *"Si je rentre avec une nouvelle question / un nouveau besoin, ça tient ?"*
- *"Simule ce qui se passe quand on veut faire X"*
- *"Tu as des challenges à transmettre pour l'agent Y ?"*
- *"Vérifie la cohérence des liens, INDEX, agents, scripts"*
- Avant une refonte / un commit important / un changement de PROCESS

**Antipattern** : ne pas utiliser pour challenger une décision business / créative. Ce skill challenge la **forme**, la **cohérence**, la **complétude** — pas le fond éditorial.

---

## Principe fondamental

Un audit utile **simule** l'usage réel. Lister "INDEX présent, agent défini" ne suffit pas — il faut **tester** :

> *Si demain matin un nouvel utilisateur arrive avec [scénario X], est-ce que le système le route correctement, sans lien cassé, sans agent obsolète, sans étape floue ?*

Si la réponse n'est pas un **OUI factuel avec chemins exacts**, c'est une zone à challenger.

---

## 🧭 Méthodologie en 6 étapes

### Étape 1 — Cartographie inventaire

Objectif : **savoir ce qui existe** avant de juger.

Actions :
- Lister tous les sous-dossiers du pôle audité (ex : un dossier par sous-domaine)
- Pour chaque sous-dossier : compter les fichiers, lire l'INDEX s'il existe
- Lister tous les agents `.claude/agents/*.md` du pôle
- Lister les scripts CLI (`scripts/`)
- Lister les templates / gabarits

Output partiel : table "fichiers par sous-dossier" + "dernière mise à jour INDEX".

### Étape 2 — Détection des liens cassés (CRITIQUE)

Objectif : **traquer** les références mortes.

Actions :
- Pour chaque INDEX : lister les fichiers cités → vérifier qu'ils existent sur disque
- Pour chaque agent : lister les fichiers cités dans "Première action OBLIGATOIRE" ou "Lis dans l'ordre" → vérifier existence
- Pour chaque PROCESS / ORGANIGRAMME : lister les agents cités → vérifier qu'ils existent dans `.claude/agents/`
- Pour chaque CLAUDE.md / racine : vérifier que tous les liens markdown pointent vers des fichiers réels

**Format issue** :
```
[CASSÉ] <fichier source> ligne N → référence <chemin cible> qui n'existe pas
Correctif suggéré : <chemin réel> ou archiver la référence
```

### Étape 3 — Détection d'obsolescence

Objectif : **traquer** ce qui parle d'un état précédent du système.

Actions :
- Chercher les mentions de versions anciennes (ex : "PROCESS 9 étapes" alors qu'on est passé à 11)
- Chercher les références à des agents supprimés / renommés
- Chercher les dates "dernière mise à jour" > 1 mois
- Chercher les dossiers / concepts supprimés mentionnés ailleurs (ex : `workshop/` supprimé mais cité dans un agent)

**Patterns à grep** :
```bash
# Mentions de chiffres "X étapes" pour repérer désalignement
grep -rn "[0-9]+ étapes" <pôle>
# Mentions d'anciens noms de dossiers
grep -rn "workshop\|deprecated\|old-" <pôle>
# Mentions d'agents par nom (vérifier qu'ils existent)
grep -rn "pole-a-\|pole-b-" <pôle> --include="*.md"
```

### Étape 4 — Simulation de scénarios utilisateur

Objectif : **valider** que les workflows usuels fonctionnent.

Identifier 3-5 scénarios canoniques selon le domaine. Exemples génériques :

| Type de scénario | Question à poser |
|---|---|
| **Entrée nouvelle idée / besoin** | "User arrive avec idée brute → où va l'idée ? Quel agent prend la main ? Quel fichier reçoit ?" |
| **Question/recherche** | "User demande X → quel agent répond ? Quels fichiers sont lus ?" |
| **Production d'un livrable** | "Lance le livrable Y → quel agent ? Quels prérequis ? Quel format de sortie ?" |
| **Variante/extension** | "Décline le livrable Z pour cible Q → quel agent ? Quels prérequis ?" |
| **Reboot après compact** | "Nouvelle session, main agent froid → quels fichiers lire pour reconstituer le contexte ?" |

Pour chaque scénario, statut **CLAIR / FLOU / CASSÉ** + justification factuelle (chemins, agents).

### Étape 5 — Top risques priorisés

Objectif : **classer** ce qui doit être fixé.

Grille de priorisation :

| Niveau | Critère | Action attendue |
|---|---|---|
| **CRITIQUE** | Bloque un scénario user (agent plante, fichier manquant en lecture obligatoire) | Fix immédiat (minutes) |
| **HAUTE** | Désaligne agents entre eux (PROCESS, INDEX, ORGANIGRAMME divergent) | Fix dans la session |
| **MOYENNE** | Confusion possible mais workaround existe | Fix planifié |
| **BASSE** | Cosmétique / dates / formulations | À acter quand on passe par là |

### Étape 6 — Recommandations concrètes

Objectif : **livrer** ce que l'utilisateur peut décider/exécuter.

Pour chaque recommandation :
- **Action précise** (avec chemins exacts, lignes à modifier)
- **Effort estimé** (minutes / heures)
- **Bloquant** (oui/non — bloque-t-il un scénario user ?)
- **Décideur** (toi peux fixer / décision auteur requise)

**Antipattern à éviter** : "il faudrait améliorer X" → trop vague. Préférer "remplacer ligne N de fichier F par Z, 5 min, non-bloquant".

---

## 📝 Format de rapport OBLIGATOIRE

```markdown
# AUDIT [pôle] — [date]

## A. CARTOGRAPHIE — état général
- Fichiers par sous-dossier : <table>
- Dernière mise à jour des INDEX : <table>
- Total : N fichiers

## B. LIENS CASSÉS (critique)
| Fichier source | Ligne | Référence cassée | Correctif suggéré |
|---|---|---|---|
| ... | ... | ... | ... |

## C. OBSOLESCENCE
- Mentions anciennes versions : <liste>
- Agents supprimés cités : <liste>
- Dossiers/concepts disparus mentionnés : <liste>
- Dates "dernière maj" > 1 mois : <liste>

## D. SIMULATION DES N SCÉNARIOS USER
Pour chaque scénario : CLAIR / FLOU / CASSÉ + détail factuel
1. <scénario 1>
2. <scénario 2>
...

## E. TOP 5 RISQUES (priorisés)
1. [CRITIQUE] <risque> — <cause> — <impact> — <priorisation>
2. [HAUTE] ...
...

## F. RECOMMANDATIONS CONCRÈTES
| # | Action | Effort | Bloquant | Décideur |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Résumé exécutif (3-5 lignes)
État général + actions urgentes avant prochaine session.
```

---

## 🛠️ Outils efficaces

### Délégation à l'agent Explore
Pour un audit large (> 30 fichiers à parcourir), déléguer à l'agent `Explore` (read-only, contexte protégé) avec un prompt structuré :

```
Audit [pôle X]. Lis : <liste fichiers clés>. Vérifie : <liste checks>.
Simule scénarios : <liste>. Rapport sous N mots, format <template>.
NE MODIFIE RIEN.
```

Avantages : économise le contexte du main agent, peut paralléliser plusieurs lectures.

### Grep ciblés
```bash
# Liens markdown vers fichiers
grep -rn "\]\\(\\.\\./" <pôle> --include="*.md"
# Mentions d'un agent
grep -rn "pole-b-pmo\|pole-a-tile-pmo" <pôle>
# Mentions de chiffres pour repérer désalignement
grep -rn "[0-9]\+ étapes\|[0-9]\+ catégories" <pôle>
```

### Glob structurel
```bash
# Lister tous les INDEX
glob "<pôle>/**/INDEX.md"
# Lister tous les agents
glob ".claude/agents/*.md"
```

---

## ❌ Anti-patterns à fuir

1. **Audit superficiel "tout va bien"** — sans avoir simulé au moins 3 scénarios user, on ne sait pas si ça tient
2. **Recommandation floue** — "il faudrait améliorer la doc" ne vaut rien. Préférer "remplacer ligne N par Z"
3. **Liste exhaustive sans priorisation** — 50 issues non priorisées = paralysie. CRITIQUE/HAUTE/MOYENNE/BASSE obligatoire
4. **Audit sans cartographie préalable** — sauter à "il manque ça" sans avoir compté ce qui existe = jugement biaisé
5. **Audit qui modifie** — un audit est en **lecture seule**. Les fixes viennent APRÈS, sur GO utilisateur
6. **Audit en isolation** — ne pas vérifier les références cross-pôles (ex : un pôle cite un autre, ou inversement)
7. **Recommandation hors scope utilisateur** — si user demande audit d'un pôle, ne pas dériver vers refonte de l'archi globale
8. **Confondre audit forme vs fond** — pmo-challenge audite la **cohérence/complétude**, pas la qualité éditoriale (c'est le rôle de Directeur / pole-b-conseiller / etc.)
9. **Auditer sans lire le fichier complètement** — pour un audit ciblé d'un agent/PMO, faire un `Read` complet **avant** de proposer un challenge "il manque X". Sinon risque réel de proposer du déjà fait (cas vécu : checklist déjà implémentée, fichier lu partiellement).
10. **Relayer un ticket BACKLOG comme bug actif sans vérifier le code** — un ticket EP-xxx peut être "ouvert" dans le sommaire mais le code peut déjà être conforme (désync sommaire↔détail). Toujours **lire le code** correspondant avant de classer en CRITIQUE/HAUTE. Risque de "bugs fantômes" qui font perdre du temps (cas vécu : des sous-tâches implémentées dans le code mais jamais cochées dans le backlog → l'audit les a relayées comme bugs actifs ; vérification ultérieure a révélé qu'elles étaient déjà résolues).

---

## ⏱️ Quand pmo-challenge VS code-reviewer

| Skill | Scope | Output |
|---|---|---|
| `pmo-challenge` | Système multi-agent (workflows, INDEX, PROCESS, agents) | Rapport d'audit structure |
| `code-reviewer` (agent) | Code source (qualité, sécurité, maintenabilité) | Rapport de revue code |
| `cheikh` (skill) | Projet entier (docs, liens, deps obsolètes, fichiers orphelins) | Audit projet global |

**Règle** : si ton audit porte sur du **markdown / agents / PROCESS / INDEX**, c'est `pmo-challenge`. Si c'est du **code**, c'est `code-reviewer`. Si c'est **tout** (incluant deps npm, .gitignore, build), c'est `cheikh`.

---

## 🔄 Boucle d'apprentissage avec pmo-design

Quand pmo-challenge détecte un pattern récurrent (ex : "3 audits sur 3 ont trouvé un INDEX non daté"), c'est un signal :
- Mettre à jour le **template** dans `pmo-design` (ex : ajouter "date obligatoire en en-tête d'INDEX")
- Documenter dans `PIPELINE-MEMORY.md` du projet la friction et la résolution

**Les deux skills s'enrichissent mutuellement** :
- `pmo-design` formalise les bonnes pratiques de conception
- `pmo-challenge` détecte les écarts et alimente `pmo-design` en cas de pattern récurrent

---

## 🔁 Audit réciproque entre PMO (pattern validé)

Quand un système a **plusieurs PMO** (un par pôle, ex : `pole-a-pmo` + `pole-b-pmo`), une boucle d'amélioration puissante consiste à **les faire s'auditer mutuellement** sans pollution de scope.

### Protocole "challenge réciproque"

1. **Main agent** vient d'enrichir le PMO A après une refonte / amélioration
2. **Main agent** liste 5-7 observations comparatives entre PMO A (frais) et PMO B (en place) — forme + fond
3. **Main agent** transmet ces observations à PMO B (via Agent tool, avec contexte précis)
4. **PMO B** trie et répond :
   - **Décliné** : déjà implémenté (l'auditeur a mal lu → leçon à graver)
   - **Reporté** : pas critique pour son scope
   - **Traité plus léger** : intégration partielle, sans créer de nouveau fichier si déjà couvert
   - **Patché** : modification directe de sa fiche pour appliquer la suggestion
   - **Question ouverte** : à débattre plus tard (ex : sous-spécialisation future)
5. **PMO B** peut renvoyer un engagement réciproque : *"À charge de revanche, ping-moi à ta prochaine évolution"*
6. **Main agent** grave le verdict dans le PIPELINE-MEMORY du PMO A et dans les études de cas

### Pourquoi c'est puissant

- **Pas de pollution de scope** : aucun PMO ne modifie l'autre, ils s'envoient des suggestions
- **Asymétrie utile** : PMO B voit dans PMO A des trucs que PMO A ne voit pas en lui-même (et vice-versa)
- **Engagement long terme** : transformer l'audit ponctuel en boucle continue d'amélioration mutuelle

### Anti-patterns spécifiques au réciproque

- **Proposer sans avoir lu le fichier en entier** → risque "déjà fait" (cas vécu). Toujours `Read` complet du PMO audité avant.
- **Insister sur un point refusé** → l'autre PMO a son contexte, son verdict prime
- **Auditer dans le même tour qu'une refonte** → laisser le PMO B finir sa session courante avant le challenge

### Exemple concret

```
PMO A refondu (hiérarchique) → main agent transmet 7 challenges à PMO B
                              ↓
PMO B répond : 5/7 retenus, 1 décliné (déjà fait — leçon), 1 reporté
                              ↓
PMO B engage : "ping-moi à ta prochaine évolution pour la réciproque"
                              ↓
main agent grave l'engagement dans le PIPELINE-MEMORY § 7
```

---

## 📚 Études de cas

### Audit d'un pôle (illustration)
- **Trigger** : *"audite tous les process et liens de ce pôle"*
- **Méthode** : 6 étapes, recherche déléguée à un sous-agent Explore
- **Découvertes typiques** : liens cassés CRITIQUE (refs vers fichiers déplacés), scénarios simulés dont certains bloqués, dette de contexte reportée
- **Résultat** : fixes appliqués rapidement, scénarios redébloqués

### Challenge ciblé d'un PMO (boucle réciproque)
- **Méthode** : mini-audit ciblé (étapes 2-3-5) sur l'agent seul
- **Verdict** : sur 7 challenges → 5 retenus, 1 décliné (déjà implémenté = **leçon : lire le fichier en entier avant de challenger**), 1 reporté, le reste patché/léger
- **Pattern identifié** : voir "Audit réciproque entre PMO" ci-dessus

---

## 🧭 Mnémonique

> **Un audit qui ne simule pas l'usage n'est pas un audit, c'est une lecture.**
>
> **Cartographier → traquer les cassés → traquer l'obsolète → simuler → prioriser → recommander concret.**
