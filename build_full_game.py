import os
import json
import base64

# Load all assets
assets = {}

if os.path.exists('marks/medallion-384.png'):
    with open('marks/medallion-384.png', 'rb') as f:
        assets['medallion'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

if os.path.exists('85cAnf-p_400x400.jpg'):
    with open('85cAnf-p_400x400.jpg', 'rb') as f:
        assets['boss_what3verman'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

if os.path.exists('iYRjRGYm_400x400.jpg'):
    with open('iYRjRGYm_400x400.jpg', 'rb') as f:
        assets['boss_kingpickle'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

for fund in ['argon', 'bogle', 'smaug', 'midas', 'vladd']:
    for i in range(1, 6):
        p_path = f'portraits/{fund}-0{i}.png'
        c_path = f'cutouts/{fund}-0{i}.png'
        if os.path.exists(p_path):
            with open(p_path, 'rb') as f:
                assets[f'p_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')
        if os.path.exists(c_path):
            with open(c_path, 'rb') as f:
                assets[f'c_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

print(f"Loaded {len(assets)} assets.")
