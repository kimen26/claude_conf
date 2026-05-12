#!/usr/bin/env bash
# push.sh <skill> — copy local to workspace, commit, push to github
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_SKILLS="$HOME/.claude/skills"
WORKSPACE="$HOME/.claude/skills-sync-workspace/claude_conf"
REMOTE_SKILLS="$WORKSPACE/skills"

PRIVATE_SKILLS=(
  "confluence"
  "gitlab-trigger"
  "ipd-snowflake"
  "netskope-ssl"
  "relecteur-fiches"
  "snowflake-snow-cli"
  "qwen3-tts"
)

if [ $# -lt 1 ]; then
  echo "Usage: push.sh <skill_name>" >&2
  exit 1
fi

SKILL="$1"
LOCAL_DIR="$LOCAL_SKILLS/$SKILL"
REMOTE_DIR="$REMOTE_SKILLS/$SKILL"

# Block private skills
for p in "${PRIVATE_SKILLS[@]}"; do
  if [ "$p" = "$SKILL" ]; then
    echo "🔒 REFUS : '$SKILL' est marqué PRIVÉ. Modifie la liste dans SKILL.md si intentionnel." >&2
    exit 2
  fi
done

if [ ! -d "$LOCAL_DIR" ]; then
  echo "❌ '$SKILL' n'existe pas localement." >&2
  exit 1
fi

bash "$SCRIPT_DIR/ensure-workspace.sh" > /dev/null

# Sync local → workspace
echo "📤 Préparation du push pour '$SKILL'..."
rm -rf "$REMOTE_DIR"
mkdir -p "$REMOTE_SKILLS"
cp -r "$LOCAL_DIR" "$REMOTE_DIR"

cd "$WORKSPACE"
git add "skills/$SKILL"

if git diff --cached --quiet; then
  echo "ℹ️  Aucune différence après copie. Rien à pousser."
  exit 0
fi

# Commit
COMMIT_MSG="sync: update skill $SKILL from $(hostname)"
git commit -m "$COMMIT_MSG" > /dev/null
echo "  ✅ Commit: $COMMIT_MSG"

# Push
if git push origin HEAD 2>&1; then
  echo "✅ Skill '$SKILL' poussé sur GitHub."
  REMOTE_URL="$(git remote get-url origin)"
  SHA="$(git rev-parse --short HEAD)"
  echo "   Commit: $SHA  ($REMOTE_URL)"
else
  echo "❌ Push échoué. Le commit est local dans $WORKSPACE — réessaie avec 'git push' depuis là." >&2
  exit 1
fi
