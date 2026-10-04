import json
import os
import re

print("Building The Mutual Fun (1987) · Comprehensive Corporate Odyssey V3...")

with open('assets_encoded.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

print(f"Loaded {len(assets)} assets from assets_encoded.json.")

# Read the template from build_custom_chair_arena.py
with open('build_custom_chair_arena.py', 'r', encoding='utf-8') as f:
    orig = f.read()

# Let's extract the html_template from build_custom_chair_arena.py
template_start = orig.find("html_template = r'''") + len("html_template = r'''")
template_end = orig.rfind("'''")
html_text = orig[template_start:template_end]

# -------------------------------------------------------------
# 1. ADD CSS FOR RETRO POKÉMON BOTTOM GUIDE & ACTIVE QUEST PANEL
# -------------------------------------------------------------
extra_css = """
    /* ==========================================================================
       RETRO POKÉMON-STYLE BOTTOM GUIDE & ACTIVE QUEST TRACKER
       ========================================================================== */
    .retro-guide-box {
      position: fixed;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%) translateY(0);
      width: min(900px, 96vw);
      background: #0d0a07;
      border: 4px solid #b9902f;
      border-radius: 4px;
      box-shadow: 0 12px 36px rgba(0,0,0,0.95), inset 0 0 0 2px #fdf3d0;
      padding: 14px 22px 16px 22px;
      z-index: 110;
      font-family: 'IBM Plex Mono', monospace;
      pointer-events: auto;
      display: none;
      opacity: 0;
      transition: opacity 0.25s ease, transform 0.25s ease;
    }
    .retro-guide-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 5px;
    }
    .retro-guide-badge {
      background: #b9902f;
      color: #0d0a07;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 8px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      border-radius: 2px;
    }
    .retro-guide-sub {
      color: #b9902f;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .retro-guide-content {
      color: #f5ebd5;
      font-size: 14px;
      line-height: 1.55;
      font-weight: 400;
      padding-right: 28px;
      letter-spacing: 0.2px;
    }
    .retro-guide-cursor {
      position: absolute;
      right: 14px;
      bottom: 8px;
      color: #b9902f;
      font-size: 11px;
      font-family: 'IBM Plex Mono', monospace;
      letter-spacing: 0.5px;
      opacity: 0;
      animation: retroBlink 0.7s infinite alternate ease-in-out;
    }
    @keyframes retroBlink {
      0% { transform: translateY(0); opacity: 0.3; }
      100% { transform: translateY(3px); opacity: 1; }
    }

    /* ACTIVE QUEST PANEL (Top Right) */
    .active-quest-panel {
      position: fixed;
      top: 66px;
      right: 16px;
      width: 320px;
      background: rgba(253, 250, 242, 0.96);
      border: 3px solid #211b14;
      border-radius: 4px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.4), inset 0 0 0 1px #b9902f;
      padding: 10px 14px;
      font-family: 'IBM Plex Mono', monospace;
      z-index: 100;
      transition: border-color 0.3s;
    }
    .quest-flash {
      animation: questFlashBorder 0.6s 2 ease;
    }
    @keyframes questFlashBorder {
      50% { border-color: #b9902f; box-shadow: 0 0 15px rgba(185, 144, 47, 0.8); }
    }
    .quest-eyebrow {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
      font-weight: 700;
      color: #7a2e2e;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }
    .quest-status-pill {
      background: #7a2e2e;
      color: #fff;
      padding: 1px 6px;
      border-radius: 2px;
      font-size: 9px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .quest-title {
      font-family: 'Cinzel', serif;
      font-size: 14px;
      font-weight: 700;
      color: #211b14;
      margin-bottom: 4px;
    }
    .quest-objective {
      font-size: 11px;
      color: #4f4335;
      line-height: 1.4;
    }
    .interact-prompt {
      position: fixed !important;
      bottom: 108px !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      background: #18120b !important;
      color: #fff9ea !important;
      padding: 8px 18px !important;
      font-family: 'IBM Plex Mono', monospace !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      border: 2px solid #b9902f !important;
      border-radius: 4px !important;
      z-index: 105 !important;
      box-shadow: 0 8px 24px rgba(0,0,0,0.75), inset 0 0 8px rgba(185,144,47,0.3) !important;
      letter-spacing: 0.5px !important;
      pointer-events: none !important;
    }
"""

html_text = html_text.replace("</style>", extra_css + "\n  </style>")

# -------------------------------------------------------------
# 2. ADD HTML ELEMENTS FOR QUEST PANEL & RETRO BOTTOM GUIDE
# -------------------------------------------------------------
extra_html = """
  <!-- Active Quest Tracker (Top Right) -->
  <div class="active-quest-panel" id="activeQuestPanel">
    <div class="quest-eyebrow">
      <span>DIRECTIVE ON RECORD</span>
      <span class="quest-status-pill" id="questStatusPill">ACTIVE</span>
    </div>
    <div class="quest-title" id="questTitle">Floor 0: Seek Admission</div>
    <div class="quest-objective" id="questObjective">Climb the granite stairs and enter the ground lobby to speak with the Security Gatekeeper.</div>
  </div>

  <!-- Retro Blocking Guide Box -->
  <div class="retro-guide-box" id="retroGuideBox" style="display:none;opacity:0;">
    <div class="retro-guide-header">
      <span class="retro-guide-badge" id="retroGuideTag">GUIDE</span>
      <span class="retro-guide-sub" id="retroGuideSub">THE MUTUAL FUN · 1987</span>
    </div>
    <div class="retro-guide-content" id="retroGuideText"></div>
    <div class="retro-guide-cursor" id="retroGuideCursor"></div>
  </div>
"""

html_text = html_text.replace("<!-- Floating Proximity Prompt -->", extra_html + "\n  <!-- Floating Proximity Prompt -->")

# -------------------------------------------------------------
# 3. ADD COLLISION SYSTEM & QUEST SYSTEM JAVASCRIPT
# -------------------------------------------------------------
extra_js_state = """
    // ==========================================================================
    // SOLID COLLISION DETECTION SYSTEM (Objects & Tables Not Passable)
    // ==========================================================================
    const colliders = [];

    function addBoxCollider(cx, cz, width, depth) {
      const hw = width / 2;
      const hd = depth / 2;
      colliders.push({ minX: cx - hw, maxX: cx + hw, minZ: cz - hd, maxZ: cz + hd });
    }

    function checkCollision(px, pz, radius) {
      for (let i = 0; i < colliders.length; i++) {
        const c = colliders[i];
        const closestX = Math.max(c.minX, Math.min(px, c.maxX));
        const closestZ = Math.max(c.minZ, Math.min(pz, c.maxZ));
        const dx = px - closestX;
        const dz = pz - closestZ;
        if ((dx * dx + dz * dz) < (radius * radius)) {
          return true;
        }
      }
      return false;
    }

    // ==========================================================================
    // FLOOR QUESTS & DIRECTIVES (Floors 0 to 9)
    // ==========================================================================
    const FLOOR_QUESTS = {
      0: {
        id: "q_floor0",
        title: "Floor 0: Seek Admission",
        holder: "Security Gatekeeper",
        roleTitle: "Admission Officer",
        chairName: "No Chair Secured",
        chairTier: 1,
        desc: "Climb the granite stairs and enter the ground lobby. Speak with the Security Gatekeeper to pledge your fund covenant and receive your TMF pass.",
        objective: "Climb stairs into lobby and speak with the Security Gatekeeper at the admissions desk",
        targetScore: 15,
        actionLabel: "Receive Covenant & Pass",
        isChairFloor: false
      },
      1: {
        id: "q_floor1",
        title: "Floor 1: Sort Mailroom Sacks",
        holder: "Chief Mail Clerk",
        roleTitle: "Head of Couriers",
        chairName: "The Intern's Folding Chair",
        chairTier: 1,
        desc: "The mailroom is overwhelmed with morning shareholder parcels. Report to the Chief Mail Clerk to sort the 5 corporate courier sacks, then contest the Intern's Folding Chair.",
        objective: "Report to the Chief Mail Clerk at the sorting table",
        targetScore: 30,
        actionLabel: "Sort Corporate Mail Sacks",
        isChairFloor: true
      },
      2: {
        id: "q_floor2",
        title: "Floor 2: Audit Syndicate Ledger",
        holder: "Senior Ledger Archivist",
        roleTitle: "Keeper of Ledgers",
        chairName: "The Oak Swivel Chair",
        chairTier: 2,
        desc: "Every transaction since 1987 must balance down to the single cent. Speak with the Senior Archivist to verify the General Syndicate Trust accounts, then contest the Oak Swivel Chair.",
        objective: "Speak with the Senior Archivist at the record archives",
        targetScore: 60,
        actionLabel: "Audit Syndicate Ledgers",
        isChairFloor: true
      },
      3: {
        id: "q_floor3",
        title: "Floor 3: Deng Credit Arbitrage",
        holder: "Head Trading Associate",
        roleTitle: "Floor Broker",
        chairName: "The Brass-Tack Armchair",
        chairTier: 3,
        desc: "The Deng credit spreads are widening between the five funds. Report to the Head Broker at the trading desk to execute the arbitrage settlement, then contest the Brass-Tack Armchair.",
        objective: "Report to the Head Broker at the trading bullpen",
        targetScore: 90,
        actionLabel: "Execute Deng Arbitrage",
        isChairFloor: true
      },
      4: {
        id: "q_floor4",
        title: "Floor 4: Synthesize Market Digest",
        holder: "Senior Market Analyst",
        roleTitle: "Head of Research",
        chairName: "The Director's Chair",
        chairTier: 4,
        desc: "The five funds require a synthesized intelligence memo before market open. Report to the Senior Analyst at the research lectern to finalize the memo, then contest the Director's Chair.",
        objective: "Report to the Senior Analyst at the research desk",
        targetScore: 120,
        actionLabel: "Synthesize Market Digest",
        isChairFloor: true
      },
      5: {
        id: "q_floor5",
        title: "Floor 5: Verify Pass Contract",
        holder: "Treasury Overseer",
        roleTitle: "Floor Manager",
        chairName: "The Executive Mahogany Chair",
        chairTier: 5,
        desc: "The on-chain TMF Pass contract (0xED37605FF0e513e46d50B26244DEb2024189751a) requires multi-sig confirmation. Report to the Treasury Overseer to seal the verification, then contest the Mahogany Chair.",
        objective: "Report to the Treasury Overseer at the management desk",
        targetScore: 150,
        actionLabel: "Verify On-Chain Pass Authority",
        isChairFloor: true
      },
      6: {
        id: "q_floor6",
        title: "Floor 6: Confront what3verman",
        holder: "what3verman",
        roleTitle: "Managing Director",
        chairName: "The Green Banker's Chair",
        chairTier: 6,
        desc: "Managing Director what3verman guards the corporate executive suite. Present your quarterly portfolio review to him, then challenge him in the arbitrage chamber for his iconic Green Banker's Chair.",
        objective: "Approach Managing Director what3verman at the executive mahogany desk",
        targetScore: 195,
        actionLabel: "Present Quarterly Review & Dispute",
        isChairFloor: true
      },
      7: {
        id: "q_floor7",
        title: "Floor 7: Syndicate Council Review",
        holder: "General Counsel",
        roleTitle: "Syndicate Trustee",
        chairName: "The Gilded High-Back Chair",
        chairTier: 7,
        desc: "The General Counsel presides over the sovereign charter. Meet with the Counsel at the syndicate covenant table to ratify the articles, then contest the Gilded High-Back Chair.",
        objective: "Meet with General Counsel at the covenant table",
        targetScore: 240,
        actionLabel: "Ratify Syndicate Charter",
        isChairFloor: true
      },
      8: {
        id: "q_floor8",
        title: "Floor 8: The Penthouse Dispute",
        holder: "The Chairman Kingpickle",
        roleTitle: "Chairman of the Board",
        chairName: "The Gilded Penthouse Throne",
        chairTier: 8,
        desc: "You have climbed from the outdoor pavement to the very summit of The Mutual Fun. Approach The Chairman Kingpickle on Seat 0, and prove your reflexes in the final arbitration dispute for the Grand Throne.",
        objective: "Approach The Chairman Kingpickle before the gilded throne",
        targetScore: 300,
        actionLabel: "The Final Arbitration Dispute",
        isChairFloor: true
      },
      9: {
        id: "q_floor9",
        title: "Floor 9: The Treasury Vault",
        holder: "Vault Sovereign",
        roleTitle: "Master Mint Custodian",
        chairName: "The Sovereign Pedestal",
        chairTier: 9,
        desc: "Inspect the On-Chain Treasury Vault (0x48dF...A118) and Pass Deployer (0x4609...Aa3e). Claim your permanent official Certificate of Employment as Master Sovereign of The Mutual Fun.",
        objective: "Inspect the Central On-Chain Vault Pedestal",
        targetScore: 300,
        actionLabel: "Inspect Treasury & Mint Pass",
        isChairFloor: false
      }
    };

    // =====================================================================
    // BLOCKING RETRO POKEMON GUIDE (typewriter + movement lock + dismiss)
    // =====================================================================
    let guideLocked = false;
    let _guideTypeTimer = null;
    let _guideFullText = '';
    let _guideCharIdx = 0;

    function setRetroGuide(tag, text, sub = "THE MUTUAL FUN · 1987") {
      const box = document.getElementById('retroGuideBox');
      const tagEl = document.getElementById('retroGuideTag');
      const subEl = document.getElementById('retroGuideSub');
      const textEl = document.getElementById('retroGuideText');
      const cursor = document.getElementById('retroGuideCursor');
      if (!box || !tagEl || !textEl) return;
      if (_guideTypeTimer) { clearTimeout(_guideTypeTimer); _guideTypeTimer = null; }
      tagEl.innerText = tag.toUpperCase();
      if (subEl) subEl.innerText = sub;
      textEl.innerText = '';
      if (cursor) { cursor.innerText = ''; cursor.style.opacity = '0'; }
      box.style.display = 'block';
      requestAnimationFrame(() => {
        box.style.opacity = '1';
        box.style.transform = 'translateX(-50%) translateY(0)';
      });
      guideLocked = true;
      _guideFullText = text;
      _guideCharIdx = 0;
      _typeGuideChar(textEl, cursor);
    }

    function _typeGuideChar(textEl, cursor) {
      if (_guideCharIdx < _guideFullText.length) {
        const ch = _guideFullText[_guideCharIdx];
        textEl.innerText += ch;
        _guideCharIdx++;
        const delay = (ch === '.' || ch === ',') ? 85 : 22;
        _guideTypeTimer = setTimeout(() => _typeGuideChar(textEl, cursor), delay);
      } else {
        _guideTypeTimer = null;
        if (cursor) { cursor.innerText = 'Press [E] or [Space] to continue'; cursor.style.opacity = '1'; }
      }
    }

    function advanceGuide() {
      if (!guideLocked) return;
      const textEl = document.getElementById('retroGuideText');
      const cursor = document.getElementById('retroGuideCursor');
      if (_guideCharIdx < _guideFullText.length) {
        if (_guideTypeTimer) { clearTimeout(_guideTypeTimer); _guideTypeTimer = null; }
        textEl.innerText = _guideFullText;
        _guideCharIdx = _guideFullText.length;
        if (cursor) { cursor.innerText = 'Press [E] or [Space] to continue'; cursor.style.opacity = '1'; }
      } else {
        _dismissGuide();
      }
    }

    function _dismissGuide() {
      const box = document.getElementById('retroGuideBox');
      if (box) {
        box.style.opacity = '0';
        box.style.transform = 'translateX(-50%) translateY(14px)';
        setTimeout(() => { box.style.display = 'none'; }, 280);
      }
      guideLocked = false;
    }

    function updateActiveQuestUI() {
      const q = FLOOR_QUESTS[currentFloor];
      const panel = document.getElementById('activeQuestPanel');
      const titleEl = document.getElementById('questTitle');
      const objEl = document.getElementById('questObjective');
      const statusPill = document.getElementById('questStatusPill');

      if (!q || !panel || !titleEl || !objEl || !statusPill) return;

      const isCompleted = (currentFloor === 0 ? flickerr.gateAdmitted : flickerr.chairsWon.includes(q.chairName));
      const isTaskDone = (currentFloor === 0 ? flickerr.gateAdmitted : (flickerr.tasksCompleted && flickerr.tasksCompleted.includes(currentFloor)));

      titleEl.innerText = q.title;
      if (currentFloor === 0) {
        if (flickerr.gateAdmitted) {
          objEl.innerHTML = `<span style="color:#2f6b3d;font-weight:700;">✓ ADMITTED:</span> Sworn to ${flickerr.department}. Use Elevator Concourse at north wall to ascend to Floor 1.`;
          statusPill.innerText = "ADMITTED";
          statusPill.style.background = "#2f6b3d";
        } else if (floor0Area === 'outside') {
          objEl.innerText = "Climb the granite stairs and step through the grand portico to enter the admissions lobby";
          statusPill.innerText = "ACTIVE";
          statusPill.style.background = "#7a2e2e";
        } else {
          objEl.innerText = "Speak with the Security Gatekeeper at the admissions desk to pledge your department covenant";
          statusPill.innerText = "ACTIVE";
          statusPill.style.background = "#7a2e2e";
        }
      } else if (isCompleted) {
        objEl.innerHTML = `<span style="color:#2f6b3d;font-weight:700;">✓ MASTERED:</span> ${q.chairName} secured. Use Elevator Concourse to ascend to Floor ${currentFloor + 1}.`;
        statusPill.innerText = "COMPLETED";
        statusPill.style.background = "#2f6b3d";
      } else if (isTaskDone) {
        objEl.innerHTML = `<span style="color:#b9902f;font-weight:700;">★ DISPUTE AUTHORIZED:</span> Challenge ${q.holder} in the Chair Arbitrage Chamber to win ${q.chairName}.`;
        statusPill.innerText = "DISPUTE READY";
        statusPill.style.background = "#b9902f";
      } else {
        objEl.innerText = q.objective;
        statusPill.innerText = "ACTIVE";
        statusPill.style.background = "#7a2e2e";
      }

      panel.classList.remove('quest-flash');
      void panel.offsetWidth;
      panel.classList.add('quest-flash');
    }
"""

html_text = html_text.replace("const ROLES = [", extra_js_state + "\n    const ROLES = [")

# Add tasksCompleted to flickerr initial state
html_text = html_text.replace('chairsWon: [],', 'chairsWon: [],\n      tasksCompleted: [],')

# Update updateHUD to also updateActiveQuestUI
html_text = html_text.replace("document.getElementById('hudScore').innerText = `${flickerr.reviewScore} Pts | ${flickerr.dengCredits} Deng`;",
"""document.getElementById('hudScore').innerText = `${flickerr.reviewScore} Pts | ${flickerr.dengCredits} Deng`;
      updateActiveQuestUI();""")

# -------------------------------------------------------------
# 4. WOOD TEXTURE PLY MATERIAL HELPER
# -------------------------------------------------------------
wood_ply_code = """
    function createWoodFloorMaterial(repeatX = 6, repeatZ = 5) {
      const woodTex = loadTextureB64(ASSETS.wood_floor);
      if (woodTex) {
        woodTex.wrapS = THREE.RepeatWrapping;
        woodTex.wrapT = THREE.RepeatWrapping;
        woodTex.repeat.set(repeatX, repeatZ);
        return new THREE.MeshStandardMaterial({
          map: woodTex,
          roughness: 0.45,
          metalness: 0.05
        });
      }
      return new THREE.MeshStandardMaterial({ color: 0x5a371e, roughness: 0.5 });
    }
"""

html_text = html_text.replace("function loadTextureB64(b64) {", wood_ply_code + "\n    function loadTextureB64(b64) {")

# -------------------------------------------------------------
# 5. OVERHAUL FLOOR 0: ROAD + STAIRS + INSIDE LOBBY WITH WOOD FLOOR
# -------------------------------------------------------------
floor0_code = """
    // ==========================================================================
    // FLOOR 0: SEPARATE OUTSIDE STREET & INSIDE GROUND ADMISSIONS LOBBY
    // ==========================================================================
    let floor0Area = 'outside'; // 'outside' or 'inside'

    function buildFloorEnvironment() {
      while(roomGroup.children.length > 0) {
        roomGroup.remove(roomGroup.children[0]);
      }
      interactiveObjects = [];
      colliders.length = 0;

      if (currentFloor === 0) {
        if (floor0Area === 'outside') {
          buildFloor0OutsideStreet();
        } else {
          buildFloor0InsideLobby();
        }
      } else {
        buildInteriorOfficeFloor();
      }
    }

    function enterGroundLobby() {
      if (floor0Area === 'inside') return;
      playDoorLatchSound();
      floor0Area = 'inside';
      buildFloorEnvironment();
      playerGroup.position.set(0, 0.0, 5.0);
      playerGroup.rotation.y = Math.PI; // Face North into lobby
      camera.position.set(0, 4.4, 6.8);
      camera.lookAt(0, 1.2, 3.5);
      showMemoToast("ENTERING HEADQUARTERS", "Entering Ground Admissions Lobby. The grand entrance gate closes behind you.");
      setRetroGuide("ADMISSIONS LOBBY", "The grand gate closed behind you. Speak with the Security Gatekeeper to receive your department covenant and pass.");
      updateActiveQuestUI();
    }

    function exitGroundLobby() {
      if (floor0Area === 'outside') return;
      playDoorLatchSound();
      floor0Area = 'outside';
      buildFloorEnvironment();
      playerGroup.position.set(0, 0.85, 2.2);
      playerGroup.rotation.y = 0; // Face South down stairs
      camera.position.set(0, 5.2, 8.5);
      camera.lookAt(0, 1.2, 2.2);
      showMemoToast("EXITING TO STREET", "Returning outside to the entrance stairs.");
      setRetroGuide("OUTSIDE STAIRS", "You stand on the entrance stairs. Climb up and step into the gate to enter the lobby.");
      updateActiveQuestUI();
    }

    function playDoorLatchSound() {
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(140, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(45, ctx.currentTime + 0.18);
        gain.gain.setValueAtTime(0.25, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.20);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.22);
      } catch(e) {}
    }

    // --------------------------------------------------------------------------
    // AREA 1: OUTSIDE STREET, SIDEWALK & 4-TIER GRANITE STAIRS
    // --------------------------------------------------------------------------
    function buildFloor0OutsideStreet() {
      colliders.length = 0;

      scene.background = new THREE.Color(0x8ab4f8);
      scene.fog = new THREE.FogExp2(0x8ab4f8, 0.007);

      const morningSun = new THREE.DirectionalLight(0xfffaed, 2.2);
      morningSun.position.set(16, 24, 18);
      morningSun.castShadow = true;
      morningSun.shadow.mapSize.width = 2048;
      morningSun.shadow.mapSize.height = 2048;
      roomGroup.add(morningSun);

      const skyAmb = new THREE.AmbientLight(0xcde0f7, 1.3);
      roomGroup.add(skyAmb);

      // --- OUTSIDE ROAD (y = 0, z = 6.5 to 15.0) ---
      const roadMat = new THREE.MeshLambertMaterial({ color: 0x2e3138 });
      const road = new THREE.Mesh(new THREE.PlaneGeometry(40, 14), roadMat);
      road.rotation.x = -Math.PI / 2;
      road.position.set(0, 0, 11);
      road.receiveShadow = true;
      roomGroup.add(road);

      // Center dashed road markings
      const stripeMat = new THREE.MeshBasicMaterial({ color: 0xe8e4d8 });
      for (let sx = -16; sx <= 16; sx += 4.5) {
        const stripe = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 0.2), stripeMat);
        stripe.rotation.x = -Math.PI / 2;
        stripe.position.set(sx, 0.002, 11);
        roomGroup.add(stripe);
      }

      // Curb & Sidewalk (z = 4.8 to 6.2, y = 0.12)
      const curbMat = new THREE.MeshLambertMaterial({ color: 0x7a746c });
      const curb = new THREE.Mesh(new THREE.BoxGeometry(40, 0.24, 2.6), curbMat);
      curb.position.set(0, 0.12, 5.5);
      curb.receiveShadow = true;
      roomGroup.add(curb);

      // --- 4-TIER GRANITE STAIRCASE LEADING TO GRAND ENTRANCE (z = 5.0 to 1.8) ---
      const stairMat = new THREE.MeshLambertMaterial({ color: 0x9a9288 });
      const stairWidth = 9.0;
      const steps = [
        { z: 4.8, y: 0.20, h: 0.20, d: 0.8 },
        { z: 4.0, y: 0.40, h: 0.40, d: 0.8 },
        { z: 3.2, y: 0.60, h: 0.60, d: 0.8 },
        { z: 2.4, y: 0.80, h: 0.80, d: 0.8 },
      ];
      steps.forEach(st => {
        const step = new THREE.Mesh(new THREE.BoxGeometry(stairWidth, st.h, st.d), stairMat);
        step.position.set(0, st.y - st.h / 2, st.z);
        step.receiveShadow = true;
        step.castShadow = true;
        roomGroup.add(step);
      });

      // Top Landing Platform (z = 1.6, y = 0.4, h = 0.8, d = 1.4)
      const landing = new THREE.Mesh(new THREE.BoxGeometry(stairWidth, 0.8, 1.4), stairMat);
      landing.position.set(0, 0.4, 1.5);
      landing.receiveShadow = true;
      roomGroup.add(landing);

      // Stair Balustrades & Bronze Handrails (Left & Right)
      const balMat = new THREE.MeshLambertMaterial({ color: 0xb5ab9d });
      const railMat = new THREE.MeshStandardMaterial({ color: 0xb9902f, metalness: 0.8, roughness: 0.3 });
      [-stairWidth/2 - 0.25, stairWidth/2 + 0.25].forEach(bx => {
        const balustrade = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.2, 4.4), balMat);
        balustrade.position.set(bx, 0.7, 3.4);
        balustrade.castShadow = true;
        roomGroup.add(balustrade);

        const handrail = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.10, 4.4), railMat);
        handrail.position.set(bx, 1.35, 3.4);
        roomGroup.add(handrail);

        addBoxCollider(bx, 3.4, 0.6, 4.6);
      });

      // --- GRAND EXTERIOR FACADE & ENTRANCE PORTICO (z = 0.8) ---
      const wallMat = new THREE.MeshLambertMaterial({ color: 0x7a3e2e }); // Corporate Brick
      const facadeL = new THREE.Mesh(new THREE.BoxGeometry(15, 18, 1.2), wallMat);
      facadeL.position.set(-11.5, 9, 0.8);
      facadeL.receiveShadow = true;
      roomGroup.add(facadeL);
      addBoxCollider(-11.5, 0.8, 15, 1.4);

      const facadeR = new THREE.Mesh(new THREE.BoxGeometry(15, 18, 1.2), wallMat);
      facadeR.position.set(11.5, 9, 0.8);
      facadeR.receiveShadow = true;
      roomGroup.add(facadeR);
      addBoxCollider(11.5, 0.8, 15, 1.4);

      // Grand Classical Archway
      const archMat = new THREE.MeshLambertMaterial({ color: 0xc49e4d });
      const archTop = new THREE.Mesh(new THREE.BoxGeometry(8.5, 2.8, 1.4), archMat);
      archTop.position.set(0, 5.8, 0.8);
      archTop.castShadow = true;
      roomGroup.add(archTop);

      // Classical Entrance Columns
      [-3.8, 3.8].forEach(colX => {
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.42, 6.2, 16), archMat);
        col.position.set(colX, 3.1, 0.8);
        col.castShadow = true;
        roomGroup.add(col);
        addBoxCollider(colX, 0.8, 1.0, 1.0);
      });

      // --- GRAND ENTRANCE DOUBLE DOORS (IN THE ARCHWAY AT z = 0.8) ---
      const doorFrameMat = new THREE.MeshStandardMaterial({ color: 0x5a371e, roughness: 0.6 });
      const doorLeafMat = new THREE.MeshStandardMaterial({ color: 0x3d2012, roughness: 0.5 });
      const brassTrimMat = new THREE.MeshStandardMaterial({ color: 0xb9902f, metalness: 0.85, roughness: 0.25 });

      // Door Frame
      const frame = new THREE.Mesh(new THREE.BoxGeometry(5.2, 4.6, 0.2), doorFrameMat);
      frame.position.set(0, 3.0, 0.8);
      roomGroup.add(frame);

      // Left Door
      const doorL = new THREE.Mesh(new THREE.BoxGeometry(2.1, 4.0, 0.15), doorLeafMat);
      doorL.position.set(-1.15, 2.8, 0.85);
      doorL.castShadow = true;
      roomGroup.add(doorL);

      // Right Door
      const doorR = new THREE.Mesh(new THREE.BoxGeometry(2.1, 4.0, 0.15), doorLeafMat);
      doorR.position.set(1.15, 2.8, 0.85);
      doorR.castShadow = true;
      roomGroup.add(doorR);

      // Brass Handles & Kickplates
      [-0.18, 0.18].forEach(hx => {
        const handle = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.5, 0.12), brassTrimMat);
        handle.position.set(hx, 2.4, 0.95);
        roomGroup.add(handle);
      });
      const kickplate = new THREE.Mesh(new THREE.BoxGeometry(4.3, 0.35, 0.05), brassTrimMat);
      kickplate.position.set(0, 1.05, 0.94);
      roomGroup.add(kickplate);

      // Golden Header Plaque
      const plaque = new THREE.Mesh(new THREE.BoxGeometry(6.4, 0.6, 0.12), brassTrimMat);
      plaque.position.set(0, 5.0, 0.92);
      roomGroup.add(plaque);

      // Interactive Portico Portal Trigger
      interactiveObjects.push({
        id: "ground_gate_enter",
        label: "Grand Portico: Step Inside to Ground Admissions Lobby [E]",
        pos: new THREE.Vector3(0, 0.8, 1.8),
        radius: 2.2,
        action: enterGroundLobby
      });

      // Player Position outside
      if (playerGroup.position.z < 2.0 || playerGroup.position.z > 14.0) {
        playerGroup.position.set(0, 0.25, 10.0);
        playerGroup.rotation.y = Math.PI; // Face North towards stairs & building
      }

      setRetroGuide("OUTSIDE GATE", "You stand on the pavement before The Mutual Fun Headquarters. Climb the granite stairs to enter the ground admissions lobby.");
      updateActiveQuestUI();
    }

    // --------------------------------------------------------------------------
    // AREA 2: INSIDE GROUND ADMISSIONS LOBBY (ROAD CUT OUT, ZERO WALL BLOCKING)
    // --------------------------------------------------------------------------
    function buildFloor0InsideLobby() {
      colliders.length = 0;

      // ROAD VIEW CUT OUT: Warm 1987 interior corporate atmosphere
      scene.background = new THREE.Color(0x16100b);
      scene.fog = new THREE.FogExp2(0x16100b, 0.016);

      const ambLight = new THREE.AmbientLight(0xd4af37, 0.75);
      roomGroup.add(ambLight);

      // Grand Chandelier
      const chandelier = new THREE.PointLight(0xffe2a0, 2.4, 25);
      chandelier.position.set(0, 5.2, -2.5);
      chandelier.castShadow = true;
      roomGroup.add(chandelier);

      // Warm side wall sconces
      const sconce1 = new THREE.PointLight(0xffd580, 1.2, 14);
      sconce1.position.set(-8, 3.8, 1);
      roomGroup.add(sconce1);
      const sconce2 = new THREE.PointLight(0xffd580, 1.2, 14);
      sconce2.position.set(8, 3.8, 1);
      roomGroup.add(sconce2);

      // --- LAVISH AUTHENTIC WOOD TEXTURE PLY FLOOR (24 wide x 20 deep) ---
      const woodPlyMat = createWoodFloorMaterial(6, 6);
      const lobbyFloor = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), woodPlyMat);
      lobbyFloor.rotation.x = -Math.PI / 2;
      lobbyFloor.position.set(0, 0.001, -2.0); // Runs from z = -12.0 to z = 8.0
      lobbyFloor.receiveShadow = true;
      roomGroup.add(lobbyFloor);

      // High Ceilings (1987 corporate headquarters)
      const ceilMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), new THREE.MeshLambertMaterial({ color: 0xede0cb }));
      ceilMesh.rotation.x = Math.PI / 2;
      ceilMesh.position.set(0, 5.8, -2.0);
      roomGroup.add(ceilMesh);

      // --- ART DEPARTMENT INTERIOR WALLS ---
      const wallPaperMat = new THREE.MeshLambertMaterial({ color: 0xc8ad72 });
      const wainscotMat = new THREE.MeshLambertMaterial({ color: 0xdcc48d });
      const trimMat = new THREE.MeshLambertMaterial({ color: 0xae9259 });

      // North Wall (Back) at z = -12.0
      buildArtWallSegment(0, -12, 24, false, wallPaperMat, wainscotMat, trimMat);
      addBoxCollider(0, -12.2, 24, 0.6);

      // West Wall at x = -11.5
      buildArtWallSegment(-11.5, -2, 20, true, wallPaperMat, wainscotMat, trimMat, true);
      addBoxCollider(-11.8, -2, 0.6, 20);

      // East Wall at x = 11.5
      buildArtWallSegment(11.5, -2, 20, true, wallPaperMat, wainscotMat, trimMat, true);
      addBoxCollider(11.8, -2, 0.6, 20);

      // --- SOUTH WALL AT z = 7.5 WITH CLOSED GRAND ENTRANCE GATES ---
      // Left South Wall Section
      buildArtWallSegment(-7.5, 7.5, 9.0, false, wallPaperMat, wainscotMat, trimMat);
      // Right South Wall Section
      buildArtWallSegment(7.5, 7.5, 9.0, false, wallPaperMat, wainscotMat, trimMat);
      // Upper Arch Header above Closed Gate
      const southHeader = new THREE.Mesh(new THREE.BoxGeometry(6.2, 1.8, 0.6), trimMat);
      southHeader.position.set(0, 4.9, 7.5);
      roomGroup.add(southHeader);

      // GRAND CLOSED SOUTH GATE / SOLID MAHOGANY DOUBLE DOORS FIRMLY SHUT BEHIND MC
      const doorMat = new THREE.MeshStandardMaterial({ color: 0x361c10, roughness: 0.5 });
      const bronzeMat = new THREE.MeshStandardMaterial({ color: 0xb9902f, metalness: 0.85, roughness: 0.25 });

      const closedDoorL = new THREE.Mesh(new THREE.BoxGeometry(1.9, 4.0, 0.25), doorMat);
      closedDoorL.position.set(-1.0, 2.0, 7.3);
      closedDoorL.castShadow = true;
      roomGroup.add(closedDoorL);

      const closedDoorR = new THREE.Mesh(new THREE.BoxGeometry(1.9, 4.0, 0.25), doorMat);
      closedDoorR.position.set(1.0, 2.0, 7.3);
      closedDoorR.castShadow = true;
      roomGroup.add(closedDoorR);

      // Bronze Security Crossbar & Latch across closed doors
      const bar = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.16, 0.12), bronzeMat);
      bar.position.set(0, 2.2, 7.15);
      roomGroup.add(bar);

      // Brass Transom Plaque above Closed Gate
      const gatePlaque = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.45, 0.1), bronzeMat);
      gatePlaque.position.set(0, 4.1, 7.3);
      roomGroup.add(gatePlaque);

      // Solid South Wall Collider (mc cannot pass through closed gate)
      addBoxCollider(0, 7.6, 24, 0.6);

      // Interactive Exit Trigger at Closed South Gate
      interactiveObjects.push({
        id: "ground_gate_exit",
        label: "Grand Entrance Portico: Exit Outside to Street & Stairs [E]",
        pos: new THREE.Vector3(0, 0.0, 6.2),
        radius: 2.2,
        action: exitGroundLobby
      });

      // --- RED RUNNER CARPET RUNNING DOWN CENTER (z = 6.8 to z = -10.5) ---
      const carpetMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });
      const carpet = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 17.5), carpetMat);
      carpet.rotation.x = -Math.PI / 2;
      carpet.position.set(0, 0.003, -2.0);
      carpet.receiveShadow = true;
      roomGroup.add(carpet);

      // --- SEATED ROLE HOLDER: SECURITY GATEKEEPER (Positioned at x = 4.2, z = -2.5) ---
      createSeatedRoleHolder(4.2, 0.0, -2.5, 0, {
        holder: "Security Gatekeeper",
        roleTitle: "Admission Officer · Ground Checkpoint",
        color: 0x223654,
        tieColor: 0x7a2e2e,
        hairColor: 0x332218,
        deskColor: 0x3a2012,
        action: openGatekeeperModal
      });

      // Additional Admissions Desk Accessories: Banker's Lamp
      const lampStand = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.14, 0.5), bronzeMat);
      lampStand.position.set(3.0, 1.45, -1.25);
      roomGroup.add(lampStand);
      const lampShade = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 0.14, 12), new THREE.MeshLambertMaterial({ color: 0x245436 }));
      lampShade.position.set(3.0, 1.70, -1.25);
      roomGroup.add(lampShade);
      const lampGlow = new THREE.PointLight(0xaaffaa, 1.2, 6);
      lampGlow.position.set(3.0, 1.65, -1.25);
      roomGroup.add(lampGlow);

      // --- ELEVATOR BANK AT NORTH REAR WALL (z = -11.5) ---
      const leftDoor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.6, 0.2), bronzeMat);
      leftDoor.position.set(-0.9, 1.8, -11.8);
      roomGroup.add(leftDoor);

      const rightDoor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.6, 0.2), bronzeMat);
      rightDoor.position.set(0.9, 1.8, -11.8);
      roomGroup.add(rightDoor);

      const dial = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.1, 16), bronzeMat);
      dial.rotation.x = Math.PI / 2;
      dial.position.set(0, 4.0, -11.75);
      roomGroup.add(dial);

      interactiveObjects.push({
        id: "elevator_panel_lobby",
        label: "Lobby Elevator Concourse: Ascend to Floor 1 (Intern Concourse)",
        pos: new THREE.Vector3(0, 0.0, -10.2),
        radius: 2.4,
        action: () => {
          if (!flickerr.gateAdmitted) {
            showMemoToast("ADMISSION REQUIRED", "Speak with the Security Gatekeeper to receive your department covenant and TMF pass.");
            setRetroGuide("GATEKEEPER", "Admission required. Speak with the Security Gatekeeper at the right desk before using the elevator.");
            tone(120, 0.3);
          } else {
            rideElevatorTo(1);
          }
        }
      });

      // Vintage Corporate Portraits / Plaque frames on East & West Walls
      [-11.4, 11.4].forEach(px => {
        const frameMesh = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.8, 2.4), bronzeMat);
        frameMesh.position.set(px, 3.0, -2.0);
        roomGroup.add(frameMesh);
      });

      setRetroGuide("ADMISSIONS LOBBY", "The grand gate closed behind you. Speak with the Security Gatekeeper to receive your department covenant and pass.");
      updateActiveQuestUI();
    }
"""

# Replace buildFloorEnvironment and buildExteriorStreet with outside/inside system
start_ext = html_text.find("function buildFloorEnvironment()")
end_ext = html_text.find("function buildInteriorOfficeFloor()")
html_text = html_text[:start_ext] + floor0_code.strip() + "\n\n    " + html_text[end_ext:]

# -------------------------------------------------------------
# 6. SEATED ROLE HOLDER CREATOR FUNCTION FOR THREE.JS
# -------------------------------------------------------------
role_holder_func = """
    // ==========================================================================
    // PROCEDURAL 3D SEATED ROLE HOLDER (Distinct NPC for Each Floor)
    // ==========================================================================
    function createSeatedRoleHolder(x, y, z, floorTier, roleData) {
      const holderGroup = new THREE.Group();
      holderGroup.position.set(x, y, z);
      roomGroup.add(holderGroup);

      // Chair for this floor
      const chair = createChair(0, 0, 0, floorTier, 0);
      holderGroup.add(chair);

      // Seated Character
      const suitColor = roleData.color || 0x223654;
      const suitMat = new THREE.MeshLambertMaterial({ color: suitColor });
      const shirtMat = new THREE.MeshLambertMaterial({ color: 0xf7f4ef });
      const tieMat = new THREE.MeshLambertMaterial({ color: roleData.tieColor || 0x7a2e2e });
      const skinMat = new THREE.MeshLambertMaterial({ color: 0xebb992 });
      const hairMat = new THREE.MeshLambertMaterial({ color: roleData.hairColor || 0x332218 });

      // Torso
      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.76, 0.38), suitMat);
      torso.position.set(0, 1.15, -0.08);
      torso.castShadow = true;
      holderGroup.add(torso);

      // Shirt & Tie
      const shirt = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.30, 0.02), shirtMat);
      shirt.position.set(0, 1.30, 0.115);
      holderGroup.add(shirt);

      const tie = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.34, 0.03), tieMat);
      tie.position.set(0, 1.25, 0.125);
      holderGroup.add(tie);

      // Head
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.40, 0.36), skinMat);
      head.position.set(0, 1.74, -0.06);
      head.castShadow = true;
      holderGroup.add(head);

      // Hair
      const hair = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.14, 0.38), hairMat);
      hair.position.set(0, 1.94, -0.06);
      holderGroup.add(hair);

      // Glasses or Boss Crown
      if (roleData.hasCrown) {
        const crownMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.2 });
        const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.22, 0.16, 8), crownMat);
        crown.position.set(0, 2.05, -0.06);
        holderGroup.add(crown);
      } else {
        const glassesMat = new THREE.MeshLambertMaterial({ color: 0x1f140e });
        const glasses = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.08, 0.04), glassesMat);
        glasses.position.set(0, 1.76, 0.125);
        holderGroup.add(glasses);
      }

      // Upper Legs (Horizontal forward on chair seat)
      const upperLegL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.52), suitMat);
      upperLegL.position.set(-0.16, 0.72, 0.18);
      holderGroup.add(upperLegL);

      const upperLegR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.52), suitMat);
      upperLegR.position.set(0.16, 0.72, 0.18);
      holderGroup.add(upperLegR);

      // Lower Legs (Vertical to floor)
      const lowerLegL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.45, 0.18), suitMat);
      lowerLegL.position.set(-0.16, 0.42, 0.38);
      holderGroup.add(lowerLegL);

      const lowerLegR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.45, 0.18), suitMat);
      lowerLegR.position.set(0.16, 0.42, 0.38);
      holderGroup.add(lowerLegR);

      // Shoes
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0x111116, roughness: 0.35 });
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

      // Official Desk in front of them
      createDesk(x, y, z + 1.25, 4.2, 1.4, roleData.deskColor || 0x3d2719);

      // Solid Collision Bounds so player CANNOT walk through desk or chair!
      addBoxCollider(x, z + 1.25, 4.5, 1.6);
      addBoxCollider(x, z, 1.4, 1.4);

      // Interactive Trigger
      interactiveObjects.push({
        id: `role_holder_f${floorTier}`,
        label: `${roleData.holder}: ${roleData.roleTitle}`,
        pos: new THREE.Vector3(x, y, z + 2.3),
        radius: 2.5,
        action: roleData.action || (() => {
          openRoleHolderQuestModal(floorTier, roleData);
        })
      });
    }

    function openRoleHolderQuestModal(floorTier, roleData) {
      const q = FLOOR_QUESTS[floorTier];
      if (!q) return;

      playClick();
      modalTitle.innerText = roleData.holder.toUpperCase();
      modalSubtitle.innerText = `${roleData.roleTitle.toUpperCase()} · FLOOR ${floorTier}`;

      const isCompleted = flickerr.chairsWon.includes(q.chairName);
      const isTaskDone = (flickerr.tasksCompleted && flickerr.tasksCompleted.includes(floorTier));

      if (isCompleted) {
        modalBody.innerHTML = `
          <blockquote style="border-left:4px solid var(--green);padding-left:12px;font-style:italic;margin-bottom:12px;color:var(--ink);font-size:13px;">
            "You have demonstrated undisputed mastery over this floor. Lawful title to ${q.chairName} rests on your record. Proceed to the elevator concourse to advance."
          </blockquote>
          <button class="desk-button" style="width:100%;background:var(--oxblood);" onclick="closeTaskModal(); triggerMusicalChairsArena(${floorTier});">
            Re-Contest Chair Arbitrage for Practice
          </button>
        `;
      } else if (isTaskDone) {
        modalBody.innerHTML = `
          <blockquote style="border-left:4px solid var(--lamp);padding-left:12px;font-style:italic;margin-bottom:12px;color:var(--ink);font-size:13px;">
            "Your duties on this floor are audited and verified. But ${q.chairName} is not surrendered on review points alone. Step into the arbitrage chamber and seize it when the needle scratches."
          </blockquote>
          <button class="desk-button" style="width:100%;background:var(--oxblood);font-weight:700;" onclick="closeTaskModal(); triggerMusicalChairsArena(${floorTier});">
            Contest ${q.chairName} in Chair Arbitrage Chamber [SPACE]
          </button>
        `;
      } else {
        modalBody.innerHTML = `
          <blockquote style="border-left:4px solid var(--oxblood);padding-left:12px;font-style:italic;margin-bottom:12px;color:var(--ink);font-size:13px;">
            "${q.desc}"
          </blockquote>
          <button class="desk-button" style="width:100%;background:var(--lamp);color:#110b06;font-weight:700;" onclick="completeFloorTask(${floorTier});">
            ${q.actionLabel}
          </button>
        `;
      }

      modalEl.classList.add('active');
    }

    function completeFloorTask(floorTier) {
      playStampThump();
      if (!flickerr.tasksCompleted) flickerr.tasksCompleted = [];
      if (!flickerr.tasksCompleted.includes(floorTier)) {
        flickerr.tasksCompleted.push(floorTier);
      }
      flickerr.reviewScore += 18;
      flickerr.dengCredits += 25.0;
      updateHUD();

      const q = FLOOR_QUESTS[floorTier];
      showMemoToast("TASK VERIFIED", `${q.actionLabel} completed. You are authorized to dispute ${q.chairName}.`);
      setRetroGuide("TASK COMPLETED", `Duties verified! Challenge ${q.holder} to dispute ${q.chairName} in the Chair Arbitrage Chamber.`);
      
      openRoleHolderQuestModal(floorTier, {
        holder: q.holder,
        roleTitle: q.roleTitle
      });
    }
"""

html_text = html_text.replace("function createDesk(x, y, z, w, d, color) {", role_holder_func + "\n    function createDesk(x, y, z, w, d, color) {")

# -------------------------------------------------------------
# 7. UPDATE INTERIOR OFFICE FLOOR TO USE WOOD PLY & SOLID COLLIDERS
# -------------------------------------------------------------
int_floor_start = html_text.find("function buildInteriorOfficeFloor()")
int_floor_end = html_text.find("function buildArchitecturalWalls()")

new_int_floor = """function buildInteriorOfficeFloor() {
      colliders.length = 0; // Reset collision bounds for office floor

      scene.background = new THREE.Color(0x140f0b);
      scene.fog = new THREE.FogExp2(0x140f0b, 0.018);

      const ambLight = new THREE.AmbientLight(0xd4af37, 0.65);
      roomGroup.add(ambLight);

      const ceilingLight = new THREE.PointLight(0xffe6b0, 1.8, 25);
      ceilingLight.position.set(0, 5.2, 0);
      ceilingLight.castShadow = true;
      roomGroup.add(ceilingLight);

      // AUTHENTIC WOOD TEXTURE PLY ON OFFICE FLOOR
      const woodFloorMat = createWoodFloorMaterial(6, 5);
      const floorMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), woodFloorMat);
      floorMesh.rotation.x = -Math.PI / 2;
      floorMesh.receiveShadow = true;
      roomGroup.add(floorMesh);

      const ceilMat = new THREE.MeshLambertMaterial({ color: 0xede0cb });
      const ceilMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), ceilMat);
      ceilMesh.rotation.x = Math.PI / 2;
      ceilMesh.position.y = 5.8;
      roomGroup.add(ceilMesh);

      buildArchitecturalWalls();
      buildElevatorConcourse();
      hangFloorPortraits();

      // Solid Perimeter Walls Colliders
      addBoxCollider(0, -10.2, 24, 0.6);
      addBoxCollider(-12.2, 0, 0.6, 20);
      addBoxCollider(12.2, 0, 0.6, 20);
      addBoxCollider(0, 10.2, 24, 0.6);

      // Build Floor-Specific Seated Role Holder & Furniture
      if (currentFloor === 1) buildFloor1Intern();
      else if (currentFloor === 2) buildFloor2Analyst();
      else if (currentFloor === 3) buildFloor3Associate();
      else if (currentFloor === 4) buildFloor4VP();
      else if (currentFloor === 5) buildFloor5Director();
      else if (currentFloor === 6) buildFloor6MD();
      else if (currentFloor === 7) buildFloor7Partner();
      else if (currentFloor === 8) buildFloor8Board();
      else if (currentFloor === 9) buildFloor9Penthouse();

      playerGroup.position.set(0, 0, 6);
      playerGroup.rotation.y = Math.PI;

      const q = FLOOR_QUESTS[currentFloor];
      if (q) {
        setRetroGuide(`FLOOR ${currentFloor}`, `${q.holder} is seated ahead. Approach them to receive the floor directive or contest the chair.`);
      }
      updateActiveQuestUI();
    }
"""

html_text = html_text[:int_floor_start] + new_int_floor.strip() + "\n\n    " + html_text[int_floor_end:]

# -------------------------------------------------------------
# 8. UPDATE EACH FLOOR TO HAVE THEIR SEATED ROLE HOLDER
# -------------------------------------------------------------
# Floor 1: Chief Mail Clerk
f1_old = """    function buildFloor1Intern() {
      createDesk(0, 0, 0, 6, 1.6, 0x3d2719);"""
f1_new = """    function buildFloor1Intern() {
      createSeatedRoleHolder(0, 0, -2.5, 1, {
        holder: "Chief Mail Clerk",
        roleTitle: "Head of Couriers · Floor 1",
        color: 0x4e8a5a,
        tieColor: 0x7a2e2e,
        hairColor: 0x221309
      });"""
html_text = html_text.replace(f1_old, f1_new)

# Floor 2: Senior Ledger Archivist
f2_old = """    function buildFloor2Analyst() {
      createDesk(0, 0, 0, 5, 1.8, 0x3d2719);"""
f2_new = """    function buildFloor2Analyst() {
      createSeatedRoleHolder(0, 0, -2.5, 2, {
        holder: "Senior Ledger Archivist",
        roleTitle: "Keeper of Ledgers · Floor 2",
        color: 0x49698c,
        tieColor: 0x211b14,
        hairColor: 0x443322
      });"""
html_text = html_text.replace(f2_old, f2_new)

# Floor 3: Head Broker
f3_old = """    function buildFloor3Associate() {
      createDesk(0, 0, 0, 5.5, 1.8, 0x3d2719);"""
f3_new = """    function buildFloor3Associate() {
      createSeatedRoleHolder(0, 0, -2.5, 3, {
        holder: "Head Trading Associate",
        roleTitle: "Floor Broker · Floor 3",
        color: 0xb9902f,
        tieColor: 0x7a2e2e,
        hairColor: 0x2e1d13
      });"""
html_text = html_text.replace(f3_old, f3_new)

# Floor 4: Senior Market Analyst
f4_old = """    function buildFloor4VP() {
      createDesk(0, 0, 0, 5.5, 1.8, 0x3d2719);"""
f4_new = """    function buildFloor4VP() {
      createSeatedRoleHolder(0, 0, -2.5, 4, {
        holder: "Senior Market Analyst",
        roleTitle: "Head of Research · Floor 4",
        color: 0x9c5248,
        tieColor: 0x49698c,
        hairColor: 0x1f140e
      });"""
html_text = html_text.replace(f4_old, f4_new)

# Floor 5: Treasury Overseer
f5_old = """    function buildFloor5Director() {
      createDesk(0, 0, 0, 5.5, 1.8, 0x3d2719);"""
f5_new = """    function buildFloor5Director() {
      createSeatedRoleHolder(0, 0, -2.5, 5, {
        holder: "Treasury Overseer",
        roleTitle: "Floor Manager · Floor 5",
        color: 0x6e5d8c,
        tieColor: 0xd4af37,
        hairColor: 0x332218
      });"""
html_text = html_text.replace(f5_old, f5_new)

# Floor 6: Managing Director what3verman (Lower Main Boss)
f6_old = """    function buildFloor6MD() {
      createDesk(0, 0, 0, 6, 2, 0x221309);"""
f6_new = """    function buildFloor6MD() {
      createSeatedRoleHolder(0, 0, -2.5, 6, {
        holder: "what3verman",
        roleTitle: "Managing Director · Floor 6",
        color: 0x1f4728,
        tieColor: 0xb9902f,
        hairColor: 0x221309,
        action: openMDTaskModal
      });"""
html_text = html_text.replace(f6_old, f6_new)

# Floor 7: General Counsel
f7_old = """    function buildFloor7Partner() {
      createDesk(0, 0, 0, 6, 2, 0x221309);"""
f7_new = """    function buildFloor7Partner() {
      createSeatedRoleHolder(0, 0, -2.5, 7, {
        holder: "General Counsel",
        roleTitle: "Syndicate Trustee · Floor 7",
        color: 0x7a2e2e,
        tieColor: 0x211b14,
        hairColor: 0x4a3424
      });"""
html_text = html_text.replace(f7_old, f7_new)

# Floor 8: The Chairman Kingpickle (Main Boss)
f8_old = """    function buildFloor8Board() {
      createDesk(0, 0, 0, 7, 2.2, 0x1c1008);"""
f8_new = """    function buildFloor8Board() {
      createSeatedRoleHolder(0, 0, -2.5, 8, {
        holder: "The Chairman Kingpickle",
        roleTitle: "Chairman of the Board · Seat 0",
        color: 0x110b06,
        tieColor: 0xd4af37,
        hairColor: 0x5a3d28,
        hasCrown: true,
        action: openKingpickleTaskModal
      });"""
html_text = html_text.replace(f8_old, f8_new)

# -------------------------------------------------------------
# 9. REMOVE CAMERA ROTATION & IMPLEMENT COLLISION MOVEMENT
# -------------------------------------------------------------
# In animate loop:
anim_old = """      if (keys['keyq']) cameraAngle += 0.03;
      if (keys['keye'] && !promptEl.style.display.includes('block')) cameraAngle -= 0.03;

      let moveX = 0;
      let moveZ = 0;
      if (keys['keyw'] || keys['arrowup']) moveZ -= 1;
      if (keys['keys'] || keys['arrowdown']) moveZ += 1;
      if (keys['keya'] || keys['arrowleft']) moveX -= 1;
      if (keys['keyd'] || keys['arrowright']) moveX += 1;

      const isMoving = (moveX !== 0 || moveZ !== 0);
      const isModalActive = modalEl.classList.contains('active') || elevModal.classList.contains('active') ||
                            arenaModal.classList.contains('active') || certModal.classList.contains('active');

      if (isMoving && !isModalActive) {
        const moveVec = new THREE.Vector3(moveX, 0, moveZ).normalize();
        moveVec.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraAngle);

        const speed = 0.12;
        playerGroup.position.x += moveVec.x * speed;
        playerGroup.position.z += moveVec.z * speed;

        const targetRot = Math.atan2(moveVec.x, moveVec.z);
        playerGroup.rotation.y = targetRot;

        walkClock += 0.2;
        leftLeg.rotation.x = Math.sin(walkClock) * 0.45;
        rightLeg.rotation.x = -Math.sin(walkClock) * 0.45;
        leftArm.rotation.x = -Math.sin(walkClock) * 0.45;
        rightArm.rotation.x = Math.sin(walkClock) * 0.35;
        torso.position.y = 1.0 + Math.abs(Math.sin(walkClock * 2)) * 0.04;

        if (Math.sin(walkClock) > 0.9) playStep();

        const boundX = (currentFloor === 0 ? 16 : 10.5);
        const boundZ = (currentFloor === 0 ? 13 : 8.5);
        playerGroup.position.x = Math.max(-boundX, Math.min(boundX, playerGroup.position.x));
        playerGroup.position.z = Math.max(-boundZ, Math.min(boundZ, playerGroup.position.z));
      } else {
        leftLeg.rotation.x *= 0.82;
        rightLeg.rotation.x *= 0.82;
        leftArm.rotation.x *= 0.82;
        rightArm.rotation.x *= 0.82;
        idleClock += 0.035;
        torso.position.y = 1.0 + Math.sin(idleClock) * 0.015;
      }

      const camDist = (currentFloor === 0 ? 8.0 : 6.5);
      const camHeight = (currentFloor === 0 ? 4.8 : 4.2);
      const targetCamX = playerGroup.position.x + Math.sin(cameraAngle) * camDist;
      const targetCamZ = playerGroup.position.z + Math.cos(cameraAngle) * camDist;

      camera.position.x += (targetCamX - camera.position.x) * 0.1;
      camera.position.y += (camHeight - camera.position.y) * 0.1;
      camera.position.z += (targetCamZ - camera.position.z) * 0.1;
      camera.lookAt(playerGroup.position.x, 1.2, playerGroup.position.z);"""

anim_new = """      // NO CAMERA ROTATION (Fixed classic high-angle follow perspective)
      let moveX = 0;
      let moveZ = 0;
      if (keys['keyw'] || keys['arrowup']) moveZ -= 1;
      if (keys['keys'] || keys['arrowdown']) moveZ += 1;
      if (keys['keya'] || keys['arrowleft']) moveX -= 1;
      if (keys['keyd'] || keys['arrowright']) moveX += 1;

      const isMoving = (moveX !== 0 || moveZ !== 0);
      const isModalActive = modalEl.classList.contains('active') || elevModal.classList.contains('active') ||
                            arenaModal.classList.contains('active') || certModal.classList.contains('active');

      if (isMoving && !isModalActive) {
        const moveVec = new THREE.Vector3(moveX, 0, moveZ).normalize();
        const speed = 0.12;
        const playerRadius = 0.38;

        const dx = moveVec.x * speed;
        const dz = moveVec.z * speed;

        if (currentFloor === 0 && floor0Area === 'outside') {
          // SOLID COLLISION DETECTION OUTSIDE
          const nextX = playerGroup.position.x + dx;
          const boundX = 14.0;
          if (Math.abs(nextX) <= boundX && !checkCollision(nextX, playerGroup.position.z, playerRadius)) {
            playerGroup.position.x = nextX;
          }

          const nextZ = playerGroup.position.z + dz;
          const minZ = 1.3;
          const maxZ = 13.5;
          if (nextZ >= minZ && nextZ <= maxZ && !checkCollision(playerGroup.position.x, nextZ, playerRadius)) {
            playerGroup.position.z = nextZ;
          }

          // Height adjustment for outside stairs
          if (playerGroup.position.z > 5.2) {
            playerGroup.position.y = 0.25; // Street / Curb
          } else if (playerGroup.position.z <= 5.2 && playerGroup.position.z >= 1.8) {
            const stT = (5.2 - playerGroup.position.z) / 3.4;
            playerGroup.position.y = 0.25 + stT * 0.80; // Climbing stairs
          } else {
            playerGroup.position.y = 1.05; // Portico landing
          }

          // Step through gate auto-trigger: MC enters inside when walking up to the gate
          if (playerGroup.position.z <= 1.45) {
            enterGroundLobby();
            return;
          }
        } else if (currentFloor === 0 && floor0Area === 'inside') {
          // INSIDE GROUND LOBBY: MC is on flat wood ply floor
          playerGroup.position.y = 0.0;
          const nextX = playerGroup.position.x + dx;
          const boundX = 10.5;
          if (Math.abs(nextX) <= boundX && !checkCollision(nextX, playerGroup.position.z, playerRadius)) {
            playerGroup.position.x = nextX;
          }

          const nextZ = playerGroup.position.z + dz;
          const minZ = -10.8;
          const maxZ = 6.4;
          if (nextZ >= minZ && nextZ <= maxZ && !checkCollision(playerGroup.position.x, nextZ, playerRadius)) {
            playerGroup.position.z = nextZ;
          }
        } else {
          // Interior office floors (1 to 9)
          playerGroup.position.y = 0.0;
          const nextX = playerGroup.position.x + dx;
          const boundX = 10.5;
          if (Math.abs(nextX) <= boundX && !checkCollision(nextX, playerGroup.position.z, playerRadius)) {
            playerGroup.position.x = nextX;
          }

          const nextZ = playerGroup.position.z + dz;
          const minZ = -8.5;
          const maxZ = 8.5;
          if (nextZ >= minZ && nextZ <= maxZ && !checkCollision(playerGroup.position.x, nextZ, playerRadius)) {
            playerGroup.position.z = nextZ;
          }
        }

        // Player rotates to face motion direction
        const targetRot = Math.atan2(moveVec.x, moveVec.z);
        playerGroup.rotation.y = targetRot;

        walkClock += 0.2;
        leftLeg.rotation.x = Math.sin(walkClock) * 0.45;
        rightLeg.rotation.x = -Math.sin(walkClock) * 0.45;
        leftArm.rotation.x = -Math.sin(walkClock) * 0.45;
        rightArm.rotation.x = Math.sin(walkClock) * 0.35;
        torso.position.y = 1.0 + Math.abs(Math.sin(walkClock * 2)) * 0.04;

        if (Math.sin(walkClock) > 0.9) playStep();
      } else {
        leftLeg.rotation.x *= 0.82;
        rightLeg.rotation.x *= 0.82;
        leftArm.rotation.x *= 0.82;
        rightArm.rotation.x *= 0.82;
        idleClock += 0.035;
        torso.position.y = 1.0 + Math.sin(idleClock) * 0.015;
      }

      // FIXED THIRD-PERSON FOLLOW CAMERA (NO 360 ROTATION)
      if (currentFloor === 0 && floor0Area === 'outside') {
        // Outside Camera POV
        const camDistZ = 8.0;
        const camHeight = 5.2;
        const targetCamX = playerGroup.position.x;
        const targetCamY = playerGroup.position.y + camHeight;
        const targetCamZ = playerGroup.position.z + camDistZ;

        camera.position.x += (targetCamX - camera.position.x) * 0.12;
        camera.position.y += (targetCamY - camera.position.y) * 0.12;
        camera.position.z += (targetCamZ - camera.position.z) * 0.12;
        camera.lookAt(playerGroup.position.x, playerGroup.position.y + 1.2, playerGroup.position.z);
      } else if (currentFloor === 0 && floor0Area === 'inside') {
        // INSIDE LOBBY POV: Camera is completely inside the room in front of south wall (z = 7.5)
        const camDistZ = 5.8;
        const camHeight = 4.4;
        const targetCamX = playerGroup.position.x * 0.65;
        const targetCamY = camHeight;
        const targetCamZ = Math.min(6.8, playerGroup.position.z + camDistZ);

        camera.position.x += (targetCamX - camera.position.x) * 0.14;
        camera.position.y += (targetCamY - camera.position.y) * 0.14;
        camera.position.z += (targetCamZ - camera.position.z) * 0.14;
        camera.lookAt(playerGroup.position.x, 1.2, playerGroup.position.z);
      } else {
        // Interior office floors
        const camDistZ = 6.8;
        const camHeight = 4.8;
        const targetCamX = playerGroup.position.x;
        const targetCamY = camHeight;
        const targetCamZ = playerGroup.position.z + camDistZ;

        camera.position.x += (targetCamX - camera.position.x) * 0.12;
        camera.position.y += (targetCamY - camera.position.y) * 0.12;
        camera.position.z += (targetCamZ - camera.position.z) * 0.12;
        camera.lookAt(playerGroup.position.x, 1.2, playerGroup.position.z);
      }"""

html_text = html_text.replace(anim_old, anim_new)

# Also update checkInteractions in proximity to update Retro Pokémon Guide Box
check_interact_old = """      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist < obj.radius) {
          obj.action();
          return;
        }
      }"""

check_interact_new = """      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist < obj.radius) {
          obj.action();
          return;
        }
      }"""
# In proximity check loop inside animate:
prox_old = """      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist < obj.radius) {
          nearby = obj;
          break;
        }
      }

      if (nearby && !isModalActive) {
        promptEl.style.display = 'block';
        promptEl.innerText = `[E] ${nearby.label}`;
      } else {
        promptEl.style.display = 'none';
      }"""

prox_new = """      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist < obj.radius) {
          nearby = obj;
          break;
        }
      }

      if (nearby && !isModalActive) {
        promptEl.style.display = 'block';
        promptEl.innerText = `[E] ${nearby.label}`;
      } else {
        promptEl.style.display = 'none';
      }"""

html_text = html_text.replace(prox_old, prox_new)

# -------------------------------------------------------------
# 10. COMPILE TO INDEX.HTML
# -------------------------------------------------------------
final_html = html_text.replace('__ASSETS_JSON__', json.dumps(assets))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Saved compiled index.html successfully!")

# Also save to artifact directory
art_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(art_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Saved compiled index.html to artifact directory: {art_path}")
