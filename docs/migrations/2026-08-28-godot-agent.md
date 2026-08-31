# Initial skill history migration

This document records the initial catalog migration for [issue #2](https://github.com/aigengame/skills/issues/2).

## Source and scope

- Source repository: `https://github.com/aigengame/godot-agent.git`
- Pinned source commit: `04d3e089b32330aeffc7da98f4824bb21873c2b3`
- Source catalog path: `.agents/skills/`
- Historical catalog path: `.claude/skills/`
- Source catalog tree: `130cc305354d03daedfac1c7e0573eb2be4b2ab5`
- Target base commit: `6ad2baf0504e2f83b3a4a87516c3cefdfb5c2ad0`
- Filtered history head: `5ad58046b58266a878f6ccd540115878b5c2b9bc`
- Import merge commit: `0089fffa0668d801b243154a50c6a929952dbe31`

The migration moved both source paths to the repository root. It did not import product paths or source tags. It changed bare issue and pull request references in imported commit messages from `#N` to `aigengame/godot-agent#N`. It did not rewrite file content.

## Reproduction commands

The migration used `git-filter-repo` 2.47.0. The following commands reproduce the history filter without `--force`:

```sh
SOURCE_URL=https://github.com/aigengame/godot-agent.git
SOURCE_COMMIT=04d3e089b32330aeffc7da98f4824bb21873c2b3
TARGET_URL=https://github.com/aigengame/skills.git
TARGET_BASE=6ad2baf0504e2f83b3a4a87516c3cefdfb5c2ad0
FILTERED_HEAD=5ad58046b58266a878f6ccd540115878b5c2b9bc
IMPORT_COMMIT=0089fffa0668d801b243154a50c6a929952dbe31
MIGRATION_ROOT="$(mktemp -d)"

git clone --no-tags --single-branch --branch main \
  "$SOURCE_URL" "$MIGRATION_ROOT/source"

git init --bare "$MIGRATION_ROOT/pinned.git"
git --git-dir="$MIGRATION_ROOT/pinned.git" fetch --no-tags \
  "$MIGRATION_ROOT/source" \
  "$SOURCE_COMMIT:refs/heads/filtered-history"
git --git-dir="$MIGRATION_ROOT/pinned.git" symbolic-ref \
  HEAD refs/heads/filtered-history

git clone --no-tags --single-branch --branch filtered-history \
  "$MIGRATION_ROOT/pinned.git" "$MIGRATION_ROOT/filtered"

cd "$MIGRATION_ROOT/filtered"
UV_CACHE_DIR="$MIGRATION_ROOT/uv-cache" \
UV_TOOL_DIR="$MIGRATION_ROOT/uv-tools" \
uvx --from 'git-filter-repo==2.47.0' git-filter-repo \
  --path .agents/skills/ \
  --path .claude/skills/ \
  --path-rename .agents/skills/: \
  --path-rename .claude/skills/: \
  --message-callback \
  'return re.sub(br"(?<![\w/#])#([0-9]+)\b", br"aigengame/godot-agent#\1", message)'
```

The following commands join the filtered history to the existing target history:

```sh
git clone --no-tags --single-branch --branch main \
  "$TARGET_URL" "$MIGRATION_ROOT/target"
git -C "$MIGRATION_ROOT/target" cat-file -e "$TARGET_BASE^{commit}"
git -C "$MIGRATION_ROOT/target" switch \
  -c codex/import-shared-skill-history "$TARGET_BASE"
git -C "$MIGRATION_ROOT/target" remote add filtered "$MIGRATION_ROOT/filtered"
git -C "$MIGRATION_ROOT/target" fetch filtered filtered-history
git -C "$MIGRATION_ROOT/target" merge \
  --allow-unrelated-histories --no-ff --no-commit \
  filtered/filtered-history
git -C "$MIGRATION_ROOT/target" commit \
  -m "feat: import shared skill history"

REPRODUCED_IMPORT="$(git -C "$MIGRATION_ROOT/target" rev-parse HEAD)"
test "$(git -C "$MIGRATION_ROOT/target" rev-parse "$REPRODUCED_IMPORT^1")" = \
  "$TARGET_BASE"
test "$(git -C "$MIGRATION_ROOT/target" rev-parse "$REPRODUCED_IMPORT^2")" = \
  "$FILTERED_HEAD"
```

## Merge requirement

Use **Create a merge commit** to merge the migration pull request. Do not use a
squash or rebase merge. Those methods do not make the filtered history an
ancestor of `main`.

After the merge, make a fresh clone of `main` and run this required
reachability check:

```sh
git clone --no-tags --single-branch --branch main \
  "$TARGET_URL" "$MIGRATION_ROOT/post-merge"
git -C "$MIGRATION_ROOT/post-merge" merge-base --is-ancestor \
  "$FILTERED_HEAD" HEAD
```

A zero exit status confirms that the filtered history is reachable from
`main`. This result is required for a valid migration.

## Recorded evidence

| Check | Result |
| --- | --- |
| Current catalog directories | 13 |
| Current catalog files | 23 |
| Source catalog tree | `130cc305354d03daedfac1c7e0573eb2be4b2ab5` |
| Filtered catalog tree | `130cc305354d03daedfac1c7e0573eb2be4b2ab5` |
| Retained filtered commits | 29 |
| Retained commits with changed author or committer metadata | 0 |
| Imported tags | 0 |
| Bare `#N` references in imported commit messages | 0 |
| Qualified `aigengame/godot-agent#N` occurrences | 29 across 27 commits |
| `quick_validate.py` results | 13 of 13 valid |
| `git fsck --full --strict` | Pass |

The four commits that touched `.claude/skills/` are present in the source history. Their non-empty skill changes remain inspectable in the filtered history. The path-neutral rename commit became empty after both source prefixes were moved to the same root and was pruned by the default filter behavior.

Historical paths contain the current skill directories and the former `evidence-driven-architecture-design` skill name. They contain no unrelated product path.

## Validation commands

```sh
git -C "$MIGRATION_ROOT/source" rev-parse \
  "$SOURCE_COMMIT:.agents/skills"
git -C "$MIGRATION_ROOT/filtered" rev-parse HEAD^{tree}
git -C "$MIGRATION_ROOT/filtered" rev-list --count HEAD
git -C "$MIGRATION_ROOT/filtered" tag --list
git -C "$MIGRATION_ROOT/filtered" fsck --full --strict

git -C "$MIGRATION_ROOT/filtered" log \
  --format='%H %s%n%b' HEAD | \
  rg --pcre2 '(?<![\w/#])#[0-9]+\b'

git -C "$MIGRATION_ROOT/filtered" rev-list --objects HEAD | \
  awk 'NF > 1 {print $2}' | cut -d/ -f1 | sort -u

git clone --no-tags --single-branch \
  --branch codex/import-shared-skill-history \
  "$TARGET_URL" "$MIGRATION_ROOT/fresh-target"
git -C "$MIGRATION_ROOT/fresh-target" rev-parse HEAD
git -C "$MIGRATION_ROOT/fresh-target" fsck --full --strict
git -C "$MIGRATION_ROOT/fresh-target" tag --list

test "$(git -C "$MIGRATION_ROOT/fresh-target" rev-parse "$IMPORT_COMMIT^1")" = \
  "$TARGET_BASE"
test "$(git -C "$MIGRATION_ROOT/fresh-target" rev-parse "$IMPORT_COMMIT^2")" = \
  "$FILTERED_HEAD"
git -C "$MIGRATION_ROOT/fresh-target" merge-base --is-ancestor \
  "$FILTERED_HEAD" "$IMPORT_COMMIT"

CATALOG_DIRS="artifact-review design-domain-modular-architecture \
design-godot-modular-architecture design-verifiable-playtest entropy-review \
git-conventional-commits handle-review pitfalls reconcile skill-review state \
subagent-worktree-parallel validation-driven-design"
git -C "$MIGRATION_ROOT/fresh-target" ls-tree HEAD -- $CATALOG_DIRS | \
  git -C "$MIGRATION_ROOT/fresh-target" mktree
git -C "$MIGRATION_ROOT/fresh-target" ls-tree -d --name-only HEAD -- \
  $CATALOG_DIRS | wc -l
git -C "$MIGRATION_ROOT/fresh-target" ls-tree -r --name-only HEAD -- \
  $CATALOG_DIRS | wc -l
git -C "$MIGRATION_ROOT/fresh-target" diff --check "$TARGET_BASE...HEAD"

QUICK_VALIDATE="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
test "$(shasum -a 256 "$QUICK_VALIDATE" | awk '{print $1}')" = \
  1fd66498c219616fd9249eacdf16c458412ea9065a9d887fd716aeef03907762
for skill_dir in $CATALOG_DIRS; do
  UV_CACHE_DIR="$MIGRATION_ROOT/validation-uv-cache" \
  UV_TOOL_DIR="$MIGRATION_ROOT/validation-uv-tools" \
  uvx --with pyyaml python "$QUICK_VALIDATE" \
    "$MIGRATION_ROOT/fresh-target/$skill_dir"
done

mapped=0
metadata_mismatches=0
while read -r old_commit new_commit; do
  if [ "$old_commit" = old ] || \
     [ "$new_commit" = 0000000000000000000000000000000000000000 ]; then
    continue
  fi
  mapped=$((mapped + 1))
  source_metadata="$(git -C "$MIGRATION_ROOT/source" show -s \
    --format='%an|%ae|%aI|%cn|%ce|%cI' "$old_commit")"
  filtered_metadata="$(git -C "$MIGRATION_ROOT/filtered" show -s \
    --format='%an|%ae|%aI|%cn|%ce|%cI' "$new_commit")"
  if [ "$source_metadata" != "$filtered_metadata" ]; then
    metadata_mismatches=$((metadata_mismatches + 1))
  fi
done < "$MIGRATION_ROOT/filtered/.git/filter-repo/commit-map"
test "$mapped" -eq 29
test "$metadata_mismatches" -eq 0

qualified_occurrences="$(git -C "$MIGRATION_ROOT/filtered" log \
  --format='%H %s%n%b' HEAD | \
  rg -o 'aigengame/godot-agent#[0-9]+' | wc -l | tr -d ' ')"
qualified_commits=0
for commit_id in $(git -C "$MIGRATION_ROOT/filtered" rev-list HEAD); do
  if git -C "$MIGRATION_ROOT/filtered" show -s --format='%B' "$commit_id" | \
     rg -q 'aigengame/godot-agent#[0-9]+'; then
    qualified_commits=$((qualified_commits + 1))
  fi
done
test "$qualified_occurrences" -eq 29
test "$qualified_commits" -eq 27
```

The target catalog tree command must return
`130cc305354d03daedfac1c7e0573eb2be4b2ab5`. The bare-reference search must
return no matches. An empty tag list is the expected result.

The metadata loop compares the raw author and committer name, email address,
and timestamp for every non-zero mapping in
`.git/filter-repo/commit-map`. All 29 retained commits matched their source
metadata.
