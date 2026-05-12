# Challenge Local — Mémoire des sessions

## Dernière session : 05/05/2026

### Profil
- Nom : Yann
- Rôle : Data Engineer / Product Owner outils IA (Infopro Digital)
- Langue : Français
- Outils : Python, SQL, Snowflake, n8n, Confluence, GitLab
- Niveau : Variable (scripts ponctuels → intensif)
- Projets : Data pipelines (SAN DOKU), PMO multi-agents, formations, automatisation n8n
- Contraintes réseau : Netskope SSL actif

### Installé / Modifié
- `~/.claude/skills/n8n-llm-json-parse/SKILL.md` → parser JSON drop-in pour AI Agent n8n (6 cas pathologiques)
- `~/.snowflake/connections.toml` → bloc `INFOPRODIGITAL_GROUP_PRODUCTION_R` (lecture seule prod)
- `.claude/settings.local.json` (san_doku) → permissions Snowflake R-only + deny DROP/DELETE/etc
- `.claude/settings.local.json` (san_doku) → consolidation ~30 entrées `python -c "import json..."` en wildcard `python -c ":*` (49 allow vs ~75 avant)
- `~/.claude/skills/translate-en/SKILL.md` → promu de fichier .md flat à dossier skill structuré

### Supprimé
- `~/.claude/skills/impact.zip` → archive obsolète
- `~/.claude/skills/datagouv*` → 7 dossiers (datagouv, datagouv-demo, datagouv-eco, datagouv-research, datagouv-sante-edu, datagouv-social, datagouv-territoire)
- `~/.claude/skills/translate-en.md` (ancien fichier flat, remplacé par dossier)

### Proposé mais non installé
- (rien en attente)

### Notes
- Le skill `n8n-llm-json-parse` est né d'un bug récurrent (8 corrections du même Code node) → pattern réutilisable pour tout AI Agent n8n
- La connexion Snowflake `_R` permet à Claude Code de challenger les données de prod sans risque (seul rôle reader, scope DB unique, deny DDL/DML)
- Consolidation settings.local.json : `Bash(python -c ":*)` couvre TOUS les one-liners Python — fini les permissions ultra-spécifiques par invocation

---

## Sessions précédentes

### 02/04/2026
- Setup initial : model sonnet-4-6, autoUpdaterStatus disabled, hook PostToolUse auto-format
- Création MEMORY.md challenge-local
- Refus : testing.md rule, suppression datagouv (revisité 05/05)
