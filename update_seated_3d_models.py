with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace createSeatedRoleHolder with the distinct 3D character generator mapping to the gallery plates
old_seated_func_start = "    function createSeatedRoleHolder(x, y, z, floorTier, roleData) {"
old_seated_func_end = "        action: roleData.action || (() => {\n          openRoleHolderQuestModal(floorTier, roleData);\n        })\n      });\n    }"

new_seated_func = """    function createSeatedRoleHolder(x, y, z, floorTier, roleData) {
      const holderGroup = new THREE.Group();
      holderGroup.position.set(x, y, z);
      roomGroup.add(holderGroup);

      // Chair for this floor
      const chair = createChair(0, 0, 0, floorTier, 0);
      holderGroup.add(chair);

      // Distinct character visual attributes mapped to gallery plates
      const suitColor = roleData.color || 0x223654;
      const suitMat = new THREE.MeshLambertMaterial({ color: suitColor });
      const shirtMat = new THREE.MeshLambertMaterial({ color: roleData.shirtColor || 0xf7f4ef });
      const tieMat = new THREE.MeshLambertMaterial({ color: roleData.tieColor || 0x7a2e2e });
      const skinMat = new THREE.MeshLambertMaterial({ color: roleData.skinColor || 0xebb992 });
      const hairMat = new THREE.MeshLambertMaterial({ color: roleData.hairColor || 0x332218 });
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0x181512, roughness: 0.4 });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x111111 });
      const eyeWhiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

      // Torso / Suit jacket
      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.76, 0.38), suitMat);
      torso.position.set(0, 1.15, -0.08);
      torso.castShadow = true;
      holderGroup.add(torso);

      // Shirt collar / bib
      const shirt = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.34, 0.02), shirtMat);
      shirt.position.set(0, 1.30, 0.115);
      holderGroup.add(shirt);

      // Necktie (if not bowtie or open collar)
      if (roleData.hasBowtie) {
        const bowtie = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.03), tieMat);
        bowtie.position.set(0, 1.40, 0.13);
        holderGroup.add(bowtie);
      } else if (!roleData.noTie) {
        const tie = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.38, 0.03), tieMat);
        tie.position.set(0, 1.23, 0.125);
        holderGroup.add(tie);
      }

      // Head
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.40, 0.42, 0.36), skinMat);
      head.position.set(0, 1.74, -0.06);
      head.castShadow = true;
      holderGroup.add(head);

      // Eyes
      const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.07, 0.02), eyeWhiteMat);
      eyeL.position.set(-0.10, 1.78, 0.125);
      holderGroup.add(eyeL);
      const pupilL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.02), eyeMat);
      pupilL.position.set(-0.09, 1.78, 0.135);
      holderGroup.add(pupilL);

      const eyeR = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.07, 0.02), eyeWhiteMat);
      eyeR.position.set(0.10, 1.78, 0.125);
      holderGroup.add(eyeR);
      const pupilR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.02), eyeMat);
      pupilR.position.set(0.09, 1.78, 0.135);
      holderGroup.add(pupilR);

      // Distinct Hair Styles
      if (roleData.hairStyle === 'bald_sides') {
        // Balding with side fringe (Plate 11 Managing Director what3verman style)
        const hairL = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.28, 0.38), hairMat);
        hairL.position.set(-0.21, 1.76, -0.06);
        holderGroup.add(hairL);
        const hairR = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.28, 0.38), hairMat);
        hairR.position.set(0.21, 1.76, -0.06);
        holderGroup.add(hairR);
        const hairB = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.24, 0.06), hairMat);
        hairB.position.set(0, 1.76, -0.22);
        holderGroup.add(hairB);
      } else if (roleData.hairStyle === 'afro' || roleData.hairStyle === 'short_dark') {
        const hairTop = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.16, 0.40), hairMat);
        hairTop.position.set(0, 1.96, -0.06);
        holderGroup.add(hairTop);
      } else if (roleData.hairStyle === 'bob') {
        const hairTop = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.20, 0.42), hairMat);
        hairTop.position.set(0, 1.96, -0.06);
        holderGroup.add(hairTop);
        const hairSideL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.36, 0.38), hairMat);
        hairSideL.position.set(-0.21, 1.74, -0.06);
        holderGroup.add(hairSideL);
        const hairSideR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.36, 0.38), hairMat);
        hairSideR.position.set(0.21, 1.74, -0.06);
        holderGroup.add(hairSideR);
      } else {
        const hairTop = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.14, 0.38), hairMat);
        hairTop.position.set(0, 1.94, -0.06);
        holderGroup.add(hairTop);
      }

      // Glasses or Boss Crown
      if (roleData.hasCrown) {
        const crownMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.2 });
        const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.22, 0.16, 8), crownMat);
        crown.position.set(0, 2.05, -0.06);
        holderGroup.add(crown);
      } else if (roleData.hasGlasses) {
        const frameColor = roleData.glassesColor || 0xb9902f;
        const frameMat = new THREE.MeshLambertMaterial({ color: frameColor });
        const gL = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.04), frameMat);
        gL.position.set(-0.10, 1.78, 0.13);
        holderGroup.add(gL);
        const gR = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.04), frameMat);
        gR.position.set(0.10, 1.78, 0.13);
        holderGroup.add(gR);
        const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.03, 0.04), frameMat);
        bridge.position.set(0, 1.79, 0.13);
        holderGroup.add(bridge);
      }

      // Upper Legs (Horizontal forward on chair seat)
      const legColor = roleData.pantsColor || suitColor;
      const legMat = new THREE.MeshLambertMaterial({ color: legColor });
      const upperLegL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.52), legMat);
      upperLegL.position.set(-0.16, 0.72, 0.18);
      holderGroup.add(upperLegL);

      const upperLegR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.52), legMat);
      upperLegR.position.set(0.16, 0.72, 0.18);
      holderGroup.add(upperLegR);

      // Lower Legs (Vertical to floor)
      const lowerLegL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.45, 0.18), legMat);
      lowerLegL.position.set(-0.16, 0.42, 0.38);
      holderGroup.add(lowerLegL);

      const lowerLegR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.45, 0.18), legMat);
      lowerLegR.position.set(0.16, 0.42, 0.38);
      holderGroup.add(lowerLegR);

      // Shoes
      const shoeL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.24), shoeMat);
      shoeL.position.set(-0.16, 0.18, 0.42);
      holderGroup.add(shoeL);

      const shoeR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.08, 0.24), shoeMat);
      shoeR.position.set(0.16, 0.18, 0.42);
      holderGroup.add(shoeR);

      // Arms resting on desk
      const armL = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.44, 0.16), suitMat);
      armL.position.set(-0.44, 1.05, 0.05);
      holderGroup.add(armL);

      const armR = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.44, 0.16), suitMat);
      armR.position.set(0.44, 1.05, 0.05);
      holderGroup.add(armR);

      // Briefcase placed beside desk (matching Gallery Plates!)
      const caseMat = new THREE.MeshLambertMaterial({ color: roleData.caseColor || 0x4a2c16 });
      const bCase = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.52, 0.68), caseMat);
      bCase.position.set(2.4, 0.26, 0.9);
      bCase.castShadow = true;
      holderGroup.add(bCase);
      const caseHandle = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.10, 0.22), new THREE.MeshLambertMaterial({ color: 0xd4af37 }));
      caseHandle.position.set(2.4, 0.56, 0.9);
      holderGroup.add(caseHandle);

      // Official Desk in front of them
      createDesk(x, y, z + 1.25, 4.2, 1.4, roleData.deskColor || 0x3d2719);

      // Solid Collision Bounds so player CANNOT walk through desk or chair!
      addBoxCollider(x, z + 1.25, 4.5, 1.6);
      addBoxCollider(x, z, 1.4, 1.4);

      // Interactive Trigger
      interactiveObjects.push({
        id: `role_holder_f${floorTier}_${Math.round(x*10)}`,
        label: `${roleData.holder}: ${roleData.roleTitle}`,
        pos: new THREE.Vector3(x, y, z + 2.3),
        radius: 2.5,
        action: roleData.action || (() => {
          openRoleHolderQuestModal(floorTier, roleData);
        })
      });
    }"""

idx_start = text.find(old_seated_func_start)
idx_end = text.find(old_seated_func_end)
assert idx_start != -1 and idx_end != -1, "createSeatedRoleHolder block not found"

text = text[:idx_start] + new_seated_func + text[idx_end + len(old_seated_func_end):]

# Now update the floor role definitions to match the gallery plates!
# Floor 6 MD what3verman (Gallery Plate 11: dark grey suit, maroon tie, bald head with glasses)
old_f6_md_seated = """      createSeatedRoleHolder(0, 0, -3.2, 6, {
        holder: "what3verman",
        roleTitle: "Managing Director · Floor 6",
        color: 0x1f4728,
        tieColor: 0xb9902f,
        hairColor: 0x221309
      });"""

new_f6_md_seated = """      createSeatedRoleHolder(0, 0, -3.2, 6, {
        holder: "what3verman",
        roleTitle: "Managing Director · Floor 6",
        color: 0x2c2b30,
        tieColor: 0x6e1b24,
        skinColor: 0xebb992,
        hairColor: 0x696870,
        hairStyle: "bald_sides",
        hasGlasses: true,
        glassesColor: 0xa0a0a8,
        caseColor: 0x3e2213,
        action: openWhat3vermanModal
      });"""
text = text.replace(old_f6_md_seated, new_f6_md_seated)

# Floor 2 Analyst (Gallery Plate 02: pale white/grey mannequin face, dark charcoal suit, blue collar)
old_f2_seated = """      createSeatedRoleHolder(0, 0, -2.5, 2, {
        holder: "Senior Ledger Archivist",
        roleTitle: "Auditing Lead · Floor 2",
        color: 0x8a4a2a,
        tieColor: 0xd4af37,
        hairColor: 0x332218,
        action: openAnalystLedgerModal
      });"""

new_f2_seated = """      createSeatedRoleHolder(0, 0, -2.5, 2, {
        holder: "Senior Ledger Archivist",
        roleTitle: "Auditing Lead · Floor 2",
        color: 0x333230,
        shirtColor: 0xf0efe8,
        tieColor: 0x2b384d,
        skinColor: 0xf2ede4,
        hairColor: 0xd8d4cc,
        hairStyle: "bob",
        noTie: true,
        caseColor: 0x4a2e1c,
        action: openAnalystLedgerModal
      });"""
text = text.replace(old_f2_seated, new_f2_seated)

# Floor 3 Associate (Gallery Plate 03: brown skin, charcoal suit, crimson tie, short dark hair)
old_f3_seated = """      createSeatedRoleHolder(0, 0, -3.2, 3, {
        holder: "Head Trading Associate",
        roleTitle: "Floor Broker · Floor 3",
        color: 0xb08a3c,
        tieColor: 0x223654,
        hairColor: 0x1f140e,
        action: openDengModal
      });"""

new_f3_seated = """      createSeatedRoleHolder(0, 0, -3.2, 3, {
        holder: "Head Trading Associate",
        roleTitle: "Floor Broker · Floor 3",
        color: 0x3d3f45,
        shirtColor: 0xf8f8f8,
        tieColor: 0x801824,
        skinColor: 0x6e432c,
        hairColor: 0x1f130c,
        hairStyle: "afro",
        caseColor: 0x8c8f94,
        action: openDengModal
      });"""
text = text.replace(old_f3_seated, new_f3_seated)

# Floor 4 VP (Gallery Plate 04 / 06: white shirt, black tie, glasses, brown hair)
old_f4_seated = """      createSeatedRoleHolder(0, 0, -1.8, 4, {
        holder: "Senior Market Analyst",
        roleTitle: "Vice President Desk · Floor 4",
        color: 0x4a6b8c,
        tieColor: 0xd4af37,
        hairColor: 0x221309,
        action: openSubscriptionModal
      });"""

new_f4_seated = """      createSeatedRoleHolder(0, 0, -1.8, 4, {
        holder: "Senior Market Analyst",
        roleTitle: "Vice President Desk · Floor 4",
        color: 0xf2efe9,
        pantsColor: 0x3c3c40,
        tieColor: 0x181818,
        skinColor: 0xedbf9e,
        hairColor: 0x4a2f1e,
        hairStyle: "short_dark",
        hasGlasses: true,
        glassesColor: 0xa87c32,
        caseColor: 0x4a2a16,
        action: openSubscriptionModal
      });"""
text = text.replace(old_f4_seated, new_f4_seated)

# Floor 1 Courier (Gallery Plate 01: grey suit, green tie, tan skin)
old_f1_seated = """      createSeatedRoleHolder(0, 0, -2.5, 1, {
        holder: "Chief Mail Clerk",
        roleTitle: "Head of Couriers · Floor 1",
        color: 0x4e8a5a,
        tieColor: 0x7a2e2e,
        hairColor: 0x221309
      });"""

new_f1_seated = """      createSeatedRoleHolder(0, 0, -2.5, 1, {
        holder: "Chief Mail Clerk",
        roleTitle: "Head of Couriers · Floor 1",
        color: 0x444b52,
        shirtColor: 0xffffff,
        tieColor: 0x2f6b3d,
        skinColor: 0xebb992,
        hairColor: 0x26160c,
        caseColor: 0x5a341b
      });"""
text = text.replace(old_f1_seated, new_f1_seated)

# Floor 5 Director (Gallery Plate 05: dark blue navy suit, yellow/gold tie)
old_f5_seated = """      createSeatedRoleHolder(0, 0, -2.5, 5, {
        holder: "Chief Compliance Dir.",
        roleTitle: "Director of Records · Floor 5",
        color: 0x6e5d8c,
        tieColor: 0xd4af37,
        hairColor: 0x332218,
        action: openDossierArchiveModal
      });"""

new_f5_seated = """      createSeatedRoleHolder(0, 0, -2.5, 5, {
        holder: "Chief Compliance Dir.",
        roleTitle: "Director of Records · Floor 5",
        color: 0x1b283d,
        shirtColor: 0xfdfdfd,
        tieColor: 0xd4af37,
        skinColor: 0xdfab87,
        hairColor: 0x24160d,
        hasGlasses: true,
        glassesColor: 0x1f140e,
        caseColor: 0x2a1a10,
        action: openDossierArchiveModal
      });"""
text = text.replace(old_f5_seated, new_f5_seated)

# Floor 7 Partner (Gallery Plate 07: dark maroon suit, gold tie, grey hair)
old_f7_seated = """      createSeatedRoleHolder(0, 0, -2.5, 7, {
        holder: "General Counsel",
        roleTitle: "Syndicate Trustee · Floor 7",
        color: 0x7a2e2e,
        tieColor: 0x211b14,
        hairColor: 0x4a3424,
        action: openPartnerSyndicateModal
      });"""

new_f7_seated = """      createSeatedRoleHolder(0, 0, -2.5, 7, {
        holder: "General Counsel",
        roleTitle: "Syndicate Trustee · Floor 7",
        color: 0x541818,
        shirtColor: 0xf6f2ea,
        tieColor: 0xd4af37,
        skinColor: 0xebb992,
        hairColor: 0x636166,
        hasGlasses: true,
        glassesColor: 0xb08a3c,
        caseColor: 0x3d1b10,
        action: openPartnerSyndicateModal
      });"""
text = text.replace(old_f7_seated, new_f7_seated)

# Floor 9 Kingpickle (Penthouse Sovereign with crown and royal burgundy)
old_f9_seated = """      createSeatedRoleHolder(-5, 0, -2, 9, {
        holder: "The Chairman Kingpickle",
        roleTitle: "Chairman of the Board · Seat 0",
        color: 0x110b06,
        tieColor: 0xd4af37,
        hairColor: 0x5a3d28,
        hasCrown: true
      });"""

new_f9_seated = """      createSeatedRoleHolder(-5, 0, -2, 9, {
        holder: "The Chairman Kingpickle",
        roleTitle: "Chairman of the Board · Seat 0",
        color: 0x1a120b,
        shirtColor: 0xfdf6e2,
        tieColor: 0xffd700,
        skinColor: 0xebb992,
        hairColor: 0xdfdfdf,
        hasCrown: true,
        caseColor: 0x801818
      });"""
text = text.replace(old_f9_seated, new_f9_seated)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('3D Seated Role Holders updated with unique faces, eyes, hair, glasses and briefcases matching gallery plates!')
