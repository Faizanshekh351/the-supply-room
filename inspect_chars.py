import glob
import xml.etree.ElementTree as ET

chairs = {
    'argon-01': 'Green Bankers Chair',
    'argon-02': 'The Interns Folding Chair',
    'argon-03': 'Deep Button Chesterfield',
    'argon-04': 'Oxblood Wingback',
    'argon-05': 'Creaking Wooden Swivel',
    'bogle-01': 'Green Bankers Chair',
    'bogle-02': 'Oxblood Wingback',
    'bogle-03': 'The Interns Folding Chair',
    'bogle-04': 'Creaking Wooden Swivel',
    'bogle-05': 'Deep Button Chesterfield',
    'smaug-01': 'Beige Task Chair',
    'smaug-02': 'The Gilded Throne',
    'smaug-03': 'Creaking Wooden Swivel',
    'smaug-04': 'Green Bankers Chair',
    'smaug-05': 'Oxblood Wingback',
    'midas-01': 'Green Bankers Chair',
    'midas-02': 'Deep Button Chesterfield',
    'midas-03': 'Creaking Wooden Swivel',
    'midas-04': 'Tasteful Walnut Lounge',
    'midas-05': 'Oxblood Wingback',
    'vladd-01': 'Deep Button Chesterfield',
    'vladd-02': 'Green Bankers Chair',
    'vladd-03': 'Beige Task Chair',
    'vladd-04': 'Oxblood Wingback',
    'vladd-05': 'The Interns Folding Chair',
}

def parse_svg(path):
    tree = ET.parse(path)
    root = tree.getroot()
    grid = [[' ' for _ in range(64)] for _ in range(64)]
    color_grid = [['' for _ in range(64)] for _ in range(64)]
    for elem in root.findall('.//{http://www.w3.org/2000/svg}rect'):
        x = int(elem.attrib.get('x', 0))
        y = int(elem.attrib.get('y', 0))
        w = int(elem.attrib.get('width', 1))
        h = int(elem.attrib.get('height', 1))
        fill = elem.attrib.get('fill', '').lower()
        for dy in range(h):
            for dx in range(w):
                if 0 <= y+dy < 64 and 0 <= x+dx < 64:
                    color_grid[y+dy][x+dx] = fill
    return color_grid

# Let's inspect specific features
for f in sorted(glob.glob('portraits/*.svg')):
    key = f.replace('portraits\\', '').replace('.svg', '')
    grid = parse_svg(f)
    # Check lines 10 to 30 for features
    colors_used = set()
    for row in grid[10:35]:
        for c in row[15:50]:
            if c: colors_used.add(c)
    
    # Check if fez (bright red #a93b3b, #7a2e2e, #6d2027 etc at y=10-18)
    has_fez = any(grid[y][x] in ['#6d2027', '#7a2e2e', '#8f3a3c'] for y in range(10, 18) for x in range(25, 40))
    # Check dog / retriever colors (golden fur: #d5a06e, #b8894b, #d1a76e, #eabf98)
    # Check skeleton (bone white #f8f0dc, #ede3cf, #bcb4a6, #e6dec8, black eye sockets)
    # Check alien / extraterrestrial (green/grey skin or plant)
    
    print(f"{key:10} | Chair: {chairs.get(key):26} | Fez-like: {has_fez}")
