from PIL import Image
import os

img_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\.user_uploaded\media_1791109247839.png'
img = Image.open(img_path)
print("Image dimensions:", img.size)
print("Image mode:", img.mode)

# Save a copy in workspace
img.save("art_department_wall.png")
print("Saved art_department_wall.png to workspace")

# Also let's check colors
colors = img.getcolors(maxcolors=1000)
if colors:
    sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
    print("Top 10 colors:")
    for count, col in sorted_colors[:10]:
        print(f"  Count: {count}, RGBA: {col}")
