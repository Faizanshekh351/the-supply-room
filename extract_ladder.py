with open('tmforgchart_raw.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', text, re.DOTALL)
if scripts:
    with open('tmforgchart_inline.js', 'w', encoding='utf-8') as f:
        f.write(scripts[0])
    print('Saved inline script to tmforgchart_inline.js, len:', len(scripts[0]))

ladder = re.findall(r'<table[^>]*class=["\']ladder["\'][^>]*>(.*?)</table>', text, re.DOTALL)
if ladder:
    print('Ladder Table found:\n', ladder[0])

# Look for certificates in HTML
certs = re.findall(r'.{0,50}certif.{0,50}', text, re.I)
for c in set(certs):
    print("Cert match:", c.strip())
