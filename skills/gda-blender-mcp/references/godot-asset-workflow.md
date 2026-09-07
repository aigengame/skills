# Godot asset workflow

Adapt these decisions to the asset and its consumer. The optional
[bundled helpers](bundled-helpers.md) automate protocol calls and base-geometry
inspection. The [worked example](worked-example.md) records one production case
and the limits of retained validation evidence.

## Establish the consumer and versions

Use the project's asset requirements for size, origin, ground contact, model
front, materials, animation, and parts addressed by name. Resolve missing choices
that affect export before building detailed geometry.

Check the installed Blender, Godot, gda, and MCP implementation versions. Select
the matching release in the [Blender Python API documentation](https://docs.blender.org/api/)
and [Godot documentation](https://docs.godotengine.org/). In that release, consult
the glTF export operator, supported 3D formats, and model export considerations.
Use `gda --help` and the relevant subcommand help for the installed CLI. Default
or latest documentation can describe options absent from the consumer's version.

## Choose the exchange and animation strategy

| Requirement | Suitable starting point and check |
| --- | --- |
| One file for delivery | Export GLB and confirm the intended mesh, material, and texture data is included. |
| Independent texture or buffer editing | Use separate glTF resources and preserve their relative paths. |
| A project already imports editable Blender files | Direct `.blend` import can fit; confirm that the import environment has the Blender version needed for conversion. |
| Static prop | Export the required geometry and materials; animation data can be omitted. |
| Rigid parts moved by game code | Preserve addressable parts and useful pivots; verify their imported hierarchy and motion. |
| Deformation, retargeting, or authored clips | Plan bones, skinning, shape keys, and clips as required; check the exporter options and imported animation behavior. |

These choices can be combined. A single character can contain skinned geometry
and rigid attachments. Do not disable animation merely because another asset did
not need it.

## Check the execution path you need

For Blender Lab MCP, the interactive path connects the stdio server to an
extension in running Blender. Its CLI tool starts a background Blender process.
Other implementations can expose different tools or results.

| Observation | Evidence it provides |
| --- | --- |
| Saved server definition | Startup information exists. |
| MCP initialization and tool discovery | The protocol server responds. |
| Read-only code returns Blender version and scenes | The selected execution path reaches Blender. |
| Tools appear in the current agent session | The agent client exposes those tools. |
| CLI inspection reports its loaded file | The background path inspected that effective input; see [P08](troubleshooting.md#p08-background-inspection-can-read-an-unsaved-snapshot). |

Check the boundary affected by the current change. A protocol probe alone does
not establish that the extension can execute Blender code.

## Edit with useful recovery points

For a new asset, a separate scene or collection helps identify task-owned data.
For existing work, inspect edits before replacing anything. Return the actual
scene and object names, including suffixes, and pass those names to later calls.
Restore selection and active context when needed to preserve the editing session.

Separate modeling, export, and inspection when this makes failures easier to
recover from. A stage result can contain identifiers, output paths, and checks
needed by the next step. A path alone does not prove that a file is complete.
After an export failure, inspect the existing asset and resume export if the
geometry is usable. A caught exception does not roll back earlier edits. Preserve
data whose ownership is unclear while resolving that uncertainty.

## Prepare the export scope and transforms

For Godot/glTF conventions, Blender `-Y` model front becomes Godot `+Z`; Godot
camera forward is `-Z`. If the project uses another convention, make the conversion
explicit in export or a wrapper node. Check scale, the contact plane, and pivot
motion against the asset's use.

Select the intended asset root and descendants, or its asset collection. Keep
studio objects outside that scope unless the task requires them. Verify the
actual selection before using a selection-only export option. Use materials the
exporter can represent. Bake or reconstruct procedural effects when necessary.
Whether to apply transforms or modifiers depends on deformation and animation;
inspect the exported result after those changes.

## Preserve editable source

Choose a save method for the intended source scope:

- Save a complete working file when the whole file belongs to the deliverable.
- Use a save-copy operation when the active editing file should remain in place;
  check that operation's behavior for the running Blender version.
- Write selected datablocks and their dependencies when a dedicated asset source
  is needed. Reopen the result and verify that it contains the required data.

Check external textures and linked libraries separately; a successful save does
not establish that dependencies are packed. If a save crashes, record the exact
path and input conditions before choosing a recovery. [P12](troubleshooting.md#p12-partial-library-writing-crashes-in-a-background-fixture)
records one partial-library-write crash and its bounded recovery.

## Import and integrate

Put the exchange asset inside the target project. After checking the installed
`gda resource import --help`, a GLB import can use:

```sh
gda resource import res://content/character/character.glb \
  --project /absolute/path/to/project --json
```

Inspect the JSON result. Import can run a project-wide pass. A copied source does
not imply that its generated import cache exists; see
[P10](troubleshooting.md#p10-a-clean-godot-checkout-has-no-import-cache).

An editable character scene can instance the imported model and own movement,
collision, and game behavior outside the imported hierarchy. This helps preserve
game logic across exports. Follow the project's existing structure.

## Match validation to the delivery

| Layer | Useful evidence | What it leaves open |
| --- | --- | --- |
| Editable source | Reopened file, effective path, required objects and dependencies | Export and engine behavior |
| Exchange asset | Exported scope, geometry, materials, and animation data | Godot import and appearance |
| Engine import and load | Successful import, instantiated hierarchy, dimensions, and required nodes | Rendered appearance and interaction |
| Engine rendering | Captured view under the target renderer and lighting | Controller response and gameplay |
| Interaction | Relevant input followed by observed movement, animation, or collision response | Other actions and delivery platforms |

For an interactive demo, drive the relevant actions through gda and observe the
result. Successful input with no movement can indicate a problem in the input
injection path or controller. Use gda-specific guidance to investigate it.
Inspect Blender previews and Godot rendering separately because their materials,
lighting, and presentation can differ.

Record the checks that ran, their relevant versions and file revisions, and the
remaining unverified behavior. Hashes identify revisions; mesh counts support
comparisons. Neither is an automatic quality or performance threshold. Application
packaging is a separate delivery step.

## Evolve the workflow selectively

Use the optional [dogfooding loop](../SKILL.md#compound-learning-through-dogfooding)
when real work exposes a reusable decision gap whose expected value justifies
shared maintenance.

Start with bounded evidence in troubleshooting or a worked example. Promote the
smallest decision rule only after repeated evidence or a stable tool or engine
contract supports it.

Do not add routine success, a project-specific choice, or a speculative branch.
