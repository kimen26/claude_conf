---
name: challenge-local
description: "Wizard interactif d'audit et d'optimisation de la configuration Claude Code locale. Analyse l'état actuel (~/.claude/ + .claude/), pose un questionnaire de profil, explique les concepts clés, propose des améliorations ciblées et installe ce qui est validé. Multi-utilisateurs. Suivi des recommandations dans MEMORY.md."
version: "1.0.0"
author: "Yann Ponaire — Infopro Digital"
disable-model-invocation: true
tags: ["setup", "onboarding", "configuration", "audit", "claude-code"]
---

# SKILL : challenge-local

> **⚠️ Activation manuelle uniquement** — Lance `/challenge-local` pour démarrer.
> Ce skill ne se déclenche JAMAIS automatiquement.

---

## Vue d'ensemble

`challenge-local` est un wizard en 6 phases qui audite ta configuration Claude Code,
construit ton profil, et propose des optimisations adaptées — sans rien modifier sans
ta validation explicite.

Conçu pour être utilisé par Yann, mais fonctionne pour n'importe quel collègue.

> **Si tu n'utilises pas Claude Code CLI :** ce skill est optimisé pour Claude Code CLI
> (fichiers SKILL.md, agents/, rules/, settings.json). Sur Cursor / GitHub Copilot /
> Windsurf : les concepts sont portables mais les chemins d'installation diffèrent —
> adapte manuellement les recommandations à ton outil.

---

## Les 6 Phases

### PHASE 1 — AUDIT : État des lieux

**Objectif :** Cartographier ce qui existe déjà, sans rien modifier.

Actions :
1. Lire `~/.claude/settings.json` (config globale — modèle, env, hooks)
2. Lire `~/.claude/` → lister : skills/, agents/, rules/, commands/, CLAUDE.md
3. Lire `.claude/` du projet courant → lister : idem
4. Lire `~/.claude/projects/*/memory/` si présent (mémoire auto)
5. Lire le MEMORY.md du skill si présent (`~/.claude/skills/challenge-local/MEMORY.md`)
   → **Si MEMORY.md existe** : montrer le DELTA depuis la dernière session
     - Quels skills ont été ajoutés / supprimés
     - Quelle date de dernière exécution
     - Nouvelles recommandations non encore appliquées

Sortie attendue (format résumé) :
```
═══════════════════════════════════════════════════════
  ÉTAT ACTUEL DE TON ENVIRONNEMENT CLAUDE CODE
═══════════════════════════════════════════════════════
  ~./claude/
    Skills     : N (liste des noms)
    Agents     : N
    Rules      : N
    CLAUDE.md  : oui / non
  
  .claude/ (projet courant : NOM)
    Skills     : N
    Agents     : N
    Rules      : N
    Hooks      : N
    Settings   : oui / non
═══════════════════════════════════════════════════════
```

---

### PHASE 2 — QUESTIONNAIRE : Profil utilisateur

**Objectif :** Comprendre qui utilise Claude Code et comment, pour personnaliser les recommandations.

Si MEMORY.md existe et que le profil est déjà renseigné → proposer de le réutiliser ou de le mettre à jour.

Questions à poser (une par une, attendre la réponse) :

1. **Prénom et langue préférée ?** (ex : Yann, Français)
2. **Ton rôle principal ?**
   - [ ] Data Engineer / Analyste
   - [ ] Dev Backend / Fullstack
   - [ ] DevOps / Platform
   - [ ] Data Scientist / ML
   - [ ] PO / PM technique
   - [ ] Autre : ...
3. **Ton niveau de coding quotidien ?**
   - [ ] Peu (scripts, config, SQL)
   - [ ] Modéré (features, PRs)
   - [ ] Intensif (jour entier dans le code)
4. **Tes outils principaux ?** (cocher tout ce qui s'applique)
   - [ ] Python    [ ] TypeScript/JS    [ ] SQL
   - [ ] Snowflake [ ] n8n             [ ] Confluence/GitLab
   - [ ] Docker    [ ] Terraform       [ ] Autre : ...
5. **Type de projets principaux ?**
   - [ ] Data pipelines / ETL
   - [ ] APIs / Services
   - [ ] Automatisation / n8n
   - [ ] Analyse / BI
   - [ ] Infrastructure
   - [ ] Contenu / Documentation
6. **As-tu des contraintes réseau ?** (ex : proxy d'entreprise, Netskope, SSL)
7. **Format de réponse préféré ?**
   - [ ] Court et direct
   - [ ] Détaillé avec exemples
   - [ ] En français uniquement
   - [ ] Mix FR/EN selon le contexte

---

### PHASE 3 — EXPLICATION : Claude Code, c'est quoi ?

**Objectif :** Donner le contexte minimum pour que l'utilisateur comprenne ce qu'on va installer.

Adapter la profondeur selon le profil (débutant = plus d'exemples, expert = résumé).

Points clés à couvrir :

**1. Deux scopes de configuration**
```
~/.claude/          → Global (tous tes projets, ta machine)
  CLAUDE.md         → Tes préférences permanentes
  settings.json     → Modèle, env vars, hooks globaux
  skills/           → Bibliothèques de savoir réutilisables
  agents/           → Sous-agents spécialisés
  rules/            → Règles de comportement cross-projets

.claude/            → Projet (spécifique à un repo)
  CLAUDE.md         → Contexte du projet
  settings.json     → Surcharges projet (model, hooks)
  skills/           → Skills spécifiques au projet
  agents/           → Agents projet
  rules/            → Règles projet
```

**2. Skills vs Agents vs Rules**
| Type | Quand utiliser | Exemple |
|------|---------------|---------|
| **Skill** | Savoir métier ou technique | snowflake-snow-cli, impact |
| **Agent** | Tâche autonome déléguée | code-reviewer, planner |
| **Rule** | Comportement permanent | coding-style, security |

**3. Auto vs Manuel**
- **Auto** : Claude lit la `description:` et charge le skill quand les mots-clés matchent
- **Manuel** : `disable-model-invocation: true` → seulement via `/nom-du-skill`

**4. MEMORY.md** : ce skill enregistre ses recommandations pour suivre les deltas session après session.

---

### PHASE 4 — VEILLE : Quoi de neuf ?

**Objectif :** Détecter les évolutions de l'écosystème Claude Code depuis la dernière session.

Actions :
1. **Vérifier la date** dans MEMORY.md — depuis combien de temps ?
2. **Tenter de fetcher** (si connecté) :
   - `https://docs.anthropic.com/fr/docs/claude-code` → nouveautés CLI
   - `https://github.com/anthropics/claude-code/releases` → changelog
3. **Scanner le GitLab skills-catalog** si disponible :
   - `https://gitlab.infopro-digital.net/[skills-catalog]` (à configurer)
   - Lister les nouveaux skills d'équipe depuis la dernière session
4. **Synthèse** : présenter les nouveautés en 3-5 points max

Si la connexion échoue (Netskope, SSL, hors ligne) :
> "⚠️ Impossible de vérifier les mises à jour (connexion bloquée ou pas de réseau).
> Je me base sur mes connaissances actuelles pour les recommandations."

---

### PHASE 5 — PROPOSITION : Recommandations personnalisées

**Objectif :** Proposer une liste priorisée de ce qui manque ou peut être amélioré.

Format de chaque proposition :

```
[ ] PRIORITÉ: HAUTE / MOYENNE / BASSE
    TYPE: skill | agent | rule | setting
    NOM: nom-du-composant
    EMPLACEMENT: ~/.claude/... ou .claude/...
    POURQUOI: [1 phrase liée au profil]
    EFFORT: [rapide / moyen / à paramétrer]
```

Recommandations types selon profil :

**Si Data Engineer / Snowflake** → proposer :
- `snowflake-snow-cli` (si absent)
- `netskope-ssl` (si Netskope détecté)
- Rule `coding-style` (si absente)

**Si proxy d'entreprise** → proposer :
- `netskoke-ssl` skill (en priorité HAUTE)

**Si pas de CLAUDE.md global** → proposer :
- Création guidée de `~/.claude/CLAUDE.md`

**Si formation / pédagogie** → proposer :
- Skill `impact` (si absent)

**Si skills impact-* individuels encore présents** → proposer :
- Migration vers `impact/` consolidated + suppression doublons

Après avoir présenté toutes les propositions :
> "Quelles propositions valides-tu ? Tu peux répondre avec les numéros (ex: 1, 3, 5)
> ou 'tout' pour tout valider. Répondre 'passer' pour ne rien installer maintenant."

---

### PHASE 6 — INSTALLATION : Mise en place

**Objectif :** Installer uniquement ce qui a été validé en Phase 5.

Règles absolues :
- **Jamais écraser** un fichier existant sans confirmation explicite
- **Jamais supprimer** quoi que ce soit sans confirmation explicite
- **Toujours montrer** ce qui va être créé/modifié avant de le faire
- **Toujours vérifier** ensuite que le fichier est bien en place

Pour chaque item validé :
1. Annoncer : "Je vais créer `[chemin]`"
2. Créer le fichier
3. Confirmer : "✓ Créé"

Après installation complète :
1. **Mettre à jour `~/.claude/skills/challenge-local/MEMORY.md`** avec :
   - La date du jour
   - Le profil utilisateur saisi
   - La liste de ce qui a été installé
   - La liste de ce qui a été proposé mais pas installé (pour le delta suivant)

2. **Résumé final** :
   ```
   ═══════════════════════════════════════════════════
     CHALLENGE LOCAL — RÉSUMÉ DE SESSION
   ═══════════════════════════════════════════════════
     Date         : JJ/MM/AAAA
     Utilisateur  : PRÉNOM
     Installé     : N éléments
     Non installé : N éléments (pour la prochaine fois)
   ═══════════════════════════════════════════════════
   ```

---

## MEMORY.md — Format

Ce fichier est écrit et lu par le skill pour le suivi des deltas.

Chemin : `~/.claude/skills/challenge-local/MEMORY.md`

```markdown
# Challenge Local — Mémoire des sessions

## Dernière session : JJ/MM/AAAA

### Profil
- Nom : PRÉNOM
- Rôle : RÔLE
- Langue : LANGUE
- Outils : [liste]
- Niveau : NIVEAU

### Installé
- [ item 1 ] — ~/.claude/...
- [ item 2 ] — ~/.claude/...

### Proposé mais non installé
- [ item A ] — raison : "pas maintenant"
- [ item B ] — raison : "à valider"

### Notes
[Observation libre sur la session]

---

## Sessions précédentes

### JJ/MM/AAAA
[Résumé condensé]
```

---

## Comportement selon le contexte

| Situation | Comportement |
|-----------|-------------|
| Première exécution (pas de MEMORY.md) | Démarrer par Phase 1 → 2 → 3 → 4 → 5 → 6 |
| MEMORY.md présent, < 7 jours | Proposer de sauter les phases 2 et 3, repartir de Phase 4 |
| MEMORY.md présent, > 30 jours | Refaire Phase 2 (profil peut avoir changé) |
| Utilisateur différent (prénom differ) | Refaire Phase 2 complète |
| Mode `--quick` mentionné | Sauter Phase 3 (explication), résumé court en Phase 5 |

---

## Notes d'implémentation

- Ce skill est **documentation pure** : il ne lance pas de scripts automatiquement
- Toutes les installations passent par les outils natifs de Claude Code (create_file, etc.)
- Les suppressions nécessitent **confirmation explicite** de l'utilisateur
- Compatible avec WSL et Windows (distinguer les chemins si nécessaire)
- Le scan GitLab skills-catalog est **optionnel** — ne pas bloquer si inaccessible
