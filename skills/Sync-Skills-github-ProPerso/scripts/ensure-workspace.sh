#!/usr/bin/env bash
# ensure-workspace.sh — clone or refresh the claude_conf workspace
set -euo pipefail

WORKSPACE_PARENT="$HOME/.claude/skills-sync-workspace"
WORKSPACE="$WORKSPACE_PARENT/claude_conf"
REPO_SSH="git@github.com:kimen26/claude_conf.git"
REPO_HTTPS="https://github.com/kimen26/claude_conf.git"

mkdir -p "$WORKSPACE_PARENT"

if [ ! -d "$WORKSPACE/.git" ]; then
  echo "📦 Cloning claude_conf workspace..."
  if git clone "$REPO_SSH" "$WORKSPACE" 2>/dev/null; then
    echo "✅ Cloned via SSH"
  else
    echo "⚠️  SSH clone failed, trying HTTPS..."
    git clone "$REPO_HTTPS" "$WORKSPACE"
    echo "✅ Cloned via HTTPS"
  fi
else
  echo "🔄 Refreshing workspace..."
  cd "$WORKSPACE"
  git fetch origin --quiet
  git reset --hard origin/main --quiet 2>/dev/null || git reset --hard origin/master --quiet
  echo "✅ Workspace up to date"
fi

echo ""
echo "Workspace: $WORKSPACE"
