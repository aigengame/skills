---
name: gda-blender-mcp
description: Create, edit, inspect, and export 3D assets through Blender MCP for Godot, then use gda to verify import and runtime behavior. Use for Blender-to-Godot asset production, handoff, and troubleshooting.
---

# GDA Blender MCP

Use this skill as a production guide. Adapt its suggestions to the asset, the
user's choices, and the project. It adds no project policy, approval gate, or
fixed acceptance checklist. Game logic and application packaging can use their
own tool guidance.

## Choose the relevant detail

- For scale, orientation, animation, export, and engine integration, read
  [Godot asset workflow](references/godot-asset-workflow.md).
- For connection failures, execution results, or incorrect bounds, find the matching
  entry in [Troubleshooting](references/troubleshooting.md).
- For repeatable protocol calls and asset checks, use the optional
  [bundled helpers](references/bundled-helpers.md).
  Already connected MCP tools are also suitable; the client helper is not a
  prerequisite for normal work.
- For the panda case and retained manual validation evidence, read the
  [worked example](references/worked-example.md).

## Identify the implementation and intended asset

Check which Blender MCP implementation and version is in use. The incidents in
this skill concern Blender Lab's `lab/blender_mcp`; another project with the same
name can expose different tools and results. Discover the actual tools. For an
uncertain `bpy` attribute or export option, consult documentation for the running
Blender version and the specific object type.

Decide which editable source, exchange file, preview, and engine checks the task
needs. A static prop, a character with separate moving parts, and a skinned
character have different requirements. A successful connection check can
separately establish saved configuration, protocol response, tool discovery, and
execution in Blender. Repeat only the checks relevant to the current change.

## Make work easy to continue

Inspect the current file and scenes before editing. A new asset can use a separate
scene or collection; an existing asset can retain its organization. Return the
actual scene and object names so later calls can find the correct data.

Long work can have separate modeling, export, render, and inspection steps. Keep
useful scripts in the project. After a failure or timeout, inspect the remaining
state before retrying: a Python exception does not roll back Blender edits.
Resume the failed step when earlier work is usable.

Pass inputs explicitly and find Blender data again in each call. A JSON dictionary
with identifiers, output paths, and measurements is easier to reuse than a Blender
object representation. Keep large media on disk and return its path when useful.

## Deliver for Godot

Choose the exchange format to match the project. GLB conveniently groups mesh and
material resources; separate glTF resources and direct `.blend` import can also
fit an existing workflow.

Establish scale, ground contact, model front, pivots, and animation needs before
export. Select the intended asset scope, such as a character without its studio
floor. After import, inspect the actual hierarchy, appearance, and relevant motion
in Godot.

Use gda's current command help and JSON results for engine work. If the `gda` skill
is available, it provides broader CLI guidance. If project modularity needs design,
`design-godot-modular-architecture` can help when available; a small asset import
does not require a new architecture exercise.

Match validation to the requested delivery: source reopening, exchange-file
import, rendered appearance, or interaction. Record what ran and what remains
unverified. Follow project Git conventions for scripts, documentation, and Godot
text resources; in projects that use Git LFS, track binary assets there.

## Compound learning through dogfooding

Dogfooding is an option, not a required step or obligation.

Use it only when a finding is likely to change a future decision, diagnosis, or
automated check. Its reuse value should justify the cost of capture, review,
testing, and maintenance.

| Finding | Narrowest owner |
| --- | --- |
| Missing or repeated asset decision | [Godot asset workflow](references/godot-asset-workflow.md) |
| Specific failure condition and recovery | [Troubleshooting](references/troubleshooting.md) |
| Reusable automation or compatibility gap | [Bundled helpers](references/bundled-helpers.md) and a focused regression test |
| One bounded production case | [Worked example](references/worked-example.md) |

Do not add routine success, duplicates, project-specific detail, or low-information
variants. Avoid process or abstraction whose complexity is disproportionate to
its expected benefit.

Before sharing evidence, remove secrets and project-private data. Keep observations,
diagnoses, and limits distinct. Promote a lesson into shared guidance only when
the evidence supports reuse.
