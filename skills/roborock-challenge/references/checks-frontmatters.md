# Phase 1 — Frontmatters & métadonnées

## Règles Anthropic officielles (SKILL.md)

- `name` : ≤ 64 chars, lowercase + chiffres + hyphens uniquement, pas de XML, pas de mots réservés (`anthropic`, `claude`)
- `description` : ≤ 1024 chars, non-vide, third person, doit dire **ce que fait** ET **quand l'invoquer**
- Pas de point-of-view première personne ("I can help...")

## Règles agent harness (CRITIQUES — incident connu)

Source : `feedback_agent_frontmatter.md` en memory.

Dans le frontmatter d'un agent `.claude/agents/*.md` :
- ❌ **JAMAIS** de `:` interne dans `description:` non quoté
- ❌ **JAMAIS** d'em-dash `—` dans `description:` non quoté
- ❌ **JAMAIS** de `×` dans `description:` non quoté

→ Sinon l'agent est **rejeté silencieusement** par le harness. Pas d'erreur visible, mais l'agent ne se charge jamais.

## Checks à exécuter

```bash
# 1. Lister tous les fichiers avec frontmatter potentiellement cassé
for f in $(find ~/.claude/agents .claude/agents -name "*.md" 2>/dev/null); do
  # Extraire la ligne description
  desc=$(awk '/^---$/{c++} c==1 && /^description:/{print; exit}' "$f")
  echo "$f → $desc"
done
```

Pour chaque fichier :
- [ ] Frontmatter ouvre par `---` et ferme par `---` ?
- [ ] `name:` présent ? Conforme regex `^[a-z0-9-]+$` et ≤ 64 chars ?
- [ ] `description:` présent ? ≤ 1024 chars ?
- [ ] Si `description:` non-quotée : pas de `:`, `—`, `×` ?
- [ ] Si description quotée (entre `"` ou `'`) : caractères spéciaux échappés ?

## Verdicts

- ✅ Frontmatter valide
- ⚠️ Description vague ou trop générique (déclenchement improbable)
- ❌ CRITIQUE : description contient `:` non quoté → agent rejeté
- ❌ CRITIQUE : `name` invalide (majuscules, espaces, `_`)
- ❌ CRITIQUE : frontmatter mal formé (pas de fermeture `---`)

## Format de sortie

```
### Phase 1 — Frontmatters
✅ challenge-roborock/SKILL.md : OK
❌ .claude/agents/foo.md : CRITIQUE — `:` non quoté dans description → agent ne charge pas
⚠️ ~/.claude/skills/bar/SKILL.md : description trop générique ("helps with stuff")
```
