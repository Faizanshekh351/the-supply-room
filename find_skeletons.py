from ascii_cutouts import get_image_rgba
import xml.etree.ElementTree as ET
import glob, os

# Find all portraits that have skeleton head
# Skeleton head: rows 12-22 with white/cream (#f8f0dc, #bcb4a6, #ede3cf) and eye sockets (dark #26201a, #1c2334)
for f in sorted(glob.glob('portraits/*.svg')):
    key = os.path.basename(f).replace('.svg', '')
    tree = ET.parse(f)
    root = tree.getroot()
    grid = [['' for _ in range(64)] for _ in range(64)]
    for elem in root.findall('.//{http://www.w3.org/2000/svg}rect'):
        x = int(elem.attrib.get('x', 0))
        y = int(elem.attrib.get('y', 0))
        w = int(elem.attrib.get('width', 1))
        h = int(elem.attrib.get('height', 1))
        fill = elem.attrib.get('fill', '').lower()
        for dy in range(h):
            for dx in range(w):
                if 0 <= y+dy < 64 and 0 <= x+dx < 64:
                    grid[y+dy][x+dx] = fill
    
    # check for two eye sockets in skull (y 14-22, x around 28-31 and 33-36)
    left_eye = any(grid[y][x] in ['#26201a', '#1c2334', '#37322e', '#451318'] for y in range(14, 20) for x in range(27, 31))
    right_eye = any(grid[y][x] in ['#26201a', '#1c2334', '#37322e', '#451318'] for y in range(14, 20) for x in range(33, 37))
    skull_bone = any(grid[y][x] in ['#f8f0dc', '#ede3cf', '#bcb4a6', '#d9c69c'] for y in range(12, 17) for x in range(28, 36))
    if left_eye and right_eye and skull_bone:
        # Check chair and suit/tie
        suit_colors = set(grid[y][x] for y in range(32, 48) for x in range(24, 40) if grid[y][x])
        print(f"Skeleton found: {key}")
        print(f"  Chair in for-your-machine: {chairs.get(key)}")
        # Check green tie vs gold tie
        # Green tie: #365839, #52774f, #223f2b, #2f6b3d
        # Gold tie: #b08a3c, #d4af37, #b9902f, #c79c3a, #e6c76d, #8a6317
        has_green_tie = any(grid[y][x] in ['#365839', '#52774f', '#223f2b', '#2f6b3d'] for y in range(30, 42) for x in range(30, 34))
        has_gold_tie = any(grid[y][x] in ['#b08a3c', '#d4af37', '#b9902f', '#c79c3a', '#e6c76d', '#8a6317'] for y in range(30, 42) for x in range(30, 34))
        print(f"  has_green_tie={has_green_tie}, has_gold_tie={has_gold_tie}")
