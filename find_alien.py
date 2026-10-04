import xml.etree.ElementTree as ET
import glob

# Look for small potted plant (leaves/plant near bottom or side: greens #2f6b3d, #3e7a4e, #52774f, #365839, #223f2b)
for f in sorted(glob.glob('portraits/*.svg')):
    tree = ET.parse(f)
    root = tree.getroot()
    plant_rects = []
    cardigan_rects = []
    alien_rects = []
    for elem in root.findall('.//{http://www.w3.org/2000/svg}rect'):
        x = int(elem.attrib.get('x', 0))
        y = int(elem.attrib.get('y', 0))
        w = int(elem.attrib.get('width', 1))
        h = int(elem.attrib.get('height', 1))
        fill = elem.attrib.get('fill', '').lower()
        # Cardigan: oxblood #7a2e2e, #6d2027, #8f3a3c, #5e2222 on body (y:30-50)
        if 30 <= y <= 50 and fill in ['#7a2e2e', '#6d2027', '#8f3a3c', '#5e2222', '#6e2b2b']:
            cardigan_rects.append((x, y, w, h, fill))
        # Plant on side (x < 20 or x > 44, y > 35)
        if (x < 22 or x > 42) and 35 <= y <= 55 and fill in ['#2f6b3d', '#3e7a4e', '#52774f', '#365839', '#223f2b']:
            plant_rects.append((x, y, w, h, fill))
    if cardigan_rects and plant_rects:
        print(f"MATCH: {f} -> cardigan={len(cardigan_rects)}, plant={len(plant_rects)}")
    elif plant_rects:
        print(f"Plant only: {f} -> plant={len(plant_rects)}")
    elif cardigan_rects:
        print(f"Cardigan only: {f} -> cardigan={len(cardigan_rects)}")
