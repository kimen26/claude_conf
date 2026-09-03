# Handoffs — mise en place dans un projet

```
mkdir -p docs/handoffs
cp ~/.claude/skills/nouveau-projet/references/handoffs/_template.md docs/handoffs/
cp ~/.claude/skills/nouveau-projet/references/handoffs/handoff-check.py scripts/   # ou tools/
```

- Un brief = `docs/handoffs/HO-NNN-<titre>.md`, copié depuis `_template.md`. Le frontmatter
  (`id`, `statut`, `fichiers`) est la seule partie lue par la machine — le reste est pour l'humain.
- **Le registre n'existe pas comme fichier** : `python scripts/handoff-check.py docs/handoffs`
  l'affiche, dérivé des briefs, et échoue sur toute collision. À mettre dans la table des
  portes du CLAUDE.md et à jouer avant d'ouvrir un brief (`pret`) et avant chaque commit.
- Numéro : relire le dossier au moment de créer, prendre le suivant (compteur partagé,
  même règle que D-NNN / L-NNN).
- Terminé (`fait`) → `docs/handoffs/archives/`, tel quel, jamais recontrôlé.

Le protocole complet (rôles cerveau / exécutant, règles) : `../protocole-handoffs.md`.
