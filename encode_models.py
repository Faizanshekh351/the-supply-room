import base64
import json
import os

with open("assets_encoded.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

# 1. Encode briefcase.glb
if os.path.exists("briefcase.glb"):
    with open("briefcase.glb", "rb") as f:
        assets["glb_briefcase"] = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode("utf-8")
        print("Encoded glb_briefcase")

# 2. Encode chair_folding.glb
if os.path.exists("chair_folding.glb"):
    with open("chair_folding.glb", "rb") as f:
        assets["glb_chair_folding"] = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode("utf-8")
        print("Encoded glb_chair_folding")

# 3. Encode chair_bankers.glb
if os.path.exists("chair_bankers.glb"):
    with open("chair_bankers.glb", "rb") as f:
        assets["glb_chair_bankers"] = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode("utf-8")
        print("Encoded glb_chair_bankers")

# 4. Encode chair_throne.glb
if os.path.exists("chair_throne.glb"):
    with open("chair_throne.glb", "rb") as f:
        assets["glb_chair_throne"] = "data:model/gltf-binary;base64," + base64.b64encode(f.read()).decode("utf-8")
        print("Encoded glb_chair_throne")

with open("assets_encoded.json", "w", encoding="utf-8") as f:
    json.dump(assets, f)

print("Updated assets_encoded.json with all Blender GLB models!")
