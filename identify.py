import glob
import xml.etree.ElementTree as ET

def analyze(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    rects = []
    for elem in root.findall('.//{http://www.w3.org/2000/svg}rect'):
        x = int(elem.attrib.get('x', 0))
        y = int(elem.attrib.get('y', 0))
        w = int(elem.attrib.get('width', 1))
        h = int(elem.attrib.get('height', 1))
        fill = elem.attrib.get('fill', '').lower()
        rects.append((x, y, w, h, fill))
    return rects

for f in sorted(glob.glob('portraits/*.svg')):
    rects = analyze(f)
    # find prominent colors in head area (y between 10 and 30, x between 20 and 44)
    head_colors = {}
    chest_colors = {}
    for x, y, w, h, fill in rects:
        if 10 <= y <= 30 and 20 <= x <= 44:
            head_colors[fill] = head_colors.get(fill, 0) + w * h
        if 30 < y <= 45 and 20 <= x <= 44:
            chest_colors[fill] = chest_colors.get(fill, 0) + w * h
    top_head = sorted(head_colors.items(), key=lambda item: item[1], reverse=True)[:4]
    top_chest = sorted(chest_colors.items(), key=lambda item: item[1], reverse=True)[:4]
    print(f"{f}: head={top_head} | chest={top_chest}")
