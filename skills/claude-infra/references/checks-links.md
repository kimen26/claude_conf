# Phase 6 — Liens & refs croisées

## Objectif

Tout lien markdown relatif `[texte](chemin)` ou mention `\`fichier.md\`` doit pointer vers un fichier existant.

## Script de scan

```bash
# Extraire tous les liens markdown relatifs (pas http/https)
grep -rEn '\[[^]]+\]\([^)]+\)' --include="*.md" . 2>/dev/null \
  | grep -vE 'https?://' \
  | grep -oP '\([^)]+\)' \
  | tr -d '()'\
  | sort -u
```

## Checks

### 6.1 — Liens .md relatifs
Pour chaque lien `[X](path/to/file.md)` :
- [ ] Le fichier existe à `path/to/file.md` (résolu depuis le fichier qui contient le lien) ?
- [ ] Si lien avec ancre `#section`, l'ancre existe-t-elle dans la cible ?

### 6.2 — Refs en backticks
Mentions `\`pole-a-pmo.md\`` ou `\`memory/MEMORY.md\`` dans le corps d'un .md :
- [ ] Le fichier mentionné existe ?

```bash
grep -roP '`[a-zA-Z0-9_./-]+\.md`' --include="*.md" .
```

### 6.3 — INDEX.md ↔ contenu sous-arbre
Pour chaque `INDEX.md` (racine pôle ou sous-dossier) :
- [ ] Tout fichier listé dans l'INDEX existe ?
- [ ] Tout fichier important du sous-arbre est dans l'INDEX ?
- [ ] Ordre / sections cohérents avec la réalité du sous-arbre ?

### 6.4 — Refs vers `_archive/`
Si un .md "vivant" cite un fichier dans `_archive/` :
- → ⚠️ référence à du contenu archivé, à requalifier ou retirer

## Verdicts

- ✅ Lien valide
- ❌ HAUTE : lien cassé (fichier cible absent)
- ⚠️ MOYENNE : ancre `#xxx` absente dans cible existante
- 🟡 BASSE : INDEX.md décalé (existe sur disque mais pas indexé, ou vice-versa)

## Format de sortie

```
### Phase 6 — Liens & refs croisées (X liens scannés)
✅ 142 liens valides
❌ CLAUDE.md → pole-b/equipe/PROCESS-old.md : cible absente
❌ memory/MEMORY.md → feedback_test.md : cible absente
⚠️ pole-b/INDEX.md cite story-001 mais story-001 absent du sous-arbre
🟡 INDEX.md skills/exemple-skill/ : 3 fichiers présents non indexés
```
