# Initial skill history migration

This document records the initial catalog migration for [issue #2](https://github.com/aigengame/skills/issues/2).

## Source and scope

- Source repository: `https://github.com/aigengame/godot-agent.git`
- Pinned source commit: `04d3e089b32330aeffc7da98f4824bb21873c2b3`
- Source catalog path: `.agents/skills/`
- Historical catalog path: `.claude/skills/`
- Source catalog tree: `130cc305354d03daedfac1c7e0573eb2be4b2ab5`
- Filtered history head: `5ad58046b58266a878f6ccd540115878b5c2b9bc`
- Import merge commit: `0089fffa0668d801b243154a50c6a929952dbe31`

The migration moved both source paths to the repository root. It did not import product paths or source tags. It changed bare issue and pull request references in imported commit messages from `#N` to `aigengame/godot-agent#N`. It did not rewrite file content.

## Reproduction commands

The migration used `git-filter-repo` 2.47.0. The following commands reproduce the history filter without `--force`:

```sh
SOURCE_URL=https://github.com/aigengame/godot-agent.git
SOURCE_COMMIT=04d3e089b32330aeffc7da98f4824bb21873c2b3
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
  https://github.com/aigengame/skills.git "$MIGRATION_ROOT/target"
git -C "$MIGRATION_ROOT/target" switch -c codex/import-shared-skill-history
git -C "$MIGRATION_ROOT/target" remote add filtered "$MIGRATION_ROOT/filtered"
git -C "$MIGRATION_ROOT/target" fetch filtered filtered-history
git -C "$MIGRATION_ROOT/target" merge \
  --allow-unrelated-histories --no-ff --no-commit \
  filtered/filtered-history
git -C "$MIGRATION_ROOT/target" commit \
  -m "feat: import shared skill history"
```

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
| Qualified `aigengame/godot-agent#N` references | 27 |
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

CATALOG_DIRS="artifact-review design-domain-modular-architecture \
design-godot-modular-architecture design-verifiable-playtest entropy-review \
git-conventional-commits handle-review pitfalls reconcile skill-review state \
subagent-worktree-parallel validation-driven-design"
git -C "$MIGRATION_ROOT/target" ls-tree HEAD -- $CATALOG_DIRS | \
  git -C "$MIGRATION_ROOT/target" mktree

QUICK_VALIDATE=/path/to/skill-creator/scripts/quick_validate.py
for skill_dir in $CATALOG_DIRS; do
  UV_CACHE_DIR="$MIGRATION_ROOT/validation-uv-cache" \
  UV_TOOL_DIR="$MIGRATION_ROOT/validation-uv-tools" \
  uvx --with pyyaml python "$QUICK_VALIDATE" \
    "$MIGRATION_ROOT/target/$skill_dir"
done
```

The target catalog tree command must return
`130cc305354d03daedfac1c7e0573eb2be4b2ab5`. The bare-reference search must
return no matches. An empty tag list is the expected result.

The migration also compared the author and committer name, email address, and
timestamp for every non-empty entry in
`.git/filter-repo/commit-map`. All 29 retained commits matched their source
metadata.
