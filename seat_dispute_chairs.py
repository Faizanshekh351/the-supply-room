with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace bare createChair calls that are dispute chairs with createSeatedRoleHolder so that an NPC sits on EVERY dispute chair
old_chair_md = """      createChair(-6, 0, 2, 6);
      interactiveObjects.push({
        id: "chair_md","""

new_chair_md = """      createSeatedRoleHolder(-6, 0, 2, 6, {
        holder: "Managing Director what3verman",
        roleTitle: "Floor 6 Seat Holder",
        color: 0x1f4728,
        tieColor: 0xb9902f,
        hairColor: 0x221309
      });
      interactiveObjects.push({
        id: "chair_md","""

if old_chair_md in text:
    text = text.replace(old_chair_md, new_chair_md)
    print("Replaced chair_md with seated role holder")

# Floor 8 board dispute chair:
old_chair_board = """      createChair(0, 0, -2.6, 8);
      interactiveObjects.push({
        id: "chair_board","""

new_chair_board = """      createSeatedRoleHolder(0, 0, -2.6, 8, {
        holder: "Governor of Board",
        roleTitle: "Floor 8 Seat Holder",
        color: 0x967822,
        tieColor: 0xd4af37,
        hairColor: 0x332218
      });
      interactiveObjects.push({
        id: "chair_board","""

if old_chair_board in text:
    text = text.replace(old_chair_board, new_chair_board)
    print("Replaced chair_board with seated role holder")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved index.html successfully")
