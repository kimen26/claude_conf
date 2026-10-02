# claude_conf

Configuration Claude Code de Yann Ponaire : une marketplace de plugins, le plugin `socle`, et des skills génériques réutilisables.

## Marketplace `yann`

    claude plugin marketplace add kimen26/claude_conf
    claude plugin install socle@yann

| Plugin | Contenu |
|--------|---------|
| [`socle`](plugins/socle/) | Méthode de travail, gardes, audit de projet, agents, skills `/socle:*`, gabarits, règles machine copiées dans `~/.claude/rules`. Installation, parcours et mise à jour : [`plugins/socle/README.md`](plugins/socle/README.md). |

La liste des autres plugins installés sur le poste est dans [`PLUGINS.md`](PLUGINS.md).

## Skills génériques (`skills/`)

Des dossiers `SKILL.md` indépendants du plugin, installables de deux façons :
- par copie : déposer le dossier voulu dans `~/.claude/skills/` ; Claude le charge quand sa description correspond à la demande ;
- par la sync : le skill `Sync-Skills-github-ProPerso` tire ou pousse les skills entre ce repo et `~/.claude/skills/` (les skills privés Infopro ne sont jamais poussés).

| Skill | Description |
|-------|-------------|
| [`deep-research`](skills/deep-research/) | Recherche profonde et plurielle : sources académiques, praticiens, voix non conventionnelles, multi-culturelle. |
| [`impact`](skills/impact/) | Pédagogie et communication : formation, storytelling, persuasion, biais cognitifs, gamification, instructional design, facilitation. |
| [`info-architecture`](skills/info-architecture/) | Catégoriser, indexer, nommer : taxonomie, MECE, Diátaxis, PARA, facettes. |
| [`lettre-recommandation`](skills/lettre-recommandation/) | Lettres de recommandation professionnelles au format Word. |
| [`linkedin-cv-tech`](skills/linkedin-cv-tech/) | LinkedIn et CV tech, IA, data : champ par champ, mots-clés, ATS. |
| [`markdown-lisibilite`](skills/markdown-lisibilite/) | Lisibilité Markdown : typographie, hiérarchie, chunking. |
| [`n8n-llm-json-parse`](skills/n8n-llm-json-parse/) | Parser la sortie JSON d'un AI Agent n8n. |
| [`n8n-website`](skills/n8n-website/) | Sites HTML hébergés via webhook n8n + Code node. |
| [`pmo-design`](skills/pmo-design/) · [`pmo-challenge`](skills/pmo-challenge/) | Concevoir puis auditer un système multi-agent PMO. |
| [`prompt-craft`](skills/prompt-craft/) | Écrire un prompt efficace, avec variante Snowflake Cortex Agent. |
| [`translate-en`](skills/translate-en/) | Traduire du français en anglais naturel. |
| [`claude-infra`](skills/claude-infra/) | Audit et nettoyage de l'infra Claude Code (CLAUDE.md, skills, hooks, mémoire). |
| [`Sync-Skills-github-ProPerso`](skills/Sync-Skills-github-ProPerso/) | Synchronisation des skills entre PC pro et perso. |
| [`browser-pilot`](skills/browser-pilot/) · [`CheiKh`](skills/CheiKh/) | Pilotage navigateur ; famille de skills CheiKh (architecte, sentinelle, stratège). |

## Structure

```
claude_conf/
├── .claude-plugin/marketplace.json   # marketplace yann
├── plugins/socle/                    # le plugin (voir son README)
├── skills/<nom>/SKILL.md             # skills génériques
├── PLUGINS.md                        # plugins installés sur le poste
└── CHANGELOG.md
```
