# UI, Frontend & Browser — Outils Claude Code

> Generation UI, navigation web, integrations IDE.

---

## 1. frontend-design (plugin officiel Anthropic)

### Description

Plugin officiel dans `anthropics/skills` (65.8k stars) et `anthropics/claude-plugins-official`.
277k+ installations. **Auto-invoque** quand Claude detecte du travail frontend.

### Ce qu'il fait

- Genere des interfaces **distinctes et production-ready**
- Evite l'esthetique generique IA (pas du "shadcn par defaut")
- Polices typographiques audacieuses, palettes couleur distinctes
- Animations intentionnelles, details contextuels
- ~400 tokens (tres leger)

### Activation

| Methode | Comment |
|---------|---------|
| Automatique | Claude le detecte quand tu travailles sur du frontend |
| Explicite | `/frontend-design` |
| Install | `/plugin install frontend-design@claude-plugins-official` |

### Complement : wilwaldon/Claude-Code-Frontend-Design-Toolkit

- **URL** : https://github.com/wilwaldon/Claude-Code-Frontend-Design-Toolkit
- **Contenu** : Toolkit complet shadcn/ui + Tailwind + react-hook-form + zod
- **Features** : @layer organization, dark mode, form handling
- **Usage** : Si tu veux du React + Tailwind + shadcn specifiquement

---

## 2. claude --chrome (browser officiel)

### Description

Integration officielle Chrome DevTools dans Claude Code (beta).

### Activation

```bash
claude --chrome
```

### Fonctionnalites

- Navigation web (URL, click, scroll)
- Remplissage de formulaires
- Lecture console logs
- Monitoring reseau
- Enregistrement GIF
- Acces aux cookies/sessions existantes (Gmail, Docs, CRM)

### Documentation

https://code.claude.com/docs/en/chrome

---

## 3. Computer Use (officiel Anthropic)

### Description

Claude peut controler le bureau : ouvrir fichiers, naviguer GUI, cliquer.
Disponible pour utilisateurs Pro/Max.

### Fonctionnalites

- Controle souris et clavier
- Capture d'ecran
- Navigation dans applications desktop
- Zoom et actions contextuelles

---

## 4. Repomix — Contexte codebase complet

### Description

Pack un repo entier en 1 seul fichier optimise LLM (XML, Markdown, JSON).

- **URL** : https://github.com/yamadashy/repomix (23.3k stars)
- **Features** : Token count, compression Tree-sitter, detection secrets, respect .gitignore

### Usage

```bash
npx repomix
# Genere un fichier repomix-output.xml avec tout le repo
```

Puis partager le fichier avec Claude pour analyse cross-repo, review, ou documentation.

---

## 5. Obsidian — Integration communautaire

> **PAS d'integration officielle Anthropic.** Tout est communautaire.

### Claudian (leader — 4.5k stars)

- **URL** : https://github.com/YishenTu/claudian
- **Type** : Plugin Obsidian natif
- **Features** : Claude assistant dans sidebar, read/write/edit natif, conversations persistantes

### obsidian-claude-code-mcp (approche moderne)

- **URL** : https://github.com/iansinnott/obsidian-claude-code-mcp
- **Type** : MCP Server (WebSocket port 22360)
- **Features** : Read, write, search notes, execute commands

---

## 6. Autres plugins officiels utiles

Depuis `anthropics/claude-plugins-official` (33 plugins) :

| Plugin | Ce qu'il fait |
|--------|--------------|
| `frontend-design` | UI production-ready (ci-dessus) |
| `code-review` | Review automatique avec 5 agents paralleles |
| `pr-review-toolkit` | Analyse PR complete (6 agents specialises) |
| `security-guidance` | Warnings patterns securite (9 patterns, hook PreToolUse) |
| `feature-dev` | 7 phases feature dev (3 agents specialises) |
| `skill-creator` | Creer tes propres skills en conversationnel |
| `ralph-wiggum` | Boucles iteratives autonomes (hook Stop qui reinjecte le prompt) |
| `commit-commands` | Helpers commit/push/PR |
| `code-simplifier` | Simplification de code |
| 12x LSP plugins | Support langages (C/C++, Go, Java, Python, Rust, TypeScript, etc.) |
