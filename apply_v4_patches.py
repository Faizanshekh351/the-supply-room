"""
apply_v4_patches.py  –  All patches in one clean pipeline
Phase 1: Patch build_complete_game_v3.py (build-script-level changes)
Phase 2: Run the build to produce index.html
Phase 3: Post-process index.html directly for HTML/JS template-level changes
"""
import subprocess, sys, re

# =========================================================================
# PHASE 1: Patch the BUILD SCRIPT (build_complete_game_v3.py)
# Only things that ARE in the build script go here
# =========================================================================
with open('build_complete_game_v3.py', 'r', encoding='utf-8') as f:
    bcode = f.read()

# --- 1a. BLOCKING GUIDE CSS ---
old_guide_css = """.retro-guide-box {
      position: fixed;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%);
      width: min(860px, 94vw);
      background: #fdfaf2;
      border: 4px solid #211b14;
      border-radius: 4px;
      box-shadow: 0 10px 28px rgba(0,0,0,0.7), inset 0 0 0 2px #b9902f;
      padding: 10px 18px 12px 18px;
      z-index: 99;
      font-family: 'IBM Plex Mono', monospace;
      pointer-events: none;
      transition: all 0.2s ease;
    }"""
new_guide_css = """.retro-guide-box {
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
    }"""
bcode = bcode.replace(old_guide_css, new_guide_css)

bcode = bcode.replace(
    ".retro-guide-sub {\n      color: #6b5f4e;",
    ".retro-guide-sub {\n      color: #b9902f;"
)
bcode = bcode.replace(
    ".retro-guide-content {\n      color: #211b14;\n      font-size: 13.5px;\n      line-height: 1.45;\n      font-weight: 500;\n      padding-right: 20px;\n    }",
    ".retro-guide-content {\n      color: #f5ebd5;\n      font-size: 14px;\n      line-height: 1.55;\n      font-weight: 400;\n      padding-right: 28px;\n      letter-spacing: 0.2px;\n    }"
)
bcode = bcode.replace(
    "      color: #7a2e2e;\n      font-size: 12px;\n      animation: retroBlink 0.7s infinite alternate ease-in-out;\n    }",
    "      color: #b9902f;\n      font-size: 11px;\n      font-family: 'IBM Plex Mono', monospace;\n      letter-spacing: 0.5px;\n      opacity: 0;\n      animation: retroBlink 0.7s infinite alternate ease-in-out;\n    }"
)
bcode = bcode.replace(
    "      background: #7a2e2e;\n      color: #fdfaf2;\n      font-size: 10px;\n      font-weight: 700;\n      padding: 2px 7px;\n      letter-spacing: 1px;",
    "      background: #b9902f;\n      color: #0d0a07;\n      font-size: 10px;\n      font-weight: 700;\n      padding: 2px 8px;\n      letter-spacing: 1.5px;"
)

# --- 1b. Guide box HTML (update to hidden + remove inline text) ---
bcode = bcode.replace(
    """  <!-- Retro Pokémon-Style Bottom Guide Box -->
  <div class="retro-guide-box" id="retroGuideBox">
    <div class="retro-guide-header">
      <span class="retro-guide-badge" id="retroGuideTag">GUIDE</span>
      <span class="retro-guide-sub" id="retroGuideSub">THE MUTUAL FUN · 1987</span>
    </div>
    <div class="retro-guide-content" id="retroGuideText">
      Welcome to The Mutual Fun. Climb the granite stairs and enter the ground lobby to seek admission.
    </div>
    <div class="retro-guide-cursor">▼</div>
  </div>""",
    """  <!-- Retro Blocking Guide Box -->
  <div class="retro-guide-box" id="retroGuideBox" style="display:none;opacity:0;">
    <div class="retro-guide-header">
      <span class="retro-guide-badge" id="retroGuideTag">GUIDE</span>
      <span class="retro-guide-sub" id="retroGuideSub">THE MUTUAL FUN · 1987</span>
    </div>
    <div class="retro-guide-content" id="retroGuideText"></div>
    <div class="retro-guide-cursor" id="retroGuideCursor"></div>
  </div>"""
)

# --- 1c. Replace setRetroGuide function with blocking version ---
old_set_guide = """    function setRetroGuide(tag, text, sub = "THE MUTUAL FUN · 1987") {
      const tagEl = document.getElementById('retroGuideTag');
      const subEl = document.getElementById('retroGuideSub');
      const textEl = document.getElementById('retroGuideText');
      if (tagEl && textEl) {
        tagEl.innerText = tag.toUpperCase();
        if (subEl) subEl.innerText = sub;
        textEl.innerText = text;
      }
    }"""
new_set_guide = """    // =====================================================================
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
    }"""
bcode = bcode.replace(old_set_guide, new_set_guide)

# --- 1d. Remove setRetroGuide from proximity loop ---
bcode = bcode.replace(
    "        setRetroGuide(\"INTERACT\", `Press [E] to interact with: ${nearby.label}`);\n      } else {",
    "      } else {"
)

# --- 1e. Auto-save (make saveGame always silent in build script) ---
bcode = bcode.replace(
    "    function saveGame(showToast = false) {",
    "    function saveGame(showToast = false) { showToast = false; // Auto-save always silent"
)
bcode = bcode.replace(
    "    function confirmResetGame() {",
    "    // AUTO-SAVE every 15 seconds\n    setInterval(() => { if (typeof saveGame === 'function') saveGame(); }, 15000);\n\n    function confirmResetGame() {"
)
bcode = bcode.replace(
    "if (confirm(\"Reset career history and return to the sunny pavement outside the gate?\")) {",
    "if (confirm(\"Restart from the beginning and return to the sunny pavement outside the gate?\")) {"
)

with open('build_complete_game_v3.py', 'w', encoding='utf-8') as f:
    f.write(bcode)
print("[OK] Phase 1: build_complete_game_v3.py patched")

# =========================================================================
# PHASE 2: Run the build
# =========================================================================
result = subprocess.run([sys.executable, 'build_complete_game_v3.py'], capture_output=True, text=True)
print("BUILD STDOUT:", result.stdout[-1000:])
if result.stderr:
    print("BUILD STDERR:", result.stderr[:1500])
if result.returncode != 0:
    print("[FAIL] Build failed")
    sys.exit(1)
print("[OK] Phase 2: index.html compiled")

# =========================================================================
# PHASE 3: Post-process index.html (template-level HTML and JS changes)
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# --- 3a. HUD: Remove Elevator + Save Device buttons, rename Reset → Restart ---
old_hud = """    <button class="hud-btn" onclick="openElevatorModal()">
      <span style="color:var(--lamp);">▲</span> Elevator Concourse
    </button>
    <button class="hud-btn" onclick="openCertModal()">
      <span style="color:var(--oxblood);">📜</span> Employment Certificate
    </button>
    <button class="hud-btn" onclick="saveGame(true)">
      <span>💾</span> Save Device
    </button>
    <button class="hud-btn" onclick="confirmResetGame()" style="color:#a84848;">
      Reset
    </button>"""
new_hud = """    <button class="hud-btn" onclick="openCertModal()">
      <span style="color:var(--oxblood);">📜</span> Employment Certificate
    </button>
    <button class="hud-btn" onclick="confirmResetGame()" style="color:#a84848;">
      Restart
    </button>"""
if old_hud in html:
    html = html.replace(old_hud, new_hud)
    print("[OK] HUD buttons patched")
else:
    print("[WARN] HUD buttons target not found")

# --- 3b. Keydown: guide advance before arena check ---
old_kd = """    const keys = {};
    window.addEventListener('keydown', (e) => {
      const code = e.code.toLowerCase();
      keys[code] = true;

      if (arenaModal.classList.contains('active')) {"""
new_kd = """    const keys = {};
    window.addEventListener('keydown', (e) => {
      const code = e.code.toLowerCase();
      keys[code] = true;

      // Guide advance: E, Space or Enter dismisses/skips guide
      if (typeof guideLocked !== 'undefined' && guideLocked &&
          (e.code === 'KeyE' || e.code === 'Space' || e.code === 'Enter')) {
        e.preventDefault();
        if (typeof advanceGuide === 'function') advanceGuide();
        return;
      }

      if (arenaModal.classList.contains('active')) {"""
if old_kd in html:
    html = html.replace(old_kd, new_kd)
    print("[OK] Keydown guide patch applied")
else:
    print("[WARN] Keydown guide patch target not found")

# --- 3c. Movement lock ---
old_mv = "if (isMoving && !isModalActive) {"
new_mv = "if (isMoving && !isModalActive && !(typeof guideLocked !== 'undefined' && guideLocked)) {"
cnt = html.count(old_mv)
html = html.replace(old_mv, new_mv)
print(f"[OK] Movement lock patched ({cnt} occurrences)")

# --- 3d. 8-TIER 2D CANVAS CHAIRS matching pixel art ---
old_draw_chair = "    // DRAW CUSTOM CHAIRS PROCEDURALLY IN 2D\n    function drawCustomFloorChair(x, y, floor) {"
new_draw_chair_prefix = "    // DRAW CUSTOM CHAIRS PROCEDURALLY IN 2D (8-tier pixel art)\n    function drawCustomFloorChair(x, y, floor) {"

if old_draw_chair in html:
    # Find end of function
    start = html.index(old_draw_chair)
    # find closing: ctx.restore(); } immediately after the if/else block
    end_marker = "\n      ctx.restore();\n    }\n\n    // ====="
    end_idx = html.index(end_marker, start) + len("\n      ctx.restore();\n    }\n")
    
    chair_2d_fn = """    // DRAW CUSTOM CHAIRS PROCEDURALLY IN 2D (8-tier pixel art)
    function drawCustomFloorChair(x, y, floor) {
      ctx.save();
      ctx.translate(x, y);

      if (floor === 1) {
        // Floor 1: Folding Metal Stool - silver frame, white seat, blue back
        ctx.strokeStyle = '#a0aaaf'; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(-20,32); ctx.lineTo(6,-14); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(20,32); ctx.lineTo(-6,-14); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-16,10); ctx.lineTo(16,10); ctx.stroke();
        ctx.fillStyle = '#e8eef2'; ctx.fillRect(-22,-20,44,10);
        ctx.strokeStyle='#a0aaaf';ctx.lineWidth=1.5;ctx.strokeRect(-22,-20,44,10);
        ctx.fillStyle = '#5b8ec4'; ctx.fillRect(-18,-40,36,18);
        ctx.fillStyle = '#7aaad6'; ctx.fillRect(-18,-40,36,6);
        ctx.strokeStyle='#a0aaaf';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(0,-20);ctx.lineTo(0,-40);ctx.stroke();

      } else if (floor === 2) {
        // Floor 2: Swivel chair - chrome star, beige seat, blue upper back
        ctx.strokeStyle='#c0c0c0';ctx.lineWidth=4;
        for(let i=0;i<5;i++){const a=(i*Math.PI*2)/5-Math.PI/2;ctx.beginPath();ctx.moveTo(0,30);ctx.lineTo(Math.cos(a)*24,30+Math.sin(a)*8);ctx.stroke();}
        ctx.fillStyle='#c0c0c0';ctx.fillRect(-4,10,8,20);
        ctx.fillStyle='#d4b896';ctx.fillRect(-26,-2,52,12);
        ctx.fillStyle='#c9a882';ctx.fillRect(-26,-2,52,5);
        ctx.fillStyle='#d4b896';ctx.fillRect(-22,-22,44,20);
        ctx.fillStyle='#6a8fb8';ctx.fillRect(-22,-44,44,22);
        ctx.fillStyle='#7aaad6';ctx.fillRect(-22,-44,44,8);

      } else if (floor === 3) {
        // Floor 3: Wood executive chair - open frame back, armrests, X-base
        ctx.strokeStyle='#6b3b1a';ctx.lineWidth=5;
        ctx.beginPath();ctx.moveTo(-22,34);ctx.lineTo(22,18);ctx.stroke();
        ctx.beginPath();ctx.moveTo(22,34);ctx.lineTo(-22,18);ctx.stroke();
        ctx.fillStyle='#6b3b1a';ctx.fillRect(-3,14,6,4);
        ctx.fillStyle='#6b3b1a';ctx.fillRect(-26,4,52,12);
        ctx.fillStyle='#8a4e24';ctx.fillRect(-26,4,52,5);
        ctx.fillStyle='#6b3b1a';ctx.fillRect(-36,-8,12,5);ctx.fillRect(24,-8,12,5);
        ctx.fillRect(-26,-48,52,6);ctx.fillRect(-26,-16,6,32);ctx.fillRect(20,-16,6,32);
        ctx.fillStyle='#d4af37';
        [-16,0,16].forEach(sx=>{ctx.beginPath();ctx.arc(sx,-11,3,0,Math.PI*2);ctx.fill();});

      } else if (floor === 4) {
        // Floor 4: Green padded chair - dark green, gold studs, star base
        ctx.strokeStyle='#222';ctx.lineWidth=4;
        for(let i=0;i<5;i++){const a=(i*Math.PI*2)/5-Math.PI/2;ctx.beginPath();ctx.moveTo(0,32);ctx.lineTo(Math.cos(a)*24,32+Math.sin(a)*8);ctx.stroke();}
        ctx.fillStyle='#222';ctx.fillRect(-3,12,6,22);
        ctx.fillStyle='#2a5c3c';ctx.fillRect(-28,0,56,14);
        ctx.fillStyle='#d4af37';[-20,-10,0,10,20].forEach(sx=>{ctx.beginPath();ctx.arc(sx,7,3,0,Math.PI*2);ctx.fill();});
        ctx.fillStyle='#2a5c3c';ctx.fillRect(-40,-12,14,6);ctx.fillRect(26,-12,14,6);
        ctx.fillStyle='#2a5c3c';ctx.fillRect(-26,-50,52,52);
        ctx.fillStyle='#1e4730';ctx.fillRect(-26,-50,52,10);
        ctx.fillStyle='#d4af37';
        [-12,0,12].forEach(row=>{[-16,-8,0,8,16].forEach(col=>{ctx.beginPath();ctx.arc(col,row-26,2.5,0,Math.PI*2);ctx.fill();});});

      } else if (floor === 5) {
        // Floor 5: Maroon velvet armchair - wings, plush seat, cabriole legs
        ctx.fillStyle='#2e1208';
        ctx.fillRect(-28,20,7,18);ctx.fillRect(21,20,7,18);
        ctx.fillRect(-20,22,6,16);ctx.fillRect(14,22,6,16);
        ctx.fillStyle='#7a1c1c';ctx.fillRect(-32,4,64,18);
        ctx.fillStyle='#9a2c2c';ctx.fillRect(-32,4,64,8);
        ctx.fillStyle='#7a1c1c';ctx.fillRect(-40,-12,14,18);ctx.fillRect(26,-12,14,18);
        ctx.fillStyle='#6a1414';ctx.fillRect(-42,-40,16,30);ctx.fillRect(26,-40,16,30);
        ctx.fillStyle='#7a1c1c';ctx.fillRect(-28,-52,56,58);
        ctx.fillStyle='#9a2c2c';ctx.fillRect(-28,-52,56,12);
        ctx.strokeStyle='#5a1010';ctx.lineWidth=1.5;
        [-12,2,16].forEach(ty=>{ctx.beginPath();ctx.moveTo(-24,ty-52);ctx.lineTo(24,ty-52);ctx.stroke();});

      } else if (floor === 6) {
        // Floor 6: Dark brown double high-back - mahogany, gold studs
        ctx.fillStyle='#3b1c0a';ctx.fillRect(-30,22,8,18);ctx.fillRect(22,22,8,18);
        ctx.fillStyle='#3b1c0a';ctx.fillRect(-32,6,64,18);
        ctx.fillStyle='#5a2c12';ctx.fillRect(-32,6,64,8);
        ctx.fillStyle='#d4af37';[-22,-11,0,11,22].forEach(sx=>{ctx.beginPath();ctx.arc(sx,20,3,0,Math.PI*2);ctx.fill();});
        ctx.fillStyle='#3b1c0a';ctx.fillRect(-44,-8,14,7);ctx.fillRect(30,-8,14,7);
        ctx.fillStyle='#3b1c0a';ctx.fillRect(-30,-28,60,34);
        ctx.fillStyle='#2a1006';ctx.fillRect(-30,-28,60,10);
        ctx.fillStyle='#1a0a04';ctx.fillRect(-30,-34,60,7);
        ctx.fillStyle='#3b1c0a';ctx.fillRect(-30,-66,60,32);
        ctx.fillStyle='#2a1006';ctx.fillRect(-30,-66,60,10);
        ctx.fillStyle='#d4af37';[-16,0,16].forEach(sx=>{ctx.beginPath();ctx.arc(sx,-56,3,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(sx,-18,3,0,Math.PI*2);ctx.fill();});

      } else if (floor === 7) {
        // Floor 7: Tan high-back throne - open arch, gold finials
        ctx.fillStyle='#c8a46a';ctx.fillRect(-28,22,8,18);ctx.fillRect(20,22,8,18);
        ctx.fillStyle='#c8a46a';ctx.fillRect(-26,4,52,20);
        ctx.fillStyle='#a8844a';ctx.fillRect(-26,4,52,8);
        ctx.fillStyle='#c8a46a';ctx.fillRect(-38,-10,14,6);ctx.fillRect(24,-10,14,6);
        ctx.fillStyle='#c8a46a';ctx.fillRect(-30,-68,10,62);ctx.fillRect(20,-68,10,62);
        ctx.fillStyle='#a8844a';ctx.fillRect(-20,-58,40,48);
        ctx.fillStyle='#b89050';ctx.fillRect(-20,-58,40,10);
        ctx.fillStyle='#7a5c30';ctx.fillRect(-18,-32,36,7);
        ctx.fillStyle='#c8a46a';ctx.fillRect(-32,-72,64,10);
        ctx.fillStyle='#d4af37';
        ctx.beginPath();ctx.arc(-26,-76,5,0,Math.PI*2);ctx.fill();
        ctx.beginPath();ctx.arc(26,-76,5,0,Math.PI*2);ctx.fill();
        ctx.beginPath();ctx.arc(0,-78,4,0,Math.PI*2);ctx.fill();

      } else {
        // Floor 8/9: Royal crimson throne - gold frame, crown top
        ctx.fillStyle='#d4af37';ctx.fillRect(-36,24,72,14);
        ctx.fillStyle='#f0c030';ctx.fillRect(-36,24,72,6);
        ctx.fillStyle='#d4af37';ctx.fillRect(-32,10,8,16);ctx.fillRect(24,10,8,16);
        ctx.fillStyle='#d4af37';ctx.fillRect(-34,0,68,12);
        ctx.fillStyle='#8b0c0c';ctx.fillRect(-30,0,60,12);
        ctx.fillStyle='#b01c1c';ctx.fillRect(-30,0,60,5);
        ctx.fillStyle='#d4af37';ctx.fillRect(-42,-14,14,7);ctx.fillRect(28,-14,14,7);
        ctx.fillStyle='#d4af37';ctx.fillRect(-36,-62,10,62);ctx.fillRect(26,-62,10,62);
        ctx.fillStyle='#8b0c0c';ctx.fillRect(-26,-60,52,60);
        ctx.fillStyle='#b01c1c';ctx.fillRect(-26,-60,52,12);
        ctx.fillStyle='#ffd700';[-16,-8,0,8,16].forEach(sx=>{[-48,-36,-24,-12].forEach(sy=>{ctx.beginPath();ctx.arc(sx,sy,2.5,0,Math.PI*2);ctx.fill();});});
        ctx.fillStyle='#d4af37';ctx.fillRect(-38,-68,76,10);
        ctx.fillStyle='#ffd700';
        [-24,-12,0,12,24].forEach((cx2,i)=>{const h=i%2===0?14:10;ctx.beginPath();ctx.moveTo(cx2-5,-68);ctx.lineTo(cx2,-68-h);ctx.lineTo(cx2+5,-68);ctx.closePath();ctx.fill();});
        if(floor===9){ctx.fillStyle='#ff3030';ctx.beginPath();ctx.arc(0,-78,4,0,Math.PI*2);ctx.fill();}
      }

      ctx.restore();
    }

"""
    html = html[:start] + chair_2d_fn + html[end_idx:]
    print("[OK] 2D chair function patched")
else:
    print("[WARN] 2D chair function not found")

# --- 3e. 8-TIER 3D CHAIRS ---
old_chair_3d_sig = "    function createChair(x, y, z, floorTier = 1, rotY = 0) {"
old_chair_3d_end = "      chairGroup.position.set(x, y, z);\n      chairGroup.rotation.y = rotY;\n      chairGroup.castShadow = true;\n      roomGroup.add(chairGroup);\n      return chairGroup;\n    }"
if old_chair_3d_sig in html and old_chair_3d_end in html:
    start = html.index(old_chair_3d_sig)
    end = html.index(old_chair_3d_end, start) + len(old_chair_3d_end)
    
    chair_3d_fn = """    function createChair(x, y, z, floorTier = 1, rotY = 0) {
      const chairGroup = new THREE.Group();

      if (floorTier === 1) {
        const silver=new THREE.MeshLambertMaterial({color:0xb0b8c1});
        const padW=new THREE.MeshLambertMaterial({color:0xe8eef2});
        const blue=new THREE.MeshLambertMaterial({color:0x5b8ec4});
        const x1=new THREE.Mesh(new THREE.BoxGeometry(0.04,0.56,0.06),silver);x1.rotation.z=0.35;x1.position.set(-0.18,0.28,0);chairGroup.add(x1);
        const x2=new THREE.Mesh(new THREE.BoxGeometry(0.04,0.56,0.06),silver);x2.rotation.z=-0.35;x2.position.set(0.18,0.28,0);chairGroup.add(x2);
        const rung=new THREE.Mesh(new THREE.BoxGeometry(0.44,0.03,0.04),silver);rung.position.set(0,0.14,0);chairGroup.add(rung);
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.52,0.05,0.46),padW);seat.position.set(0,0.50,0);chairGroup.add(seat);
        const bp=new THREE.Mesh(new THREE.BoxGeometry(0.03,0.52,0.03),silver);bp.position.set(0,0.74,-0.22);chairGroup.add(bp);
        const bpad=new THREE.Mesh(new THREE.BoxGeometry(0.48,0.26,0.04),blue);bpad.position.set(0,0.80,-0.21);chairGroup.add(bpad);

      } else if (floorTier === 2) {
        const beige=new THREE.MeshLambertMaterial({color:0xd4b896});
        const blueP=new THREE.MeshLambertMaterial({color:0x7b9fc7});
        const chrome=new THREE.MeshLambertMaterial({color:0xc8c8c8});
        for(let i=0;i<5;i++){const a=(i*Math.PI*2)/5;const arm=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.03,0.28),chrome);arm.rotation.y=a;arm.position.set(Math.sin(a)*0.14,0.04,Math.cos(a)*0.14);chairGroup.add(arm);}
        const col=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.34,10),chrome);col.position.set(0,0.24,0);chairGroup.add(col);
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.64,0.10,0.58),beige);seat.position.set(0,0.48,0.02);chairGroup.add(seat);
        const lb=new THREE.Mesh(new THREE.BoxGeometry(0.62,0.28,0.07),beige);lb.position.set(0,0.73,-0.26);chairGroup.add(lb);
        const ub=new THREE.Mesh(new THREE.BoxGeometry(0.62,0.30,0.06),blueP);ub.position.set(0,1.02,-0.25);chairGroup.add(ub);

      } else if (floorTier === 3) {
        const wood=new THREE.MeshLambertMaterial({color:0x6b3b1a});
        const brass=new THREE.MeshLambertMaterial({color:0xc8a23a});
        const xb1=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.04,0.46),wood);xb1.rotation.y=0.45;xb1.position.set(0,0.04,0);chairGroup.add(xb1);
        const xb2=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.04,0.46),wood);xb2.rotation.y=-0.45;xb2.position.set(0,0.04,0);chairGroup.add(xb2);
        const post=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.3,0.06),wood);post.position.set(0,0.18,0);chairGroup.add(post);
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.70,0.07,0.62),wood);seat.position.set(0,0.50,0);chairGroup.add(seat);
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.04,0.44),wood);aL.position.set(-0.38,0.72,-0.04);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.38,0.72,-0.04);chairGroup.add(aR);
        const bt=new THREE.Mesh(new THREE.BoxGeometry(0.72,0.06,0.05),wood);bt.position.set(0,1.12,-0.28);chairGroup.add(bt);
        const bb=new THREE.Mesh(new THREE.BoxGeometry(0.72,0.05,0.05),wood);bb.position.set(0,0.60,-0.28);chairGroup.add(bb);
        const bsL=new THREE.Mesh(new THREE.BoxGeometry(0.05,0.56,0.05),wood);bsL.position.set(-0.34,0.86,-0.28);chairGroup.add(bsL);
        const bsR=bsL.clone();bsR.position.set(0.34,0.86,-0.28);chairGroup.add(bsR);
        for(let i=-1;i<=1;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(0.025,6,6),brass);s.position.set(i*0.22,0.54,0.32);chairGroup.add(s);}

      } else if (floorTier === 4) {
        const dg=new THREE.MeshLambertMaterial({color:0x2a5c3c});
        const gs=new THREE.MeshLambertMaterial({color:0xd4af37});
        const db=new THREE.MeshLambertMaterial({color:0x1a1a1a});
        for(let i=0;i<5;i++){const a=(i*Math.PI*2)/5;const arm=new THREE.Mesh(new THREE.BoxGeometry(0.05,0.03,0.30),db);arm.rotation.y=a;arm.position.set(Math.sin(a)*0.14,0.04,Math.cos(a)*0.14);chairGroup.add(arm);}
        const col=new THREE.Mesh(new THREE.CylinderGeometry(0.042,0.042,0.36,10),db);col.position.set(0,0.24,0);chairGroup.add(col);
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.72,0.12,0.64),dg);seat.position.set(0,0.50,0.02);chairGroup.add(seat);
        for(let i=-3;i<=3;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(0.022,6,6),gs);s.position.set(i*0.10,0.50,0.34);chairGroup.add(s);}
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.04,0.46),dg);aL.position.set(-0.40,0.76,-0.04);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.40,0.76,-0.04);chairGroup.add(aR);
        const back=new THREE.Mesh(new THREE.BoxGeometry(0.70,0.80,0.09),dg);back.position.set(0,0.98,-0.30);chairGroup.add(back);
        for(let r=0;r<3;r++)for(let c=-2;c<=2;c++){const s=new THREE.Mesh(new THREE.SphereGeometry(0.018,6,6),gs);s.position.set(c*0.12,0.72+r*0.22,-0.26);chairGroup.add(s);}

      } else if (floorTier === 5) {
        const mr=new THREE.MeshLambertMaterial({color:0x7a1c1c});
        const dw=new THREE.MeshLambertMaterial({color:0x2e1208});
        [[-0.28,0.20],[0.28,0.20],[-0.28,-0.20],[0.28,-0.20]].forEach(([lx,lz])=>{const l=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.025,0.40,8),dw);l.position.set(lx,0.20,lz);chairGroup.add(l);});
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.80,0.16,0.72),mr);seat.position.set(0,0.48,0.02);chairGroup.add(seat);
        const back=new THREE.Mesh(new THREE.BoxGeometry(0.76,0.72,0.14),mr);back.position.set(0,0.98,-0.30);chairGroup.add(back);
        const wL=new THREE.Mesh(new THREE.BoxGeometry(0.12,0.42,0.22),mr);wL.position.set(-0.44,0.92,-0.22);chairGroup.add(wL);
        const wR=wL.clone();wR.position.set(0.44,0.92,-0.22);chairGroup.add(wR);
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.12,0.05,0.52),mr);aL.position.set(-0.46,0.72,-0.06);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.46,0.72,-0.06);chairGroup.add(aR);

      } else if (floorTier === 6) {
        const db=new THREE.MeshLambertMaterial({color:0x3b1c0a});
        const gs=new THREE.MeshLambertMaterial({color:0xd4af37});
        [[-0.30,0.22],[0.30,0.22],[-0.30,-0.22],[0.30,-0.22]].forEach(([lx,lz])=>{const l=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.032,0.38,8),db);l.position.set(lx,0.19,lz);chairGroup.add(l);});
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.84,0.14,0.74),db);seat.position.set(0,0.45,0.02);chairGroup.add(seat);
        const bL=new THREE.Mesh(new THREE.BoxGeometry(0.82,0.46,0.12),db);bL.position.set(0,0.80,-0.33);chairGroup.add(bL);
        const gap=new THREE.Mesh(new THREE.BoxGeometry(0.82,0.06,0.08),db);gap.position.set(0,1.06,-0.33);chairGroup.add(gap);
        const bH=new THREE.Mesh(new THREE.BoxGeometry(0.82,0.46,0.12),db);bH.position.set(0,1.32,-0.33);chairGroup.add(bH);
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.10,0.05,0.56),db);aL.position.set(-0.47,0.72,-0.08);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.47,0.72,-0.08);chairGroup.add(aR);
        for(let i=-3;i<=3;i++){const s1=new THREE.Mesh(new THREE.SphereGeometry(0.018,6,6),gs);s1.position.set(i*0.12,0.45,0.38);chairGroup.add(s1);const s2=new THREE.Mesh(new THREE.SphereGeometry(0.018,6,6),gs);s2.position.set(i*0.12,1.56,-0.26);chairGroup.add(s2);}

      } else if (floorTier === 7) {
        const tn=new THREE.MeshLambertMaterial({color:0xc8a46a});
        const gd=new THREE.MeshLambertMaterial({color:0xd4af37});
        const dw=new THREE.MeshLambertMaterial({color:0x5a3518});
        [[-0.26,0.20],[0.26,0.20],[-0.26,-0.20],[0.26,-0.20]].forEach(([lx,lz])=>{const l=new THREE.Mesh(new THREE.BoxGeometry(0.07,0.40,0.07),tn);l.position.set(lx,0.20,lz);chairGroup.add(l);});
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.74,0.12,0.64),tn);seat.position.set(0,0.46,0.02);chairGroup.add(seat);
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.08,0.04,0.48),tn);aL.position.set(-0.41,0.72,-0.04);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.41,0.72,-0.04);chairGroup.add(aR);
        const sL=new THREE.Mesh(new THREE.BoxGeometry(0.08,1.10,0.08),tn);sL.position.set(-0.34,1.08,-0.30);chairGroup.add(sL);
        const sR=sL.clone();sR.position.set(0.34,1.08,-0.30);chairGroup.add(sR);
        const top=new THREE.Mesh(new THREE.BoxGeometry(0.76,0.10,0.08),tn);top.position.set(0,1.64,-0.30);chairGroup.add(top);
        const fL=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.10,8),gd);fL.position.set(-0.34,1.74,-0.30);chairGroup.add(fL);
        const fR=fL.clone();fR.position.set(0.34,1.74,-0.30);chairGroup.add(fR);
        const cr=new THREE.Mesh(new THREE.BoxGeometry(0.64,0.07,0.06),dw);cr.position.set(0,1.14,-0.30);chairGroup.add(cr);

      } else {
        // Floor 8+: Royal crimson throne with gold frame and crown
        const cr=new THREE.MeshLambertMaterial({color:0x8b0c0c});
        const gL=new THREE.MeshLambertMaterial({color:0xd4af37});
        const rG=new THREE.MeshLambertMaterial({color:0xffd700});
        const dais=new THREE.Mesh(new THREE.BoxGeometry(1.0,0.16,1.0),gL);dais.position.set(0,0.08,0);chairGroup.add(dais);
        [[-0.40,0.18],[0.40,0.18],[-0.40,-0.18],[0.40,-0.18]].forEach(([px,pz])=>{const p=new THREE.Mesh(new THREE.BoxGeometry(0.08,0.36,0.08),gL);p.position.set(px,0.34,pz);chairGroup.add(p);});
        const seat=new THREE.Mesh(new THREE.BoxGeometry(0.82,0.16,0.72),cr);seat.position.set(0,0.44,0.02);chairGroup.add(seat);
        const sf=new THREE.Mesh(new THREE.BoxGeometry(0.90,0.06,0.80),gL);sf.position.set(0,0.36,0);chairGroup.add(sf);
        const back=new THREE.Mesh(new THREE.BoxGeometry(0.82,1.10,0.12),cr);back.position.set(0,1.08,-0.34);chairGroup.add(back);
        const gsL=new THREE.Mesh(new THREE.BoxGeometry(0.09,1.14,0.10),gL);gsL.position.set(-0.46,1.08,-0.34);chairGroup.add(gsL);
        const gsR=gsL.clone();gsR.position.set(0.46,1.08,-0.34);chairGroup.add(gsR);
        const aL=new THREE.Mesh(new THREE.BoxGeometry(0.10,0.06,0.54),gL);aL.position.set(-0.48,0.74,-0.06);chairGroup.add(aL);
        const aR=aL.clone();aR.position.set(0.48,0.74,-0.06);chairGroup.add(aR);
        const cb=new THREE.Mesh(new THREE.BoxGeometry(0.92,0.10,0.09),gL);cb.position.set(0,1.68,-0.34);chairGroup.add(cb);
        for(let cp=-2;cp<=2;cp++){const pt=new THREE.Mesh(new THREE.CylinderGeometry(0,0.055,0.18,4),rG);pt.position.set(cp*0.18,1.82,-0.34);chairGroup.add(pt);}
        for(let row=0;row<4;row++)for(let c=-3;c<=3;c++){const s=new THREE.Mesh(new THREE.SphereGeometry(0.016,6,6),rG);s.position.set(c*0.11,0.64+row*0.26,-0.28);chairGroup.add(s);}
        if(floorTier===9){const gw=new THREE.PointLight(0xffd700,1.2,4.5);gw.position.set(0,1.9,-0.2);chairGroup.add(gw);}
      }

      chairGroup.position.set(x, y, z);
      chairGroup.rotation.y = rotY;
      chairGroup.castShadow = true;
      roomGroup.add(chairGroup);
      return chairGroup;
    }"""
    html = html[:start] + chair_3d_fn + html[end:]
    print("[OK] 3D chair function patched")
else:
    print("[WARN] 3D createChair function not found in index.html")

# --- 3f. 1v1 Arena: setupArenaContenders ---
old_setup = """    function setupArenaContenders() {
      const flickerrAvatar = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      arenaContenders = [
        { id: 0, name: "You", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color }
      ];"""
new_setup = """    const ARENA_FLOOR_HOLDERS = {
      1: { name: "Chief Mail Clerk",        role: "Intern Supervisor",     color: "#5a3518", hasCrown: false },
      2: { name: "Senior Ledger Archivist", role: "Floor 2 Analyst Lead",  color: "#2a3d4e", hasCrown: false },
      3: { name: "Head Trading Associate",  role: "Floor 3 Senior Assoc.", color: "#2e3d4a", hasCrown: false },
      4: { name: "VP Syndications",         role: "Vice President",        color: "#4a2a12", hasCrown: false },
      5: { name: "Chief Compliance Dir.",   role: "Director",              color: "#6e5d8c", hasCrown: false },
      6: { name: "what3verman",             role: "Managing Director",     color: "#1f4728", hasCrown: false },
      7: { name: "General Counsel",         role: "Syndicate Trustee",     color: "#7a2e2e", hasCrown: false },
      8: { name: "The Chairman Kingpickle", role: "Chairman of the Board", color: "#110b06", hasCrown: true  },
      9: { name: "Vault Sovereign",         role: "Master Mint Custodian", color: "#8b6914", hasCrown: false }
    };

    function setupArenaContenders() {
      const flickerrAvatar = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      const holder = ARENA_FLOOR_HOLDERS[arenaFloor] || { name: "Floor Holder", role: "Seat Holder", color: "#5a3518", hasCrown: false };
      arenaContenders = [
        { id: 0, name: "You", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color },
        { id: 1, name: holder.name, role: holder.role, fund: `Floor ${arenaFloor} Seat`, avatar: null, color: holder.color, hasCrown: holder.hasCrown }
      ];"""
if old_setup in html:
    html = html.replace(old_setup, new_setup)
    print("[OK] 1v1 setupArenaContenders patched")
else:
    print("[WARN] setupArenaContenders target not found")

# --- 3g. Arena active = [0,1] (1v1) ---
html = html.replace(
    "      arenaRound = 1;\n      arenaActive = [0, 1, 2, 3];",
    "      arenaRound = 1;\n      arenaActive = [0, 1]; // 1v1"
)
html = html.replace(
    "      arenaActive = [0, 1, 2, 3];\n      arenaRound = 1;",
    "      arenaActive = [0, 1]; // 1v1\n      arenaRound = 1;"
)

# --- 3h. Arena round label → "FINAL DISPUTE" ---
html = html.replace(
    "      arenaRoundLabel.innerText = `ROUND 0${arenaRound} / 03`;",
    "      arenaRoundLabel.innerText = 'FINAL DISPUTE';"
)

# --- 3i. Arena intro text for 1v1 ---
html = html.replace(
    "`There is always one chair too few. Circle the parquet marquetry while the phonograph spins. When the needle cuts and the boardroom bell tolls, seize an available seat immediately. Press SPACE to sit. Beware: sitting on green results in immediate forfeiture.`;",
    "`One chair. One chance. Circle the parquet while the phonograph spins. When the needle scratches and the boardroom bell tolls, seize the chair before the seat holder does. Press SPACE to sit. Moving during the music is immediate forfeiture.`;"
)

# --- 3j. Win text for 1v1 ---
html = html.replace(
    "        body.innerText = `Three rounds. Three flawless moves. You secure lawful title to ${arenaChairName} on Floor ${arenaFloor}.`;",
    "        body.innerText = `You out-reflexed ${arenaContenders[1] ? arenaContenders[1].name : 'the Floor Holder'} and secured lawful title to ${arenaChairName} on Floor ${arenaFloor}.`;"
)

# --- 3k. Crown for any holder with hasCrown ---
html = html.replace(
    "      // Crown for Kingpickle on Penthouse!\n      if (arenaFloor === 9 && id === 1) {",
    "      // Crown for floor holders with hasCrown flag\n      if (id === 1 && arenaContenders[1] && arenaContenders[1].hasCrown) {"
)
html = html.replace(
    "      ctx.fillStyle = (id === 1 && arenaFloor === 9 ? \"#ffffff\" : \"#3d2719\");",
    "      ctx.fillStyle = (id === 1 && arenaContenders[1] && arenaContenders[1].hasCrown ? \"#ffffff\" : \"#3d2719\");"
)
html = html.replace(
    "      } else if (id === 1 && (arenaFloor === 6 || arenaFloor === 9)) {",
    "      } else if (id === 1) {"
)

# =========================================================================
# SAVE
# =========================================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
art_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(art_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"[OK] All patches applied. index.html saved ({len(html)//1024}KB)")
