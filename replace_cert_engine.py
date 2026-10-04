with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function renderEngravedCertificate()')
end = text.find('function downloadCert()', start)

new_cert_func = """function renderEngravedCertificate() {
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

      // 2. Official Engraved Double Border (Matching tmforgchart.xyz)
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

      // 3. Header Typography
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
    }
    """

assert start != -1 and end != -1, "Boundaries not found"
text = text[:start] + new_cert_func + text[end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully replaced renderEngravedCertificate with authentic tmforgchart.xyz implementation!")
