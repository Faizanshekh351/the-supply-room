from ascii_cutouts import get_image_rgba
import glob, os

def inspect_all():
    results = {}
    for f in sorted(glob.glob('cutouts/*.png')):
        key = os.path.basename(f).replace('.png', '')
        w, h, rows = get_image_rgba(f)
        # Check colors
        color_counts = {}
        for y in range(h):
            for x in range(w):
                idx = x * 4
                if idx + 3 < len(rows[y]):
                    r, g, b, a = rows[y][idx:idx+4]
                    if a > 128:
                        hex_c = f"#{r:02x}{g:02x}{b:02x}"
                        color_counts[hex_c] = color_counts.get(hex_c, 0) + 1
        top_c = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        results[key] = top_c
    return results

res = inspect_all()
for k, v in res.items():
    print(f"{k}: {v}")
