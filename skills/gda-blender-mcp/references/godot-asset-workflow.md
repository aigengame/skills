# Godot asset workflow

Use the parts that affect the current asset. The panda example below supplies
concrete evidence, not a required model type or directory layout.

## Decide what the engine needs

Establish the asset's size, origin, ground contact, front direction, material
needs, animation method, and any parts the game must address by name. Reuse
information already present in the project.

The original panda used separate meshes and limb pivots, animated procedurally in
Godot. It had no skinning or baked walk clip. A character that needs retargeting,
complex deformation, or animation clips can use a skeleton and a suitable export
plan instead.

## Check the relevant connection

Blender Lab's interactive path is MCP client → stdio server → Blender extension →
running Blender. Its CLI tool also starts a background Blender process.

| Observation | Evidence it provides |
| --- | --- |
| Saved server definition | Startup information exists |
| MCP initialization and tool discovery | The protocol server responds |
| Read-only code returns Blender version and scenes | The extension reaches Blender |
| Tools appear in the current agent session | The client exposes those tools |
| CLI inspection succeeds | That background path works for its effective input file; see [P08](troubleshooting.md#p08-background-inspection-can-read-an-unsaved-snapshot) |

Do not infer one state from another. The original installation listed 26 tools;
that number is a historical observation, not a health threshold.

## Keep useful recovery points

For a new asset, a separate scene or collection helps identify task-owned data.
For existing work, inspect edits before replacing anything. Store actual names
returned by Blender rather than assuming an unsuffixed name. Restore selection,
active scene, and UI context when that helps preserve the user's editing session.

A stage result might contain `scene`, `root`, `stage`, `outputs`, and `checks`.
Use only fields the next step needs. A path in a result does not prove the file is
complete. After an export failure, inspect the asset that already exists and
resume export when appropriate. If ownership is unclear, preserve the data while
you resolve that uncertainty; cleanup is not an automatic retry step.

## Prepare and export

For assets that follow Godot/glTF conventions, Blender `-Y` is model front and
becomes Godot `+Z`. Godot camera forward is `-Z`. If the project uses another
convention, make the conversion explicit in export or a wrapper node. Check
scale, the contact plane, and pivot motion against the asset's use.
[Godot export considerations](https://docs.godotengine.org/en/4.6/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html)

Use materials the exporter can represent. Complex procedural materials may need
baking or reconstruction in Godot; the original simple PBR panda did not test
that workflow. Whether to apply transforms or modifiers depends on deformation
and animation needs, so inspect the result after those changes.

For a character-only export, select its root and descendants, or its asset
collection. Keep studio objects outside that scope. The original export used
`export_format="GLB"`, `use_selection=True`, and `export_yup=True`; it disabled
animations because that asset had none. Check the current
[Blender glTF export API](https://docs.blender.org/api/current/bpy.ops.export_scene.html)
for assets with bones, shape keys, or clips.

Preserve editable source as needed. The original task used
`bpy.data.libraries.write` to save a dedicated scene and its dependencies without
switching the user's current main file. It then reopened the saved source. Other
save operations can suit a complete working file. External textures and linked
libraries need their own dependency checks; this simple asset did not establish
that all dependencies of arbitrary `.blend` files are packed.

GLB can group mesh and texture data. Separate glTF resources can suit independent
texture editing. Direct `.blend` import invokes Blender to convert the asset to
glTF, so that import environment needs Blender installed. Explicit GLB export can
remove that dependency from engine import.
[Godot supported formats](https://docs.godotengine.org/en/4.6/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)

## Import and observe in Godot

Put the exchange asset inside the target project. For example, after replacing
the paths with actual values:

```sh
gda resource import res://content/character/character.glb \
  --project /absolute/path/to/project --json
```

Consult `gda resource import --help` for the installed version. Import can run a
project-wide pass. A copied source asset does not imply that the import cache
exists; see [P10](troubleshooting.md#p10-a-clean-godot-checkout-has-no-import-cache).

An editable character scene can instance the imported model and own movement,
collision, and game behavior outside the imported hierarchy. This helps preserve
game logic across model exports; follow the project's existing structure.

Choose checks that matter: loading, dimensions, orientation, materials, required
nodes, motion, and collision alignment. For an interactive demo, drive its relevant
actions through gda and observe the result. A successful input command with no
movement can concern the input injection path or controller, not the model.
Use gda-specific guidance to investigate it.

Inspect Blender preview and Godot rendering separately. The original engine
screenshots exposed color and presentation issues that the studio render did not
settle. That observation does not prescribe one renderer for every project.
Record relevant versions, files, measurements, and a rendered view. Hashes help
identify a file revision. Mesh counts are comparison evidence, not automatic
quality or performance thresholds. Application packaging is a separate delivery
step.

## Bundled helpers

These helpers target Blender Lab MCP. The client supports Python 3.11+ and MCP SDK
1.x; its PEP 723 script metadata pins the tested `mcp==1.29.1`. With uv available,
`uv run --script` prepares that dependency. An existing environment with the SDK
can instead run the file with its Python executable. `--help` needs no SDK.
The scripts themselves do not install dependencies or change server configuration.

The client reads one stdio definition from `--config`, defaulting to
`$CODEX_HOME/config.toml`, or `~/.codex/config.toml` when unset. `--server` defaults
to `blender`. It uses the definition's `command`, `args`, `env`, and optional
absolute `cwd`, adding explicit environment values to the caller's environment.
Arguments are passed literally, without a shell. Without `cwd`, startup uses the
caller's working directory. This is a protocol helper, not an emulator for Codex
profiles, authentication, tool permission filters, or remote transports.

Run from any directory using the actual installed skill path in place of
`/path/to/gda-blender-mcp`:

```sh
uv run --script /path/to/gda-blender-mcp/scripts/mcp_stdio_client.py probe \
  --config /absolute/path/to/config.toml --server blender \
  --receipt /absolute/path/to/results/probe-01.json
```

`probe` initializes and lists tools; it does not run code in Blender. For an
interactive asset check, create a JSON parameter file with actual names:

```json
{"scene": "Asset_Work.001", "root": "Character.001", "expected_nodes": ["Arm_L.001"]}
```

Then call the bundled inspector:

```sh
uv run --script /path/to/gda-blender-mcp/scripts/mcp_stdio_client.py execute \
  --code-file /path/to/gda-blender-mcp/scripts/inspect_blender_asset.py \
  --params-file /absolute/path/to/asset-params.json \
  --receipt /absolute/path/to/results/inspect-01.json
```

Add `--blend-file /absolute/path/to/source.blend` to use the MCP CLI tool. That
option can synchronize unsaved data before running the inspection; read
[P08](troubleshooting.md#p08-background-inspection-can-read-an-unsaved-snapshot)
when validating a disk artifact. `--config` and `--server` also apply to `execute`.
For custom code, supply another `--code-file`; its inputs are in `params` and its
output belongs in `result`, a JSON dictionary. Custom code has the side effects
it specifies. The CLI tool does not wait for deferred completion hooks.

Receipts use new paths and are never overwritten. Each records the last stage
reached, tool definitions, raw call result when available, decoded result, and
failure details. Server stderr goes to `<receipt>.stderr.log`; stdout is a short
JSON summary. Existing stderr files are also preserved. Exit 0 means protocol
probe or recognized tool execution completed; exit 1 means failure, and argument
syntax errors use exit 2. Application-specific keys in a CLI result do not define
success for the client. Custom checks can raise an exception on failure, as the
bundled inspector does. Results and server logs can contain task data, so select
what to share rather than publishing receipts automatically.

`--timeout` sets a positive, finite per-request client timeout (default 300 seconds).
It does not change server timeouts or retry the task. A timeout can leave earlier
Blender edits in place.

The inspector reads a named scene subtree, including a mesh root itself. Optional
`expected_nodes` are checked within that subtree, not the whole scene. Missing
inputs, scenes, roots, or expected nodes raise a diagnostic exception. It reports
the loaded file, Blender version, nodes, materials, mesh count, base vertices,
triangle count, unit scale, and world bounds. Shared mesh data is counted once
per object; polygons contribute `n-2` triangles. Bounds use base vertices and each
object's world matrix. It updates derived transforms in the scene's first view
layer before reading them, and reports that layer. Objects excluded from that
layer cause a diagnostic failure rather than stale bounds. Modifiers, skin deformation, and collection instances are
not evaluated or expanded. Counts can differ from exported geometry after
triangulation or vertex splitting. Inspection code does not save, delete, or
export data; the surrounding MCP CLI synchronization can write a temporary file.
