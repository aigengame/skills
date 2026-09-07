# Troubleshooting

Use an entry when its conditions match. Observed incidents, source findings, and
suggested recovery checks are labeled separately. A version-specific workaround
is not a requirement for other implementations or future versions.

## Improve troubleshooting selectively

Use the optional [dogfooding loop](../SKILL.md#compound-learning-through-dogfooding)
when a reusable failure mode is likely to save future diagnosis or recovery work.
Extend a matching entry instead of adding a low-value variant.

Keep the symptom, applicability, evidence, cause or hypothesis, recovery, check,
and limit distinct. Do not retain routine errors already explained by the tool,
project-specific mistakes, duplicate symptoms, or unverified workarounds.

When repeated evidence changes a general asset decision, update the workflow and
keep the incident evidence here.

## Find a symptom

- [P01: SDK import failure](#p01-sdk-upgrade-breaks-the-fastmcp-import)
- [P02: Configuration, paths, and tool visibility](#p02-configuration-paths-and-session-tool-visibility)
- [P03: Partial edits after a failed call](#p03-a-failed-script-leaves-geometry-in-blender)
- [P04: Repeated names select an older asset](#p04-fixed-names-can-select-an-older-generation)
- [P05: Variables and process environments](#p05-python-locals-and-environments-do-not-cross-calls)
- [P06: Inner errors and result shapes](#p06-protocol-success-does-not-prove-code-success)
- [P07: UI context in background execution](#p07-interactive-ui-context-is-unavailable-in-background-execution)
- [P08: Unsaved snapshots during file inspection](#p08-background-inspection-can-read-an-unsaved-snapshot)
- [P09: Nested timeouts](#p09-the-inner-timeout-can-expire-first)
- [P10: Godot import cache](#p10-a-clean-godot-checkout-has-no-import-cache)
- [P11: uv cache permissions](#p11-uv-cannot-prepare-its-cache)
- [P12: Crash while saving newly created scenes](#p12-partial-library-writing-crashes-in-a-background-fixture)
- [P13: Incorrect world bounds](#p13-successful-inspection-reports-incorrect-world-bounds)
- [P14: Deferred work returns too early](#p14-deferred-work-is-not-awaited-by-every-execution-path)

## Evidence baseline

The production incidents were observed on 2026-09-06 with Blender 5.2.1 LTS,
Godot 4.6.3, gda 0.14.0, and macOS on Apple M2. The server was
[Blender Lab blender_mcp](https://projects.blender.org/lab/blender_mcp) at revision
`4309a39646e644261624bfcd2bca669b343b7621`, with a local MCP dependency upper bound
added as described in P01. The working SDK was `mcp 1.29.1`.

The SDK import and partial-model failure messages below come from the production
session. The original attempt logs were replaced by successful recovery logs;
they are not presented as retained failure artifacts. The essential messages,
source locations, recovery, and limits are recorded here so the guide does not
depend on that private session. Source locations below refer to this upstream
revision unless stated otherwise.

## P01: SDK upgrade breaks the FastMCP import

**Applies when:** Startup reports the missing `mcp.server.fastmcp` module, the
source imports its `FastMCP` class, and the environment has resolved an incompatible
SDK such as 2.1.1. A dependency range that permits 2.x is not itself a failure
when the lock still resolves to a compatible release.

**Observed:** The original `mcp[cli]>=1.2.0` resolved to 2.1.1. Server startup failed
with `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`, before modeling.
The source still expected an SDK 1.x interface. This concerns the `mcp` package;
the separately distributed `fastmcp` package is not the same dependency.

**Recovery used:** The local server dependency became `mcp[cli]>=1.2.0,<2`, with
its environment and lock updated to 1.29.1. MCP initialization, discovery, live
code, GLB export, rendering, and background source inspection then passed.

**Reuse:** Compare imports, installed package version, and lock state. A compatible
range can preserve the old source. If a required feature needs a new SDK, migrate
the source and client calls, then verify the same real paths. Installing a related
package or relaxing the version bound does not perform that migration. Client
signatures also matter: the tested SDK 1 client supplies a `datetime.timedelta`
for `read_timeout_seconds`.

**Limit:** This task found no required capability blocked by SDK 1. It did not
establish that SDK 2 cannot support Blender. Inspect current source before reusing
the bound. See upstream `mcp/pyproject.toml` and the import in
`mcp/blmcp/tools/execute_blender_code.py`.

## P02: Configuration, paths, and session tool visibility

**Applies when:** A stdio argument contains literal `$HOME`, a CLI tool cannot
locate Blender, or a newly configured server is absent from the active session.

**Verified setup:** The production configuration used resolved absolute executable
and project paths. `BLENDER_PATH` identified the background executable. A real
stdio client tested the saved configuration even though the original agent tool
list did not establish that the client had reloaded it. These were setup findings,
not a claim that every listed failure occurred.

**Cause and response:** An argv array is not a shell script; `$HOME` in an argument
is not expanded by a direct process launch. Resolve it while preparing the
configuration. The interactive path connects to an already running extension;
the CLI path finds an executable through `BLENDER_PATH`, falling back to `blender`
on PATH in this source revision. Use paths from the actual machine.

Distinguish server startup, extension connection, CLI launch, and client tool
exposure. Check or repair the failing boundary. Do not repeatedly rewrite a
configuration that already passes protocol checks merely because tools have not
appeared in the session. The original extension used loopback port 9876; confirm
the current implementation and settings instead of assuming that port.

**Check:** Read the effective definition, initialize, discover tools, and run a
read-only Blender query. Check the CLI path separately when needed. The bundled
client uses MCP stdio, not a direct socket shortcut. The executable lookup is in
`mcp/blmcp/tools_helpers/blender_cli.py`.

## P03: A failed script leaves geometry in Blender

**Applies when:** Code modifies Blender data before a later step fails.

**Observed:** Geometry creation completed, then export selection used
`Object.parent_recursive`. It raised
`AttributeError: 'Object' object has no attribute 'parent_recursive'`.
The created model remained in Blender. The intended traversal was the root's
recursive children, available through `root.children_recursive`. An attribute
available on Bone or PoseBone does not imply it exists on Object.

**Recovery used:** Inspect the existing asset, correct selection to include its
root and descendants, then resume export and save. The existing user scene was
preserved. A proposed delete-by-scene-name retry was rejected by that environment's
automatic approval review because it could delete user data; continuing from the
existing geometry resolved the task. That rejection is historical context, not
a new universal approval rule for scene deletion.

**Reuse:** A caught Python exception does not roll back earlier data edits. Separate
output stages when that helps recovery. Before retrying, inspect the stage and
data that remain. Replace old data only when its ownership and the intended edit
are clear; preserve uncertain user edits while resolving that uncertainty.

**Check:** Verify the resulting file and its import, retained original data, and
absence of accidental duplicate generation from recovery. The exception return
path is in `addon/blender_mcp_addon/mcp_to_blender_server.py`, `_execute_code`.

## P04: Fixed names can select an older generation

**Evidence type:** Source finding in the original project scripts; repeated
production generation was not rerun to reproduce it.

**Applies when:** A creator always calls `bpy.data.scenes.new("Asset_Work")`, while
rendering or inspection always retrieves `bpy.data.scenes.get("Asset_Work")`.
Blender can suffix the new name when the old one exists, while lookup still
selects the old scene. Object names can acquire suffixes too.

**Reuse:** Return the actual scene and root names from creation and pass them to
later stages. Decide whether the operation creates a new revision or edits an
existing asset. This is simpler than assuming fixed names make a script safe to
repeat. The original panda generator documented one run in a fresh session;
it is not bundled as a general repeatable generator.

**Suggested check:** In an isolated file, create distinct assets with colliding
requested names. Explicitly render and inspect the second using returned names,
and confirm the first remains. The bundled inspector requires actual scene and
root names; it does not fall back to an active or similarly named object.

## P05: Python locals and environments do not cross calls

**Evidence type:** Source inspection and the production input-passing code.

**Applies when:** A later call references a previous call's local `scene` or `root`,
or expects a new server environment value inside an already running Blender.

**Cause:** The current extension executes each call in a new namespace initialized
with `{"result": {}}`. This does not clear Blender data or restart its Python
process. The MCP server and interactive Blender are separate processes.

**Reuse:** Import what each code file needs and locate Blender data from explicit
identifiers. Pass paths and other inputs with the code. The original client
injected a workspace variable into Blender code; the bundled client instead
injects a general JSON `params` dictionary without changing environment variables.

**Suggested check:** Create and query one object in separate calls, relying only on
its returned identity. Change the output parameter and check the actual output.
Both namespace setup and result processing are in the extension's `_execute_code`;
the CLI wrapper also creates a fresh execution namespace.

## P06: Protocol success does not prove code success

**Evidence type:** Current server implementation and production recovery.

**Applies when:** A caller checks only MCP `isError`, or treats any returned text
as proof that an asset was made.

**Cause:** Interactive execution catches code exceptions and can return
`{"status": "error", "message": ...}` as ordinary tool data. Interactive success
uses `{"status": "ok", "result": ...}`. The CLI tool returns the user's dictionary
directly; its code exceptions become server errors. A `status` key in that user
dictionary is not a shared MCP status field.

**Reuse:** Check the MCP result and the selected tool's known execution shape.
The bundled client keeps raw results, handles these two shapes separately, and
fails on unknown shapes. Custom CLI checks can raise an exception rather than
returning an error-shaped dictionary that still represents normal execution.
The bundled inspector follows this approach for missing scenes, roots, or nodes.

The source expects `result` to be a dictionary. Some paths convert non-JSON Blender
objects to `repr` strings. That allows transport but does not preserve an object
reference usable in the next call. Prefer actual names, numbers, paths, and useful
summaries.

**Check:** Cover successful data, code exceptions, non-dictionary returns, and
outer MCP failures. For the helper pair, a missing expected node in CLI mode should
retain diagnostics and produce a nonzero client exit. See `_execute_code` and
`mcp/blmcp/tools_helpers/blender_cli.py`.

## P07: Interactive UI context is unavailable in background execution

**Evidence type:** Source inspection; background asset inspection passed, but not
all possible background failure shapes were exercised.

**Applies when:** A script accesses `bpy.context.window.scene`, UI areas, or other
interactive context and is then sent unchanged to a background tool.

**Cause and response:** The original generator and renderer depend on a window.
That does not mean Blender CLI cannot model or render. Data inspection can use
explicit references without UI access. Choose interactive execution for code that
needs its context, or adapt the operators and verify background execution.

**Check:** Run the adapted code through the intended execution path. Confirm that
it uses the requested scene and object references without an interactive window.
A successful run in interactive Blender does not establish this property.

## P08: Background inspection can read an unsaved snapshot

**Evidence type:** Source finding; the original source-file check did not trigger
this branch.

**Applies when:** The requested `.blend` resolves to the interactive Blender's
current file, and that file has unsaved changes.

**Behavior:** `synced_blend_for_cli` saves a numbered copy containing those changes,
opens the copy in background Blender, then attempts to remove it. A read-only
inspection script therefore does not make the whole tool call free of writes.
Its success also does not prove the original disk file has the latest edits.

**Reuse:** Decide whether to check current editing state or the delivered disk
artifact. The former can use synchronization. For the latter, one approach is to
copy the delivered file to a distinct task-owned path, inspect that copy through
MCP, and record the actual loaded path and hash. Preserve resolution of relative
textures and linked libraries when relocating a file. This copy approach is a
suggested provenance check, not evidence that arbitrary external dependencies
were validated.

**Original scope:** Interactive Blender had an empty current filepath. The task
saved its dedicated scene with library writing, then inspected that separate
source file. The old inspector's `source_loaded: true` alone was weaker evidence
than an actual loaded path; the bundled inspector reports `loaded_file`.
See `synced_blend_for_cli` in `mcp/blmcp/tools_helpers/blender_cli.py`.

## P09: The inner timeout can expire first

**Evidence type:** Source finding, not an observed production render timeout.

**Applies when:** Work approaches one of the time limits along its execution path.
The examined revision uses a 300-second interactive connection timeout and a
120-second default CLI subprocess timeout. The production client also used a
300-second request timeout.

**Reuse:** Identify whether the client, extension connection, or subprocess reached
its limit. Split work where useful, use completion mechanisms that the chosen path
actually supports, or adjust the effective implementation limit within authorized
scope. Raising only the outer timeout does not change an inner limit.

**Recovery:** Check whether Blender is still working and which outputs already
exist. An interactive timeout provides no rollback guarantee. Inspect before
resubmitting; the bundled helper does not retry. A low-cost controlled task can
verify completion and timeout behavior without repeatedly regenerating an asset.
See `tools_helpers/connection.py` and `tools_helpers/blender_cli.py` under `mcp/blmcp`.

## P10: A clean Godot checkout has no import cache

**Applies when:** A copied or newly checked-out project contains GLB and scene
references but lacks the generated `.godot` cache.

**Observed:** Independent review found a cold-start failure even though the
production working directory ran successfully. The source file's presence did
not mean the engine had imported it.

**Recovery used:** The launcher ran headless editor import before starting the
game. The actual launcher then passed in an isolated copy without `.godot`.

**Reuse:** Use gda resource import or an engine import pass, inspect its result,
then run the scene. An ordinary script run does not replace import. Diagnose the
specific import error before regenerating a valid model. Import can process other
project assets too. Keep native input, export templates, and platform signing
issues in the relevant gda or platform workflow rather than attributing them to
Blender asset export.

## P11: uv cannot prepare its cache

**Applies when:** A managed environment allows project reads but the default uv
cache or project environment is outside writable paths.

**Observed:** A production call failed while preparing the uv cache, before MCP
server code ran.

**Response:** Identify the unwritable location. A task-local writable
`UV_CACHE_DIR` can address a cache restriction. A read-only check can also use an
existing virtual environment after confirming its source. Neither changes Blender
or SDK functionality. If reproducing the original configured command matters,
run that command within the permissions already available or authorized.

**Recovery used and limit:** The production run obtained the required execution
permission and retried the configured command successfully. Cache redirection is
an alternative from environment experience, not the recovery used in that run.
Confirm initialization after environment preparation; do not classify a cache
access error as a failed modeling feature.

## P12: Partial library writing crashes in a background fixture

**Observed during helper validation:** With Blender 5.2.1 LTS on this Mac, an
isolated factory-startup process created two scenes with linked mesh objects and
called `bpy.data.libraries.write` on those scenes. Blender exited with signal 11.
The crash trace passed through `BKE_view_layer_copy_data`, `scene_copy_data`, and
`bpy_lib_write`. This was a native crash during saving, not a Python exception or
a failure to start Blender. The precise engine defect was not established.

**Recovery used:** The temporary test process saved its complete working file
with `bpy.ops.wm.save_as_mainfile`, reopened it, and completed the asset checks.
The original production panda had successfully used partial library writing after
export. Thus the observed crash does not establish that all library writes fail.

**Reuse and limit:** If this save path crashes in a matching environment, preserve
the crash location and input conditions. A full save in an isolated process can
provide a test artifact. Applying that replacement to an interactive user file
would change the current file and include its other data; choose a save or copy
strategy that fits the intended source. Verify the saved artifact by reopening it.
Updating the view layer fixes the separate non-active-scene bounds issue in P13; it has not been
established here as a fix for this native save crash.

## P13: Successful inspection reports incorrect world bounds

**Applies when:** A query measures world-space geometry in a reopened, non-active
scene, or includes hidden or excluded objects whose transforms might be stale.

**Observed during helper validation:** After reopening a file
with two scenes, a child in the non-active scene had location `(3, 2, 1)` but an
identity `matrix_world`. This gave incorrect world bounds. Updating that scene's
view layer evaluated its transform and exposed the correct translation. The
inspector now updates derived transforms in the first view layer before measuring.

Independent review then found that layer membership alone was insufficient.
An object with `hide_viewport=True`, or one in a collection with that setting,
remained in `view_layer.objects` but kept an identity world matrix after update.
For a triangle at `(3, 2, 1)`, both direct and MCP inspection incorrectly reported
bounds from `(0, 0, 0)` to `(1, 1, 0)` with successful execution. The visible control
reported `(3, 2, 1)` to `(4, 3, 1)`.

The helper now checks viewport visibility in the selected layer and reports hidden
or excluded objects by name. It conservatively refuses local hiding too, although
the review's `hide_set(True)` control had correct transforms. It does not toggle
visibility in user data. Regression cases cover object, collection, and local
hiding alongside the visible control; the hidden cases produce diagnostics instead
of measurements.

**Reuse:** Update derived transforms in the selected scene's view layer before
measuring. Check which objects that layer can evaluate. If an inspection cannot
establish reliable transforms without changing authored visibility, return the
affected names and a diagnostic instead of successful measurements.

**Check:** Reopen a fixture with a non-active scene and translated children; compare
measured bounds with known coordinates. Test object, collection, and local hiding
separately, plus layer exclusion. The helper's tests require either correct visible
bounds or a diagnostic for unsupported visibility. They also check that the source
file and visibility remain unchanged.

## P14: Deferred work is not awaited by every execution path

**Evidence type:** Source inspection at the baseline revision; no delayed-work
failure was reproduced during production.

**Applies when:** A script returns an initial `result` and uses
`check_is_finished` to signal completion later.

**Cause:** The interactive extension supports that hook. The
`execute_blender_code_for_cli` wrapper only reads the synchronous `result`; it does
not wait for the hook. A separate background socket path in the extension
explicitly rejects deferred completion. Thus neither “all background calls reject
it” nor “all background calls await it” describes the examined implementation.

**Reuse:** Choose a path that supports the completion mechanism, or complete the
work synchronously before returning the CLI result. Raising a client timeout does
not add a missing completion mechanism.

**Suggested check:** Use a small task with a distinct final marker through the
chosen path. Confirm that the returned result contains that marker. An initial
dictionary alone does not prove completion. Compare
`mcp/blmcp/tools_helpers/blender_cli.py` with the extension's execution paths;
the tool docstring's broad background statement does not describe every wrapper.
