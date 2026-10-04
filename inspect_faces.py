import xml.etree.ElementTree as ET

def get_face(path):
    tree = ET.parse(path)
    root = tree.getroot()
    # Let's inspect rows 18-28, cols 26-38 (face area)
    grid = [[' ' for _ in range(64)] for _ in range(64)]
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
    return grid

for key in ['bogle-01', 'bogle-02', 'bogle-03', 'bogle-04', 'midas-01', 'midas-02', 'midas-04', 'smaug-01', 'smaug-02', 'smaug-04', 'vladd-01', 'vladd-02', 'vladd-03', 'vladd-05']:
    g = get_face(f'portraits/{key}.svg')
    # check face colors and suit colors
    face_colors = set(g[y][x] for y in range(16, 28) for x in range(26, 38))
    suit_colors = set(g[y][x] for y in range(32, 45) for x in range(26, 38))
    tie_colors = set(g[y][x] for y in range(30, 42) for x in range(30, 34))
    print(f"{key}: face={face_colors} | suit={suit_colors} | tie={tie_colors}")
