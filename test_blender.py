import bpy
import sys

print("Hello from Blender", bpy.app.version_string)
# Create a test cube and export gltf
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add(size=1)
bpy.ops.export_scene.gltf(filepath="test_blender_export.glb", export_format='GLB')
print("Successfully exported test_blender_export.glb")
