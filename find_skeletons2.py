import xml.etree.ElementTree as ET
import glob, os

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
    
    # check for skull shape
    left_eye = any(grid[y][x] in ['#26201a', '#1c2334', '#37322e', '#451318'] for y in range(14, 20) for x in range(27, 31))
    right_eye = any(grid[y][x] in ['#26201a', '#1c2334', '#37322e', '#451318'] for y in range(14, 20) for x in range(33, 37))
    skull_bone = any(grid[y][x] in ['#f8f0dc', '#ede3cf', '#bcb4a6'] for y in range(12, 17) for x in range(28, 36))
    teeth = any(grid[y][x] in ['#f8f0dc', '#ede3cf', '#bcb4a6'] for y in range(20, 24) for x in range(29, 35))
    if left_eye and right_eye and skull_bone and teeth:
        has_green_tie = any(grid[y][x] in ['#365839', '#52774f', '#223f2b', '#2f6b3d'] for y in range(30, 44) for x in range(28, 36))
        has_gold_tie = any(grid[y][x] in ['#b08a3c', '#d4af37', '#b9902f', '#c79c3a', '#e6c76d', '#8a6317'] for y in range(30, 44) for x in range(28, 36))
        suit_brown = any(grid[y][x] in ['#5d3b20', '#6a4128', '#4c4640', '#3a2415', '#6b4423'] for y in range(32, 48) for x in range(22, 42))
        print(f"Skeleton: {key:10} | Chair: {chairs.get(key):25} | green_tie={has_green_tie}, gold_tie={has_gold_tie}, brown_suit={suit_brown}")
