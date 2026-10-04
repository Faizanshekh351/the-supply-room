import xml.etree.ElementTree as ET

def render_ascii(grid, y1, y2, x1, x2):
    lines = []
    for y in range(y1, y2):
        row = []
        for x in range(x1, x2):
            c = grid[y][x]
            if not c or c == ' ': row.append(' ')
            elif c in ['#26201a', '#1c2334', '#37322e', '#451318']: row.append('@')
            elif c in ['#f8f0dc', '#ede3cf', '#d9c69c', '#bcb4a6']: row.append('.')
            elif c in ['#eabf98', '#d5a06e', '#d1a76e', '#c89774']: row.append('o')
            elif c in ['#6d2027', '#7a2e2e', '#8f3a3c']: row.append('X')
            elif c in ['#365839', '#52774f', '#223f2b', '#2f6b3d']: row.append('%')
            else: row.append('*')
        lines.append(''.join(row))
    return '\n'.join(lines)

def load_grid(path):
    tree = ET.parse(path)
    root = tree.getroot()
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

for key in ['vladd-03', 'smaug-01', 'midas-04', 'midas-01', 'vladd-05', 'smaug-02', 'bogle-02', 'bogle-04']:
    g = load_grid(f'portraits/{key}.svg')
    print(f"=== {key} ===")
    print(render_ascii(g, 12, 36, 18, 46))
