with open('build_custom_chair_arena.py', 'r', encoding='utf-8') as f:
    t = f.read()

replacements = [
    ('seize an available seat immediately!', 'seize an available seat immediately.'),
    ('Strike SPACE or click SEIZE SEAT instantly!', 'Strike SPACE or click SEIZE SEAT instantly.'),
    ("setArenaSignal('red', 'NEEDLE CUT! SIT NOW!');", "setArenaSignal('red', 'NEEDLE CUT: SIT NOW');"),
    ('setDeckHint("NOW! Press SPACE or tap SEIZE SEAT to secure a chair!");', 'setDeckHint("Press SPACE or tap SEIZE SEAT to secure a chair.");'),
    ('setDeckHint("Seat secured! Hold your position.");', 'setDeckHint("Seat secured. Hold your position.");'),
    ('setDeckHint("Too soon! You moved while phonograph was still playing.");', 'setDeckHint("Too soon. You moved while phonograph was still playing.");'),
    ('title.innerText = "THE LAST CHAIR IS YOURS!";', 'title.innerText = "THE LAST CHAIR IS YOURS";'),
    ('title.innerText = "SEAT SECURED!";', 'title.innerText = "SEAT SECURED";'),
]

for old, new in replacements:
    if old in t:
        t = t.replace(old, new)
        print(f"Replaced: {old[:30]}...")
    else:
        print(f"Warning: not found: {old[:30]}...")

with open('build_custom_chair_arena.py', 'w', encoding='utf-8') as f:
    f.write(t)

print('Cleaned exclamation marks successfully!')
