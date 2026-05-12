---
name: Sync-Skills-github-ProPerso
description: Synchroniser les skills Claude Code entre PC pro et PC perso via le repo GitHub kimen26/claude_conf. Skill interactif qui propose pull / push / compare / status, liste les skills concernés avec leur diff, et demande confirmation avant tout écrasement. Maintient une liste de skills PRIVÉS (Infopro) à ne JAMAIS pousser. Auto-trigger sur — sync skills, github skills, pousser skill, récupérer skill, comparer skills, partager skill, claude_conf, kimen26, skills perso pro, maj skills.
---

# Sync-Skills-github-ProPerso

> Sync manuelle assistée des skills `~/.claude/skills/` entre PC pro et PC perso, via le repo `kimen26/claude_conf`.

## 🎯 Quand ce skill se déclenche

Auto-trigger sur : **sync skills, github skills, pousser skill, récupérer skill, comparer skills, partager skill, claude_conf, kimen26, MAJ skills, skills perso pro**.

L'utilisateur veut synchroniser ses skills entre deux machines. Il décide à chaque fois quoi pousser et quoi récupérer — **rien d'automatique**.

## 🔒 Skills PRIVÉS — JAMAIS pousser sur GitHub

Cette liste est **load-bearing**. Avant tout `push`, vérifier que le skill ciblé n'est PAS dans cette liste. Si l'utilisateur insiste, **refuser et expliquer pourquoi**.

```
confluence              # API + URLs Infopro Digital
gitlab-trigger          # Pipeline GitLab interne IPD
ipd-snowflake           # Naming conventions + comptes IPD
netskope-ssl            # Chemins de certificats Netskope corpo
relecteur-fiches        # Contenu projet SAN DOKU interne
snowflake-snow-cli      # Contient des références SANDBOX Infopro
qwen3-tts               # Contient potentiellement des clés API perso
Sync-Skills-github-ProPerso  # ⚠️ EXCEPTION : peut être poussé (cf. ci-dessous)
```

**Exception `Sync-Skills-github-ProPerso`** : ce skill lui-même PEUT être poussé sur GitHub (c'est utile pour l'autre PC). Le filtrage de la liste privée est fait à l'exécution, pas par exclusion du repo.

## 📁 Configuration

```
LOCAL_SKILLS_DIR  = C:\Users\yann.ponaire\.claude\skills\
REPO_URL_SSH      = git@github.com:kimen26/claude_conf.git
REPO_URL_HTTPS    = https://github.com/kimen26/claude_conf.git
REPO_SUBFOLDER    = skills/                          # chemin dans le repo
WORKSPACE         = C:\Users\yann.ponaire\.claude\skills-sync-workspace\claude_conf\
```

> **Auth GitHub** : tenter SSH d'abord (clé `~/.ssh/id_ed25519` + `ssh.github.com:443` pour Netskope). Si Permission denied → fallback HTTPS avec credential manager Windows.

## 🚀 Flow principal

Quand le skill se déclenche, **toujours** commencer par poser cette question :

```
🔄 Sync skills — Que veux-tu faire ?

  1. 📊 Status      — Voir l'état de chaque skill (à jour / divergé / manquant)
  2. 🔍 Compare     — Diff détaillé local ↔ GitHub
  3. 📥 Pull        — Récupérer un skill depuis GitHub vers ce PC
  4. 📤 Push        — Envoyer un skill de ce PC vers GitHub
  5. ❌ Annuler
```

Attendre la réponse, puis suivre la procédure correspondante.

### 📊 1. STATUS

But : aperçu rapide.

1. Lancer `bash scripts/status.sh` (ou équivalent inline si bash absent)
2. Afficher un tableau type :

| Skill | Local | GitHub | État |
|-------|-------|--------|------|
| impact | 2026-05-12 | 2026-05-10 | 🟡 Local plus récent |
| deep-research | 2026-04-01 | 2026-04-01 | ✅ Identique |
| n8n-website | 2026-04-09 | 2026-04-15 | 🔵 GitHub plus récent |
| info-architecture | 2026-03-13 | — | ⚪ Manquant sur GitHub |
| confluence | 2026-03-20 | — | 🔒 PRIVÉ (jamais sur GitHub) |

3. Proposer la suite : "Tu veux compare/pull/push un skill ?"

### 🔍 2. COMPARE

1. Demander : "Quel skill comparer ? (ou 'all' pour tous les non-privés)"
2. Lancer `bash scripts/compare.sh <skill_name>` 
3. Afficher pour chaque fichier : `+N/-M lignes`, ou "identique", ou "nouveau"
4. Proposer pull ou push

### 📥 3. PULL (GitHub → Local)

1. Demander : "Quel skill récupérer depuis GitHub ?" (si pas déjà précisé)
2. **Vérifier que le skill existe sur GitHub.** Si non, refuser.
3. Lancer `scripts/compare.sh <skill>` et afficher le diff résumé
4. **Demander confirmation explicite** :
   ```
   ⚠️ Tu vas écraser la version LOCALE du skill 'impact'.
   
   Diff: SKILL.md (+12/-3), storytelling.md (+5/-0), nouveau fichier: gamification-v2.md
   
   Confirmer le pull ? (oui/non)
   ```
5. Si "oui" → `scripts/pull.sh <skill>` → confirmer succès

### 📤 4. PUSH (Local → GitHub)

1. Demander : "Quel skill envoyer vers GitHub ?"
2. **VÉRIFIER LA LISTE PRIVÉE** (cf. début du fichier). Si le skill y figure :
   ```
   🔒 Refus : 'confluence' est marqué comme PRIVÉ (contient des références internes Infopro Digital).
   Modifie la liste dans SKILL.md si c'est intentionnel.
   ```
   STOP.
3. Lancer `scripts/compare.sh <skill>` et afficher le diff résumé
4. **Demander confirmation explicite** :
   ```
   ⚠️ Tu vas écraser la version DISTANTE (GitHub) du skill 'impact'.
   
   Diff: SKILL.md (+12/-3), storytelling.md (+5/-0)
   Commit sera fait sous: Yann PONAIRE <yann.ponaire@infopro-digital.com>
   
   Confirmer le push ? (oui/non)
   ```
5. Si "oui" → `scripts/push.sh <skill>` → confirmer + afficher URL du commit

## 🛠️ Scripts helpers

Voir `scripts/` :
- `ensure-workspace.sh` — clone ou fetch+reset le workspace
- `status.sh` — tableau d'état
- `compare.sh <skill>` — diff local ↔ workspace
- `pull.sh <skill>` — workspace → local
- `push.sh <skill>` — local → workspace + commit + push

Tous les scripts sont **idempotents** et **sûrs** : aucune écriture sans avoir affiché ce qui va changer.

## ⚠️ Règles de comportement strictes

1. **JAMAIS** de push sans confirmation `oui` explicite de l'utilisateur dans le tour de conversation.
2. **JAMAIS** push un skill de la liste privée, même si l'utilisateur le demande directement. Lui rappeler de modifier la liste d'abord.
3. **TOUJOURS** afficher le diff avant pull/push.
4. **TOUJOURS** préférer SSH (port 443) ; fallback HTTPS si échec.
5. Si le workspace n'existe pas → le cloner. Si vieux → `git fetch + reset --hard origin/main`.
6. Si conflit ou erreur réseau → s'arrêter et expliquer, **ne jamais retry en boucle**.

## 🧪 Premier lancement (bootstrap)

Si `~/.claude/skills-sync-workspace/claude_conf/` n'existe pas :
1. Créer le dossier parent
2. `git clone git@github.com:kimen26/claude_conf.git` (ou HTTPS si échec)
3. Si l'auth SSH échoue → expliquer à l'user comment ajouter sa clé publique (`~/.ssh/id_ed25519.pub`) à https://github.com/settings/keys
4. Configurer SSH sur port 443 si Netskope bloque le 22 : ajouter à `~/.ssh/config` :
   ```
   Host github.com
     Hostname ssh.github.com
     Port 443
     User git
   ```

## 📚 Mémo — Structure du repo

```
kimen26/claude_conf/
├── README.md
└── skills/
    ├── impact/
    ├── deep-research/
    ├── markdown-lisibilite/
    ├── linkedin-cv-tech/
    ├── lettre-recommandation/
    ├── n8n-website/
    ├── prompt-craft/
    └── (nouveaux skills publics ajoutés ici)
```

Chaque skill = un sous-dossier avec **a minima** un `SKILL.md`, plus éventuellement des fichiers thématiques.
