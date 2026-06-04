# Phase 7 — Orphelins

## Définition

Un fichier est **orphelin** si :
1. Il est dans le périmètre (cf. SKILL.md)
2. **Aucun** autre fichier du périmètre ne le mentionne (par nom, par lien md, par backtick)
3. Il n'est **pas** un point d'entrée canonique :
   - `CLAUDE.md` (tous niveaux)
   - `MEMORY.md`
   - `INDEX.md`
   - `README.md`
   - `SKILL.md` (un par dossier skill)
   - `settings.json`

## Algorithme

```bash
# 1. Lister tous les fichiers candidats
candidates=$(find . -name "*.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/_archive/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" 2>/dev/null)

# 2. Pour chaque candidat, compter ses backlinks
for f in $candidates; do
  basename=$(basename "$f")
  # Skip points d'entrée
  case "$basename" in
    CLAUDE.md|MEMORY.md|INDEX.md|README.md|SKILL.md) continue ;;
  esac
  # Compter mentions ailleurs
  count=$(grep -rl "$basename" --include="*.md" . 2>/dev/null \
    | grep -v "^$f$" | wc -l)
  if [ "$count" -eq 0 ]; then
    mtime=$(stat -c %y "$f" 2>/dev/null || stat -f %Sm "$f")
    echo "ORPHELIN | $f | mtime=$mtime"
  fi
done
```

## Qualification

Pour chaque orphelin détecté, classer :

### ❓ À qualifier (WIP possible)
- mtime < 7 jours
- Pattern de nom évoquant brouillon (`-wip`, `-draft`, `-test`, date récente)
- Présent dans `git status` (non commité)

→ **Action** : demander à l'humain "ce fichier est-il en cours ?"

### 🟡 Candidat archive
- mtime > 1 mois
- Contenu informatif historique (décisions passées, brouillons abandonnés)
- Mentionné dans git log mais plus dans le code actuel

→ **Action proposée** : déplacer vers `_archive/` avec entrée dans `_archive/INDEX.md` (date + raison)

### 🔴 Candidat suppression
- mtime > 3 mois
- Duplicate d'un autre fichier vivant
- Erreur évidente (fichier vide, typo dans le nom, fichier de test oublié)

→ **Action proposée** : `git rm` après validation humaine

## Cas particuliers

### Skills, agents, hooks
- Un `SKILL.md` sans backlink n'est PAS orphelin par défaut — Claude le découvre par sa description, pas par citation. Vérifier plutôt s'il s'est jamais déclenché (cf. Phase 2).
- Un agent `.claude/agents/X.md` doit être cité au moins dans CLAUDE.md ou un autre agent. Sinon orphelin probable.

### Frontmatters mentionnant le fichier
Un .md mentionné UNIQUEMENT dans son propre frontmatter `name:` ne compte pas comme référencé.

## Format de sortie

```
### Phase 7 — Orphelins (X candidats)

❓ À qualifier (3) :
  - memory/draft_new_idea.md (mtime 2026-05-10, dans git status)
  - pole-b/wip-sandbox.md (mtime 2026-05-09)
  - infra/test-output.md (mtime 2026-05-12)

🟡 Candidat archive (5) :
  - memory/old_session_notes_2026-02.md
  - pole-b/abandoned-pitch-v1.md
  - ...

🔴 Candidat suppression (2) :
  - tmp.md (vide, mtime 2025-12-03)
  - test (typo, contenu inutilisable)
```
