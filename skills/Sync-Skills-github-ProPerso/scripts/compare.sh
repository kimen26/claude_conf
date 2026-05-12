#!/usr/bin/env bash
# compare.sh <skill> — diff local vs github for a single skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_SKILLS="$HOME/.claude/skills"
WORKSPACE="$HOME/.claude/skills-sync-workspace/claude_conf"
REMOTE_SKILLS="$WORKSPACE/skills"

if [ $# -lt 1 ]; then
  echo "Usage: compare.sh <skill_name>" >&2
  exit 1
fi

SKILL="$1"
LOCAL_DIR="$LOCAL_SKILLS/$SKILL"
REMOTE_DIR="$REMOTE_SKILLS/$SKILL"

bash "$SCRIPT_DIR/ensure-workspace.sh" > /dev/null

echo ""
echo "🔍 Diff pour '$SKILL'"
echo "  Local:  $LOCAL_DIR"
echo "  GitHub: $REMOTE_DIR"
echo ""

local_exists=0; remote_exists=0
[ -d "$LOCAL_DIR" ] && local_exists=1
[ -d "$REMOTE_DIR" ] && remote_exists=1

if [ $local_exists -eq 0 ] && [ $remote_exists -eq 0 ]; then
  echo "❌ Le skill '$SKILL' n'existe ni en local ni sur GitHub."
  exit 1
fi
if [ $local_exists -eq 0 ]; then
  echo "📥 N'existe que sur GitHub → un PULL le créera localement."
  ls -1 "$REMOTE_DIR"
  exit 0
fi
if [ $remote_exists -eq 0 ]; then
  echo "📤 N'existe que localement → un PUSH le créera sur GitHub."
  ls -1 "$LOCAL_DIR"
  exit 0
fi

# Both exist: show file-by-file diff summary
if diff -rq "$LOCAL_DIR" "$REMOTE_DIR" > /dev/null 2>&1; then
  echo "✅ Aucune différence. Skill identique."
  exit 0
fi

diff -rq "$LOCAL_DIR" "$REMOTE_DIR" 2>/dev/null | while IFS= read -r line; do
  case "$line" in
    "Only in $LOCAL_DIR"*)
      f="${line#Only in $LOCAL_DIR}"
      f="${f#: }"; f="${f#/}"
      echo "  ➕ Local uniquement: $f"
      ;;
    "Only in $REMOTE_DIR"*)
      f="${line#Only in $REMOTE_DIR}"
      f="${f#: }"; f="${f#/}"
      echo "  ➕ GitHub uniquement: $f"
      ;;
    "Files "*"differ")
      lf="$(echo "$line" | sed -E 's|Files (.*) and (.*) differ|\1|')"
      rf="$(echo "$line" | sed -E 's|Files (.*) and (.*) differ|\2|')"
      rel="${lf#$LOCAL_DIR/}"
      adds="$(diff "$rf" "$lf" 2>/dev/null | grep -c '^>' || true)"
      dels="$(diff "$rf" "$lf" 2>/dev/null | grep -c '^<' || true)"
      echo "  📝 Modifié: $rel  (+$adds / -$dels lignes — local vs github)"
      ;;
  esac
done
