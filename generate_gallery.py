import glob
import os

html = ['<html><body style="background:#111;color:#eee;font-family:sans-serif;"><h2>All Portraits</h2><div style="display:flex;flex-wrap:wrap;gap:20px;">']

for f in sorted(glob.glob('portraits/*.png')):
    name = os.path.basename(f)
    html.append(f'<div style="text-align:center;"><img src="portraits/{name}" style="image-rendering:pixelated;width:128px;height:128px;border:1px solid #444;"><br><span>{name}</span></div>')

html.append('</div><h2>All Cutouts</h2><div style="display:flex;flex-wrap:wrap;gap:20px;">')
for f in sorted(glob.glob('cutouts/*.png')):
    name = os.path.basename(f)
    html.append(f'<div style="text-align:center;"><img src="cutouts/{name}" style="image-rendering:pixelated;width:128px;height:128px;border:1px solid #444;background:#333;"><br><span>{name}</span></div>')
html.append('</div></body></html>')

with open('gallery.html', 'w', encoding='utf-8') as out:
    out.write(''.join(html))
print('Created gallery.html')
