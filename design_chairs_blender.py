import bpy
import math

print("Blender 3D Chair Generator for The Mutual Fun...")

# --- 1. FOLDING CHAIR (Floor 1) ---
bpy.ops.wm.read_factory_settings(use_empty=True)

steel_mat = bpy.data.materials.new(name="TubularSteel")
s_bsdf = steel_mat.node_tree.nodes.get("Principled BSDF")
if s_bsdf:
    s_bsdf.inputs['Base Color'].default_value = (0.7, 0.72, 0.75, 1.0)
    s_bsdf.inputs['Metallic'].default_value = 0.8
    s_bsdf.inputs['Roughness'].default_value = 0.3

vinyl_mat = bpy.data.materials.new(name="BeigeVinyl")
v_bsdf = vinyl_mat.node_tree.nodes.get("Principled BSDF")
if v_bsdf:
    v_bsdf.inputs['Base Color'].default_value = (0.83, 0.74, 0.55, 1.0) # #d5bd82
    v_bsdf.inputs['Roughness'].default_value = 0.5

# X legs
for sign in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.75)
    legA = bpy.context.active_object
    legA.rotation_euler = (0, 0, sign * 0.35)
    legA.location = (sign * 0.22, 0, 0.35)
    legA.data.materials.append(steel_mat)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.75)
    legB = bpy.context.active_object
    legB.rotation_euler = (0, 0, -sign * 0.35)
    legB.location = (sign * 0.22, 0, 0.35)
    legB.data.materials.append(steel_mat)

# Seat pad
bpy.ops.mesh.primitive_cube_add(size=1.0)
seat = bpy.context.active_object
seat.scale = (0.58, 0.52, 0.05)
seat.location = (0, 0, 0.52)
seat.data.materials.append(vinyl_mat)

# Back arch & pad
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.55)
arch = bpy.context.active_object
arch.location = (0, -0.22, 0.82)
arch.data.materials.append(steel_mat)

bpy.ops.mesh.primitive_cube_add(size=1.0)
back = bpy.context.active_object
back.scale = (0.48, 0.04, 0.24)
back.location = (0, -0.22, 0.85)
back.data.materials.append(vinyl_mat)

bpy.ops.export_scene.gltf(filepath="chair_folding.glb", export_format='GLB')
print("Exported chair_folding.glb!")

# --- 2. GREEN BANKER'S CHAIR (Floor 6 / MD what3verman) ---
bpy.ops.wm.read_factory_settings(use_empty=True)

mahog_mat = bpy.data.materials.new(name="CubanMahogany")
m_bsdf = mahog_mat.node_tree.nodes.get("Principled BSDF")
if m_bsdf:
    m_bsdf.inputs['Base Color'].default_value = (0.24, 0.1, 0.06, 1.0)
    m_bsdf.inputs['Roughness'].default_value = 0.35

green_mat = bpy.data.materials.new(name="BankerGreenLeather")
g_bsdf = green_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.1, 0.26, 0.16, 1.0) # #1b432a
    g_bsdf.inputs['Roughness'].default_value = 0.4

gold_mat = bpy.data.materials.new(name="BrassStuds")
gold_bsdf = gold_mat.node_tree.nodes.get("Principled BSDF")
if gold_bsdf:
    gold_bsdf.inputs['Base Color'].default_value = (0.83, 0.68, 0.23, 1.0)
    gold_bsdf.inputs['Metallic'].default_value = 0.9

# 4-star base
for i in range(4):
    ang = i * math.pi / 2
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    leg = bpy.context.active_object
    leg.scale = (0.08, 0.36, 0.06)
    leg.rotation_euler = (0, ang, 0)
    leg.location = (math.sin(ang)*0.18, math.cos(ang)*0.18, 0.12)
    leg.data.materials.append(mahog_mat)

# Seat cushion
bpy.ops.mesh.primitive_cube_add(size=1.0)
seat = bpy.context.active_object
seat.scale = (0.72, 0.68, 0.14)
seat.location = (0, 0, 0.54)
seat.data.materials.append(green_mat)

# Horseshoe crest rail
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.08)
crest = bpy.context.active_object
crest.location = (0, -0.05, 0.98)
crest.scale = (1.0, 0.8, 1.0)
crest.data.materials.append(mahog_mat)

bpy.ops.export_scene.gltf(filepath="chair_bankers.glb", export_format='GLB')
print("Exported chair_bankers.glb!")

# --- 3. THE GILDED THRONE (Penthouse / Kingpickle) ---
bpy.ops.wm.read_factory_settings(use_empty=True)

goldleaf_mat = bpy.data.materials.new(name="GoldLeaf24k")
gl_bsdf = goldleaf_mat.node_tree.nodes.get("Principled BSDF")
if gl_bsdf:
    gl_bsdf.inputs['Base Color'].default_value = (1.0, 0.84, 0.0, 1.0)
    gl_bsdf.inputs['Metallic'].default_value = 0.95
    gl_bsdf.inputs['Roughness'].default_value = 0.2

crimson_mat = bpy.data.materials.new(name="RoyalCrimson")
cr_bsdf = crimson_mat.node_tree.nodes.get("Principled BSDF")
if cr_bsdf:
    cr_bsdf.inputs['Base Color'].default_value = (0.54, 0.0, 0.0, 1.0)
    cr_bsdf.inputs['Roughness'].default_value = 0.5

# Dais
bpy.ops.mesh.primitive_cube_add(size=1.0)
dais = bpy.context.active_object
dais.scale = (1.1, 1.1, 0.2)
dais.location = (0, 0, 0.1)
dais.data.materials.append(goldleaf_mat)

# Cushion
bpy.ops.mesh.primitive_cube_add(size=1.0)
cush = bpy.context.active_object
cush.scale = (0.84, 0.8, 0.18)
cush.location = (0, 0, 0.35)
cush.data.materials.append(crimson_mat)

# Backrest
bpy.ops.mesh.primitive_cube_add(size=1.0)
back = bpy.context.active_object
back.scale = (0.84, 0.14, 1.4)
back.location = (0, -0.34, 1.1)
back.data.materials.append(crimson_mat)

# Crown arch
bpy.ops.mesh.primitive_cylinder_add(radius=0.45, depth=0.18)
crown = bpy.context.active_object
crown.rotation_euler = (math.pi/2, 0, 0)
crown.location = (0, -0.34, 1.95)
crown.data.materials.append(goldleaf_mat)

bpy.ops.export_scene.gltf(filepath="chair_throne.glb", export_format='GLB')
print("Exported chair_throne.glb!")
