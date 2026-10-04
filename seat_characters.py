with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Floor 1 intern chair with seated character
old_f1_chair = """      createChair(8, 0, -6, 1);
      interactiveObjects.push({
        id: "chair_intern",
        label: "Musical Chair Dispute: The Intern's Folding Chair",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(1)
      });"""

new_f1_chair = """      createSeatedRoleHolder(8, 0, -6, 1, {
        holder: "Junior Courier",
        roleTitle: "Floor 1 Dispatcher",
        color: 0x3d6b4e,
        tieColor: 0xd4af37,
        hairColor: 0x221309
      });
      interactiveObjects.push({
        id: "chair_intern",
        label: "Musical Chair Dispute: The Intern's Folding Chair",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(1)
      });"""
text = text.replace(old_f1_chair, new_f1_chair)

# 2. Update Floor 2 Analyst
old_f2 = """    // 2. FLOOR 2: ANALYST
    function buildFloor2Analyst() {
      createDesk(0, 0, -1, 7, 2.0, 0x4a321d);

      interactiveObjects.push({
        id: "audit_ledger",
        label: "Ledger Desk: Audit Department Balance Sheets",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.5,
        action: openAnalystLedgerModal
      });

      createChair(7, 0, -5, 2);
      interactiveObjects.push({
        id: "chair_analyst",
        label: "Musical Chair Dispute: The Typist Stool",
        pos: new THREE.Vector3(7, 0, -5),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(2)
      });
    }"""

new_f2 = """    // 2. FLOOR 2: ANALYST
    function buildFloor2Analyst() {
      createSeatedRoleHolder(0, 0, -2.5, 2, {
        holder: "Senior Ledger Archivist",
        roleTitle: "Auditing Lead · Floor 2",
        color: 0x8a4a2a,
        tieColor: 0xd4af37,
        hairColor: 0x332218,
        action: openAnalystLedgerModal
      });

      interactiveObjects.push({
        id: "audit_ledger",
        label: "Ledger Desk: Audit Department Balance Sheets",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.5,
        action: openAnalystLedgerModal
      });

      createSeatedRoleHolder(7, 0, -5, 2, {
        holder: "Assistant Auditor",
        roleTitle: "Floor 2 Contender",
        color: 0x3a5a7a,
        tieColor: 0xb08a3c,
        hairColor: 0x221309
      });
      interactiveObjects.push({
        id: "chair_analyst",
        label: "Musical Chair Dispute: The Typist Stool",
        pos: new THREE.Vector3(7, 0, -5),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(2)
      });
    }"""
text = text.replace(old_f2, new_f2)

# 3. Update Floor 3 Associate
old_f3 = """    // 3. FLOOR 3: ASSOCIATE
    function buildFloor3Associate() {
      createDesk(0, 0, -2, 8, 2.2, 0x331e10);

      const grille = new THREE.Mesh(new THREE.BoxGeometry(8, 2.2, 0.1), new THREE.MeshLambertMaterial({ color: 0xb08a3c, wireframe: true }));
      grille.position.set(0, 2.5, -2);
      roomGroup.add(grille);

      interactiveObjects.push({
        id: "deng_window",
        label: "Cashier Window: Tender Deng Credit Deposit",
        pos: new THREE.Vector3(-2, 0, -2),
        radius: 2.4,
        action: openDengModal
      });

      interactiveObjects.push({
        id: "forge_pass",
        label: "Embossing Press: Mint TMF Pass",
        pos: new THREE.Vector3(2, 0, -2),
        radius: 2.4,
        action: forgePassAction
      });

      createChair(6, 0, 2, 3);
      interactiveObjects.push({
        id: "chair_associate",
        label: "Musical Chair Dispute: Creaking Wooden Swivel",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(3)
      });
    }"""

new_f3 = """    // 3. FLOOR 3: ASSOCIATE
    function buildFloor3Associate() {
      createSeatedRoleHolder(0, 0, -3.2, 3, {
        holder: "Head Trading Associate",
        roleTitle: "Floor Broker · Floor 3",
        color: 0xb08a3c,
        tieColor: 0x223654,
        hairColor: 0x1f140e,
        action: openDengModal
      });

      const grille = new THREE.Mesh(new THREE.BoxGeometry(8, 2.2, 0.1), new THREE.MeshLambertMaterial({ color: 0xb08a3c, wireframe: true }));
      grille.position.set(0, 2.5, -2);
      roomGroup.add(grille);

      interactiveObjects.push({
        id: "deng_window",
        label: "Cashier Window: Tender Deng Credit Deposit",
        pos: new THREE.Vector3(-2, 0, -2),
        radius: 2.4,
        action: openDengModal
      });

      interactiveObjects.push({
        id: "forge_pass",
        label: "Embossing Press: Mint TMF Pass",
        pos: new THREE.Vector3(2, 0, -2),
        radius: 2.4,
        action: forgePassAction
      });

      createSeatedRoleHolder(6, 0, 2, 3, {
        holder: "Pit Arbitrageur",
        roleTitle: "Associate Arbitrageur",
        color: 0x2d4d3a,
        tieColor: 0x7a2e2e,
        hairColor: 0x3d2719
      });
      interactiveObjects.push({
        id: "chair_associate",
        label: "Musical Chair Dispute: Creaking Wooden Swivel",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(3)
      });
    }"""
text = text.replace(old_f3, new_f3)

# 4. Update Floor 4 VP
old_f4 = """    // 4. FLOOR 4: VICE PRESIDENT
    function buildFloor4VP() {
      createDesk(0, 0, 0, 7, 2.4, 0x472e18);

      interactiveObjects.push({
        id: "subscription_desk",
        label: "Vice President Desk: Audit Shareholder Roll",
        pos: new THREE.Vector3(0, 0, 0),
        radius: 2.6,
        action: openSubscriptionModal
      });

      createChair(0, 0, -4, 4);
      interactiveObjects.push({
        id: "chair_vp",
        label: "Musical Chair Dispute: Beige Task Chair",
        pos: new THREE.Vector3(0, 0, -4),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(4)
      });
    }"""

new_f4 = """    // 4. FLOOR 4: VICE PRESIDENT
    function buildFloor4VP() {
      createSeatedRoleHolder(0, 0, -1.8, 4, {
        holder: "Senior Market Analyst",
        roleTitle: "Vice President Desk · Floor 4",
        color: 0x4a6b8c,
        tieColor: 0xd4af37,
        hairColor: 0x221309,
        action: openSubscriptionModal
      });

      interactiveObjects.push({
        id: "subscription_desk",
        label: "Vice President Desk: Audit Shareholder Roll",
        pos: new THREE.Vector3(0, 0, 0),
        radius: 2.6,
        action: openSubscriptionModal
      });

      createSeatedRoleHolder(0, 0, -4.8, 4, {
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
      });
    }"""
text = text.replace(old_f4, new_f4)

# 5. Update Floor 5 Director
old_f5 = """    // 5. FLOOR 5: DIRECTOR
    function buildFloor5Director() {
      createDesk(0, 0, -1, 8, 2.4, 0x2e1a0d);

      interactiveObjects.push({
        id: "dossier_terminal",
        label: "Director Archive: Inspect Flagged Dossiers",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.6,
        action: openDossierArchiveModal
      });

      createChair(6, 0, 2, 5);
      interactiveObjects.push({
        id: "chair_director",
        label: "Musical Chair Dispute: High-Back Leather Desk Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(5)
      });
    }"""

new_f5 = """    // 5. FLOOR 5: DIRECTOR
    function buildFloor5Director() {
      createSeatedRoleHolder(0, 0, -2.5, 5, {
        holder: "Chief Compliance Dir.",
        roleTitle: "Director of Records · Floor 5",
        color: 0x6e5d8c,
        tieColor: 0xd4af37,
        hairColor: 0x332218,
        action: openDossierArchiveModal
      });

      interactiveObjects.push({
        id: "dossier_terminal",
        label: "Director Archive: Inspect Flagged Dossiers",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.6,
        action: openDossierArchiveModal
      });

      createSeatedRoleHolder(6, 0, 2, 5, {
        holder: "Compliance Inspector",
        roleTitle: "Director Assistant",
        color: 0x3e4a59,
        tieColor: 0x7a2e2e,
        hairColor: 0x221309
      });
      interactiveObjects.push({
        id: "chair_director",
        label: "Musical Chair Dispute: High-Back Leather Desk Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(5)
      });
    }"""
text = text.replace(old_f5, new_f5)

# 6. Update Floor 7 Partner
old_f7 = """    // 7. FLOOR 7: PARTNER
    function buildFloor7Partner() {
      createDesk(0, 0, -1, 10, 2.8, 0x1f0f08);

      interactiveObjects.push({
        id: "partner_syndicate",
        label: "Partner Chamber: Review Underwriting Treaties",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.6,
        action: openPartnerSyndicateModal
      });

      createChair(6, 0, 2, 7);
      interactiveObjects.push({
        id: "chair_partner",
        label: "Musical Chair Dispute: Oxblood Wingback Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(7)
      });
    }"""

new_f7 = """    // 7. FLOOR 7: PARTNER
    function buildFloor7Partner() {
      createSeatedRoleHolder(0, 0, -2.5, 7, {
        holder: "General Counsel",
        roleTitle: "Syndicate Trustee · Floor 7",
        color: 0x7a2e2e,
        tieColor: 0x211b14,
        hairColor: 0x4a3424,
        action: openPartnerSyndicateModal
      });

      interactiveObjects.push({
        id: "partner_syndicate",
        label: "Partner Chamber: Review Underwriting Treaties",
        pos: new THREE.Vector3(0, 0, -1),
        radius: 2.6,
        action: openPartnerSyndicateModal
      });

      createSeatedRoleHolder(6, 0, 2, 7, {
        holder: "Senior Underwriter",
        roleTitle: "Syndicate Underwriter",
        color: 0x421b1b,
        tieColor: 0xd4af37,
        hairColor: 0x2e1a0d
      });
      interactiveObjects.push({
        id: "chair_partner",
        label: "Musical Chair Dispute: Oxblood Wingback Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(7)
      });
    }"""
text = text.replace(old_f7, new_f7)

# 7. Update Floor 8 Board of Governors with seated characters
old_f8 = """    // 8. FLOOR 8: BOARD OF DIRECTORS
    function buildFloor8Board() {
      const table = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.2, 0.2, 32), new THREE.MeshLambertMaterial({ color: 0x2d170a }));
      table.position.set(0, 1.25, 0);
      roomGroup.add(table);

      for (let i = 0; i < 6; i++) {
        const ang = (i * Math.PI * 2) / 6;
        createChair(Math.sin(ang) * 5.0, 0, Math.cos(ang) * 5.0, 8, ang + Math.PI);
      }

      interactiveObjects.push({
        id: "board_conclave",
        label: "Boardroom Conclave: Concur With Governors",
        pos: new THREE.Vector3(0, 0, 0),
        radius: 3.2,
        action: openBoardConclaveModal
      });

      createChair(0, 0, -2.6, 8);
      interactiveObjects.push({
        id: "chair_board",
        label: "Musical Chair Dispute: Board of Directors High Seat",
        pos: new THREE.Vector3(0, 0, -2.6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(8)
      });
    }"""

new_f8 = """    // 8. FLOOR 8: BOARD OF DIRECTORS
    function buildFloor8Board() {
      const table = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.2, 0.2, 32), new THREE.MeshLambertMaterial({ color: 0x2d170a }));
      table.position.set(0, 1.25, 0);
      roomGroup.add(table);

      const govColors = [0x967822, 0x4e6b5a, 0x3d4a6e, 0x6e3d5a, 0x5a4a3d, 0x7a2e2e];
      for (let i = 0; i < 6; i++) {
        const ang = (i * Math.PI * 2) / 6;
        createSeatedRoleHolder(Math.sin(ang) * 5.0, 0, Math.cos(ang) * 5.0, 8, {
          holder: `Governor ${i + 1}`,
          roleTitle: "Board Governor",
          color: govColors[i],
          tieColor: 0xd4af37,
          hairColor: 0x332218
        });
      }

      interactiveObjects.push({
        id: "board_conclave",
        label: "Boardroom Conclave: Concur With Governors",
        pos: new THREE.Vector3(0, 0, 0),
        radius: 3.2,
        action: openBoardConclaveModal
      });

      interactiveObjects.push({
        id: "chair_board",
        label: "Musical Chair Dispute: Board of Directors High Seat",
        pos: new THREE.Vector3(0, 0, -2.6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(8)
      });
    }"""
text = text.replace(old_f8, new_f8)

# 8. Floor 6 Boss what3verman chair:
text = text.replace('createChair(0, 0, -3.2, 6);', """createSeatedRoleHolder(0, 0, -3.2, 6, {
        holder: "what3verman",
        roleTitle: "Managing Director · Floor 6",
        color: 0x1f4728,
        tieColor: 0xb9902f,
        hairColor: 0x221309
      });""")

# 9. Floor 9 Boss Kingpickle throne:
text = text.replace('createChair(-5, 0, -2, 9);', """createSeatedRoleHolder(-5, 0, -2, 9, {
        holder: "The Chairman Kingpickle",
        roleTitle: "Chairman of the Board · Seat 0",
        color: 0x110b06,
        tieColor: 0xd4af37,
        hairColor: 0x5a3d28,
        hasCrown: true
      });""")

# 10. Fix intro preview thumbnails to only show [player, holder] with neat VS badge
old_preview_calc = "previewDiv.innerHTML = arenaContenders.map(c => `<img class=\"chamber-thumb\" src=\"${c.avatar}\" title=\"${c.name}\">`).join('');"
new_preview_calc = """previewDiv.innerHTML = arenaContenders.slice(0, 2).map((c, idx) => `
        <div style="display:inline-flex;flex-direction:column;align-items:center;gap:4px;margin:0 12px;">
          <img class="chamber-thumb" style="width:58px;height:58px;border:3px solid ${c.color};border-radius:4px;" src="${c.avatar}" alt="${c.name}">
          <span style="font-size:11px;font-weight:700;color:#211b14;font-family:'Cinzel',serif;">${c.name}</span>
          <small style="font-size:9px;color:#7a6d5d;font-family:'IBM Plex Mono',monospace;">${idx === 0 ? 'YOU' : 'RIVAL'}</small>
        </div>
      `).join('<div style="display:inline-block;font-size:20px;font-weight:900;color:#7a2e2e;font-family:\'Cinzel\',serif;vertical-align:middle;margin:0 6px;">VS</div>');"""
text = text.replace(old_preview_calc, new_preview_calc)

# 11. Also hide promptEl explicitly when opening any modal
old_open_arena = "arenaModal.classList.add('active');"
new_open_arena = "arenaModal.classList.add('active'); if (promptEl) promptEl.style.display = 'none';"
text = text.replace(old_open_arena, new_open_arena)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('All chair characters seated & 1v1 VS layout applied successfully!')
