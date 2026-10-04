import bpy
import math

print("Blender 3D Asset Generator for The Mutual Fun...")

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. CREATE AUTHENTIC CORPORATE BRIEFCASE (themutual.fun/art-department)
# "Every sitter carries one. It stands for the real on-chain account each Seat owns."
briefcase_mat = bpy.data.materials.new(name="LeatherBriefcase")
briefcase_mat.use_nodes = True
bsdf = briefcase_mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.22, 0.12, 0.06, 1.0) # Warm rich dark brown leather
    bsdf.inputs['Roughness'].default_value = 0.45

brass_mat = bpy.data.materials.new(name="PolishedBrass")
brass_mat.use_nodes = True
b_bsdf = brass_mat.node_tree.nodes.get("Principled BSDF")
if b_bsdf:
    b_bsdf.inputs['Base Color'].default_value = (0.83, 0.68, 0.23, 1.0) # Brass gold
    b_bsdf.inputs['Metallic'].default_value = 0.85
    b_bsdf.inputs['Roughness'].default_value = 0.25

# Briefcase body
bpy.ops.mesh.primitive_cube_add(size=1.0)
case = bpy.context.active_object
case.name = "Briefcase_Body"
case.scale = (0.55, 0.16, 0.38)
case.location = (0, 0, 0.38)
case.data.materials.append(briefcase_mat)

# Brass corner guards
for x_sign in [-1, 1]:
    for z_sign in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        guard = bpy.context.active_object
        guard.name = f"Corner_Guard_{x_sign}_{z_sign}"
        guard.scale = (0.05, 0.165, 0.05)
        guard.location = (x_sign * 0.52, 0, 0.38 + z_sign * 0.35)
        guard.data.materials.append(brass_mat)

# Dual brass latches on top
for x_pos in [-0.22, 0.22]:
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    latch = bpy.context.active_object
    latch.name = f"Brass_Latch_{x_pos}"
    latch.scale = (0.06, 0.17, 0.04)
    latch.location = (x_pos, 0, 0.77)
    latch.data.materials.append(brass_mat)

# Briefcase Handle
bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.025)
handle = bpy.context.active_object
handle.name = "Briefcase_Handle"
handle.rotation_euler = (math.pi / 2, 0, 0)
handle.location = (0, 0, 0.86)
handle.data.materials.append(briefcase_mat)

# Export Briefcase GLB
bpy.ops.export_scene.gltf(filepath="briefcase.glb", export_format='GLB')
print("Successfully generated and exported briefcase.glb!")
