# Worked example and retained evidence

This is historical evidence from 2026-09-06, not a model template or an acceptance
checklist. Use the [workflow](godot-asset-workflow.md) for reusable decisions and
[troubleshooting](troubleshooting.md) for the detailed failure conditions.

## Panda production choices

The task required a controllable cartoon panda in a Godot bamboo scene. Separate
meshes and limb pivots supported procedural movement in Godot, so this asset did
not need skinning or a baked walk clip. Simple PBR materials avoided a procedural
texture-baking step.

The export selected the character root and descendants, excluding the studio.
It used `export_format="GLB"`, `use_selection=True`, and `export_yup=True`, with
animation export disabled because the asset had no clips. A dedicated scene and
its dependencies were saved with `bpy.data.libraries.write`, then reopened. That
successful save does not generalize to every scene or dependency arrangement;
[P12](troubleshooting.md#p12-partial-library-writing-crashes-in-a-background-fixture)
records a later crash with another fixture.

Inspection reported 33 mesh objects, 19,696 base vertices, 39,232 triangles, and
four requested limb pivots. These are measurements of that revision, not targets
for other characters. Blender preview and Godot screenshots led to presentation
adjustments during the original demo task. That task's rendered and gameplay
observations were manual; their media and demo are not bundled with this skill.
They are not a reproducible rendered or gameplay acceptance result for this PR.

## Separate helper integration fixture

A smaller manual check tested the MCP-to-Godot boundary. Through the configured
MCP stdio server, code created two scenes with colliding requested names. The
second asset contained an empty root and two translated triangle meshes. A studio
object was outside its subtree. The code saved a complete temporary `.blend` file
and exported the second subtree to GLB in a path containing spaces. gda imported
the GLB into a clean temporary Godot project. A strict engine script loaded and
instantiated it, found two meshes, and found no `SkillStudioExcluded` object.

The environment was Blender 5.2.1 LTS, Godot 4.6.3, gda 0.14.0, MCP SDK 1.29.1,
and macOS on Apple M2. Blender Lab MCP was at
`4309a39646e644261624bfcd2bca669b343b7621`, with the local server dependency bound
recorded in [P01](troubleshooting.md#p01-sdk-upgrade-breaks-the-fastmcp-import).

The following blocks are selected fields from retained local JSON outputs, not
complete receipts or an automated test report. Only the two absolute output paths
in the MCP excerpt were replaced with `<fixture-directory>`. Configuration,
server tool definitions, raw MCP content, and generated-file inventories are
omitted. The GLB and full logs remain local and are not required skill resources.
These excerpts let a reader inspect the reported observations; they do not make
the original integration run reproducible from the repository alone.

### MCP export result

```json
{
  "operation": "execute",
  "ok": true,
  "stage": "completed",
  "mcp_sdk": "1.29.1",
  "result": {
    "first": {
      "scene": "SkillAsset",
      "root": "SkillRoot"
    },
    "second": {
      "scene": "SkillAsset.001",
      "root": "SkillRoot.001",
      "expected_nodes": [
        "SkillPart",
        "SkillPart.001"
      ]
    },
    "blend": "<fixture-directory>/fixture.blend",
    "glb": "<fixture-directory>/asset.glb"
  }
}
```

### gda import result

```json
{
  "dry_run": false,
  "engine_pass": true,
  "assets": [
    {
      "path": "res://asset.glb",
      "status": "imported",
      "sidecar": "res://asset.glb.import",
      "dest_files": [
        "res://.godot/imported/asset.glb-902bf56c04f0e336e0138854afb3ec39.scn"
      ]
    }
  ],
  "summary": {
    "requested": 1,
    "cached": 0,
    "missing": 0,
    "stale": 0,
    "invalid": 0,
    "imported": 1,
    "not_importable": 0,
    "failed": 0,
    "created_cache_owned": 8,
    "created_source_adjacent": 2
  }
}
```

### Godot load and scope check

```json
{
  "path": "res://inspect.gd",
  "exit_status": 0,
  "stdout": "Godot Engine v4.6.3.stable.official.7d41c59c4 - https://godotengine.org\n\n{\"mesh_count\":2,\"root_name\":\"SkillAsset_001\",\"studio_excluded\":true}\nSKILL_IMPORT_COMPLETE\n",
  "stderr": "",
  "stdout_truncated": false,
  "diagnostics": []
}
```

The script loaded `res://asset.glb` as a `PackedScene`, instantiated it, counted
`MeshInstance3D` descendants, and checked for the excluded studio name. It emitted
`SKILL_IMPORT_COMPLETE` only after those checks. The GLB used for this run had
SHA-256 `57bbb646bf3c9583a7d12d739f90fe670c3e97a46ba51f321af73f54841986b1`;
this identifies the retained file but does not replace the checks.

## Validation boundary

The manual fixture established export, clean import, loading, and that specific
hierarchy check. It did not render the model, drive a controller, evaluate skinning
or clips, or establish appearance and gameplay acceptance. The repository's
optional real-Blender test separately checks the inspector in a fresh background
process. It does not connect through MCP or run Godot. Repeat the relevant engine
and player checks when a consumer asset or its requirements change.

## Promote lessons selectively

Use the optional [dogfooding loop](../SKILL.md#compound-learning-through-dogfooding)
when an example adds evidence that the skill does not already represent. Do not
add routine runs or low-information variants.

If later evidence confirms a reusable decision, failure mode, or helper gap, move
the narrow lesson to its owning reference. Keep this case as provenance rather
than duplicating the guidance here.
