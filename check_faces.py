from PIL import Image
import os

for f in sorted(os.listdir("inspected_portraits")):
    p = os.path.join("inspected_portraits", f)
    img = Image.open(p)
    # Check pixels in the face region (center area)
    w, h = img.size
    face_box = (int(w*0.35), int(h*0.25), int(w*0.65), int(h*0.55))
    face_crop = img.crop(face_box)
    colors = face_crop.getcolors(maxcolors=256)
    has_brown_fur = False
    has_human_skin = False
    for cnt, col in colors or []:
        r, g, b = col[:3]
        # Monkey brown/dark fur:
        if 50 < r < 100 and 30 < g < 70 and 15 < b < 45:
            has_brown_fur = True
        # Human warm skin:
        if r > 190 and g > 150 and b > 120 and r > g > b:
            has_human_skin = True
    print(f"{f}: size={img.size}, brown_fur={has_brown_fur}, human_skin={has_human_skin}")
