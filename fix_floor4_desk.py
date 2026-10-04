with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# On Floor 4, put the dispute chair on the side at (-6, 0, 1) with no desk in front of it!
old_f4_dispute = """      createSeatedRoleHolder(0, 0, -4.8, 4, {
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

new_f4_dispute = """      createSeatedRoleHolder(-6, 0, 1, 4, {
        holder: "VP Syndications",
        roleTitle: "Syndicate VP",
        color: 0x5a3518,
        tieColor: 0xb08a3c,
        skinColor: 0x6e432c,
        hairColor: 0x1f130c,
        noDesk: true
      });
      interactiveObjects.push({
        id: "chair_vp",
        label: "Musical Chair Dispute: Beige Task Chair",
        pos: new THREE.Vector3(-6, 0, 1),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(4)
      });"""

if old_f4_dispute in text:
    text = text.replace(old_f4_dispute, new_f4_dispute)
    print("Replaced old_f4_dispute successfully")

# In createSeatedRoleHolder, only build desk if not roleData.noDesk
old_desk_creation = """      // Official Desk in front of them
      createDesk(x, y, z + 1.25, 4.2, 1.4, roleData.deskColor || 0x3d2719);

      // Solid Collision Bounds so player CANNOT walk through desk or chair!
      addBoxCollider(x, z + 1.25, 4.5, 1.6);
      addBoxCollider(x, z, 1.4, 1.4);"""

new_desk_creation = """      if (!roleData.noDesk) {
        // Official Desk in front of them
        createDesk(x, y, z + 1.25, 4.2, 1.4, roleData.deskColor || 0x3d2719);
        addBoxCollider(x, z + 1.25, 4.5, 1.6);
      }
      addBoxCollider(x, z, 1.4, 1.4);"""

if old_desk_creation in text:
    text = text.replace(old_desk_creation, new_desk_creation)
    print("Added noDesk support to createSeatedRoleHolder")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Floor 4 layout and noDesk condition updated cleanly!")
