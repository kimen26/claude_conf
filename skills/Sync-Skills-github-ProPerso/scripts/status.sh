#!/usr/bin/env bash
# status.sh — show sync status of all local skills vs github
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

is_private() {
  local skill="$1"
  for p in "${PRIVATE_SKILLS[@]}"; do
    [ "$p" = "$skill" ] && return 0
  done
  return 1
}

bash "$SCRIPT_DIR/ensure-workspace.sh" > /dev/null
echo ""
printf "%-30s %-12s %-12s %s\n" "SKILL" "LOCAL" "GITHUB" "ÉTAT"
printf "%-30s %-12s %-12s %s\n" "------------------------------" "------------" "------------" "----"

declare -A seen
for dir in "$LOCAL_SKILLS"/*/; do
  [ -d "$dir" ] || continue
  skill="$(basename "$dir")"
  seen[$skill]=1

  if is_private "$skill"; then
    local_date="$(date -r "$dir" '+%Y-%m-%d' 2>/dev/null || echo 'n/a')"
    printf "%-30s %-12s %-12s %s\n" "$skill" "$local_date" "—" "🔒 PRIVÉ"
    continue
  fi

  local_date="$(date -r "$dir" '+%Y-%m-%d' 2>/dev/null || echo 'n/a')"
  remote_dir="$REMOTE_SKILLS/$skill"

  if [ ! -d "$remote_dir" ]; then
    printf "%-30s %-12s %-12s %s\n" "$skill" "$local_date" "—" "⚪ Manquant sur GitHub"
    continue
  fi

  remote_date="$(date -r "$remote_dir" '+%Y-%m-%d' 2>/dev/null || echo 'n/a')"

  if diff -rq "$dir" "$remote_dir" > /dev/null 2>&1; then
    printf "%-30s %-12s %-12s %s\n" "$skill" "$local_date" "$remote_date" "✅ Identique"
  else
    if [ "$dir" -nt "$remote_dir" ]; then
      printf "%-30s %-12s %-12s %s\n" "$skill" "$local_date" "$remote_date" "🟡 Local plus récent"
    else
      printf "%-30s %-12s %-12s %s\n" "$skill" "$local_date" "$remote_date" "🔵 GitHub plus récent"
    fi
  fi
done

# Skills présents sur GitHub mais absents localement
for dir in "$REMOTE_SKILLS"/*/; do
  [ -d "$dir" ] || continue
  skill="$(basename "$dir")"
  if [ -z "${seen[$skill]:-}" ]; then
    remote_date="$(date -r "$dir" '+%Y-%m-%d' 2>/dev/null || echo 'n/a')"
    printf "%-30s %-12s %-12s %s\n" "$skill" "—" "$remote_date" "🟢 Nouveau sur GitHub"
  fi
done
