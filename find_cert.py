import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('build_custom_chair_arena.py', 'r', encoding='utf-8') as f:
    c = f.read()

for m in re.finditer(r'getContext\(\s*[\'\"]2d[\'\"]\s*\)', c):
    idx = m.start()
    print('--- MATCH ---')
    print(c[idx-80:idx+350])
