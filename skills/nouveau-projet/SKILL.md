---
name: nouveau-projet
description: "Socle de démarrage d'un projet Claude Code selon la méthode Yann — CLAUDE.md court avec table de routage, quintette memory/, portes de vérification, hooks de base, .gitignore. Checklist en 6 étapes + gabarits prêts à copier. Auto-trigger sur : nouveau projet, init projet, setup projet, démarrer un projet, socle projet, bootstrap projet, créer un projet."
---

# Nouveau projet — le socle

> Distillé de ce qui a marché : IArtcane (usine handoffs, portes de vérification),
> le CLAUDE.md global (essence Boris Cherny : court, dense, actionnable),
> la règle `~/.claude/rules/memoire-projet.md` (quintette memory/).
> **Simplicity first. Un fichier ne rentre au socle que s'il a fait ses preuves dans 2 projets.**

## Les 4 principes (avant la checklist)

1. **Une règle que ne vérifie aucune commande n'est pas une règle.** Chaque invariant a sa porte de vérification (script, hook, check). Sinon c'est un vœu.
2. **CLAUDE.md racine < 100 lignes.** Mission en 1 phrase, table de routage (mots de la demande → skill/fichier à charger), invariants numérotés, table des portes. Le détail vit dans les fichiers routés, jamais dans la racine.
3. **Une correction humaine non gravée sera refaite.** Le quintette memory/ n'est pas optionnel (→ `rules/memoire-projet.md`).
4. **Les archives racontent le passé** : DECISIONS, LESSONS, briefs gardent leur syntaxe d'époque. Seule la doc normative (celle qui décrit la réalité courante) est contrôlée.

## Checklist de démarrage (6 étapes)

```
- [ ] 1. git init + .gitignore (gabarit ci-dessous : .env, inbox/, _a_supprimer/)
- [ ] 2. CLAUDE.md racine depuis references/gabarit-claude-md.md — remplir mission,
        routage, invariants. Viser < 100 lignes AU DÉPART (ça grossira bien assez vite)
- [ ] 3. memory/ : le quintette complet — MEMORY.md (état) + TODO.md (lanes) +
        DECISIONS.md (D-NNN) + LESSONS.md (L-NNN) + CHANGELOG.md (releases,
        se remplit en vidant les lanes terminées)
- [ ] 4. Hooks de base : copier depuis IArtcane/.claude/hooks/ →
        garde-git-large.py (refuse git add -A) + garde-secrets.py (refuse toute
        commande dont la sortie exposerait un .env) ; les déclarer dans
        .claude/settings.json ; TESTER dans les deux sens (bloque le mauvais,
        laisse passer le légitime)
- [ ] 5. Première porte de vérification : au minimum un check syntaxe/lint adapté
        à la stack, listé dans la table des portes du CLAUDE.md. Dès qu'il y a un
        écran : une recette visuelle (Playwright — captures mobile + desktop, échoue
        sur erreur console) ; dès qu'il y a un pipeline : des tests hors-ligne (.py/.mjs).
        Et la règle d'or : un critère VISUEL se valide en OUVRANT les captures —
        un log de succès prouve que le code a tourné, jamais que l'œil voit juste
- [ ] 6. Premier commit conventionnel : `chore: socle projet`
```

## Ce qui n'entre PAS au socle (anti-sur-ingénierie)

- Pas de skills projet au départ — un skill naît quand un savoir-faire a servi 2 fois.
- Pas d'agents projet au départ — même règle.
- Pas d'usine handoffs au départ — elle se justifie à partir de plusieurs sessions
  parallèles. Le jour où : `references/protocole-handoffs.md` (squelette portable).
  Les briefs terminés s'archivent tels quels — on ne recontrôle jamais le passé.
- Pas de miroir AGENTS.md sauf usage bi-outil réel (Claude + Kimi).

## Gabarits

- `references/gabarit-claude-md.md` — CLAUDE.md racine à trous
- `references/gabarit-gitignore.md` — .gitignore + memory/ fichiers de départ
- `references/protocole-handoffs.md` — l'usine de dev, quand elle se justifie

## Règles associées (globales, déjà en place)

- `~/.claude/rules/memoire-projet.md` — le quintette memory/, compteurs partagés D-NNN/L-NNN
- `~/.claude/rules/interaction-style.md` — questions en texte, jamais de formulaire
- CLAUDE.md global — simplicity first, commits conventionnels, jamais de secret en dur

_Créé 2026-09-03 (Roborock + refonte socle). Sync : kimen26/claude_conf._
