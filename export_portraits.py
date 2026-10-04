import json
import base64
import os
from PIL import Image
import io

with open("assets_encoded.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

portrait_keys = [k for k in assets.keys() if k.startswith("p_") or "boss" in k]
print("Found portrait keys:", len(portrait_keys))

# Save all portraits as pngs in a temp folder so we can inspect them
os.makedirs("inspected_portraits", exist_ok=True)
for k in portrait_keys:
    data = assets[k]
    if "," in data:
        data = data.split(",")[1]
    raw = base64.b64decode(data)
    with open(os.path.join("inspected_portraits", f"{k}.png"), "wb") as out:
        out.write(raw)

print("Saved all portraits to inspected_portraits/")
