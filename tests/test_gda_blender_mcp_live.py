"""Optional real-Blender regression: set BLENDER_TEST_EXECUTABLE to opt in.

The test uses a fresh background process and temporary files. It does not connect
to an interactive Blender or require an MCP server. Protocol integration is a
separate validation path.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

BLENDER = os.environ.get("BLENDER_TEST_EXECUTABLE")
INSPECTOR = (
    Path(__file__).resolve().parents[1]
    / "skills/gda-blender-mcp/scripts/inspect_blender_asset.py"
)


@unittest.skipUnless(BLENDER, "Set BLENDER_TEST_EXECUTABLE for real Blender validation")
class BlenderInspectorTests(unittest.TestCase):
    def test_reopened_non_active_scene_bounds_and_scope(self):
        with tempfile.TemporaryDirectory(prefix="skill asset spaces ") as directory:
            folder = Path(directory)
            script = folder / "check.py"
            setup = f"import runpy\nfrom pathlib import Path\nfolder = Path({str(folder)!r})\ninspect_asset = runpy.run_path({str(INSPECTOR)!r})['inspect_asset']\n"
            script.write_text(
                setup
                + """
import bpy
first = bpy.data.scenes.new('Asset')
second = bpy.data.scenes.new('Asset')
mesh = bpy.data.meshes.new('Triangle')
mesh.from_pydata([(0,0,0), (1,0,0), (0,1,0)], [], [(0,1,2)])
mesh.update()
a = bpy.data.objects.new('Root', mesh)
first.collection.objects.link(a)
b = bpy.data.objects.new('Root', None)
second.collection.objects.link(b)
children = []
for index in range(2):
    child = bpy.data.objects.new('Part', mesh)
    second.collection.objects.link(child)
    child.parent = b
    child.location = (3+index, 2, 1)
    children.append(child)
extra = bpy.data.objects.new('Studio', mesh)
second.collection.objects.link(extra)
extra.location = (100,100,100)
pa = {'scene':first.name, 'root':a.name}
pb = {'scene':second.name, 'root':b.name, 'expected_nodes':[c.name for c in children]}
hidden_cases = []
for mode in ['ObjectHidden', 'CollectionHidden', 'LocallyHidden']:
    obj = bpy.data.objects.new(mode, mesh)
    collection = bpy.data.collections.new(mode)
    second.collection.children.link(collection)
    collection.objects.link(obj)
    obj.location = (-6, 4, 2)
    if mode == 'ObjectHidden':
        obj.hide_viewport = True
    elif mode == 'CollectionHidden':
        collection.hide_viewport = True
    else:
        second.view_layers[0].update()
        obj.hide_set(True, view_layer=second.view_layers[0])
    hidden_cases.append(obj.name)
path = folder/'fixture.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(path))
bpy.ops.wm.open_mainfile(filepath=str(path))
before = path.read_bytes()
first_result = inspect_asset(pa)
second_result = inspect_asset(pb)
assert first_result['mesh_objects'] == 1 and first_result['vertices'] == 3
assert second_result['mesh_objects'] == 2 and second_result['vertices'] == 6
assert second_result['triangles'] == 2
assert second_result['world_bounds'] == {'min':[3.0,2.0,1.0], 'max':[5.0,3.0,1.0]}, second_result
assert 'Studio' not in [n['name'] for n in second_result['nodes']]
assert second_result['loaded_file'] == str(path)
assert path.read_bytes() == before
for name in hidden_cases:
    obj = bpy.data.scenes[pb['scene']].objects[name]
    layer = bpy.data.scenes[pb['scene']].view_layers[0]
    visibility = (obj.hide_viewport, obj.hide_get(view_layer=layer),
                  tuple(c.hide_viewport for c in obj.users_collection))
    try:
        inspect_asset({'scene':pb['scene'], 'root':name})
    except ValueError as error:
        assert 'hidden' in str(error) and name in str(error)
    else:
        raise AssertionError('Hidden object returned measurements: ' + name)
    assert visibility == (obj.hide_viewport, obj.hide_get(view_layer=layer),
                          tuple(c.hide_viewport for c in obj.users_collection))
assert path.read_bytes() == before
try:
    inspect_asset({**pb, 'expected_nodes':['Missing']})
except ValueError as error:
    assert 'Expected nodes missing' in str(error)
else:
    raise AssertionError('Missing node was accepted')
scene = bpy.data.scenes[pb['scene']]
obj = scene.objects[pb['expected_nodes'][0]]
hidden = bpy.data.collections.new('Hidden')
scene.collection.children.link(hidden)
scene.collection.objects.unlink(obj)
hidden.objects.link(obj)
scene.view_layers[0].layer_collection.children[hidden.name].exclude = True
try:
    inspect_asset(pb)
except ValueError as error:
    assert 'excluded' in str(error)
else:
    raise AssertionError('Excluded object was accepted for bounds')
print('BLENDER_SKILL_REGRESSION_PASSED')
"""
            )
            completed = subprocess.run(
                [
                    BLENDER,
                    "--background",
                    "--factory-startup",
                    "--python-exit-code",
                    "1",
                    "--python",
                    str(script),
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                completed.returncode, 0, completed.stdout + completed.stderr
            )
            self.assertIn("BLENDER_SKILL_REGRESSION_PASSED", completed.stdout)
