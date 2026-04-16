# claude_conf — Skills Claude Code

Collection de skills Claude Code génériques et réutilisables.

> **Claude Code Skills** : des fichiers `SKILL.md` qui donnent à Claude une expertise spécialisée sur demande. Chaque skill contient des instructions, patterns et meilleures pratiques pour un domaine précis.

## Utilisation

1. Copier le(s) dossier(s) voulus dans `~/.claude/skills/`
2. Référencer le skill dans ton `CLAUDE.md` :

```markdown
<skill>
<name>prompt-craft</name>
<description>Déclencheur : quand tu veux créer ou améliorer un prompt</description>
<file>~/.claude/skills/prompt-craft/SKILL.md</file>
</skill>
```

3. Claude chargera automatiquement le skill quand la description correspond à ta demande.

---

## Skills disponibles

| Skill | Description |
|-------|-------------|
| [`deep-research`](skills/deep-research/) | Méthodologie de recherche profonde et plurielle — sources académiques, philosophiques, praticiens, voix non-conventionnelles. Multi-culturelle (USA, France, Europe, Asie). |
| [`impact`](skills/impact/) | Famille de skills pédagogiques et de communication : formation, storytelling, persuasion, biais cognitifs, gamification, instructional design, enneagramme, facilitation... |
| [`lettre-recommandation`](skills/lettre-recommandation/) | Génère des lettres de recommandation professionnelles au format Word (.docx) avec mise en page élégante et structure narrative impactante. |
| [`linkedin-cv-tech`](skills/linkedin-cv-tech/) | Bonnes pratiques LinkedIn et CV dans les domaines tech, IA, no-code/low-code, data. Guide champ par champ, mots-clés, ATS, anti-patterns. |
| [`markdown-lisibilite`](skills/markdown-lisibilite/) | Expert en lisibilité visuelle Markdown : typographie, hiérarchie, chunking, progressive disclosure, anti-patterns. |
| [`n8n-website`](skills/n8n-website/) | Génère des sites HTML complets hébergés via webhook n8n + Code node JS. Gère l'échappement, les thèmes CSS, le multi-page, la validation. |
| [`prompt-craft`](skills/prompt-craft/) | L'art d'écrire un prompt efficace — template humanisé, frameworks (few-shot, chain-of-thought), anti-patterns, évaluation. Inclut une variante pour Snowflake Cortex Agent. |

---

## Structure

```
~/.claude/
├── skills/
│   ├── deep-research/SKILL.md
│   ├── impact/
│   │   ├── SKILL.md
│   │   ├── storytelling.md
│   │   ├── gamification.md
│   │   └── ... (22 fichiers thématiques)
│   ├── lettre-recommandation/
│   │   ├── SKILL.md
│   │   └── generate_lettre_template.py
│   ├── linkedin-cv-tech/SKILL.md
│   ├── markdown-lisibilite/SKILL.md
│   ├── n8n-website/SKILL.md
│   └── prompt-craft/SKILL.md
└── CLAUDE.md  ← référence les skills
```

---

## Ressources

- [Claude Code documentation](https://docs.anthropic.com/claude-code)
- [Anthropic Claude](https://www.anthropic.com)
