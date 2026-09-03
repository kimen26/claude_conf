# Plugins Claude Code — liste d'installation (pas de copie de fichiers !)

> Les plugins se réinstallent depuis leur marketplace, jamais par sync de fichiers
> (sinon plus de MAJ). Ce fichier = la liste de référence, tenue à jour à chaque
> ajout/retrait sur l'un des PC. État : 2026-09-03 (rev c, +rtk), PC pro.
> Retirés le 2026-09-03 : pr-review-toolkit (doublon de /code-review intégré),
> security-guidance (remplacé par claude-security). Ne pas réinstaller.

## Marketplaces

```
claude plugin marketplace add anthropics/claude-plugins-official   # (souvent déjà présente)
claude plugin marketplace add JuliusBrussee/caveman
```

## Installation

```
claude plugin install caveman@caveman                              # économie tokens (sorties, cavecrew, compress)
claude plugin install skill-creator@claude-plugins-official        # créer/tester des skills
claude plugin install hookify@claude-plugins-official              # créer des hooks depuis la conversation
claude plugin install commit-commands@claude-plugins-official      # /commit, /commit-push-pr, /clean_gone
claude plugin install claude-md-management@claude-plugins-official # audit CLAUDE.md, /revise-claude-md
claude plugin install claude-code-setup@claude-plugins-official    # recommandeur d'automations
claude plugin install frontend-design@claude-plugins-official      # direction visuelle UI
claude plugin install claude-security@claude-plugins-official      # scan sécu profond (findings challengés, patchs vérifiés)
claude plugin install pyright-lsp@claude-plugins-official          # LSP Python (symboles, types, gain tokens)
claude plugin install typescript-lsp@claude-plugins-official       # LSP JS/TS (tsserver, marche sur JS vanilla)
claude plugin install telegram@claude-plugins-official             # relais Telegram
```

## Optionnels (selon stack, non installés partout)

```
claude plugin install serena@claude-plugins-official               # navigation LSP par symboles
claude plugin install context7@claude-plugins-official             # doc de lib ciblée
```

## Outillage hors plugins (binaire + hook, une fois par PC)

**rtk** — proxy CLI qui compresse la sortie des commandes Bash AVANT qu'elle
n'entre dans le contexte (`git status`, `ls`, `cat`, `find`, `grep`…). Mesuré sur
le PC pro : 1 946 commandes, 3,5 M tokens économisés (83 %). Complément de caveman,
qui agit sur les sorties du modèle ; rtk agit sur les entrées.

```
# 1. binaire — release GitHub (rtk-rs/rtk) ou cargo install rtk ; vérifier : rtk --version
# 2. hook global dans ~/.claude/settings.json :
#    "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "rtk hook claude" }] }]
# 3. bilan : rtk gain
```

Derrière un proxy SSL d'entreprise, ajouter `--ssl-revoke-best-effort` au curl de
téléchargement si erreur de révocation schannel.

## Entretien

- MAJ : `claude plugin update <nom>@<marketplace>` (les officiels se rafraîchissent souvent seuls)
- Le cache `~/.claude/plugins/cache/` accumule les vieilles versions — purger de temps en temps (voir CLEANUP-LOG du PC)
