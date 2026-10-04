from ascii_cutouts import get_image_rgba
import os

candidates = ['argon-04', 'bogle-02', 'smaug-05', 'midas-05', 'vladd-04']
for key in candidates:
    path = f'cutouts/{key}.png'
    w, h, rows = get_image_rgba(path)
    lines = []
    for y in range(0, h // 2, h // 30):
        line = []
        for x in range(w // 4, 3 * w // 4, w // 40):
            idx = x * 4
            if idx + 3 < len(rows[y]):
                r, g, b, a = rows[y][idx:idx+4]
                if a < 128: line.append(' ')
                else:
                    lum = (r * 299 + g * 587 + b * 114) // 1000
                    if lum > 200: line.append('#')
                    elif lum > 140: line.append('*')
                    elif lum > 70: line.append(':')
                    else: line.append('.')
        lines.append(''.join(line))
    print(f"=== {key} ===")
    print('\n'.join(lines))
