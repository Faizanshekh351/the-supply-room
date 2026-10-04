with open('build_custom_chair_arena.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HUD role display
content = content.replace(
    "document.getElementById('hudRole').innerText = `Flickerr · ${flickerr.role}`;",
    "document.getElementById('hudRole').innerText = `You · ${flickerr.role}`;",
)
content = content.replace(
    "document.getElementById('hudRole').innerText = `Flickerr \u00b7 ${flickerr.role}`;",
    "document.getElementById('hudRole').innerText = `You \u00b7 ${flickerr.role}`;",
)

# 2. Gatekeeper dialogue
content = content.replace(
    "Choose your covenant carefully, Flickerr. The Mutual Fun operates with clockwork precision.",
    "Choose your covenant carefully. You are now within The Mutual Fun. It operates with clockwork precision.",
)

# 3. what3verman dialogue
content = content.replace(
    "\"You climb fast, Flickerr. But my green banker's chair is not given away on review points alone.",
    "\"You climb fast. But my green banker's chair is not given away on review points alone.",
)

# 4. Kingpickle dialogue
content = content.replace(
    "\"Welcome to Seat 0, Flickerr. You started outside on the pavement.",
    "\"Welcome to Seat 0. You started outside on the pavement.",
)

# 5. Arena contenders roster
content = content.replace(
    '{ id: 0, name: "Flickerr", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color }',
    '{ id: 0, name: "You", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color }',
)

# 6. Arena overhead floating label
content = content.replace(
    'ctx.fillText("FLICKERR [YOU]", 0, -62 - walkBob);',
    'ctx.fillText("YOU", 0, -62 - walkBob);',
)

# 7. Arena victory result description
content = content.replace(
    "Three rounds. Three flawless moves. Flickerr secures lawful title to ${arenaChairName} on Floor ${arenaFloor}.",
    "Three rounds. Three flawless moves. You secure lawful title to ${arenaChairName} on Floor ${arenaFloor}.",
)

# 8. Certificate name
content = content.replace(
    'g.fillText("FLICKERR", px, py + pr + 22);',
    'g.fillText("YOU", px, py + pr + 22);',
)

# 9. Certificate download filename
content = content.replace(
    'TMF_Certificate_Flickerr_${flickerr.role',
    'TMF_Certificate_You_${flickerr.role',
)

with open('build_custom_chair_arena.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied name change from Flickerr to You across build_custom_chair_arena.py successfully!")
