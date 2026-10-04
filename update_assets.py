import base64
import json
import os
from PIL import Image

# Read assets_encoded.json
with open("assets_encoded.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

# 1. Encode art_department_wall.png
if os.path.exists("art_department_wall.png"):
    with open("art_department_wall.png", "rb") as f:
        wall_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        assets["art_wall"] = wall_b64
        print("Encoded art_wall successfully.")

# 2. Encode sprites.png
if os.path.exists("sprites.png"):
    with open("sprites.png", "rb") as f:
        sprites_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        assets["lastchair_sprites"] = sprites_b64
        print("Encoded lastchair_sprites successfully.")

# 3. Encode room.png
if os.path.exists("room.png"):
    with open("room.png", "rb") as f:
        room_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        assets["lastchair_room"] = room_b64
        print("Encoded lastchair_room successfully.")

# 4. Remove monkey pfp from Flickerr:
# Replace p_bogle_1 with bogle-03 (human clerk)
if os.path.exists("portraits/bogle-03.png"):
    with open("portraits/bogle-03.png", "rb") as f:
        bogle3_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
        assets["p_bogle_1"] = bogle3_b64
        assets["flickerr_human"] = bogle3_b64
        print("Replaced p_bogle_1 with authentic human clerk bogle-03!")

# Save back to assets_encoded.json
with open("assets_encoded.json", "w", encoding="utf-8") as f:
    json.dump(assets, f)

print("Updated assets_encoded.json with art_wall, sprites, room, and human clerk!")
