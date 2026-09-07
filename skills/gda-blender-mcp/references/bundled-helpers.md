# Bundled helpers

These helpers target Blender Lab MCP. The client requires Python 3.11+ and exactly
`mcp==1.29.1`. Its PEP 723 script metadata pins that dependency. With uv available,
`uv run --script` prepares it. An existing environment with that exact SDK version
can instead run the file with its Python executable. `--help` needs no SDK.
The scripts themselves do not install dependencies or change server configuration.

This client constraint is separate from the server dependency workaround in
[P01](troubleshooting.md#p01-sdk-upgrade-breaks-the-fastmcp-import). SDK 1.2.0
was tested with an earlier helper and failed because `stdio_client` did not
accept `errlog`; its `list_tools` also lacked cursor support. No wider client
compatibility interval has been established. The helper now rejects other
versions before loading server configuration or starting a server, and records
the installed version with a diagnostic.

## Configuration and invocation

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
it specifies. The CLI tool does not wait for deferred completion hooks; see
[P14](troubleshooting.md#p14-deferred-work-is-not-awaited-by-every-execution-path).

## Results and failures

Receipts use new paths and are never overwritten. Each records the operation,
success state, and last stage reached. Other fields depend on progress: server
information follows initialization, tool definitions follow discovery, and raw
and decoded execution results appear only after their corresponding stages. A
probe has no execution result. Failure details appear when an operation fails;
an early failure can have no server information or tool definitions. Server stderr goes to `<receipt>.stderr.log`; stdout is a short
JSON summary. Existing stderr files are also preserved. Exit 0 means protocol
probe or recognized tool execution completed; exit 1 means failure, and argument
syntax errors use exit 2. Application-specific keys in a CLI result do not define
success for the client. Custom checks can raise an exception on failure, as the
bundled inspector does. Results and server logs can contain task data, so select
what to share rather than publishing receipts automatically.

`--timeout` sets a positive, finite per-request client timeout (default 300 seconds).
It does not change server timeouts or retry the task. A timeout can leave earlier
Blender edits in place.

## Asset inspector

The inspector reads a named scene subtree, including a mesh root itself. Optional
`expected_nodes` are checked within that subtree, not the whole scene. Missing
inputs, scenes, roots, or expected nodes raise a diagnostic exception. It reports
the loaded file, Blender version, nodes, materials, mesh count, base vertices,
triangle count, unit scale, and world bounds. Shared mesh data is counted once
per object; polygons contribute `n-2` triangles. Bounds use base vertices and each
object's world matrix. It updates derived transforms in the scene's first view
layer before reading them, and reports that layer. It conservatively requires
viewport visibility for all objects in the subtree. Excluded objects, viewport
disabling on an object or collection, and local hiding cause a diagnostic failure
that names the objects. The helper does not change visibility to obtain bounds.
Modifiers, skin deformation, and collection instances are
not evaluated or expanded. Counts can differ from exported geometry after
triangulation or vertex splitting. Inspection code does not save, delete, or
export data; the surrounding MCP CLI synchronization can write a temporary file.

For the observed stale-transform and visibility cases, see
[P13](troubleshooting.md#p13-successful-inspection-reports-incorrect-world-bounds).
