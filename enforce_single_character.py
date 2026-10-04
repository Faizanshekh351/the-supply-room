with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update createSeatedRoleHolder desk sizing
old_holder_desk = "createDesk(x, y, z + 1.25, 4.2, 1.4, roleData.deskColor || 0x3d2719);"
new_holder_desk = "createDesk(x, y, z + 1.45, 7.2, 2.4, roleData.deskColor || 0x2c180d);"
if old_holder_desk in text:
    text = text.replace(old_holder_desk, new_holder_desk)

text = text.replace("addBoxCollider(x, z + 1.25, 4.5, 1.6);", "addBoxCollider(x, z + 1.45, 7.6, 2.6);")
text = text.replace("pos: new THREE.Vector3(x, y, z + 2.3),", "pos: new THREE.Vector3(x, y, z + 2.8),")

# 2. Floor 1: Remove second character
old_f1_dual = """      createSeatedRoleHolder(8, 0, -6, 1, {
        holder: "Junior Courier",
        roleTitle: "Floor 1 Dispatcher",
        color: 0x3d6b4e,
        tieColor: 0xd4af37,
        hairColor: 0x221309
      });"""
new_f1_dual = """      createChair(8, 0, -6, 1);"""
if old_f1_dual in text:
    text = text.replace(old_f1_dual, new_f1_dual)
    print("Cleaned Floor 1 to 1 character")

# 3. Floor 2: Remove second character
old_f2_dual = """      createSeatedRoleHolder(7, 0, -5, 2, {
        holder: "Assistant Auditor",
        roleTitle: "Floor 2 Contender",
        color: 0x3a5a7a,
        tieColor: 0xb08a3c,
        hairColor: 0x221309
      });"""
new_f2_dual = """      createChair(7, 0, -5, 2);"""
if old_f2_dual in text:
    text = text.replace(old_f2_dual, new_f2_dual)
    print("Cleaned Floor 2 to 1 character")

# 4. Floor 3: Remove second character
old_f3_dual = """      createSeatedRoleHolder(6, 0, 2, 3, {
        holder: "Pit Arbitrageur",
        roleTitle: "Associate Arbitrageur",
        color: 0x2d4d3a,
        tieColor: 0x7a2e2e,
        hairColor: 0x3d2719
      });"""
new_f3_dual = """      createChair(6, 0, 2, 3);"""
if old_f3_dual in text:
    text = text.replace(old_f3_dual, new_f3_dual)
    print("Cleaned Floor 3 to 1 character")

# 5. Floor 4: Clean up second character
old_f4_dual = """      createSeatedRoleHolder(0, 0, -4.8, 4, {
        holder: "VP Syndications",
        roleTitle: "Syndicate VP",
        color: 0x5a3518,
        tieColor: 0xb08a3c,
        hairColor: 0x442211
      });
      interactiveObjects.push({
        id: "chair_vp",
        label: "Musical Chair Dispute: Beige Task Chair",
        pos: new THREE.Vector3(0, 0, -4.8),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(4)
      });"""
new_f4_dual = """      createChair(7, 0, -5, 4);
      interactiveObjects.push({
        id: "chair_vp",
        label: "Musical Chair Dispute: Beige Task Chair",
        pos: new THREE.Vector3(7, 0, -5),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(4)
      });"""
if old_f4_dual in text:
    text = text.replace(old_f4_dual, new_f4_dual)
    print("Cleaned Floor 4 to 1 character")

# 6. Floor 5: Remove second character
old_f5_dual = """      createSeatedRoleHolder(6, 0, 2, 5, {
        holder: "Compliance Inspector",
        roleTitle: "Director Assistant",
        color: 0x3e4a59,
        tieColor: 0x7a2e2e,
        hairColor: 0x221309
      });"""
new_f5_dual = """      createChair(6, 0, 2, 5);"""
if old_f5_dual in text:
    text = text.replace(old_f5_dual, new_f5_dual)
    print("Cleaned Floor 5 to 1 character")

# 7. Floor 6: Remove second character at (-6, 0, 2)
old_f6_dual = """      createSeatedRoleHolder(-6, 0, 2, 6, {
        holder: "Managing Director what3verman",
        roleTitle: "Floor 6 Seat Holder",
        color: 0x1f4728,
        tieColor: 0xb9902f,
        hairColor: 0x221309
      });
      interactiveObjects.push({
        id: "chair_md",
        label: "Musical Chair Dispute: Green Banker's Chair (Boss Showdown)",
        pos: new THREE.Vector3(-6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(6)
      });"""
new_f6_dual = """      createChair(-7, 0, -4, 6);
      interactiveObjects.push({
        id: "chair_md",
        label: "Musical Chair Dispute: Green Banker's Chair (Boss Showdown)",
        pos: new THREE.Vector3(-7, 0, -4),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(6)
      });"""
if old_f6_dual in text:
    text = text.replace(old_f6_dual, new_f6_dual)
    print("Cleaned Floor 6 to 1 character")

# 8. Floor 7: Remove second character
old_f7_dual = """      createSeatedRoleHolder(6, 0, 2, 7, {
        holder: "Senior Underwriter",
        roleTitle: "Syndicate Underwriter",
        color: 0x421b1b,
        tieColor: 0xd4af37,
        hairColor: 0x2e1a0d
      });"""
new_f7_dual = """      createChair(6, 0, 2, 7);"""
if old_f7_dual in text:
    text = text.replace(old_f7_dual, new_f7_dual)
    print("Cleaned Floor 7 to 1 character")

# 9. Floor 8: Only 1 Chairman presiding
old_f8_circle = """      const govColors = [0x967822, 0x4e6b5a, 0x3d4a6e, 0x6e3d5a, 0x5a4a3d, 0x7a2e2e];
      for (let i = 0; i < 6; i++) {
        const ang = (i * Math.PI * 2) / 6;
        createSeatedRoleHolder(Math.sin(ang) * 5.0, 0, Math.cos(ang) * 5.0, 8, {
          holder: `Governor ${i + 1}`,
          roleTitle: "Board Governor",
          color: govColors[i],
          tieColor: 0xd4af37,
          hairColor: 0x332218
        });
      }"""
new_f8_circle = """      for (let i = 0; i < 6; i++) {
        const ang = (i * Math.PI * 2) / 6;
        createChair(Math.sin(ang) * 5.0, 0, Math.cos(ang) * 5.0, 8, ang + Math.PI);
      }
      createSeatedRoleHolder(0, 0, -3.2, 8, {
        holder: "Executive Governor",
        roleTitle: "Governor of Board · Floor 8",
        color: 0x967822,
        shirtColor: 0xfdfdfd,
        tieColor: 0xd4af37,
        skinColor: 0xebb992,
        hairColor: 0x332218,
        hairStyle: "bald_sides",
        hasGlasses: true,
        caseColor: 0x3a2211,
        action: openBoardConclaveModal
      });"""
if old_f8_circle in text:
    text = text.replace(old_f8_circle, new_f8_circle)
    print("Cleaned Floor 8 to 1 presiding Governor")

# 10. Also position floor 4 role holder at (0, 0, -2.5) with room to breathe
text = text.replace("createSeatedRoleHolder(0, 0, -1.8, 4", "createSeatedRoleHolder(0, 0, -2.5, 4")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved index.html with 1 character per floor & spacious layout!")
