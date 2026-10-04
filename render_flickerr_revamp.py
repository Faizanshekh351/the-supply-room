import bpy
import math
import os

print("=== Designing Revamped Flickerr (The 1987 Corporate Clerk) in Blender ===")

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Scene settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 720
scene.render.resolution_y = 960
scene.render.film_transparent = True

# Materials Helper
def create_mat(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = metallic
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = roughness
    return mat

m_navy = create_mat("NavySuit", (0.08, 0.12, 0.18, 1.0), metallic=0.05, roughness=0.7)
m_dark_navy = create_mat("DarkNavyLapel", (0.05, 0.08, 0.12, 1.0), metallic=0.05, roughness=0.8)
m_shirt = create_mat("WhiteShirt", (0.95, 0.94, 0.92, 1.0), roughness=0.6)
m_tie = create_mat("OxbloodTie", (0.45, 0.12, 0.12, 1.0), roughness=0.4)
m_gold = create_mat("GoldAccent", (0.83, 0.68, 0.23, 1.0), metallic=0.9, roughness=0.2)
m_skin = create_mat("FairSkin", (0.92, 0.72, 0.58, 1.0), roughness=0.6)
m_hair = create_mat("ChestnutHair", (0.16, 0.10, 0.06, 1.0), roughness=0.6)
m_glasses = create_mat("Tortoiseshell", (0.10, 0.06, 0.04, 1.0), roughness=0.3)
m_lens = create_mat("GlassLens", (0.75, 0.88, 0.95, 0.5), roughness=0.1)
m_shoes = create_mat("BlackLeather", (0.05, 0.05, 0.06, 1.0), roughness=0.35)
m_briefcase = create_mat("BrownLeather", (0.22, 0.12, 0.06, 1.0), roughness=0.5)
m_eyes = create_mat("DarkPupil", (0.05, 0.04, 0.03, 1.0), roughness=0.2)

def add_cube(name, size, pos, mat, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    obj.location = pos
    obj.rotation_euler = rot
    obj.data.materials.append(mat)
    return obj

# 1. TORSO & JACKET
# Main jacket body
add_cube("Jacket_Body", (0.68, 0.38, 0.75), (0, 0, 1.0), m_navy)

# Front shirt V-opening (ONLY ON FRONT, Y < 0 in Blender default, let's treat +Y as FRONT for camera or +Y as forward)
# Let's align: +Y = Forward (Front), -Y = Back.
# In Blender, Y is depth. Let's make +Y = Front, -Y = Back, Z = Up, X = Left/Right.
# Front is Y > 0.
add_cube("Shirt_Front", (0.22, 0.03, 0.32), (0, 0.18, 1.15), m_shirt)
add_cube("Tie_Front", (0.08, 0.03, 0.36), (0, 0.20, 1.08), m_tie)
add_cube("Tie_Knot", (0.09, 0.04, 0.09), (0, 0.20, 1.28), m_tie)
add_cube("Tie_Clip", (0.10, 0.02, 0.02), (0, 0.215, 1.12), m_gold)

# Notched Lapels (Front only)
add_cube("Lapel_L", (0.10, 0.04, 0.30), (-0.14, 0.185, 1.15), m_dark_navy, (0, 0, -0.15))
add_cube("Lapel_R", (0.10, 0.04, 0.30), (0.14, 0.185, 1.15), m_dark_navy, (0, 0, 0.15))

# Breast pocket with ID pass on left chest
add_cube("Pocket_Welt", (0.11, 0.03, 0.02), (-0.20, 0.19, 1.18), m_dark_navy)
add_cube("TMF_ID_Pass", (0.08, 0.02, 0.07), (-0.20, 0.192, 1.22), m_shirt)

# Gold buttons on front
add_cube("Button_1", (0.03, 0.02, 0.03), (0.02, 0.192, 0.95), m_gold)
add_cube("Button_2", (0.03, 0.02, 0.03), (0.02, 0.192, 0.82), m_gold)

# Belt & Buckle at waist
add_cube("Belt", (0.69, 0.39, 0.08), (0, 0, 0.64), m_shoes)
add_cube("Belt_Buckle", (0.10, 0.03, 0.07), (0, 0.20, 0.64), m_gold)

# Back jacket vent / seam strip (ONLY ON BACK, Y < 0)
add_cube("Back_Seam", (0.02, 0.02, 0.68), (0, -0.192, 0.98), m_dark_navy)

# 2. HEAD & NECK
# Neck & Shirt collar
add_cube("Neck", (0.20, 0.20, 0.18), (0, 0, 1.45), m_skin)
add_cube("Collar_Front", (0.24, 0.03, 0.10), (0, 0.11, 1.42), m_shirt)

# Head core
add_cube("Head_Core", (0.38, 0.36, 0.40), (0, 0, 1.68), m_skin)

# FACE (FRONT ONLY, Y > 0)
# Nose
add_cube("Nose", (0.06, 0.08, 0.10), (0, 0.21, 1.66), m_skin)
# Mouth
add_cube("Mouth", (0.10, 0.02, 0.02), (0, 0.185, 1.57), m_dark_navy)
# Eyes & Eyebrows
add_cube("Eye_L", (0.05, 0.02, 0.04), (-0.09, 0.185, 1.70), m_eyes)
add_cube("Eye_R", (0.05, 0.02, 0.04), (0.09, 0.185, 1.70), m_eyes)
add_cube("Brow_L", (0.08, 0.03, 0.02), (-0.09, 0.19, 1.75), m_hair)
add_cube("Brow_R", (0.08, 0.03, 0.02), (0.09, 0.19, 1.75), m_hair)

# 1987 Tortoiseshell Spectacles
add_cube("Glasses_Rim_L", (0.11, 0.03, 0.09), (-0.09, 0.198, 1.70), m_glasses)
add_cube("Glasses_Rim_R", (0.11, 0.03, 0.09), (0.09, 0.198, 1.70), m_glasses)
add_cube("Glasses_Bridge", (0.06, 0.02, 0.02), (0, 0.205, 1.70), m_glasses)
add_cube("Glasses_Stem_L", (0.02, 0.22, 0.02), (-0.195, 0.07, 1.70), m_glasses)
add_cube("Glasses_Stem_R", (0.02, 0.22, 0.02), (0.195, 0.07, 1.70), m_glasses)

# Ears
add_cube("Ear_L", (0.04, 0.08, 0.12), (-0.20, 0, 1.67), m_skin)
add_cube("Ear_R", (0.04, 0.08, 0.12), (0.20, 0, 1.67), m_skin)

# HAIR (FRONT BANGS + FULL BACK COVERAGE)
# Top hair
add_cube("Hair_Top", (0.42, 0.38, 0.10), (0, -0.01, 1.91), m_hair)
# Front side-part swoop (1987 executive look)
add_cube("Hair_Front_Swoop", (0.34, 0.08, 0.08), (0.04, 0.18, 1.86), m_hair)
# Side hair
add_cube("Hair_Side_L", (0.05, 0.34, 0.24), (-0.195, -0.03, 1.76), m_hair)
add_cube("Hair_Side_R", (0.05, 0.34, 0.24), (0.195, -0.03, 1.76), m_hair)
# BACK HAIR - COVERS ENTIRE REAR OF SKULL DOWN TO THE NECK
add_cube("Hair_Back_Full", (0.40, 0.08, 0.38), (0, -0.185, 1.70), m_hair)

# 3. LEGS & OXFORD SHOES
# Left Leg
add_cube("Leg_L", (0.20, 0.22, 0.58), (-0.17, 0, 0.31), m_navy)
# Left Shoe (Points forward in +Y!)
add_cube("Shoe_Body_L", (0.20, 0.26, 0.09), (-0.17, 0.04, 0.045), m_shoes)
add_cube("Shoe_ToeCap_L", (0.18, 0.08, 0.07), (-0.17, 0.18, 0.035), m_shoes)
add_cube("Shoe_Heel_L", (0.18, 0.10, 0.04), (-0.17, -0.08, 0.02), m_shoes)

# Right Leg
add_cube("Leg_R", (0.20, 0.22, 0.58), (0.17, 0, 0.31), m_navy)
# Right Shoe (Points forward in +Y!)
add_cube("Shoe_Body_R", (0.20, 0.26, 0.09), (0.17, 0.04, 0.045), m_shoes)
add_cube("Shoe_ToeCap_R", (0.18, 0.08, 0.07), (0.17, 0.18, 0.035), m_shoes)
add_cube("Shoe_Heel_R", (0.18, 0.10, 0.04), (0.17, -0.08, 0.02), m_shoes)

# 4. ARMS & HANDS
# Left Arm (with Gold Watch)
add_cube("Arm_L", (0.16, 0.18, 0.52), (-0.44, 0, 1.05), m_navy)
add_cube("Cuff_L", (0.15, 0.17, 0.04), (-0.44, 0, 0.77), m_shirt)
add_cube("Watch_Band_L", (0.15, 0.17, 0.03), (-0.44, 0, 0.74), m_shoes)
add_cube("Watch_Gold_L", (0.03, 0.08, 0.05), (-0.52, 0, 0.74), m_gold)
add_cube("Hand_L", (0.12, 0.13, 0.12), (-0.44, 0, 0.67), m_skin)

# Right Arm (Gripping Briefcase)
add_cube("Arm_R", (0.16, 0.18, 0.52), (0.44, 0, 1.05), m_navy)
add_cube("Cuff_R", (0.15, 0.17, 0.04), (0.44, 0, 0.77), m_shirt)
add_cube("Hand_R", (0.12, 0.13, 0.12), (0.44, 0, 0.67), m_skin)

# Briefcase in Right Hand
add_cube("Briefcase_Body", (0.14, 0.44, 0.34), (0.50, 0.04, 0.48), m_briefcase)
add_cube("Briefcase_Handle", (0.04, 0.16, 0.08), (0.46, 0.04, 0.68), m_briefcase)
# Dual brass latches on FRONT of briefcase (+Y)
add_cube("Latch_1", (0.145, 0.02, 0.04), (0.50, 0.18, 0.58), m_gold)
add_cube("Latch_2", (0.145, 0.02, 0.04), (0.50, -0.10, 0.58), m_gold)

# Export GLB
glb_path = os.path.abspath("flickerr_revamp.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB')
print(f"Exported {glb_path}")

# Camera & Lighting setup for rendering front & back previews
cam_data = bpy.data.cameras.new("RenderCam")
cam_obj = bpy.data.objects.new("RenderCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Ambient world lighting
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.7, 0.75, 0.8, 1.0)
    bg.inputs['Strength'].default_value = 1.0

# Key light shining onto the front (+Y)
sun_data = bpy.data.lights.new("Sun", type='SUN')
sun_data.energy = 4.0
sun_obj = bpy.data.objects.new("Sun", sun_data)
bpy.context.collection.objects.link(sun_obj)
sun_obj.location = (2, 5, 4)
sun_obj.rotation_euler = (math.radians(-45), math.radians(15), math.radians(30))

# Rim light
rim_data = bpy.data.lights.new("Rim", type='SUN')
rim_data.energy = 2.0
rim_obj = bpy.data.objects.new("Rim", rim_data)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-2, -5, 3)
rim_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(-150))

# RENDER FRONT VIEW (Looking at +Y front from +Y)
cam_obj.location = (0, 3.2, 1.25)
cam_obj.rotation_euler = (math.radians(85), 0, math.radians(180))
scene.render.filepath = os.path.abspath("flickerr_front_preview.png")
bpy.ops.render.render(write_still=True)
print("Rendered Front Preview")

# RENDER BACK VIEW (Looking at -Y back from -Y)
cam_obj.location = (0, -3.2, 1.25)
cam_obj.rotation_euler = (math.radians(95), 0, 0)
scene.render.filepath = os.path.abspath("flickerr_back_preview.png")
bpy.ops.render.render(write_still=True)
print("Rendered Back Preview")

# RENDER 3/4 FRONT VIEW
cam_obj.location = (2.2, 2.4, 1.6)
cam_obj.rotation_euler = (math.radians(72), 0, math.radians(140))
scene.render.filepath = os.path.abspath("flickerr_isometric_preview.png")
bpy.ops.render.render(write_still=True)
print("Rendered Isometric Preview")
