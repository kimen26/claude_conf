---
name: nouveau-projet
description: "Socle de démarrage d'un projet Claude Code selon la méthode Yann — CLAUDE.md court avec table de routage, quintette memory/, portes de vérification, hooks de base, .gitignore. Checklist en 6 étapes + gabarits prêts à copier. Auto-trigger sur : nouveau projet, init projet, setup projet, démarrer un projet, socle projet, bootstrap projet, créer un projet."
---

# Nouveau projet — le socle

> Distillé de ce qui a marché sur un premier projet (usine handoffs, portes de vérification),
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
- [ ] 4. Hooks de base : livrés AVEC ce skill →
        cp ~/.claude/skills/nouveau-projet/references/hooks/garde-*.py .claude/hooks/
        garde-git-large.py (refuse git add -A / commit -a) + garde-secrets.py
        (refuse toute lecture d'un .env ou dump d'environnement) ; les déclarer
        dans .claude/settings.json en chemin RELATIF (le hook suit le clone) ;
        TESTER dans les deux sens — recette : references/hooks/INSTALL.md
- [ ] 5. Première porte de vérification : au minimum un check syntaxe/lint adapté
        à la stack, listé dans la table des portes du CLAUDE.md. Dès qu'il y a un
        écran : la recette visuelle livrée avec ce skill →
        cp ~/.claude/skills/nouveau-projet/references/recette-visuelle.py scripts/
        (Playwright : mobile + desktop, échoue sur erreur console / pageerror /
        HTTP>=400 / sélecteur absent ; `--auth state.json` pour le SSO) ;
        dès qu'il y a un pipeline : des tests hors-ligne (.py/.mjs) ;
        dès que le README annonce des compteurs : `cp ~/.claude/skills/nouveau-projet/
        references/check-coherence.py tools/` (à adapter — voir Gabarits).
        Et la règle d'or : un critère VISUEL se valide en OUVRANT les captures —
        un log de succès prouve que le code a tourné, jamais que l'œil voit juste
- [ ] 6. Premier commit conventionnel : `chore: socle projet`
```

## Ce qui n'entre PAS au socle (anti-sur-ingénierie)

- Pas de skills projet au départ — un skill naît quand un savoir-faire a servi 2 fois.
- Pas d'agents projet au départ — même règle.
- Pas d'usine handoffs au départ — elle se justifie à partir de plusieurs sessions
  parallèles. Le jour où : `references/protocole-handoffs.md` (les règles) +
  `references/handoffs/` (`_template.md` du brief, `handoff-check.py` anti-collision,
  `README.md` de mise en place). Les briefs terminés s'archivent tels quels — on ne
  recontrôle jamais le passé.
- Pas de miroir AGENTS.md sauf usage bi-outil réel (Claude + Kimi).

## Gabarits

- `references/gabarit-claude-md.md` — CLAUDE.md racine à trous
- `references/gabarit-gitignore.md` — .gitignore + memory/ fichiers de départ
- `references/protocole-handoffs.md` — l'usine de dev, quand elle se justifie
- `references/hooks/` — `garde-git-large.py`, `garde-secrets.py` + `INSTALL.md` (recette et tests)
- `references/recette-visuelle.py` — porte visuelle Playwright, prête à copier dans `scripts/`
- `references/handoffs/` — `_template.md`, `handoff-check.py`, `README.md`
- `references/check-coherence.py` — **porte de cohérence** : recompte tout sur disque
  (fichiers, entrées de mémoire, compteurs) et signale les écarts avec ce qu'annoncent le
  README et le CLAUDE.md. À adapter au projet ; garder la mécanique. Un compteur écrit à la
  main dérive **toujours** : mesuré sur un projet réel, 3 écarts coexistaient (320 vs 326
  sources, 137 vs 139 rapports, 130 vs 129). Il **dit**, il ne corrige pas — la correction
  reste éditoriale. **Éprouvé sur un seul projet (IArtscan) : candidat au socle, pas encore
  membre** — la règle « 2 projets » s'applique ; il s'arrête avec un message clair tant qu'il
  n'est pas adapté.

## Accès web (lecture, pilotage, anti-bot)

Un projet qui touche au web charge le skill global `browser-pilot` et applique sa doctrine
(`~/.claude/skills/browser-pilot/references/doctrine-acces-web.md`) : **curl d'abord,
navigateur en dernier**, `WebSearch` pour trouver jamais pour lire, JSON embarqué avant de
conclure à une SPA, `curl_cffi` contre les 403 par empreinte TLS, `pilot.mjs` (Playwright)
pour le JS, Brave via CDP pour les sites logués. Au démarrage :

- réserver un **port CDP et un profil Brave dédiés** au projet (9222 MaxPlay, 9223 IArtcane,
  9224 IArtscan, suivant libre : 9225+, profil `C:/tmp/brave-<projet>`) — jamais partagés ;
- pas de MCP navigateur (Playwright MCP, Chrome DevTools MCP) par défaut : 13 à 19k tokens
  de schéma par session. Pour interagir avec une page : `agent-browser` (CLI global,
  `--headed` passe Turnstile) ; un CLI coûte zéro tant qu'il n'est pas appelé ;
- CAPTCHA : vrai Chrome visible d'abord, puis un clic humain dans le Brave du projet
  (session persistante) ; jamais de service de résolution payant ni de proxy résidentiel ;
- chaque domaine bloqué puis débloqué se grave dans `LESSONS.md` avec la marche qui a marché.

## Outillage machine (une fois par PC, jamais par projet)

Les plugins ne se copient pas via le sync — ils s'installent depuis leur marketplace :

- **caveman** (`claude plugin marketplace add JuliusBrussee/caveman` puis
  `claude plugin install caveman@caveman`) — économie de tokens : sorties compressées,
  subagents cavecrew (retours ~-60%), `caveman-compress` pour les fichiers mémoire.
- **agent-browser** (`npm install -g agent-browser && agent-browser install`) — pilotage
  navigateur économe en tokens, voir doctrine `browser-pilot`. Si le shim npm répond
  « This: command not found », un paquet global `node` fantôme traîne : `npm uninstall -g node`.
- Optionnels selon stack : **serena** (navigation LSP par symboles, évite de lire des
  fichiers entiers) et **context7** (doc de lib à jour, utile dès que Playwright ou une lib à API mouvante est
  dans la stack — sans rapport avec le pilotage navigateur) — marketplace officielle.
  Un outil déclaré mais jamais testé rend l'agent silencieusement aveugle : le tester une fois.

## Règles associées (globales, déjà en place)

- `~/.claude/rules/memoire-projet.md` — le quintette memory/, compteurs partagés D-NNN/L-NNN
- `~/.claude/rules/interaction-style.md` — questions en texte, jamais de formulaire
- CLAUDE.md global — simplicity first, commits conventionnels, jamais de secret en dur

_Créé 2026-09-03 (Roborock + refonte socle). 2026-09-03b : hooks embarqués dans le skill, plus de chemin machine. 2026-09-03c : recette-visuelle.py + handoffs/ (template, check, README) livrés et testés. 2026-09-07 : section Accès web (doctrine browser-pilot, ports CDP par projet). 2026-09-07b : `check-coherence.py` (porte de cohérence des compteurs, éprouvée sur IArtscan). Sync : kimen26/claude_conf._
