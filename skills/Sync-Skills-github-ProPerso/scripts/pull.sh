#!/usr/bin/env bash
# pull.sh <skill> — copy from workspace (github) to local
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_SKILLS="$HOME/.claude/skills"
WORKSPACE="$HOME/.claude/skills-sync-workspace/claude_conf"
REMOTE_SKILLS="$WORKSPACE/skills"

if [ $# -lt 1 ]; then
  echo "Usage: pull.sh <skill_name>" >&2
  exit 1
fi

SKILL="$1"
LOCAL_DIR="$LOCAL_SKILLS/$SKILL"
REMOTE_DIR="$REMOTE_SKILLS/$SKILL"

bash "$SCRIPT_DIR/ensure-workspace.sh" > /dev/null

if [ ! -d "$REMOTE_DIR" ]; then
  echo "❌ '$SKILL' n'existe pas sur GitHub." >&2
  exit 1
fi

echo "📥 Pull '$SKILL' depuis GitHub..."

# Backup local version if it exists
if [ -d "$LOCAL_DIR" ]; then
  BACKUP="$LOCAL_SKILLS/.backup-$SKILL-$(date +%Y%m%d-%H%M%S)"
  cp -r "$LOCAL_DIR" "$BACKUP"
  echo "  💾 Backup local: $BACKUP"
  rm -rf "$LOCAL_DIR"
fi

cp -r "$REMOTE_DIR" "$LOCAL_DIR"
echo "✅ Skill '$SKILL' récupéré dans $LOCAL_DIR"
