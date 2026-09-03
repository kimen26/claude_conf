# Hooks de base — installation dans un projet

Deux gardes Python, sans dépendance, à copier dans le projet (pas de chemin
absolu : le hook vit AVEC le projet, il suit le clone).

```
mkdir -p .claude/hooks
cp ~/.claude/skills/nouveau-projet/references/hooks/garde-*.py .claude/hooks/
```

Puis dans `.claude/settings.json` (les hooks s'exécutent avec le projet pour
répertoire courant, d'où les chemins relatifs) :

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "python .claude/hooks/garde-git-large.py" }] },
      { "matcher": "Bash|PowerShell|Read",
        "hooks": [{ "type": "command", "command": "python .claude/hooks/garde-secrets.py" }] }
    ]
  }
}
```

`python` → `python3` ou `py` selon la machine : vérifier avec `python --version`.

## Tester dans les deux sens (obligatoire)

```
echo '{"tool_name":"Bash","tool_input":{"command":"git add -A"}}'       | python .claude/hooks/garde-git-large.py ; echo "exit=$?"   # attendu 2
echo '{"tool_name":"Bash","tool_input":{"command":"git add src/a.py"}}' | python .claude/hooks/garde-git-large.py ; echo "exit=$?"   # attendu 0
echo '{"tool_name":"Read","tool_input":{"file_path":".env"}}'           | python .claude/hooks/garde-secrets.py   ; echo "exit=$?"   # attendu 2
echo '{"tool_name":"Read","tool_input":{"file_path":".env.example"}}'   | python .claude/hooks/garde-secrets.py   ; echo "exit=$?"   # attendu 0
```

Un hook qui bloque le légitime est pire qu'aucun hook : si un faux positif
apparaît, corriger la regex ici ET dans le skill, puis repousser via le sync.
