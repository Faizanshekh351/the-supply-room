import os
import re

print("Applying Floor 0 outside/inside transition and POV revamp to build_complete_game_v3.py...")

with open("build_complete_game_v3.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update updateActiveQuestUI inside extra_js_state
old_quest_ui = """      const isCompleted = (currentFloor === 0 ? flickerr.gateAdmitted : flickerr.chairsWon.includes(q.chairName));
      const isTaskDone = (currentFloor === 0 ? flickerr.gateAdmitted : (flickerr.tasksCompleted && flickerr.tasksCompleted.includes(currentFloor)));

      titleEl.innerText = q.title;
      if (isCompleted) {
        objEl.innerHTML = `<span style="color:#2f6b3d;font-weight:700;">[OK] MASTERED:</span> ${q.chairName} secured. Use Elevator Concourse to ascend to Floor ${currentFloor + 1}.`;
        statusPill.innerText = "COMPLETED";
        statusPill.style.background = "#2f6b3d";
      } else if (isTaskDone) {
        objEl.innerHTML = `<span style="color:#b9902f;font-weight:700;">[*] DISPUTE AUTHORIZED:</span> Challenge ${q.holder} in the Chair Arbitrage Chamber to win ${q.chairName}.`;
        statusPill.innerText = "DISPUTE READY";
        statusPill.style.background = "#b9902f";
      } else {
        objEl.innerText = q.objective;
        statusPill.innerText = "ACTIVE";
        statusPill.style.background = "#7a2e2e";
      }"""

new_quest_ui = """      const isCompleted = (currentFloor === 0 ? flickerr.gateAdmitted : flickerr.chairsWon.includes(q.chairName));
      const isTaskDone = (currentFloor === 0 ? flickerr.gateAdmitted : (flickerr.tasksCompleted && flickerr.tasksCompleted.includes(currentFloor)));

      titleEl.innerText = q.title;
      if (currentFloor === 0) {
        if (flickerr.gateAdmitted) {
          objEl.innerHTML = `<span style="color:#2f6b3d;font-weight:700;">[OK] ADMITTED:</span> Sworn to ${flickerr.department}. Use Elevator Concourse at north wall to ascend to Floor 1.`;
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
        objEl.innerHTML = `<span style="color:#2f6b3d;font-weight:700;">[OK] MASTERED:</span> ${q.chairName} secured. Use Elevator Concourse to ascend to Floor ${currentFloor + 1}.`;
        statusPill.innerText = "COMPLETED";
        statusPill.style.background = "#2f6b3d";
      } else if (isTaskDone) {
        objEl.innerHTML = `<span style="color:#b9902f;font-weight:700;">[*] DISPUTE AUTHORIZED:</span> Challenge ${q.holder} in the Chair Arbitrage Chamber to win ${q.chairName}.`;
        statusPill.innerText = "DISPUTE READY";
        statusPill.style.background = "#b9902f";
      } else {
        objEl.innerText = q.objective;
        statusPill.innerText = "ACTIVE";
        statusPill.style.background = "#7a2e2e";
      }"""

if old_quest_ui in code:
    code = code.replace(old_quest_ui, new_quest_ui)
    print("[OK] Updated updateActiveQuestUI")
else:
    print("! Could not find old_quest_ui")

# 2. Overhaul floor0_code and its replacement target
new_floor0_code = '''floor0_code = """
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
      camera.position.set(0, 4.4, 9.5);
      camera.lookAt(0, 1.2, 5.0);
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
      camera.position.set(0, 5.2, -4.0);
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
"""'''

# Find where floor0_code is defined and replaced
old_f0_match = re.search(r'floor0_code\s*=\s*""".*?"""\s*# Replace old buildExteriorStreet with our comprehensive road \+ stairs \+ lobby version\s*start_ext = html_text\.find\("function buildExteriorStreet\(\)"\)\s*end_ext = html_text\.find\("function buildInteriorOfficeFloor\(\)"\)\s*html_text = html_text\[:start_ext\] \+ floor0_code\.strip\(\) \+ "\\n\\n    " \+ html_text\[end_ext:\]', code, re.DOTALL)

if old_f0_match:
    replacement = new_floor0_code + """\n\n# Replace buildFloorEnvironment and buildExteriorStreet with outside/inside system\nstart_ext = html_text.find("function buildFloorEnvironment()")\nend_ext = html_text.find("function buildInteriorOfficeFloor()")\nhtml_text = html_text[:start_ext] + floor0_code.strip() + "\\n\\n    " + html_text[end_ext:]"""
    code = code[:old_f0_match.start()] + replacement + code[old_f0_match.end():]
    print("[OK] Replaced floor0_code definition and injection logic")
else:
    print("! Could not find old_f0_match with regex, let's check manual string replace")

# 3. Update rideElevatorTo and enrollAtGate
elevator_code_injection = '''
# Update rideElevatorTo to support floor0Area and inside landing
old_ride = """    function rideElevatorTo(targetFloor) {
      closeElevatorModal();
      playElevatorDing();
      currentFloor = targetFloor;
      buildFloorEnvironment();
      updateHUD();
      saveGame();
      showMemoToast("CAR DISPATCHED", `Arrived at ${getFloorName(currentFloor)}.`);
    }"""

new_ride = """    function rideElevatorTo(targetFloor) {
      closeElevatorModal();
      playElevatorDing();
      currentFloor = targetFloor;
      if (currentFloor === 0) {
        floor0Area = 'inside';
      }
      buildFloorEnvironment();
      if (currentFloor === 0) {
        playerGroup.position.set(0, 0.0, -8.5);
        playerGroup.rotation.y = 0; // Face South into lobby
        camera.position.set(0, 4.4, -3.0);
        camera.lookAt(0, 1.2, -8.5);
      }
      updateHUD();
      saveGame();
      showMemoToast("CAR DISPATCHED", `Arrived at ${getFloorName(currentFloor)}.`);
    }"""
html_text = html_text.replace(old_ride, new_ride)

# Update enrollAtGate memo toast and retro guide
old_enroll = 'showMemoToast("ADMISSION GRANTED", `Sworn to ${deptName}. Walk through the wrought iron turnstiles to Floor 1.`);'
new_enroll = """showMemoToast("ADMISSION GRANTED", `Sworn to ${deptName}. Take the elevator concourse at the north wall to Floor 1.`);
      setRetroGuide("ADMISSION GRANTED", `Admission approved for ${deptName}! Proceed to the elevator concourse at the north wall to ascend to Floor 1.`);
      updateActiveQuestUI();"""
html_text = html_text.replace(old_enroll, new_enroll)
'''

if "Update rideElevatorTo to support floor0Area" not in code:
    code = code.replace("# 8. FLOOR-SPECIFIC PROCEDURAL ROLE HOLDERS", elevator_code_injection + "\n# 8. FLOOR-SPECIFIC PROCEDURAL ROLE HOLDERS")
    print("[OK] Added rideElevatorTo and enrollAtGate updates")

# 4. Update anim_new for outside/inside bounds and camera
old_anim_new = """anim_new = \"\"\"      // NO CAMERA ROTATION (Fixed classic high-angle follow perspective)
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

        // SOLID COLLISION DETECTION (MC CANNOT pass through tables, desks or chairs)
        const nextX = playerGroup.position.x + dx;
        const boundX = (currentFloor === 0 ? 15.0 : 10.5);
        if (Math.abs(nextX) <= boundX && !checkCollision(nextX, playerGroup.position.z, playerRadius)) {
          playerGroup.position.x = nextX;
        }

        const nextZ = playerGroup.position.z + dz;
        const minZ = (currentFloor === 0 ? -13.5 : -8.5);
        const maxZ = (currentFloor === 0 ? 14.5 : 8.5);
        if (nextZ >= minZ && nextZ <= maxZ && !checkCollision(playerGroup.position.x, nextZ, playerRadius)) {
          playerGroup.position.z = nextZ;
        }

        // Height adjustment for Floor 0 stairs
        if (currentFloor === 0) {
          if (playerGroup.position.z > 5.5) {
            playerGroup.position.y = 0.25; // Street / Curb
          } else if (playerGroup.position.z <= 5.5 && playerGroup.position.z >= 2.0) {
            const stT = (5.5 - playerGroup.position.z) / 3.5;
            playerGroup.position.y = 0.25 + stT * 0.80; // Climbing stairs
          } else {
            playerGroup.position.y = 1.05; // Inside Lobby Floor
          }
        } else {
          playerGroup.position.y = 0.0;
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
      const camDistZ = (currentFloor === 0 ? 8.2 : 6.8);
      const camHeight = (currentFloor === 0 ? 5.6 : 4.8);
      const targetCamX = playerGroup.position.x;
      const targetCamY = playerGroup.position.y + camHeight;
      const targetCamZ = playerGroup.position.z + camDistZ;

      camera.position.x += (targetCamX - camera.position.x) * 0.12;
      camera.position.y += (targetCamY - camera.position.y) * 0.12;
      camera.position.z += (targetCamZ - camera.position.z) * 0.12;
      camera.lookAt(playerGroup.position.x, playerGroup.position.y + 1.2, playerGroup.position.z);\"\"\""""

new_anim_new = """anim_new = \"\"\"      // NO CAMERA ROTATION (Fixed classic high-angle follow perspective)
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
      }\"\"\""""

if old_anim_new in code:
    code = code.replace(old_anim_new, new_anim_new)
    print("[OK] Replaced anim_new logic for outside/inside")
else:
    print("! Could not find old_anim_new directly")

with open("build_complete_game_v3.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved updated build_complete_game_v3.py successfully!")
