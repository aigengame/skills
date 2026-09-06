"""Inspect a scene subtree in Blender; the MCP client supplies the params dict."""


def inspect_asset(parameters):
    if not isinstance(parameters, dict):
        raise ValueError("Supply a params dictionary with scene and root names")
    for field in ("scene", "root"):
        if not isinstance(parameters.get(field), str) or not parameters[field]:
            raise ValueError(f"params.{field} must be a non-empty string")
    expected = parameters.get("expected_nodes", [])
    if not isinstance(expected, list) or not all(
        isinstance(n, str) and n for n in expected
    ):
        raise ValueError("params.expected_nodes must be a list of non-empty names")

    import bpy

    scene = bpy.data.scenes.get(parameters["scene"])
    if scene is None:
        raise ValueError(f"Scene not found: {parameters['scene']}")
    root = scene.objects.get(parameters["root"])
    if root is None:
        raise ValueError(f"Root not found in scene: {parameters['root']}")
    objects = [root] + [o for o in root.children_recursive if o.name in scene.objects]
    names = {o.name for o in objects}
    missing = sorted(set(expected) - names)
    if missing:
        raise ValueError(f"Expected nodes missing from asset subtree: {missing}")
    view_layer = scene.view_layers[0]
    # A reopened, non-active scene can still have unevaluated world matrices.
    # Update derived transforms without changing or saving the authored data.
    view_layer.update()
    unavailable = [
        o.name
        for o in objects
        if o.name not in view_layer.objects or not o.visible_get(view_layer=view_layer)
    ]
    if unavailable:
        raise ValueError(
            "Asset objects are excluded or hidden in the scene's first view layer: "
            + ", ".join(unavailable)
        )
    meshes = [o for o in objects if o.type == "MESH"]
    low = [float("inf")] * 3
    high = [-float("inf")] * 3
    vertices = 0
    triangles = 0
    for obj in meshes:
        vertices += len(obj.data.vertices)
        triangles += sum(max(0, len(p.vertices) - 2) for p in obj.data.polygons)
        for vertex in obj.data.vertices:
            point = obj.matrix_world @ vertex.co
            for axis in range(3):
                low[axis] = min(low[axis], point[axis])
                high[axis] = max(high[axis], point[axis])
    return {
        "blender_version": bpy.app.version_string,
        "loaded_file": bpy.data.filepath,
        "background": bpy.app.background,
        "scene": scene.name,
        "root": root.name,
        "view_layer": view_layer.name,
        "unit_scale_length": scene.unit_settings.scale_length,
        "nodes": [{"name": o.name, "type": o.type} for o in objects],
        "mesh_objects": len(meshes),
        "vertices": vertices,
        "triangles": triangles,
        "count_basis": "base mesh data per object; n-2 triangles per polygon",
        "bounds_basis": "base mesh vertices transformed by each object's matrix_world",
        "world_bounds": {"min": low, "max": high} if vertices else None,
        "materials": sorted(
            {s.material.name for o in meshes for s in o.material_slots if s.material}
        ),
        "expected_nodes_found": sorted(set(expected)),
        "limitations": "No evaluated modifiers, skin deformation, or expansion of collection instances",
    }


if "params" in globals() or __name__ == "__main__":
    result = inspect_asset(globals().get("params"))
