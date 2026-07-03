
# Challenge Roborock — Méta-audit GED de l'écosystème Claude

> Roborock balaie la maison Claude : skills, agents, hooks, rules, memory, CLAUDE.md, .md transverses, configs. Détecte **ce qui n'est lié à rien ni personne** — les fichiers qu'on a écrits, qu'on a oubliés, et qui pourrissent dans un coin.
>
> **Mode** : audit pur. Aucune écriture, aucune suppression. Rapport structuré avec verdicts et actions priorisées. L'humain décide ensuite.


## Quand invoquer

- Fin de grosse session avant commit/push structurel
- L'utilisateur dit : "Roborock", "passe le Roborock", "nettoie la GED", "audite la connaissance", "fichiers orphelins", "y'a quoi qui sert plus", "knowledge rot"
- Après refactor d'agents/skills/hooks
- Avant un `/compact` important — pour s'assurer que la mémoire qui reste a du sens

## Quand NE PAS invoquer

- Audit de **code** → utiliser `cheikh` (flux JS, dépendances script, console.log)
- Audit **PMO sémantique fond** pôle B → utiliser `/pole-b-pmo-audit`
- Audit **PMO sémantique fond** jeu → utiliser `/pole-a-pmo-audit`
- Audit **forme** d'un pôle → utiliser `/pole-b-archiviste-audit` ou `/pole-a-archiviste-audit`

Roborock = **transverse écosystème Claude + GED projet**, pas substitut des audits métier.


## Périmètre par défaut

**Inclus :**
- `~/.claude/skills/**/*` — tous les skills user-level
- `~/.claude/agents/**/*` — tous les agents user-level
- `~/.claude/rules/**/*` — toutes les rules path-scoped
- `~/.claude/commands/**/*` — toutes les slash-commands
- `~/.claude/hooks/**/*` — hooks user-level
- `~/.claude/settings.json` + `settings.local.json`
- `<project>/.claude/**/*` — agents, hooks, settings projet
- `<project>/CLAUDE.md` (tous niveaux : racine + pôles)
- `<project>/memory/**/*.md` + auto-memory dans `~/.claude/projects/<projet>/memory/`
- `<project>/**/*.md` (sauf `_archive/`, `node_modules/`, `dist/`, `build/`, `.git/`)
- `<project>/**/*.{yml,yaml,json}` de config (frontmatters, manifests)

**Exclus par défaut :**
- Code source (`.ts`, `.js`, `.py`, `.html`, `.css`, etc.) — sauf si demandé explicitement
- `_archive/` (cadavres préservés volontairement)
- `node_modules/`, `dist/`, `build/`, `.git/`

L'utilisateur peut élargir : "Roborock + le code de `infra/bot/`" → étendre au scope demandé.


## Workflow général

Copie cette checklist en début d'audit et coche au fur et à mesure :

```
Audit Roborock — Progress
- [ ] Phase 0   : Inventaire (recensement brut)
- [ ] Phase 0bis: Refresh doc Anthropic (vérif règles à jour)
- [ ] Phase 1   : Frontmatters & métadonnées
- [ ] Phase 2   : Skills (discovery, doublons, jamais déclenchés)
- [ ] Phase 3   : Agents (refs croisées, fantômes)
- [ ] Phase 4   : Hooks & Rules (pointeurs cassés, scope mort)
- [ ] Phase 5   : CLAUDE.md & Memory (hiérarchie, knowledge rot)
- [ ] Phase 6   : Liens & refs croisées (.md transverses)
- [ ] Phase 6bis: Navigabilité / cartographie (atteignabilité ≤2 sauts, routage par pôle, tenants liés)
- [ ] Phase 7   : Orphelins (fichiers liés à rien)
- [ ] Phase 8   : Rapport final agrégé
```

**Règle d'or** : on s'arrête PAS à la première anomalie. On passe les 8 phases, on agrège, on priorise. C'est un balayage complet, pas un debug ciblé.


## Phase 0 — Inventaire

Recense la matière brute avant de juger. Pas d'opinion ici, juste compter.

```bash
# Skills user-level
find ~/.claude/skills -name "SKILL.md" 2>/dev/null | wc -l
# Agents user-level
find ~/.claude/agents -name "*.md" 2>/dev/null | wc -l
# Hooks
ls ~/.claude/hooks 2>/dev/null
# Rules
ls ~/.claude/rules 2>/dev/null
# Commands
find ~/.claude/commands -name "*.md" 2>/dev/null | wc -l
# Projet .claude
ls .claude/ 2>/dev/null
# CLAUDE.md du projet
find . -name "CLAUDE.md" -not -path "*/node_modules/*" -not -path "*/_archive/*" 2>/dev/null
# Memory
ls memory/ 2>/dev/null
find ~/.claude/projects -name "MEMORY.md" 2>/dev/null
```

Produire un tableau récap :

| Catégorie | Nombre | Plus ancien (mtime) | Plus récent |
|-----------|--------|--------------------|--------------| 
| Skills user | X | date | date |
| Agents user | X | date | date |
| Rules | X | date | date |
| Commands | X | date | date |
| Hooks | X | date | date |
| CLAUDE.md projet | X | - | - |
| Memory .md | X | date | date |

Ce tableau est le **point zéro**. Tout le reste s'y rattache.


## Phase 0bis — Refresh doc Anthropic

Voir [refresh-doc.md](refresh-doc.md) pour la liste exhaustive des URLs et la méthode de diff.

**Pourquoi** : les règles Anthropic (frontmatter SKILL.md, structure agents, conventions hooks, format memory) évoluent. Les `` de Roborock sont gravés à la création — sans refresh, l'audit utilise des règles potentiellement périmées.

**Méthode rapide** :
1. WebFetch sur 4 URLs canoniques (voir `refresh-doc.md`)
2. Extraire les contraintes actuelles (limites chars, regex name, mots réservés, structure dossiers)
3. Comparer avec ce que disent les `checks-*.md` locaux
4. Si divergence détectée → ⚠️ ajouter au rapport "Phase 0bis — règles locales à mettre à jour" + proposer le diff

**Important** :
- Si WebFetch échoue (réseau, URL changée) → ⚠️ "doc Anthropic non rafraîchie ce run, audit avec règles locales" — ne PAS bloquer l'audit
- Ne PAS modifier les `` sans validation explicite de l'utilisateur


## Phase 1 — Frontmatters & métadonnées

Voir [checks-frontmatters.md](checks-frontmatters.md) pour la grille détaillée.

**Check rapide :**
- Tout `SKILL.md` a-t-il `name` + `description` valides ? (cf. règles Anthropic : name ≤ 64 chars, lowercase + hyphens, description ≤ 1024 chars, third person)
- Tout agent `.claude/agents/*.md` a-t-il un frontmatter valide ? **Pas de `:` interne non quoté, pas d'em-dash `—`, pas de `×`** (sinon agent rejeté silencieusement par le harness — cf. `feedback_agent_frontmatter.md` en memory).


## Phase 2 — Skills

Voir [checks-skills.md](checks-skills.md).

**Checks clés :**
- Doublons sémantiques (deux skills qui font ~la même chose → lequel survit ?)
- Descriptions vagues / non-actionnables (ne déclencheront jamais)
- Skills jamais référencés ni invoqués (vérifier git log + transcripts)
- Skills avec `` ou `scripts/` dont les fichiers cités sont absents


## Phase 3 — Agents

Voir [checks-agents.md](checks-agents.md).

**Checks clés :**
- Frontmatter strict (incident connu : `:` interne dans description → rejet silencieux)
- Agents référencés dans CLAUDE.md / autres agents mais inexistants
- Agents existants jamais référencés nulle part (orphelins)
- Parent/enfant cohérent (pole-a-pmo → pole-a-tile-pmo, etc.)


## Phase 4 — Hooks & Rules

Voir [checks-hooks-rules.md](checks-hooks-rules.md).

**Checks clés :**
- `settings.json` → hooks pointent vers scripts existants ?
- Rules path-scoped (`rules/*.md` avec champ `applies-to`) → le path existe-t-il dans un projet ?
- Hooks qui n'ont jamais loggé (jamais déclenchés en pratique)


## Phase 5 — CLAUDE.md & Memory

Voir [checks-claude-memory.md](checks-claude-memory.md).

**Checks clés :**
- Hiérarchie CLAUDE.md (racine légère, pôles auto-loadés) → racine < 100 lignes ?
- `MEMORY.md` index → tous les `*.md` cités existent-ils ?
- Memory files orphelins (présents dans le dossier mais pas indexés dans MEMORY.md)
- Knowledge rot : dates absolues > 3 mois sans confirmation, "TODO en attente droits" jamais traités


## Phase 6 — Liens & refs croisées

Voir [checks-links.md](checks-links.md).

**Checks clés :**
- Tous les liens markdown `[texte](chemin)` relatifs pointent vers un fichier qui existe
- Toute mention `[\`pole-a-pmo\`](.claude/agents/pole-a-pmo.md)` → fichier présent ?
- INDEX.md des pôles → cohérent avec contenu du sous-arbre ?

```bash
# Tous les liens .md relatifs (hors http)
grep -rn '\[.*\](.*\.md)' --include="*.md" . 2>/dev/null | grep -v "http"
```

### Phase 6bis — Navigabilité / cartographie (« peut-on trouver l'info depuis n'importe où ? »)

Au-delà des liens cassés (refs qui existent), vérifier que la **carte est complète** : depuis un point d'entrée, Claude peut-il atteindre chaque source-de-vérité, et chaque pôle sait-il router une question ?

- **Atteignabilité racine** : depuis le `CLAUDE.md` racine, chaque pôle est-il atteignable en **≤ 2 sauts** (racine → pôle/CLAUDE.md → INDEX/source) ? Un pôle ou un domaine déployé non cité dans le routage racine = **trou de cartographie** (HAUTE).
- **Table de routage par pôle** : chaque `<pôle>/CLAUDE.md` a-t-il une table « quelle question → quel fichier source » (ou une section « source de vérité ») ? Un pôle sans table de routage = navigation aveugle (MOYENNE).
- **Tenants déployés ailleurs** : un domaine dont le code vit hors de son dossier (ex : pôle dont les fichiers sont déployés dans un autre pôle) est-il **lié par une rule path-scoped** + signalé dans le CLAUDE.md hôte ? Sinon, quelqu'un qui édite ce code ne charge pas les bonnes règles (HAUTE).
- **Réciprocité des pointeurs** : si A pointe vers B comme « pôle voisin / consommateur / hôte », B pointe-t-il en retour ? Pointeur unidirectionnel = angle mort (BASSE).
- **Index ⇄ réalité** : chaque source-de-vérité majeure (INVARIANTS, decisions, figées) est-elle listée dans l'INDEX de son pôle ? Fichier de vérité non indexé = introuvable sauf à le connaître (MOYENNE).

But : garantir qu'un agent qui démarre **n'importe où** (n'importe quel fichier touché) sait, en peu de sauts, où trouver l'info ou quel fichier la détient. On ne surcharge pas les fichiers — on vérifie juste que les **pointeurs structurants** (routage racine, table par pôle, rules path-scoped, INDEX) existent et sont réciproques.


## Phase 7 — Orphelins

Voir [checks-orphans.md](checks-orphans.md).

**Définition orphelin** : fichier qui n'est référencé par **aucun** autre fichier du périmètre, ET qui n'est pas un point d'entrée canonique (CLAUDE.md, MEMORY.md, INDEX.md, SKILL.md).

```bash
# Pour chaque .md, vérifier qu'il est cité quelque part
# Pseudo-algorithme :
# 1. Lister tous les .md du périmètre → liste L
# 2. Pour chaque fichier f de L, compter combien de fichiers du périmètre le mentionnent (par nom)
# 3. Si count == 0 ET f n'est pas un point d'entrée → ORPHELIN
```

Verdict par orphelin :
- ❓ **À qualifier** : peut-être brouillon en cours → demander
- 🟡 **Candidat archive** : utile historiquement, déplacer vers `_archive/`
- 🔴 **À supprimer** : duplicate ou erreur

⚠️ **JAMAIS supprimer pendant l'audit**. Reporter seulement.


## Phase 8 — Rapport final

Voir [report-template.md](report-template.md) pour le gabarit complet.

**Après le rapport** : Roborock n'applique rien (audit pur). Pour transformer le rapport validé en actions concrètes (suppression, archivage), voir [application.md](application.md).

Structure agrégée :

```
# Rapport Roborock — [date ISO]
## Périmètre
- Inclus : ...
- Exclus : ...

## Synthèse
- X items audités
- Y anomalies (Z CRITIQUES, A HAUTES, B MOYENNES, C BASSES)
- D orphelins candidats

## Détail par phase
[bloc par phase 1-7 avec verdicts ✅/⚠️/❌]

## TOP 5 actions prioritaires
1. [CRITIQUE] ...
2. [CRITIQUE] ...
3. [HAUTE] ...
4. [HAUTE] ...
5. [MOYENNE] ...

## Annexe : liste complète orphelins
- file1.md (jamais référencé, dernière modif YYYY-MM-DD)
- ...
```


## Niveaux de sévérité

| Niveau | Critère | Exemples |
|--------|---------|----------|
| 🔴 CRITIQUE | Casse silencieuse en prod (agent rejeté, hook mort, ref pétée) | Frontmatter agent invalide, hook pointe vers script absent |
| 🟠 HAUTE | Information fausse ou trompeuse activement utilisée | MEMORY.md cite fichier inexistant, INDEX.md décalé |
| 🟡 MOYENNE | Friction modérée, à corriger sans urgence | Skill description vague, doublon sémantique |
| 🟢 BASSE | Cosmétique ou dette future | Fichier orphelin probable mais peut-être brouillon |

### Grille de décision — écart aux normes (pas juste orphelins)

Avant de classer un écart CRITIQUE/HAUTE/MOYENNE/BASSE, poser 3 questions (évite le jugement subjectif) :

1. **Ça fonctionne ?** Si oui, l'écart peut être un détail.
2. **Y a-t-il une raison qui le justifie ?** Contrainte, héritage, choix conscient documenté.
3. **Le coût de l'écart dépasse-t-il son bénéfice ?** Friction, dette, risque.

| (1) Fonctionne | (2) Justifié | (3) Coût > bénéfice | Verdict |
|---|---|---|---|
| oui | oui | non | **Toléré** — mention informative seulement |
| oui | non | non | **BASSE/MOYENNE** — suggérer, ne pas imposer |
| non | — | — | **HAUTE/CRITIQUE** — argumenter le changement |
| — | — | oui | **HAUTE/CRITIQUE** — argumenter le changement |

Toujours argumenter avec l'impact attendu, jamais imposer.

### Triage des orphelins (avant de reporter en Phase 7)

Ne pas se contenter de "orphelin, à qualifier" — trier en 3 catégories pour que la décision d'application (voir `application.md`) soit immédiate :

| Catégorie | Définition | Exemple |
|---|---|---|
| **Trace temporaire** | Run avorté, draft jetable, sans valeur de rétention | `tmp_*`, brouillon de session |
| **Archive volontaire** | Utile historiquement, à garder mais hors circuit actif | Version figée, exemple de référence |
| **Orphelin d'itération** | Était utilisé avant, refactor en cours, à arbitrer | Ancien skill remplacé, référence pas encore migrée |

Décision **par catégorie, jamais en bloc** — voir `application.md` pour le protocole complet une fois le rapport validé.


## Anti-patterns Roborock

- ❌ **Ne JAMAIS corriger pendant l'audit.** Rapport seul. La correction est un autre acte, qui demande validation explicite.
- ❌ **Ne pas s'arrêter à la première anomalie.** Balayage complet, puis priorisation.
- ❌ **Ne pas faire de jugement subjectif** ("ce nom est moche") — seulement des faits vérifiables (frontmatter invalide, lien cassé, fichier non référencé).
- ❌ **Ne pas appeler un fichier "orphelin" sans vérifier les transcripts/git log récents.** Un fichier créé hier ET non encore référencé peut être un WIP légitime → marquer ❓ "à qualifier", pas 🔴.

## Patterns à suivre

- ✅ Toujours commencer par Phase 0 (inventaire). Tu ne peux pas auditer ce que tu n'as pas compté.
- ✅ Vérifier les feedbacks memory pertinents avant verdict (ex : `feedback_agent_frontmatter.md` est la source de vérité pour Phase 1 agents).
- ✅ Croiser plusieurs sources : un agent listé dans CLAUDE.md mais absent du dossier `.claude/agents/` → CRITIQUE. Un agent présent mais cité nulle part → orphelin candidat.
- ✅ Garder le rapport actionnable : chaque ❌ ou ⚠️ doit avoir une action proposée concrète.


## Extension : code à la demande

Par défaut, Roborock ignore le code. Si l'utilisateur dit "et le code aussi" ou "étend au code de X" :
1. Ajouter le scope au périmètre Phase 0
2. Lancer `cheikh` en parallèle (skill code/projet) plutôt que dupliquer ses checks
3. Agréger les deux rapports dans la synthèse finale


_Skill créé 2026-05-12. Méthode conforme [Anthropic Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) (progressive disclosure, body < 500 lignes, refs one-level-deep)._
