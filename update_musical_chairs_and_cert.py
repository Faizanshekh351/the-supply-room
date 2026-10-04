with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Lower musical chair difficulty:
# Base reaction time increased across all floors so the player has generous time to react, with wider spread.
old_diff = """    const FLOOR_REFLEX_DIFFICULTY = {
      1: { base: 460, spread: 130, label: "~460 ms" },
      2: { base: 410, spread: 120, label: "~410 ms" },
      3: { base: 360, spread: 110, label: "~360 ms" },
      4: { base: 310, spread: 100, label: "~310 ms" },
      5: { base: 260, spread: 90,  label: "~260 ms" },
      6: { base: 220, spread: 80,  label: "~220 ms (Boss: what3verman)" },
      7: { base: 195, spread: 70,  label: "~195 ms" },
      8: { base: 175, spread: 60,  label: "~175 ms" },
      9: { base: 155, spread: 50,  label: "~155 ms (Boss: Kingpickle)" }
    };"""

new_diff = """    const FLOOR_REFLEX_DIFFICULTY = {
      1: { base: 820, spread: 180, label: "~820 ms (Gentle)" },
      2: { base: 750, spread: 160, label: "~750 ms (Moderate)" },
      3: { base: 680, spread: 150, label: "~680 ms (Standard)" },
      4: { base: 610, spread: 140, label: "~610 ms (Attentive)" },
      5: { base: 540, spread: 130, label: "~540 ms (Agile)" },
      6: { base: 480, spread: 120, label: "~480 ms (Managing Director what3verman)" },
      7: { base: 430, spread: 110, label: "~430 ms (Executive)" },
      8: { base: 380, spread: 100, label: "~380 ms (Governor of Board)" },
      9: { base: 330, spread: 90,  label: "~330 ms (The Chairman Kingpickle)" }
    };"""

if old_diff in text:
    text = text.replace(old_diff, new_diff)
    print("Lowered musical chair reflex difficulty successfully!")

# Also ensure minimum bot delay is relaxed from 130 to 280ms
text = text.replace("return Math.round(Math.max(130, reaction));", "return Math.round(Math.max(280, reaction));")

# 2. Richer 2D Arena Canvas Background & Movement Animation
old_draw_arena_start = "    function drawChamberArenaCanvas(now) {"
old_draw_arena_end = "      // 2. Animated 1987 Corporate Phonograph Turntable in Upper-Left Corner\n      drawCornerPhonograph(85, 75, now);"

new_draw_arena = """    function drawChamberArenaCanvas(now) {
      ctx.imageSmoothingEnabled = true;

      // 1. Grand Boardroom Marquetry Herringbone & Parquet Flooring
      const bgGrad = ctx.createRadialGradient(480, 270, 80, 480, 270, 520);
      bgGrad.addColorStop(0, "#2c170b");
      bgGrad.addColorStop(0.55, "#1f0f07");
      bgGrad.addColorStop(1, "#120803");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, 960, 540);

      // Fine Inlaid Marquetry Radial Starburst
      ctx.save();
      ctx.translate(480, 275);
      for (let i = 0; i < 32; i++) {
        const ang = (i * Math.PI * 2) / 32;
        ctx.strokeStyle = (i % 2 === 0 ? "rgba(74, 40, 20, 0.45)" : "rgba(40, 20, 10, 0.45)");
        ctx.lineWidth = 18;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(ang) * 480, Math.sin(ang) * 250);
        ctx.stroke();
      }
      ctx.restore();

      // Outer Inlaid Brass Rail
      ctx.strokeStyle = "#c89d3a";
      ctx.lineWidth = 5;
      ctx.beginPath();
      ctx.ellipse(480, 275, 430, 205, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Outer Guilloche Pattern Dots
      ctx.fillStyle = "#8a6624";
      for (let a = 0; a < 48; a++) {
        const ra = (a * Math.PI * 2) / 48;
        ctx.beginPath();
        ctx.arc(480 + Math.cos(ra) * 430, 275 + Math.sin(ra) * 205, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }

      // Warm Boardroom Spotlight over Central Turntable Floor
      const spotGrad = ctx.createRadialGradient(480, 275, 20, 480, 275, 340);
      spotGrad.addColorStop(0, "rgba(255, 220, 140, 0.18)");
      spotGrad.addColorStop(0.7, "rgba(255, 190, 80, 0.05)");
      spotGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
      ctx.fillStyle = spotGrad;
      ctx.beginPath();
      ctx.ellipse(480, 275, 370, 175, 0, 0, Math.PI * 2);
      ctx.fill();

      // Inner Polished Oak Oval
      ctx.fillStyle = "#3e2012";
      ctx.beginPath();
      ctx.ellipse(480, 275, 360, 165, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#805828";
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Central Golden TMF Medallion Inlaid in Floor
      ctx.save();
      ctx.translate(480, 275);
      ctx.fillStyle = "rgba(176, 138, 60, 0.28)";
      ctx.beginPath();
      ctx.ellipse(0, 0, 200, 88, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "rgba(212, 175, 55, 0.65)";
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // TMF Compass Compass Rose Star
      ctx.fillStyle = "rgba(212, 175, 55, 0.4)";
      for (let s = 0; s < 8; s++) {
        const sa = (s * Math.PI * 2) / 8;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(sa) * 170, Math.sin(sa) * 72);
        ctx.lineTo(Math.cos(sa + 0.22) * 55, Math.sin(sa + 0.22) * 24);
        ctx.closePath();
        ctx.fill();
      }
      ctx.restore();

      // 2. Animated 1987 Corporate Phonograph Turntable in Upper-Left Corner
      drawCornerPhonograph(85, 75, now);"""

idx_a_start = text.find(old_draw_arena_start)
idx_a_end = text.find(old_draw_arena_end)
if idx_a_start != -1 and idx_a_end != -1:
    text = text[:idx_a_start] + new_draw_arena + text[idx_a_end + len(old_draw_arena_end):]
    print("Replaced arena background rendering with luxury boardroom marquetry!")

# 3. Dynamic Walking and Running Movement Animation in Musical Chairs
old_anim_contender = """    // DRAW CUSTOM ANIMATED CONTENDER (Walking limbs, briefcase, seated posture)
    function drawAnimatedContender(id, x, y, isWalking, now) {
      const c = arenaContenders[id];
      if (!c) return;

      ctx.save();
      ctx.translate(x, y);

      const walkBob = isWalking ? Math.abs(Math.sin(now / 115 + id * 2)) * 5 : 0;
      const legCycle = isWalking ? Math.sin(now / 115 + id * 2) * 12 : 0;

      // Legs
      ctx.fillStyle = (id === 0 ? "#1b212c" : "#241913");
      ctx.lineWidth = 5;
      ctx.lineCap = "round";

      // Left leg
      ctx.beginPath();
      ctx.moveTo(-6, -18);
      ctx.lineTo(-6 - legCycle * 0.7, 0);
      ctx.stroke();

      // Right leg
      ctx.beginPath();
      ctx.moveTo(6, -18);
      ctx.lineTo(6 + legCycle * 0.7, 0);
      ctx.stroke();

      // Body Torso
      ctx.fillStyle = c.color;
      ctx.fillRect(-12, -42 - walkBob, 24, 26);

      // Shirt collar & tie
      ctx.fillStyle = "#fff";
      ctx.fillRect(-4, -42 - walkBob, 8, 8);
      ctx.fillStyle = (id === 0 ? "#7a2e2e" : "#b08a3c");
      ctx.fillRect(-2, -38 - walkBob, 4, 12);

      // Suit jacket lapels
      ctx.strokeStyle = "rgba(0,0,0,0.3)";
      ctx.lineWidth = 2;
      ctx.strokeRect(-12, -42 - walkBob, 24, 26);"""

new_anim_contender = """    // DRAW CUSTOM ANIMATED CONTENDER (Walking limbs, briefcase, seated posture)
    function drawAnimatedContender(id, x, y, isWalking, now) {
      const c = arenaContenders[id];
      if (!c) return;

      ctx.save();
      ctx.translate(x, y);

      // Natural rhythmic stepping animation with arm swings and head bob
      const stepFreq = (arenaPhase === 'green' ? 100 : 130);
      const walkBob = isWalking ? Math.abs(Math.sin(now / stepFreq + id * Math.PI)) * 6 : 0;
      const legCycle = isWalking ? Math.sin(now / stepFreq + id * Math.PI) * 15 : 0;
      const armCycle = isWalking ? Math.cos(now / stepFreq + id * Math.PI) * 12 : 0;

      // Natural drop shadow under character
      ctx.fillStyle = "rgba(10, 6, 4, 0.45)";
      ctx.beginPath();
      ctx.ellipse(0, 2, 18, 6, 0, 0, Math.PI * 2);
      ctx.fill();

      // Legs with joint movement
      ctx.strokeStyle = (id === 0 ? "#1b212c" : (c.pantsColor || "#241913"));
      ctx.lineWidth = 5.5;
      ctx.lineCap = "round";

      // Left leg
      ctx.beginPath();
      ctx.moveTo(-7, -18);
      ctx.lineTo(-7 - legCycle * 0.75, 1);
      ctx.stroke();

      // Right leg
      ctx.beginPath();
      ctx.moveTo(7, -18);
      ctx.lineTo(7 + legCycle * 0.75, 1);
      ctx.stroke();

      // Shoes
      ctx.fillStyle = "#111116";
      ctx.fillRect(-11 - legCycle * 0.75, 0, 9, 4);
      ctx.fillRect(3 + legCycle * 0.75, 0, 9, 4);

      // Left arm (swinging backwards/forwards opposite to legs)
      ctx.strokeStyle = c.color;
      ctx.lineWidth = 4.5;
      ctx.beginPath();
      ctx.moveTo(-13, -38 - walkBob);
      ctx.lineTo(-15 + armCycle * 0.6, -22 - walkBob);
      ctx.stroke();

      // Body Torso
      ctx.fillStyle = c.color;
      ctx.fillRect(-13, -42 - walkBob, 26, 26);

      // Shirt collar & tie
      ctx.fillStyle = "#fff";
      ctx.fillRect(-4, -42 - walkBob, 8, 8);
      ctx.fillStyle = (id === 0 ? "#7a2e2e" : (c.tieColor || "#b08a3c"));
      ctx.fillRect(-2, -38 - walkBob, 4, 13);

      // Suit jacket lapels
      ctx.strokeStyle = "rgba(0,0,0,0.35)";
      ctx.lineWidth = 1.5;
      ctx.strokeRect(-13, -42 - walkBob, 26, 26);

      // Right arm (holding briefcase)
      ctx.strokeStyle = c.color;
      ctx.lineWidth = 4.5;
      ctx.beginPath();
      ctx.moveTo(13, -38 - walkBob);
      ctx.lineTo(15 - armCycle * 0.6, -22 - walkBob);
      ctx.stroke();"""

if old_anim_contender in text:
    text = text.replace(old_anim_contender, new_anim_contender)
    print("Upgraded 2D contender walking/running animations!")

# 4. Exact tmforgchart.xyz Certificate Engine
# Matches the guilloche waves, department rosettes, oval gold ring portrait,
# authentic typography, employee numbering, and floor progression!
old_cert_code_start = "    function renderEngravedCertificate() {"
old_cert_code_end = "      g.fillText(\"MANAGING DIRECTOR (FLOOR 6)\", 440, sigY + 16);\n      g.fillText(\"THE CHAIRMAN (SEAT 0)\", 840, sigY + 16);\n    }"

new_cert_code = """    function renderEngravedCertificate() {
      const W = 1200, H = 675;
      certCanvas.width = W;
      certCanvas.height = H;
      const g = certCanvas.getContext('2d');

      const PAPER = "#f6efe3", INK = "#211b14", MUTED = "#6b5f4e", OX = "#7a2e2e", GOLD = "#b08a3c";
      const dept = DEPARTMENTS[flickerr.deptIndex] || DEPARTMENTS[0];
      const F = dept.color;
      const CAS = "'Cinzel', 'Libre Caslon Text', Georgia, serif";
      const SER = "'Libre Caslon Text', Georgia, serif";
      const MON = "'IBM Plex Mono', Menlo, monospace";

      // 1. Warm Intaglio Paper Surface
      g.fillStyle = PAPER;
      g.fillRect(0, 0, W, H);

      // Delicate Paper Grain Texture
      for (let i = 0; i < 4800; i++) {
        g.fillStyle = "rgba(120, 95, 60, " + (Math.random() * 0.045).toFixed(3) + ")";
        g.fillRect(Math.random() * W, Math.random() * H, 1, 1);
      }

      // 2. Official Engraved Double Border
      g.strokeStyle = OX;
      g.lineWidth = 3.5;
      g.strokeRect(22, 22, W - 44, H - 44);

      g.lineWidth = 1.2;
      g.strokeStyle = GOLD;
      g.strokeRect(46, 46, W - 92, H - 92);

      // Guilloche Band: Interleaved waves along all 4 outer margins
      g.strokeStyle = "rgba(122, 46, 46, 0.45)";
      g.lineWidth = 0.9;
      const wave = (horiz, fixed, from, to) => {
        for (const ph of [0, Math.PI]) {
          g.beginPath();
          for (let s = from; s <= to; s += 1.5) {
            const o = Math.sin(s / 3 + ph) * 7;
            if (horiz) {
              s === from ? g.moveTo(s, fixed + o) : g.lineTo(s, fixed + o);
            } else {
              s === from ? g.moveTo(fixed + o, s) : g.lineTo(fixed + o, s);
            }
          }
          g.stroke();
        }
      };
      wave(true, 34, 48, W - 48);
      wave(true, H - 34, 48, W - 48);
      wave(false, 34, 48, H - 48);
      wave(false, W - 34, 48, H - 48);

      // Corner Rosettes in Department Colors
      for (const [rx, ry] of [[34, 34], [W - 34, 34], [34, H - 34], [W - 34, H - 34]]) {
        g.beginPath();
        g.arc(rx, ry, 10, 0, Math.PI * 2);
        g.fillStyle = F;
        g.fill();
        g.lineWidth = 1.5;
        g.strokeStyle = OX;
        g.stroke();
      }

      // 3. Header Typography (Matching tmforgchart.xyz)
      g.textAlign = "center";
      g.fillStyle = MUTED;
      g.font = "600 14px " + MON;
      g.fillText("THE MUTUAL FUN · PERSONNEL DEPARTMENT · EST. 1987", W / 2, 88);

      g.fillStyle = INK;
      g.font = "700 48px " + CAS;
      g.fillText("Certificate of Employment", W / 2, 145);

      g.strokeStyle = GOLD;
      g.lineWidth = 1.5;
      g.beginPath();
      g.moveTo(W / 2 - 240, 166);
      g.lineTo(W / 2 + 240, 166);
      g.stroke();

      // 4. Portrait in Gold-Ringed Oval
      const ox = 250, oy = 350, rx = 96, ry = 118;
      g.save();
      g.beginPath();
      g.ellipse(ox, oy, rx, ry, 0, 0, Math.PI * 2);
      g.fillStyle = "#ede3cf";
      g.fill();
      g.clip();

      const memberImg = new Image();
      memberImg.src = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      if (memberImg.complete && memberImg.naturalWidth) {
        const s = Math.max((rx * 2) / memberImg.naturalWidth, (ry * 2) / memberImg.naturalHeight);
        g.drawImage(memberImg, ox - (memberImg.naturalWidth * s) / 2, oy - (memberImg.naturalHeight * s) / 2, memberImg.naturalWidth * s, memberImg.naturalHeight * s);
      } else {
        g.fillStyle = MUTED;
        g.font = "700 80px " + CAS;
        g.fillText("Y", ox, oy + 28);
      }
      g.restore();

      g.lineWidth = 4;
      g.strokeStyle = GOLD;
      g.beginPath();
      g.ellipse(ox, oy, rx + 5, ry + 5, 0, 0, Math.PI * 2);
      g.stroke();

      g.lineWidth = 1.2;
      g.strokeStyle = OX;
      g.beginPath();
      g.ellipse(ox, oy, rx + 11, ry + 11, 0, 0, Math.PI * 2);
      g.stroke();

      // 5. Official Instrument Certifications & Dynamic Role
      const tx = 720;
      g.textAlign = "center";
      g.fillStyle = MUTED;
      g.font = "italic 400 22px " + SER;
      g.fillText("This certifies that", tx, 228);

      g.fillStyle = INK;
      g.font = "700 50px " + CAS;
      g.fillText("YOU", tx, 285);

      g.fillStyle = MUTED;
      g.font = "italic 400 22px " + SER;
      g.fillText("holds lawful title and chair occupancy of", tx, 332);

      g.fillStyle = OX;
      g.font = "700 42px " + CAS;
      g.fillText(flickerr.role.toUpperCase(), tx, 385);

      g.fillStyle = MUTED;
      g.font = "italic 400 20px " + SER;
      g.fillText("in the department of", tx, 428);

      g.fillStyle = F;
      g.font = "700 32px " + CAS;
      g.fillText("The " + flickerr.department + " Fund", tx, 470);

      // 6. Security Ledger Line & Employee Stats
      g.strokeStyle = GOLD;
      g.lineWidth = 1.2;
      g.beginPath();
      g.moveTo(90, 515);
      g.lineTo(W - 90, 515);
      g.stroke();

      g.fillStyle = INK;
      g.font = "500 14px " + MON;
      const floorStr = currentFloor === 0 ? "GROUND LOBBY" : `FLOOR ${currentFloor} OF 9`;
      g.fillText(`EMPLOYEE No. 0401   ·   ${floorStr}   ·   TITLE: ${flickerr.chairName.toUpperCase()}   ·   REVIEW PTS: ${flickerr.reviewScore}`, W / 2, 542);

      // 7. Official Signatures and Wax Seal
      g.textAlign = "left";
      g.fillStyle = INK;
      g.font = "italic 400 24px " + CAS;
      g.fillText("what3verman", 108, 584);
      g.strokeStyle = INK;
      g.lineWidth = 0.8;
      g.beginPath();
      g.moveTo(104, 592);
      g.lineTo(320, 592);
      g.stroke();

      g.fillStyle = MUTED;
      g.font = "400 12px " + MON;
      g.fillText("Managing Director · Executive Floor 6", 104, 610);

      // Official Personnel Wax Seal
      const sx = W - 150, sy = 582;
      g.beginPath();
      g.arc(sx, sy, 36, 0, Math.PI * 2);
      g.fillStyle = OX;
      g.fill();
      g.beginPath();
      g.arc(sx, sy, 30, 0, Math.PI * 2);
      g.strokeStyle = "rgba(246,239,227,0.85)";
      g.lineWidth = 1.5;
      g.stroke();

      g.fillStyle = PAPER;
      g.textAlign = "center";
      g.font = "700 10px " + CAS;
      g.fillText("SEAT 0", sx, sy - 2);
      g.font = "500 10px " + MON;
      g.fillText("OFFICIAL", sx, sy + 13);
    }"""

idx_c_start = text.find(old_cert_code_start)
idx_c_end = text.find(old_cert_code_end)
if idx_c_start != -1 and idx_c_end != -1:
    text = text[:idx_c_start] + new_cert_code + text[idx_c_end + len(old_cert_code_end):]
    print("Replaced certificate renderer with exact tmforgchart.xyz engraved certificate!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated index.html with all requested features!")
