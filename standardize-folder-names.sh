#!/usr/bin/env bash
#
# standardize-folder-names.sh
#
# Standardizes top-level folder names in the repo to kebab-case.
# Example: "AI_Resume Analyzer" -> "ai-resume-analyzer"
#
# Usage:
#   ./standardize-folder-names.sh              # dry run (preview only, no changes)
#   ./standardize-folder-names.sh --apply      # actually rename (git mv, preserves history)
#
# Optional:
#   ./standardize-folder-names.sh --apply --snake path1,path2
#       -> these specific folders become snake_case instead of kebab-case
#          (use for real importable Python packages)
#
set -euo pipefail

APPLY=false
SNAKE_LIST=""
EXCLUDES=(".git" ".github" ".vscode" ".venv" "venv" "node_modules" "tests")

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=true; shift ;;
    --snake) SNAKE_LIST="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

IFS=',' read -ra SNAKE_FOLDERS <<< "$SNAKE_LIST"

is_excluded() {
  local name="$1"
  for ex in "${EXCLUDES[@]}"; do
    [[ "$name" == "$ex" ]] && return 0
  done
  return 1
}

is_snake_target() {
  local name="$1"
  for s in "${SNAKE_FOLDERS[@]}"; do
    [[ "$name" == "$s" ]] && return 0
  done
  return 1
}

to_kebab() {
  local name="$1"
  # & -> and
  name="${name//&/ and }"
  # strip apostrophes (straight + curly)
  name="$(echo "$name" | sed "s/['’]//g")"
  # brackets/parens -> space
  name="$(echo "$name" | sed 's/[][()]/ /g')"
  # underscores, dots -> space
  name="$(echo "$name" | sed 's/[_.]/ /g')"
  # anything not alnum/space/hyphen -> space
  name="$(echo "$name" | sed 's/[^a-zA-Z0-9 -]/ /g')"
  # collapse whitespace, trim
  name="$(echo "$name" | tr -s ' ' | sed 's/^ *//; s/ *$//')"
  # spaces -> hyphens
  name="${name// /-}"
  # collapse multiple hyphens, trim leading/trailing
  name="$(echo "$name" | sed 's/-\{2,\}/-/g; s/^-//; s/-$//')"
  # lowercase
  echo "$name" | tr '[:upper:]' '[:lower:]'
}

to_snake() {
  local kebab
  kebab="$(to_kebab "$1")"
  echo "${kebab//-/_}"
}

is_git_repo=false
[[ -d .git ]] && is_git_repo=true

echo "Repo path: $(pwd)"
echo "Git repo detected: $is_git_repo"
if $APPLY; then
  echo "Mode: APPLY (renaming for real)"
else
  echo "Mode: DRY RUN (preview only)"
fi
echo ""

declare -A new_name_of
declare -A old_names_seen  # new_name -> "\n"-joined list of old names, for collision detection

# Build the plan
while IFS= read -r -d '' dir; do
  old_name="$(basename "$dir")"
  is_excluded "$old_name" && continue

  if is_snake_target "$old_name"; then
    new_name="$(to_snake "$old_name")"
  else
    new_name="$(to_kebab "$old_name")"
  fi

  if [[ -z "$new_name" ]]; then
    echo "WARNING: skipping '$old_name' - normalization produced an empty name." >&2
    continue
  fi

  new_name_of["$old_name"]="$new_name"
  old_names_seen["$new_name"]+="${old_name}"$'\n'
done < <(find . -mindepth 1 -maxdepth 1 -type d -print0)

# Check collisions
collision_found=false
for new_name in "${!old_names_seen[@]}"; do
  count=$(echo -n "${old_names_seen[$new_name]}" | grep -c '.' || true)
  if [[ "$count" -gt 1 ]]; then
    collision_found=true
    echo "CONFLICT: '$new_name' <- $(echo "${old_names_seen[$new_name]}" | tr '\n' ',' | sed 's/,$//')"
  fi
done

if $collision_found; then
  echo ""
  echo "Resolve conflicts before using --apply (e.g. via --snake for one of the colliding names)."
  echo ""
fi

# Show the plan
echo "Planned renames:"
changed_count=0
for old_name in "${!new_name_of[@]}"; do
  new_name="${new_name_of[$old_name]}"
  if [[ "$old_name" != "$new_name" ]]; then
    printf "  %-55s -> %s\n" "$old_name" "$new_name"
    changed_count=$((changed_count + 1))
  fi
done
echo ""
echo "$changed_count folder(s) need renaming."

if ! $APPLY; then
  echo ""
  echo "Dry run complete. Re-run with --apply to perform these renames."
  exit 0
fi

if $collision_found; then
  echo "Aborting: fix conflicts before applying."
  exit 1
fi

# Perform renames
for old_name in "${!new_name_of[@]}"; do
  new_name="${new_name_of[$old_name]}"
  [[ "$old_name" == "$new_name" ]] && continue

  tmp_name="${new_name}.__tmp_rename__"

  if $is_git_repo; then
    git mv -- "$old_name" "$tmp_name"
    git mv -- "$tmp_name" "$new_name"
  else
    mv -- "$old_name" "$tmp_name"
    mv -- "$tmp_name" "$new_name"
  fi
  echo "Renamed: $old_name -> $new_name"
done

echo ""
echo "Done. Review 'git status' / 'git diff --stat' before committing."