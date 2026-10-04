# -*- coding: utf-8 -*-
import json
import os

print("Building complete The Mutual Fun: Flickerr's 3D Office Odyssey...")

with open('assets_encoded.json', 'r', encoding='utf-8') as f:
    assets = json.load(f)

print(f"Loaded {len(assets)} assets from cache.")

# We will write out the full index.html file
html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Mutual Fun: Flickerr's 3D Office Odyssey (1987)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <script src="three.min.js"></script>
  <style>
    :root {
      --paper: #F6EFE3;
      --paper-raised: #FDF8EE;
      --paper-sunken: #EDE3CF;
      --ink: #211B14;
      --ink-muted: #6B5F4E;
      --rule: #D8CCB4;
      --oxblood: #7A2E2E;
      --gold: #B08A3C;
      --lamp: #2F6B3D;
      --argon: #5b8ac2;
      --bogle: #57a671;
      --smaug: #c97258;
      --midas: #d19a19;
      --vladd: #977bc4;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #120e0a;
      font-family: 'Source Serif 4', Georgia, serif;
      color: var(--ink);
    }

    #gameCanvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
    }

    .vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 2;
      box-shadow: inset 0 0 120px rgba(10, 7, 5, 0.75), inset 0 0 40px rgba(0, 0, 0, 0.9);
    }

    /* Top HUD */
    .top-hud {
      position: absolute;
      top: 14px;
      left: 18px;
      right: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
      pointer-events: none;
      gap: 12px;
    }

    .brass-badge {
      pointer-events: auto;
      background: linear-gradient(180deg, #ede3cf 0%, #dfd3bd 100%);
      border: 2px solid #5a422e;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5), inset 0 1px 0 #fff;
      padding: 6px 14px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .brass-badge h1 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--oxblood);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      line-height: 1.1;
    }

    .brass-badge span {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 9px;
      color: var(--ink-muted);
      letter-spacing: 0.8px;
      display: block;
    }

    .status-ribbon {
      pointer-events: auto;
      background: rgba(22, 16, 12, 0.92);
      border: 1px solid #4a3626;
      box-shadow: 0 4px 14px rgba(0,0,0,0.6);
      padding: 6px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: #dfd3bd;
      border-radius: 4px;
      flex-wrap: wrap;
    }

    .character-pill {
      background: var(--oxblood);
      color: #fff;
      padding: 2px 7px;
      font-weight: 700;
      font-size: 10px;
      letter-spacing: 1px;
      border-radius: 2px;
    }

    .dept-pill {
      background: var(--bogle);
      color: #fff;
      padding: 2px 7px;
      font-weight: 700;
      font-size: 10px;
      letter-spacing: 0.5px;
      border-radius: 2px;
    }

    .hud-btn {
      background: #2a1e16;
      border: 1px solid #5c422f;
      color: #e5c178;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      padding: 3px 8px;
      cursor: pointer;
      border-radius: 2px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.15s ease;
    }

    .hud-btn:hover {
      background: #422f22;
      border-color: #d4af37;
      color: #fff;
    }

    .floor-indicator {
      position: absolute;
      top: 68px;
      left: 18px;
      background: rgba(22, 16, 12, 0.9);
      border: 1px solid #4a3626;
      padding: 4px 12px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: #e5c178;
      z-index: 10;
      pointer-events: none;
    }

    /* Floating Interaction Prompt */
    .interact-prompt {
      position: absolute;
      bottom: 70px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(246, 239, 227, 0.96);
      border: 2px solid var(--ink);
      box-shadow: 0 6px 20px rgba(0,0,0,0.6);
      padding: 8px 22px;
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--oxblood);
      z-index: 20;
      display: none;
      animation: pulsePrompt 1.2s infinite;
      letter-spacing: 1px;
      text-transform: uppercase;
      pointer-events: none;
    }

    @keyframes pulsePrompt {
      0%, 100% { transform: translateX(-50%) scale(1); }
      50% { transform: translateX(-50%) scale(1.04); }
    }

    /* Controls Guide */
    .controls-guide {
      position: absolute;
      bottom: 14px;
      left: 18px;
      background: rgba(18, 13, 10, 0.88);
      border: 1px solid #33261c;
      padding: 6px 12px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: #9d8b76;
      z-index: 10;
      pointer-events: none;
    }
    .controls-guide b { color: #e5c178; }

    /* Bottom Ticker */
    .bottom-ticker {
      position: absolute;
      bottom: 14px;
      right: 18px;
      background: rgba(18, 13, 10, 0.88);
      border: 1px solid #33261c;
      padding: 6px 12px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: #c9a86a;
      z-index: 10;
      pointer-events: none;
      max-width: 520px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Standard Modal Sheet */
    .modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(10, 7, 5, 0.88);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 50;
      padding: 20px;
    }
    .modal-overlay.active { display: flex; }

    .modal-paper-sheet {
      background: var(--paper);
      border: 3px solid var(--ink);
      max-width: 640px;
      width: 100%;
      padding: 24px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      position: relative;
      background-image: repeating-linear-gradient(0deg, transparent, transparent 23px, rgba(216, 204, 180, 0.3) 24px);
      max-height: 90vh;
      overflow-y: auto;
    }

    .modal-header-row {
      display: flex;
      justify-content: space-between;
      border-bottom: 2px solid var(--ink);
      padding-bottom: 6px;
      margin-bottom: 12px;
      align-items: baseline;
    }

    .modal-header-row h3 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 18px;
      color: var(--oxblood);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 1px;
    }

    .modal-instruction-box {
      background: var(--paper-sunken);
      border: 1px solid var(--rule);
      padding: 8px 12px;
      border-left: 3px solid var(--oxblood);
      font-size: 12px;
      line-height: 1.45;
      margin-bottom: 14px;
    }

    .desk-button {
      background: var(--oxblood);
      color: #fff;
      border: 1px solid var(--ink);
      padding: 8px 14px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 2px 2px 0 var(--ink);
      transition: all 0.1s ease;
      display: inline-block;
      text-align: center;
    }

    .desk-button:hover {
      transform: translate(-1px, -1px);
      box-shadow: 3px 3px 0 var(--ink);
      filter: brightness(1.08);
    }

    .desk-button:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0 var(--ink);
    }

    .desk-button.secondary {
      background: var(--paper-raised);
      color: var(--ink);
      border: 1px solid var(--rule);
      box-shadow: 2px 2px 0 var(--rule);
    }

    /* In-game Memorandum Toast */
    .memo-toast {
      position: absolute;
      top: 70px;
      left: 50%;
      transform: translateX(-50%) translateY(-150px);
      background: var(--paper-raised);
      border: 2px solid var(--ink);
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      padding: 12px 24px;
      border-left: 6px solid var(--oxblood);
      z-index: 60;
      transition: transform 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28);
      max-width: 540px;
      width: 90%;
      text-align: center;
      pointer-events: none;
    }
    .memo-toast.show {
      transform: translateX(-50%) translateY(0);
    }
    .memo-toast-title {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: var(--oxblood);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 4px;
    }
    .memo-toast-body {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 13px;
      color: var(--ink);
      line-height: 1.4;
    }

    /* Musical Chairs Fight Arena Modal */
    .musical-arena-overlay {
      position: absolute;
      inset: 0;
      background: rgba(8, 5, 4, 0.94);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 65;
      padding: 20px;
    }
    .musical-arena-overlay.active { display: flex; }

    .arena-box {
      background: var(--paper-raised);
      border: 4px solid var(--ink);
      box-shadow: 0 25px 60px rgba(0,0,0,0.9);
      max-width: 620px;
      width: 100%;
      padding: 26px;
      text-align: center;
      position: relative;
    }

    .record-spinner {
      width: 90px;
      height: 90px;
      border-radius: 50%;
      background: radial-gradient(circle, #b08a3c 22%, #1a120c 24%, #2c1e14 60%, #110b06 100%);
      margin: 12px auto;
      border: 3px solid #6b5f4e;
      position: relative;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .record-spinner.spinning {
      animation: spinRecord 1.8s linear infinite;
    }
    @keyframes spinRecord {
      100% { transform: rotate(360deg); }
    }

    .turntable-needle {
      position: absolute;
      top: -10px;
      right: -10px;
      width: 4px;
      height: 48px;
      background: #b08a3c;
      transform-origin: top right;
      transform: rotate(25deg);
      border-radius: 2px;
    }

    .arena-status-badge {
      display: inline-block;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 14px;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 12px;
    }
    .arena-status-badge.waiting {
      background: #ede3cf;
      color: #6b5f4e;
      border: 1px solid #bfaea0;
    }
    .arena-status-badge.active {
      background: #7a2e2e;
      color: #fff;
      animation: pulseActive 0.6s infinite alternate;
    }
    @keyframes pulseActive {
      0% { transform: scale(1); }
      100% { transform: scale(1.08); }
    }

    .arena-rival-row {
      display: flex;
      justify-content: space-around;
      align-items: center;
      margin: 16px 0;
      padding: 12px;
      background: #faf4e8;
      border: 1px solid var(--rule);
    }

    .fighter-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }
    .fighter-img {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 2px solid var(--ink);
      object-fit: cover;
    }

    .sit-action-btn {
      width: 100%;
      padding: 16px;
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      border: 3px solid var(--ink);
      cursor: pointer;
      transition: all 0.1s ease;
      box-shadow: 0 6px 0 var(--ink);
    }
    .sit-action-btn.disabled {
      background: #ccc;
      color: #777;
      cursor: not-allowed;
      box-shadow: none;
    }
    .sit-action-btn.ready {
      background: #2f6b3d;
      color: #fff;
      animation: flashBtn 0.4s infinite alternate;
    }
    @keyframes flashBtn {
      0% { background: #2f6b3d; }
      100% { background: #409153; }
    }

    /* Certificate Modal */
    .cert-modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(10, 7, 5, 0.94);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 70;
      padding: 20px;
      overflow-y: auto;
    }
    .cert-modal-overlay.active { display: flex; }

    .cert-container {
      max-width: 820px;
      width: 100%;
      text-align: center;
    }

    #certCanvas {
      max-width: 100%;
      height: auto;
      box-shadow: 0 25px 60px rgba(0,0,0,0.9);
      border: 4px solid #1a120b;
      display: block;
      margin: 0 auto 16px auto;
    }

    /* Elevator Concourse Modal */
    .elevator-grid {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 14px 0;
    }

    .elevator-floor-btn {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 9px 14px;
      background: var(--paper-raised);
      border: 1px solid var(--rule);
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .elevator-floor-btn:hover {
      border-color: var(--ink);
      background: #fff;
      box-shadow: 2px 2px 0 var(--ink);
    }

    .elevator-floor-btn.locked {
      opacity: 0.4;
      cursor: not-allowed;
      background: #ece3d3;
    }

    .elevator-floor-btn.current {
      border-left: 5px solid var(--oxblood);
      font-weight: 700;
      background: #faf4e8;
    }
  </style>
</head>
<body>

  <!-- 3D Canvas -->
  <canvas id="gameCanvas"></canvas>
  <div class="vignette"></div>

  <!-- Top HUD -->
  <div class="top-hud">
    <div class="brass-badge">
      <img id="hudMedallion" style="width:28px;height:28px;object-fit:contain;" alt="Seal">
      <div>
        <h1>The Mutual Fun</h1>
        <span>ORGANIZATION LADDER · 1987</span>
      </div>
    </div>

    <div class="status-ribbon">
      <span class="character-pill">FLICKERR</span>
      <span class="dept-pill" id="hudDept">The Bogle Fund</span>
      <span>Rank: <b id="hudRank">Floor 0 · Pavement</b></span>
      <span>Chair: <b id="hudChair">The Pavement</b></span>
      <span>Postage: <b id="hudPostage">0.000 ETH</b></span>
      <span>Deng: <b id="hudDeng">0.00</b></span>
      <span>$TMF: <b id="hudTmf">0</b></span>
      <button class="hud-btn" onclick="openCertModal()">📜 Certificate</button>
      <button class="hud-btn" onclick="saveGame(true)">💾 Save Ledger</button>
      <button class="hud-btn" onclick="confirmResetGame()">🔄 Reset</button>
    </div>
  </div>

  <div class="floor-indicator" id="floorIndicatorText">
    CURRENT LEVEL: OUTSIDE HEADQUARTERS · SEEK GATE ENTRY
  </div>

  <!-- Proximity Interaction Badge -->
  <div class="interact-prompt" id="interactPrompt">
    [E] Interact
  </div>

  <!-- Controls Guide -->
  <div class="controls-guide">
    <b>WASD / ARROWS:</b> Walk · <b>[E] / SPACE:</b> Interact / Seat Action · <b>Q / E:</b> Orbit Camera
  </div>

  <!-- Bottom Ticker -->
  <div class="bottom-ticker" id="tickerText">
    LOBBY TICKER: FLICKERR ARRIVES AT WALL STREET HEADQUARTERS.
  </div>

  <!-- In-Game Memorandum Notification Toast -->
  <div class="memo-toast" id="memoToast">
    <div class="memo-toast-title" id="memoToastTitle">INTERNAL MEMORANDUM</div>
    <div class="memo-toast-body" id="memoToastBody">House instructions updated.</div>
  </div>

  <!-- General Task Interaction Modal -->
  <div class="modal-overlay" id="taskModal">
    <div class="modal-paper-sheet">
      <div class="modal-header-row">
        <h3 id="modalTitle">Station Title</h3>
        <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--ink-muted);" id="modalBadge">OFFICIAL DESK</span>
      </div>

      <div class="modal-instruction-box" id="modalInstructions">
        Instructions go here.
      </div>

      <div id="modalBody">
        <!-- Content injected dynamically -->
      </div>

      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:16px;">
        <button class="desk-button secondary" onclick="closeTaskModal()">Step Back</button>
      </div>
    </div>
  </div>

  <!-- Musical Chairs Arena Modal -->
  <div class="musical-arena-overlay" id="arenaModal">
    <div class="arena-box">
      <div class="modal-header-row">
        <h3 id="arenaTitle">CHAIR CONTEST</h3>
        <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--oxblood);font-weight:700;">1987 MUSICAL CHAIRS</span>
      </div>

      <p style="font-size:12px;color:var(--ink-muted);margin-bottom:8px;">
        Circle the chair while the corporate phonograph plays. When the needle cuts and the bell tolls, seize the seat before your rival!
      </p>

      <div class="record-spinner" id="recordSpinner">
        <div class="turntable-needle"></div>
      </div>

      <div class="arena-status-badge waiting" id="arenaStatus">Phonograph Spinning...</div>

      <div class="arena-rival-row">
        <div class="fighter-card">
          <div style="font-family:'IBM Plex Mono';font-size:11px;font-weight:700;">FLICKERR</div>
          <div style="font-size:10px;color:var(--ink-muted);">Applicant / Aspirant</div>
        </div>
        <div style="font-family:'Libre Caslon Text';font-size:20px;font-weight:700;color:var(--oxblood);font-style:italic;">
          VS
        </div>
        <div class="fighter-card">
          <img id="rivalImg" class="fighter-img" alt="Rival">
          <div style="font-family:'IBM Plex Mono';font-size:11px;font-weight:700;" id="rivalName">Rival Clerk</div>
          <div style="font-size:10px;color:var(--ink-muted);" id="rivalRole">Contender</div>
        </div>
      </div>

      <button class="sit-action-btn disabled" id="sitBtn" onclick="onPlayerSitAction()">
        WAIT FOR THE BELL...
      </button>

      <div style="margin-top:14px;">
        <button class="desk-button secondary" onclick="closeArenaModal()">Concede Contest</button>
      </div>
    </div>
  </div>

  <!-- Certificate of Employment Modal (tmforgchart.xyz) -->
  <div class="cert-modal-overlay" id="certModal">
    <div class="cert-container">
      <canvas id="certCanvas" width="1200" height="675"></canvas>
      <div style="display:flex;justify-content:center;gap:12px;">
        <button class="desk-button" style="background:var(--lamp);padding:10px 20px;" onclick="downloadCert()">📥 Download Official Certificate (PNG)</button>
        <button class="desk-button secondary" onclick="closeCertModal()">Close Registry</button>
      </div>
    </div>
  </div>

  <!-- Script for 3D Game Engine -->
  <script>
    const ASSETS = __ASSETS_JSON__;

    // Set HUD medallion
    if (ASSETS.medallion) {
      document.getElementById('hudMedallion').src = ASSETS.medallion;
    }

    // WEB AUDIO SYNTHESIZER
    let audioCtx = null;
    let audioEnabled = true;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function playStampThump() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(95, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(26, audioCtx.currentTime + 0.28);
        gain.gain.setValueAtTime(0.85, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.38);
      } catch(e) {}
    }

    function playClick() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.06);
      } catch(e) {}
    }

    function playStep() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const bSize = audioCtx.sampleRate * 0.04;
        const b = audioCtx.createBuffer(1, bSize, audioCtx.sampleRate);
        const d = b.getChannelData(0);
        for (let i = 0; i < bSize; i++) d[i] = (Math.random() * 2 - 1) * 0.05;
        const n = audioCtx.createBufferSource();
        n.buffer = b;
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(600, audioCtx.currentTime);
        n.connect(filter);
        filter.connect(audioCtx.destination);
        n.start();
      } catch(e) {}
    }

    function playElevatorDing() {
      if (!audioEnabled) return;
      initAudio();
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.2);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 1.3);
      } catch(e) {}
    }

    function playBell() {
      if (!audioEnabled) return;
      initAudio();
      try {
        [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.12);
          gain.gain.setValueAtTime(0.35, audioCtx.currentTime + idx * 0.12);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + idx * 0.12 + 1.8);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.12);
          osc.stop(audioCtx.currentTime + idx * 0.12 + 1.9);
        });
      } catch(e) {}
    }

    // RHYTHMIC MUSIC TONES FOR MUSICAL CHAIRS
    let musicInterval = null;
    function startMusicalChairsTune() {
      initAudio();
      const notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25];
      let step = 0;
      musicInterval = setInterval(() => {
        try {
          const freq = notes[step % notes.length];
          step = (step + Math.floor(Math.random() * 3) + 1);
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
          gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.22);
          const filter = audioCtx.createBiquadFilter();
          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(1100, audioCtx.currentTime);
          osc.connect(filter);
          filter.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.25);
        } catch(e) {}
      }, 240);
    }

    function stopMusicalChairsTune() {
      if (musicInterval) {
        clearInterval(musicInterval);
        musicInterval = null;
      }
    }

    // GAME STATE & FLICKERR PROGRESSION (MATCHING tmforgchart.xyz)
    const ROLES = [
      { floor: 0, title: "Applicant", minPts: 0, chair: "The Pavement", tier: "Unadmitted" },
      { floor: 1, title: "Intern", minPts: 15, chair: "The Interns Folding Chair", tier: "Class I Intern" },
      { floor: 2, title: "Analyst", minPts: 29, chair: "The Typist Stool", tier: "Class II Analyst" },
      { floor: 3, title: "Associate", minPts: 59, chair: "Creaking Wooden Swivel", tier: "Class III Associate" },
      { floor: 4, title: "Vice President", minPts: 118, chair: "Beige Task Chair", tier: "Class IV Vice President" },
      { floor: 5, title: "Director", minPts: 221, chair: "High-Back Leather Desk Chair", tier: "Class V Director" },
      { floor: 6, title: "Managing Director", minPts: 358, chair: "Green Bankers Chair", tier: "Class VI Managing Director" },
      { floor: 7, title: "Partner", minPts: 592, chair: "Oxblood Wingback Chair", tier: "Class VII Partner" },
      { floor: 8, title: "Board of Directors", minPts: 855, chair: "Board of Directors High Seat", tier: "Class VIII Board Member" },
      { floor: 9, title: "The Chairman", minPts: 1200, chair: "The Gilded Throne & Seat 1", tier: "Class IX Sovereign Trustee" }
    ];

    const DEPARTMENTS = [
      { name: "The Bogle Fund", color: "#57a671" },
      { name: "The Argon Fund", color: "#5b8ac2" },
      { name: "The Smaug Fund", color: "#c97258" },
      { name: "The Midas Fund", color: "#d19a19" },
      { name: "The Vladd Fund", color: "#977bc4" }
    ];

    let currentFloor = 0; // Starts outside on Level 0
    let unlockedFloor = 0;

    let flickerr = {
      empNo: 401,
      department: "The Bogle Fund",
      deptIndex: 0,
      role: "Applicant",
      chairName: "The Pavement",
      chairTier: "Unadmitted",
      postageETH: 0.000,
      dengCredits: 0.0,
      tmfTokens: 0,
      seatsOwned: 0,
      reviewScore: 0,
      postsOnFile: 0,
      hasPass: false,
      gateAdmitted: false,
      chairsWon: []
    };

    // LOCAL STORAGE PROGRESS PERSISTENCE
    const SAVE_KEY = "tmf_odyssey_save_v3";

    function saveGame(showToast = false) {
      try {
        const payload = {
          currentFloor,
          unlockedFloor,
          flickerr
        };
        localStorage.setItem(SAVE_KEY, JSON.stringify(payload));
        if (showToast) {
          showMemoToast("LEDGER SAVED", "Employee dossier persisted to local apparatus storage.");
        }
      } catch(e) {
        console.error("Save error:", e);
      }
    }

    function loadGame() {
      try {
        const raw = localStorage.getItem(SAVE_KEY);
        if (raw) {
          const data = jsonParseSafe(raw);
          if (data && data.flickerr) {
            currentFloor = data.currentFloor || 0;
            unlockedFloor = data.unlockedFloor || 0;
            flickerr = Object.assign(flickerr, data.flickerr);
            console.log("Restored employee file:", flickerr);
            return true;
          }
        }
      } catch(e) {
        console.error("Load error:", e);
      }
      return false;
    }

    function jsonParseSafe(str) {
      try { return JSON.parse(str); } catch(e) { return null; }
    }

    function confirmResetGame() {
      if (confirm("Reset employee file and return to the pavement outside?")) {
        localStorage.removeItem(SAVE_KEY);
        location.reload();
      }
    }

    // THREE.JS SCENE SETUP
    const canvas = document.getElementById('gameCanvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x16100b);
    scene.fog = new THREE.FogExp2(0x16100b, 0.012);

    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, 4.5, 9);

    // BALANCED 1987 LIGHTING
    const hemiLight = new THREE.HemisphereLight(0xfff5e6, 0x4a3222, 0.55);
    scene.add(hemiLight);

    const ambientLight = new THREE.AmbientLight(0xffeedd, 0.45);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xfffae6, 0.75);
    dirLight.position.set(8, 16, 8);
    dirLight.castShadow = true;
    scene.add(dirLight);

    // FLICKERR 3D CHARACTER GROUP
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // Suited character mesh
    const suitMat = new THREE.MeshLambertMaterial({ color: 0x2b221b }); // Charcoal suit
    const shirtMat = new THREE.MeshLambertMaterial({ color: 0xf6efe3 }); // Cream shirt
    const tieMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });   // Oxblood tie
    const skinMat = new THREE.MeshLambertMaterial({ color: 0xd4a373 });  // Face skin
    const hairMat = new THREE.MeshLambertMaterial({ color: 0x1a120c });  // Dark hair
    const leatherMat = new THREE.MeshLambertMaterial({ color: 0x4a2a14 }); // Briefcase leather

    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.75, 0.35), suitMat);
    torso.position.y = 1.0;
    torso.castShadow = true;
    playerGroup.add(torso);

    const tie = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.45, 0.05), tieMat);
    tie.position.set(0, 1.0, 0.18);
    playerGroup.add(tie);

    const head = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.38), skinMat);
    head.position.y = 1.6;
    head.castShadow = true;
    playerGroup.add(head);

    const hair = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.15, 0.4), hairMat);
    hair.position.y = 1.8;
    playerGroup.add(hair);

    const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.65, 0.22), suitMat);
    leftLeg.position.set(-0.16, 0.35, 0);
    leftLeg.castShadow = true;
    playerGroup.add(leftLeg);

    const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.65, 0.22), suitMat);
    rightLeg.position.set(0.16, 0.35, 0);
    rightLeg.castShadow = true;
    playerGroup.add(rightLeg);

    const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.6, 0.18), suitMat);
    leftArm.position.set(-0.4, 0.95, 0);
    leftArm.castShadow = true;
    playerGroup.add(leftArm);

    const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.6, 0.18), suitMat);
    rightArm.position.set(0.4, 0.95, 0);
    rightArm.castShadow = true;
    playerGroup.add(rightArm);

    const briefcase = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.38, 0.48), leatherMat);
    briefcase.position.set(0.48, 0.65, 0);
    briefcase.castShadow = true;
    playerGroup.add(briefcase);

    playerGroup.position.set(0, 0, 5);

    // INTERACTIVE ROOM ENVIRONMENT REGISTRY
    let interactiveObjects = [];
    let roomGroup = new THREE.Group();
    scene.add(roomGroup);

    function loadTextureB64(b64) {
      if (!b64) return null;
      const img = new Image();
      img.src = b64;
      const tex = new THREE.Texture(img);
      img.onload = () => { tex.needsUpdate = true; };
      tex.magFilter = THREE.NearestFilter;
      tex.minFilter = THREE.NearestFilter;
      return tex;
    }

    const bossTexWhat3verman = loadTextureB64(ASSETS.boss_what3verman);
    const bossTexKingpickle = loadTextureB64(ASSETS.boss_kingpickle);

    // REBUILD 3D ENVIRONMENT FOR CURRENT FLOOR
    function buildFloorEnvironment() {
      while(roomGroup.children.length > 0) {
        roomGroup.remove(roomGroup.children[0]);
      }
      interactiveObjects = [];

      if (currentFloor === 0) {
        buildExteriorStreet();
      } else {
        buildInteriorOfficeFloor();
      }

      updateTicker(`Flickerr stepped onto ${getFloorName(currentFloor)}.`);
    }

    // 0. EXTERIOR STREET & SECURITY GATE
    function buildExteriorStreet() {
      // Asphalt street & stone sidewalk
      const streetGeo = new THREE.PlaneGeometry(32, 16);
      const streetMat = new THREE.MeshLambertMaterial({ color: 0x1f1f22 });
      const street = new THREE.Mesh(streetGeo, streetMat);
      street.rotation.x = -Math.PI / 2;
      street.position.set(0, 0, 5);
      street.receiveShadow = true;
      roomGroup.add(street);

      const sidewalkGeo = new THREE.BoxGeometry(32, 0.2, 10);
      const sidewalkMat = new THREE.MeshLambertMaterial({ color: 0x48423b });
      const sidewalk = new THREE.Mesh(sidewalkGeo, sidewalkMat);
      sidewalk.position.set(0, 0.1, -4);
      sidewalk.receiveShadow = true;
      roomGroup.add(sidewalk);

      // Imposing 1987 Granite Building Facade
      const facadeMat = new THREE.MeshLambertMaterial({ color: 0x362c23 });
      const facade = new THREE.Mesh(new THREE.BoxGeometry(32, 8, 1.2), facadeMat);
      facade.position.set(0, 4, -9.5);
      roomGroup.add(facade);

      // Building brass nameplate architrave
      const archMat = new THREE.MeshStandardMaterial({ color: 0xb08a3c, metalness: 0.8, roughness: 0.3 });
      const arch = new THREE.Mesh(new THREE.BoxGeometry(10, 0.8, 0.3), archMat);
      arch.position.set(0, 5.2, -8.8);
      roomGroup.add(arch);

      // Gate pillars with brass globes
      const pillarMat = new THREE.MeshLambertMaterial({ color: 0x221a14 });
      for (let x of [-3.5, 3.5]) {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(0.9, 4.5, 0.9), pillarMat);
        pil.position.set(x, 2.25, -6.5);
        roomGroup.add(pil);

        const globe = new THREE.Mesh(new THREE.SphereGeometry(0.25, 16, 16), archMat);
        globe.position.set(x, 4.6, -6.5);
        roomGroup.add(globe);
      }

      // Wrought iron gate
      const ironMat = new THREE.MeshStandardMaterial({ color: 0x181818, metalness: 0.9 });
      for (let x = -3.2; x <= 3.2; x += 0.4) {
        if (Math.abs(x) < 1.0) continue; // Walkway gap
        const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 3.2), ironMat);
        bar.position.set(x, 1.6, -6.5);
        roomGroup.add(bar);
      }

      // Streetlamp with warm yellow pool of light
      const lampPost = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 4.2), ironMat);
      lampPost.position.set(5.5, 2.1, 1.5);
      roomGroup.add(lampPost);

      const lampHead = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.6, 0.5), new THREE.MeshBasicMaterial({ color: 0xffea88 }));
      lampHead.position.set(5.5, 4.2, 1.5);
      roomGroup.add(lampHead);

      const streetLight = new THREE.PointLight(0xffe288, 1.8, 14);
      streetLight.position.set(5.5, 4.0, 1.5);
      roomGroup.add(streetLight);

      // Security Gatekeeper Booth
      const booth = new THREE.Mesh(new THREE.BoxGeometry(2.0, 3.0, 2.0), new THREE.MeshLambertMaterial({ color: 0x2d2218 }));
      booth.position.set(-2.5, 1.5, -4.5);
      roomGroup.add(booth);

      // Gatekeeper interaction
      interactiveObjects.push({
        id: "gatekeeper",
        label: "Present Credentials at Security Gate",
        pos: new THREE.Vector3(0, 0, -4.8),
        radius: 2.5,
        action: openGatekeeperModal
      });
    }

    // INTERIOR OFFICE BUILDING FLOORS (1 to 9)
    function buildInteriorOfficeFloor() {
      // 1. Floor Ground Plane with distinct textures
      let floorColor = 0x442817; // Rich walnut plank
      if (currentFloor === 2) floorColor = 0x4a301d; // Oak parquet
      if (currentFloor === 4) floorColor = 0x522f1d; // Terracotta parquet
      if (currentFloor === 6) floorColor = 0x1a3325; // Deep executive green marble (what3verman)
      if (currentFloor === 7) floorColor = 0x381e18; // Oxblood marble
      if (currentFloor === 8) floorColor = 0x221c17; // Royal dark marble
      if (currentFloor === 9) floorColor = 0x1a3325; // Penthouse green marble

      const floorMat = new THREE.MeshLambertMaterial({ color: floorColor });
      const floorMesh = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), floorMat);
      floorMesh.rotation.x = -Math.PI / 2;
      floorMesh.receiveShadow = true;
      roomGroup.add(floorMesh);

      // Warm overhead chandelier
      const ceilingLight = new THREE.PointLight(0xfff7e8, 0.75, 22);
      ceilingLight.position.set(0, 3.8, 0);
      roomGroup.add(ceilingLight);

      // 2. Architectural Walls with Rich Mahogany Wainscoting
      buildArchitecturalWalls();

      // 3. Elevator Concourse (North Center)
      buildElevatorConcourse();

      // 4. Floor-Specific Furniture, Props & Bosses
      switch(currentFloor) {
        case 1: buildFloor1Intern(); break;
        case 2: buildFloor2Analyst(); break;
        case 3: buildFloor3Associate(); break;
        case 4: buildFloor4VP(); break;
        case 5: buildFloor5Director(); break;
        case 6: buildFloor6MD(); break;
        case 7: buildFloor7Partner(); break;
        case 8: buildFloor8Board(); break;
        case 9: buildFloor9Penthouse(); break;
      }
    }

    // ARCHITECTURAL WALLS WITH TWO-TONE WAINSCOTING & FLUTED PILASTERS
    function buildArchitecturalWalls() {
      const wainscotMat = new THREE.MeshLambertMaterial({ color: 0x341e12 }); // Dark mahogany wainscoting
      const wallMat = new THREE.MeshLambertMaterial({ color: 0xf2ece1 });     // Warm parchment upper wall
      const railMat = new THREE.MeshLambertMaterial({ color: 0x25140b });     // Carved wood moulding trim
      const pilasterMat = new THREE.MeshLambertMaterial({ color: 0x3c2417 }); // Fluted columns

      // North Wall Left
      buildWainscotWallSegment(-7, -10, 11, false, wainscotMat, wallMat, railMat);
      // North Wall Right
      buildWainscotWallSegment(7, -10, 11, false, wainscotMat, wallMat, railMat);
      // North Wall Lintel above elevator
      const lintel = new THREE.Mesh(new THREE.BoxGeometry(4, 0.8, 0.4), wallMat);
      lintel.position.set(0, 3.6, -10);
      roomGroup.add(lintel);

      // West Wall
      buildWainscotWallSegment(-12, 0, 20, true, wainscotMat, wallMat, railMat);
      // East Wall
      buildWainscotWallSegment(12, 0, 20, true, wainscotMat, wallMat, railMat);

      // Pilasters / architectural columns along walls
      for (let x of [-10, -4, 4, 10]) {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(0.5, 4.0, 0.2), pilasterMat);
        pil.position.set(x, 2.0, -9.85);
        roomGroup.add(pil);
      }

      // Hang historical member portraits
      hangFloorPortraits();
    }

    function buildWainscotWallSegment(x, z, length, isSide, wainMat, topMat, railMat) {
      const wGeo = isSide ? new THREE.BoxGeometry(0.4, 1.3, length) : new THREE.BoxGeometry(length, 1.3, 0.4);
      const wMesh = new THREE.Mesh(wGeo, wainMat);
      wMesh.position.set(x, 0.65, z);
      wMesh.receiveShadow = true;
      roomGroup.add(wMesh);

      const rGeo = isSide ? new THREE.BoxGeometry(0.48, 0.12, length) : new THREE.BoxGeometry(length, 0.12, 0.48);
      const rMesh = new THREE.Mesh(rGeo, railMat);
      rMesh.position.set(x, 1.36, z);
      roomGroup.add(rMesh);

      const tGeo = isSide ? new THREE.BoxGeometry(0.4, 2.6, length) : new THREE.BoxGeometry(length, 2.6, 0.4);
      const tMesh = new THREE.Mesh(tGeo, topMat);
      tMesh.position.set(x, 2.7, z);
      tMesh.receiveShadow = true;
      roomGroup.add(tMesh);
    }

    function hangFloorPortraits() {
      const fKeys = ['p_argon_', 'p_bogle_', 'p_smaug_', 'p_midas_', 'p_vladd_'];
      const k1 = fKeys[(currentFloor) % 5] + '1';
      const k2 = fKeys[(currentFloor + 1) % 5] + '1';
      createWallPortrait(-6, 2.4, -9.7, 0, k1);
      createWallPortrait(6, 2.4, -9.7, 0, k2);
    }

    function createWallPortrait(x, y, z, rotY, assetKey) {
      if (!ASSETS[assetKey]) return;
      const group = new THREE.Group();
      const frameMat = new THREE.MeshStandardMaterial({ color: 0xb08a3c, metalness: 0.75, roughness: 0.3 });
      const frame = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1.9, 0.08), frameMat);
      group.add(frame);

      const canvasMat = new THREE.MeshBasicMaterial({ map: loadTextureB64(ASSETS[assetKey]) });
      const canvas = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 1.7), canvasMat);
      canvas.position.z = 0.05;
      group.add(canvas);

      group.position.set(x, y, z);
      group.rotation.y = rotY;
      roomGroup.add(group);
    }

    function buildElevatorConcourse() {
      const elevMat = new THREE.MeshStandardMaterial({ color: 0x9c7a3c, metalness: 0.85, roughness: 0.25 });
      const elevDoors = new THREE.Mesh(new THREE.BoxGeometry(3.5, 3.2, 0.3), elevMat);
      elevDoors.position.set(0, 1.6, -9.9);
      roomGroup.add(elevDoors);

      // Floor indicator light
      const lightMesh = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), new THREE.MeshBasicMaterial({ color: 0xe5c178 }));
      lightMesh.position.set(0, 3.4, -9.8);
      roomGroup.add(lightMesh);

      // Elevator trigger
      interactiveObjects.push({
        id: "elevator",
        label: "Take Elevator to Another Floor",
        pos: new THREE.Vector3(0, 0, -8.5),
        radius: 2.2,
        action: openElevatorModal
      });
    }

    // HELPER: BUILD DESK WITH 1987 GREEN BANKER'S LAMP
    function createDesk(x, y, z, w, d, color) {
      const deskMat = new THREE.MeshLambertMaterial({ color: color });
      const top = new THREE.Mesh(new THREE.BoxGeometry(w, 0.15, d), deskMat);
      top.position.set(x, y + 1.0, z);
      top.castShadow = true;
      roomGroup.add(top);

      for (let dx of [-w/2 + 0.2, w/2 - 0.2]) {
        for (let dz of [-d/2 + 0.2, d/2 - 0.2]) {
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.0, 0.2), deskMat);
          leg.position.set(x + dx, y + 0.5, z + dz);
          roomGroup.add(leg);
        }
      }

      // 1987 Banker's Lamp
      const brassMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.85, roughness: 0.25 });
      const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.05, 12), brassMat);
      lampBase.position.set(x + w * 0.28, y + 1.1, z);
      roomGroup.add(lampBase);

      const lampArm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.35, 8), brassMat);
      lampArm.position.set(x + w * 0.28, y + 1.25, z);
      roomGroup.add(lampArm);

      const lampShade = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.16, 0.3, 12), new THREE.MeshLambertMaterial({ color: 0x1f5c2b }));
      lampShade.rotation.z = Math.PI / 2;
      lampShade.position.set(x + w * 0.28, y + 1.42, z);
      roomGroup.add(lampShade);

      const lampLight = new THREE.PointLight(0xfff2b0, 0.9, 6);
      lampLight.position.set(x + w * 0.28, y + 1.35, z);
      roomGroup.add(lampLight);
    }

    // HELPER: BUILD 3D CHAIR
    function createChair(x, y, z, color) {
      const chairGroup = new THREE.Group();
      const cMat = new THREE.MeshLambertMaterial({ color: color });
      
      const seat = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.1, 0.7), cMat);
      seat.position.y = 0.5;
      chairGroup.add(seat);

      const back = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.8, 0.1), cMat);
      back.position.set(0, 0.9, -0.3);
      chairGroup.add(back);

      const leg = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.12), cMat);
      leg.position.set(0, 0.25, 0);
      chairGroup.add(leg);

      chairGroup.position.set(x, y, z);
      chairGroup.castShadow = true;
      roomGroup.add(chairGroup);
      return chairGroup;
    }

    // 1. FLOOR 1: INTERN (MAILROOM & PNEUMATIC CHUTES)
    function buildFloor1Intern() {
      createDesk(0, 0, 0, 6, 1.6, 0x3d2719);

      // Pneumatic Chutes along West Wall
      const chuteColors = [0x5b8ac2, 0x57a671, 0xc97258, 0xd19a19, 0x977bc4];
      for (let i = 0; i < 5; i++) {
        const cMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 3.2, 16), new THREE.MeshLambertMaterial({ color: chuteColors[i] }));
        cMesh.position.set(-11.5, 1.8, -6 + i * 2.8);
        roomGroup.add(cMesh);
      }

      // Public dispatch lever console
      const consoleMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.1, 1.2), new THREE.MeshLambertMaterial({ color: 0x573e13 }));
      consoleMesh.position.set(7, 0.55, 2);
      roomGroup.add(consoleMesh);

      const lever = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.8), new THREE.MeshLambertMaterial({ color: 0xd4af37 }));
      lever.position.set(7, 1.3, 2);
      lever.rotation.z = 0.3;
      roomGroup.add(lever);

      interactiveObjects.push({
        id: "mailroom_chutes",
        label: "Sort Pneumatic Ticker Memos",
        pos: new THREE.Vector3(0, 0, 1.8),
        radius: 2.5,
        action: openMailroomChuteModal
      });

      interactiveObjects.push({
        id: "public_lever",
        label: "Pull Public Dispatch Lever (+0.010 ETH)",
        pos: new THREE.Vector3(7, 0, 2),
        radius: 2.2,
        action: pullDispatchLever
      });

      // The Intern's Folding Chair (Musical Chairs Fight!)
      createChair(8, 0, -6, 0x6b5f4e);
      interactiveObjects.push({
        id: "chair_intern",
        label: "Musical Chair Fight: Claim Folding Chair (Intern)",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.2,
        action: () => startMusicalChairsContest(1, "The Interns Folding Chair", "Class I Intern", "Intern Biff", ASSETS.p_bogle_1)
      });
    }

    // 2. FLOOR 2: ANALYST (LEDGER FLOOR)
    function buildFloor2Analyst() {
      createDesk(-4, 0, 0, 5, 1.8, 0x422a1b);
      createDesk(4, 0, 0, 5, 1.8, 0x422a1b);

      interactiveObjects.push({
        id: "analyst_calc",
        label: "Rebalance Token Basket Ledger (+15 Pts)",
        pos: new THREE.Vector3(0, 0, 1.8),
        radius: 2.5,
        action: openAnalystLedgerModal
      });

      // Typist Stool (Musical Chairs Fight!)
      createChair(7, 0, -5, 0x7a5835);
      interactiveObjects.push({
        id: "chair_analyst",
        label: "Musical Chair Fight: Claim Typist Stool (Analyst)",
        pos: new THREE.Vector3(7, 0, -5),
        radius: 2.2,
        action: () => startMusicalChairsContest(2, "The Typist Stool", "Class II Analyst", "Analyst Mallow", ASSETS.p_smaug_1)
      });
    }

    // 3. FLOOR 3: ASSOCIATE (DENG DESK & PASS KILN)
    function buildFloor3Associate() {
      createDesk(0, 0, -1, 7, 2.0, 0x4a3222);

      // ApeChain CRT Terminal
      const terminal = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.0, 1.1), new THREE.MeshLambertMaterial({ color: 0x221a14 }));
      terminal.position.set(0, 1.5, -1);
      roomGroup.add(terminal);

      const crtScreen = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.6), new THREE.MeshBasicMaterial({ color: 0x33ff66 }));
      crtScreen.position.set(0, 1.5, -0.44);
      roomGroup.add(crtScreen);

      const terminalLight = new THREE.PointLight(0x33ff66, 1.2, 5);
      terminalLight.position.set(0, 1.6, 0);
      roomGroup.add(terminalLight);

      interactiveObjects.push({
        id: "deng_desk",
        label: "Audit ApeChain Slips & Forge TMF Pass",
        pos: new THREE.Vector3(0, 0, 1.2),
        radius: 2.5,
        action: openDengModal
      });

      // Wooden Swivel Chair (Musical Chairs Fight!)
      createChair(6, 0, 2, 0x7a5835);
      interactiveObjects.push({
        id: "chair_associate",
        label: "Musical Chair Fight: Claim Wooden Swivel (Associate)",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.2,
        action: () => startMusicalChairsContest(3, "Creaking Wooden Swivel", "Class III Associate", "Associate Vance", ASSETS.p_midas_1)
      });
    }

    // 4. FLOOR 4: VICE PRESIDENT (SUBSCRIPTION & ADMISSIONS)
    function buildFloor4VP() {
      createDesk(-6, 0, 0, 4, 1.8, 0x422a1b);
      createDesk(6, 0, 0, 4, 1.8, 0x422a1b);

      const bench = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.6, 5), new THREE.MeshLambertMaterial({ color: 0x7a2e2e }));
      bench.position.set(0, 0.3, 4);
      roomGroup.add(bench);

      interactiveObjects.push({
        id: "subscription_desk",
        label: "Burn TMF Pass & Mint Seats (Subscription Desk)",
        pos: new THREE.Vector3(-6, 0, 1.8),
        radius: 2.5,
        action: openSubscriptionModal
      });

      interactiveObjects.push({
        id: "admissions_counter",
        label: "Review Dossiers & Rubber Stamp (Admissions Desk)",
        pos: new THREE.Vector3(6, 0, 1.8),
        radius: 2.5,
        action: openAdmissionsModal
      });

      // Beige Task Chair (Musical Chairs Fight!)
      createChair(0, 0, -4, 0xb08a3c);
      interactiveObjects.push({
        id: "chair_vp",
        label: "Musical Chair Fight: Claim Beige Task Chair (VP)",
        pos: new THREE.Vector3(0, 0, -4),
        radius: 2.2,
        action: () => startMusicalChairsContest(4, "Beige Task Chair", "Class IV Vice President", "VP Sterling", ASSETS.p_vladd_1)
      });
    }

    // 5. FLOOR 5: DIRECTOR (STRATEGY & REBALANCE)
    function buildFloor5Director() {
      createDesk(0, 0, -1, 7, 2.0, 0x362014);

      interactiveObjects.push({
        id: "director_rebalance",
        label: "Deploy Robinhood Chain Liquidity Protocol (+30 Pts)",
        pos: new THREE.Vector3(0, 0, 1.5),
        radius: 2.5,
        action: openDirectorRebalanceModal
      });

      // High-Back Leather Desk Chair (Musical Chairs Fight!)
      createChair(6, 0, 2, 0x5a3219);
      interactiveObjects.push({
        id: "chair_director",
        label: "Musical Chair Fight: Claim Leather Desk Chair (Director)",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.2,
        action: () => startMusicalChairsContest(5, "High-Back Leather Desk Chair", "Class V Director", "Director Cromwell", ASSETS.p_argon_2)
      });
    }

    // 6. FLOOR 6: MANAGING DIRECTOR (BOSS: WHAT3VERMAN)
    function buildFloor6MD() {
      createDesk(0, 0, -2, 6, 2.2, 0x2e1c12);

      // what3verman Boss Billboard
      const bossMat = new THREE.MeshBasicMaterial({ map: bossTexWhat3verman });
      const bossQuad = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.8), bossMat);
      bossQuad.position.set(0, 1.8, -3.2);
      roomGroup.add(bossQuad);

      createChair(0, 0, -3.2, 0x7a2e2e); // Oxblood Wingback behind desk

      const lamp = new THREE.PointLight(0x2f6b3d, 1.8, 6);
      lamp.position.set(1.5, 1.6, -2);
      roomGroup.add(lamp);

      interactiveObjects.push({
        id: "boss_what3verman",
        label: "Confront what3verman (Head of Operations)",
        pos: new THREE.Vector3(0, 0, 0.5),
        radius: 2.8,
        action: openWhat3vermanModal
      });

      // Green Banker's Chair (Musical Chairs Fight vs what3verman!)
      createChair(-6, 0, 2, 0x2f6b3d);
      interactiveObjects.push({
        id: "chair_md",
        label: "Musical Chair Fight: Claim Green Bankers Chair (MD)",
        pos: new THREE.Vector3(-6, 0, 2),
        radius: 2.2,
        action: () => startMusicalChairsContest(6, "Green Bankers Chair", "Class VI Managing Director", "what3verman", ASSETS.boss_what3verman)
      });
    }

    // 7. FLOOR 7: PARTNER (PRIVATE VAULT LOUNGE)
    function buildFloor7Partner() {
      createDesk(0, 0, -2, 6, 2.0, 0x2a160d);

      interactiveObjects.push({
        id: "partner_vault",
        label: "Audit Underground Vault Till (0x48dF...A118)",
        pos: new THREE.Vector3(0, 0, 0.5),
        radius: 2.5,
        action: openPartnerVaultModal
      });

      // Oxblood Wingback Chair (Musical Chairs Fight!)
      createChair(6, 0, 2, 0x7a2e2e);
      interactiveObjects.push({
        id: "chair_partner",
        label: "Musical Chair Fight: Claim Oxblood Wingback (Partner)",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.2,
        action: () => startMusicalChairsContest(7, "Oxblood Wingback Chair", "Class VII Partner", "Partner Montgomery", ASSETS.p_bogle_2)
      });
    }

    // 8. FLOOR 8: BOARD OF DIRECTORS (THE HIGH TABLE)
    function buildFloor8Board() {
      // Long mahogany boardroom conference table
      createDesk(0, 0, 0, 9, 2.8, 0x22130a);

      interactiveObjects.push({
        id: "board_quorum",
        label: "Convene Board Quorum on Continuation Clause",
        pos: new THREE.Vector3(0, 0, 2.2),
        radius: 2.8,
        action: openBoardQuorumModal
      });

      // Board of Directors High Seat (Musical Chairs Fight!)
      createChair(0, 0, -2.6, 0xb08a3c);
      interactiveObjects.push({
        id: "chair_board",
        label: "Musical Chair Fight: Claim High Seat (Board Member)",
        pos: new THREE.Vector3(0, 0, -2.6),
        radius: 2.2,
        action: () => startMusicalChairsContest(8, "Board of Directors High Seat", "Class VIII Board Member", "Director Archibald", ASSETS.p_smaug_2)
      });
    }

    // 9. PENTHOUSE · SEAT 0 (FINAL BOSS: KINGPICKLE)
    function buildFloor9Penthouse() {
      // Circular elevated marble dais in center
      const daisGeo = new THREE.CylinderGeometry(4.5, 4.8, 0.4, 32);
      const daisMat = new THREE.MeshLambertMaterial({ color: 0xede4d4 });
      const dais = new THREE.Mesh(daisGeo, daisMat);
      dais.position.set(0, 0.2, 0);
      dais.receiveShadow = true;
      roomGroup.add(dais);

      // Golden Braided Velvet Ropes with Stanchions
      const stanchionMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.9, roughness: 0.2 });
      for (let i = 0; i < 8; i++) {
        const ang = (i / 8) * Math.PI * 2;
        const s = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.2), stanchionMat);
        s.position.set(Math.cos(ang) * 3.6, 0.8, Math.sin(ang) * 3.6);
        roomGroup.add(s);
      }

      // SEAT 0: The Chairman's Mahogany Throne in the center
      const seat0Mat = new THREE.MeshLambertMaterial({ color: 0x5e2222 });
      const seat0 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.6, 1.2), seat0Mat);
      seat0.position.set(0, 1.1, 0);
      roomGroup.add(seat0);

      const seat0Light = new THREE.PointLight(0xfffae6, 1.2, 8);
      seat0Light.position.set(0, 3.5, 0);
      roomGroup.add(seat0Light);

      // Kingpickle Boss Billboard
      const kpMat = new THREE.MeshBasicMaterial({ map: bossTexKingpickle });
      const kpQuad = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 2.0), kpMat);
      kpQuad.position.set(2.4, 1.8, 1.5);
      roomGroup.add(kpQuad);

      interactiveObjects.push({
        id: "boss_kingpickle",
        label: "Speak with Kingpickle & Inspect Seat 0",
        pos: new THREE.Vector3(2.0, 0, 2.2),
        radius: 2.8,
        action: openKingpickleModal
      });

      // The Gilded Throne Platform
      createChair(-5, 0, -2, 0xd4af37);
      interactiveObjects.push({
        id: "chair_throne",
        label: "Ascend to The Gilded Throne (Seat 1 · Sovereign)",
        pos: new THREE.Vector3(-5, 0, -2),
        radius: 2.2,
        action: () => startMusicalChairsContest(9, "The Gilded Throne & Seat 1", "Class IX Sovereign Trustee", "Kingpickle", ASSETS.boss_kingpickle)
      });
    }

    // HELPER: GET FLOOR NAME
    function getFloorName(f) {
      if (f === 0) return "Level 0 (The Pavement & Gate)";
      if (f === 1) return "Floor 1 (Intern - Mailroom)";
      if (f === 2) return "Floor 2 (Analyst - Ledgers)";
      if (f === 3) return "Floor 3 (Associate - The Deng Desk)";
      if (f === 4) return "Floor 4 (Vice President - Admissions)";
      if (f === 5) return "Floor 5 (Director - Strategy)";
      if (f === 6) return "Floor 6 (Managing Director - what3verman)";
      if (f === 7) return "Floor 7 (Partner - Private Vault)";
      if (f === 8) return "Floor 8 (Board of Directors)";
      if (f === 9) return "Penthouse (Seat 0 · Boss: Kingpickle)";
      return `Floor ${f}`;
    }

    // INTERACTION MODALS & CONTROLS
    const modalEl = document.getElementById('taskModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBadge = document.getElementById('modalBadge');
    const modalInstructions = document.getElementById('modalInstructions');
    const modalBody = document.getElementById('modalBody');

    function closeTaskModal() {
      playClick();
      modalEl.classList.remove('active');
    }

    function showMemoToast(title, body) {
      const toast = document.getElementById('memoToast');
      document.getElementById('memoToastTitle').innerText = title;
      document.getElementById('memoToastBody').innerText = body;
      toast.classList.add('show');
      playStampThump();
      setTimeout(() => {
        toast.classList.remove('show');
      }, 4200);
    }

    // ELEVATOR CONCOURSE MODAL
    function openElevatorModal() {
      playElevatorDing();
      modalTitle.innerText = "Elevator Concourse";
      modalBadge.innerText = "BRASS ELEVATOR DIAL";
      modalInstructions.innerText = "Select a floor to ride the elevator. Floors unlock as you win musical chairs and earn promotions.";

      let buttonsHtml = '';
      for (let i = 0; i <= 9; i++) {
        const unlocked = i <= unlockedFloor;
        const isCurrent = i === currentFloor;
        buttonsHtml += `
          <div class="elevator-floor-btn ${unlocked ? '' : 'locked'} ${isCurrent ? 'current' : ''}" onclick="${unlocked ? `rideElevatorTo(${i})` : `showMemoToast('CLEARANCE REQUIRED', 'Floor locked. Earn chair title on current floor first.')`}">
            <span>${getFloorName(i)}</span>
            <span>${isCurrent ? 'HERE ●' : unlocked ? 'RIDE ➔' : 'LOCKED 🔒'}</span>
          </div>
        `;
      }

      modalBody.innerHTML = `<div class="elevator-grid">${buttonsHtml}</div>`;
      modalEl.classList.add('active');
    }

    function rideElevatorTo(f) {
      closeTaskModal();
      playElevatorDing();
      currentFloor = f;
      playerGroup.position.set(0, 0, (f === 0 ? 0 : -6.5));
      playerGroup.rotation.y = 0;
      buildFloorEnvironment();
      updateHUD();
      saveGame();
      showMemoToast("ELEVATOR ARRIVAL", `Flickerr stepped onto ${getFloorName(currentFloor)}.`);
    }

    // 0. GATEKEEPER MODAL (OUTSIDE ENROLLMENT)
    function openGatekeeperModal() {
      playClick();
      modalTitle.innerText = "The Security Gate";
      modalBadge.innerText = "PERSONNEL ADMISSIONS";
      modalInstructions.innerText = "Present your petition for employment at The Mutual Fun. Choose your assigned department fund.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:14px;">
          <p style="font-size:13px;line-height:1.5;">
            "Halt. This is The Mutual Fun private institution. The house deals in arithmetic, never enthusiasm. State your name and select your founding department to receive Employee No. 0401."
          </p>
        </div>
        <div style="display:flex;flex-direction:column;gap:8px;">
          <button class="desk-button" style="background:var(--bogle);" onclick="enrollAtGate('The Bogle Fund', 0)">
            Enroll under The Bogle Fund (Green Rosette)
          </button>
          <button class="desk-button" style="background:var(--argon);" onclick="enrollAtGate('The Argon Fund', 1)">
            Enroll under The Argon Fund (Blue Rosette)
          </button>
          <button class="desk-button" style="background:var(--smaug);" onclick="enrollAtGate('The Smaug Fund', 2)">
            Enroll under The Smaug Fund (Rust Rosette)
          </button>
          <button class="desk-button" style="background:var(--midas);" onclick="enrollAtGate('The Midas Fund', 3)">
            Enroll under The Midas Fund (Gold Rosette)
          </button>
          <button class="desk-button" style="background:var(--vladd);" onclick="enrollAtGate('The Vladd Fund', 4)">
            Enroll under The Vladd Fund (Purple Rosette)
          </button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function enrollAtGate(deptName, deptIdx) {
      playStampThump();
      flickerr.gateAdmitted = true;
      flickerr.department = deptName;
      flickerr.deptIndex = deptIdx;
      flickerr.empNo = 401;
      flickerr.role = "Intern";
      unlockedFloor = Math.max(unlockedFloor, 1);
      closeTaskModal();
      showMemoToast("ADMISSION CONFIRMED", `Badge stamped. Assigned to ${deptName}. Proceed through turnstile to Floor 1.`);
      rideElevatorTo(1);
    }

    // 1. MAILROOM CHUTES
    let mailroomIndex = 0;
    const mailroomDispatches = [
      { text: "Unverified rumors of market contraction. Disregard headlines completely.", correctFund: "argon" },
      { text: "Acquiring a weighted basket of every verified token across Robinhood Chain.", correctFund: "bogle" },
      { text: "Quarterly audit of vault till coins. Every individual penny accounted for.", correctFund: "smaug" },
      { text: "Tender requisition: convert all operational yields into gold-backed certificates.", correctFund: "midas" },
      { text: "Sudden margin call cascade on decentralized exchange. Deploy distress reserve.", correctFund: "vladd" }
    ];

    function openMailroomChuteModal() {
      playClick();
      modalTitle.innerText = "Pneumatic Mail Chutes";
      modalBadge.innerText = "DISPATCH TERMINAL";
      modalInstructions.innerText = "Route incoming ticker slips into the matching fund chute to earn Postage tips.";

      const item = mailroomDispatches[mailroomIndex % mailroomDispatches.length];
      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:12px;">
          <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--oxblood);font-weight:600;">INCOMING TICKER MEMO:</span>
          <p style="font-size:13px;font-style:italic;margin-top:6px;">"${item.text}"</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(5, 1fr);gap:6px;">
          <button class="desk-button" style="background:var(--argon);" onclick="routeMailChute('argon')">Argon</button>
          <button class="desk-button" style="background:var(--bogle);" onclick="routeMailChute('bogle')">Bogle</button>
          <button class="desk-button" style="background:var(--smaug);" onclick="routeMailChute('smaug')">Smaug</button>
          <button class="desk-button" style="background:var(--midas);" onclick="routeMailChute('midas')">Midas</button>
          <button class="desk-button" style="background:var(--vladd);" onclick="routeMailChute('vladd')">Vladd</button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function routeMailChute(fund) {
      const item = mailroomDispatches[mailroomIndex % mailroomDispatches.length];
      if (fund === item.correctFund) {
        playStampThump();
        flickerr.postageETH += 0.010;
        flickerr.reviewScore += 10;
        flickerr.postsOnFile += 1;
        mailroomIndex++;
        updateTicker(`CHUTE ROUTED: Deposited into ${fund.toUpperCase()} book. +0.010 ETH Postage.`);
      } else {
        playClick();
        updateTicker(`CHUTE REJECT: Incorrect philosophy match.`);
      }
      openMailroomChuteModal();
      updateHUD();
      saveGame();
    }

    function pullDispatchLever() {
      playStampThump();
      flickerr.postageETH += 0.010;
      flickerr.reviewScore += 5;
      updateTicker("DISPATCH PULLED: Public rebalance errand run on-chain. +0.010 ETH.");
      updateHUD();
      saveGame();
    }

    // 2. ANALYST LEDGER MODAL
    function openAnalystLedgerModal() {
      playClick();
      modalTitle.innerText = "Daily Ledger Rebalance";
      modalBadge.innerText = "ANALYSIS DESK";
      modalInstructions.innerText = "Audit Robinhood token ratio allocations across the 5 books.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:12px;">
          <p style="font-size:12px;line-height:1.5;">
            "Verify ratio 1:1 parity between decentralized reserves and house vault vouchers. Affix signature ledger tally."
          </p>
        </div>
        <button class="desk-button" style="background:var(--lamp);width:100%;" onclick="auditLedgerAction()">
          Affix Calculation Seal (+15 Review Points)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function auditLedgerAction() {
      playStampThump();
      flickerr.reviewScore += 15;
      flickerr.postsOnFile += 2;
      showMemoToast("LEDGER CERTIFIED", "Parity verified. +15 Review Score on file.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 3. DENG DESK MODAL
    function openDengModal() {
      playClick();
      modalTitle.innerText = "The Deng Desk";
      modalBadge.innerText = "APECHAIN BRIDGE";
      modalInstructions.innerText = "Verify ApeChain Deng NFT holding tenure slips. Accumulate 10.00 credits to forge your soulbound TMF Pass.";

      modalBody.innerHTML = `
        <div style="background:#fdfaf3;border:2px dashed #bfaea0;padding:12px;margin-bottom:12px;">
          <div style="font-family:'IBM Plex Mono';font-size:11px;line-height:1.6;">
            <div><b>Current Deng Credits:</b> ${flickerr.dengCredits.toFixed(2)} / 10.00</div>
            <div><b>TMF Pass Status:</b> ${flickerr.hasPass ? 'SOULBOUND PASS FORGED' : 'NOT YET FORGED'}</div>
          </div>
        </div>
        <div style="display:flex;gap:10px;">
          <button class="desk-button" style="flex:1;background:var(--lamp);" onclick="tenderDengSlip(2.5)">
            Audit Deng Slip (+2.50 Credits)
          </button>
          <button class="desk-button" style="flex:1;background:var(--gold);color:#1a1207;font-weight:700;" onclick="forgePassAction()">
            Forge TMF Pass (10 Credits)
          </button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function tenderDengSlip(cr) {
      playStampThump();
      flickerr.dengCredits += cr;
      flickerr.reviewScore += 10;
      updateTicker(`DENG CREDITED: Tendered ApeChain voucher. +${cr} Credits.`);
      openDengModal();
      updateHUD();
      saveGame();
    }

    function forgePassAction() {
      if (flickerr.dengCredits < 10.0) {
        playClick();
        showMemoToast("TENDER DEFICIT", "The Deng Desk requires at least 10.00 credits to forge a TMF Pass.");
        return;
      }
      playBell();
      flickerr.hasPass = true;
      flickerr.reviewScore += 30;
      showMemoToast("TMF PASS FORGED", "Soulbound pass minted into satchel. Floor 4 clearance unlocked.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 4. SUBSCRIPTION & ADMISSIONS
    function openSubscriptionModal() {
      playClick();
      modalTitle.innerText = "Subscription Desk";
      modalBadge.innerText = "BURNING KILN";
      modalInstructions.innerText = "Burn your soulbound TMF Pass at 0.01 ETH to mint 2 Seats and bind your ERC-6551 Briefcase.";

      modalBody.innerHTML = `
        <div style="text-align:center;padding:16px;">
          <p style="font-size:13px;margin-bottom:14px;">
            ${flickerr.hasPass ? 'You hold a soulbound TMF Pass. Ready for consumption.' : 'You do not hold a TMF Pass. Visit Floor 3.'}
          </p>
          <button class="desk-button" style="background:var(--oxblood);font-size:13px;padding:8px 18px;" onclick="burnPassAction()">
            Burn TMF Pass & Mint 2 Seats
          </button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function burnPassAction() {
      if (!flickerr.hasPass) {
        playClick();
        showMemoToast("PASS REQUIRED", "You must forge a TMF Pass at the Deng Desk on Floor 3 first.");
        return;
      }
      playStampThump();
      flickerr.seatsOwned = 2;
      flickerr.tmfTokens = 401000;
      flickerr.reviewScore += 50;
      showMemoToast("PASS CONSUMED", "2 Seats minted into The Bogle Fund. Briefcase bound on-chain.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    function openAdmissionsModal() {
      playClick();
      modalTitle.innerText = "Admissions Counter";
      modalBadge.innerText = "WAITING ROOM DESK";
      modalInstructions.innerText = "Review shareholder applications and affix official rubber stamps.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:12px;margin-bottom:12px;">
          <p style="font-size:12px;font-style:italic;">
            "Applicant requests enrollment under Argon books. Stated intent: hold dividend checks in briefcase until quarterly liquidation. Displays inert temperament, completely unmoved by volatile headlines."
          </p>
        </div>
        <div style="display:flex;gap:8px;">
          <button class="desk-button" style="flex:1;background:var(--lamp);" onclick="stampDossierAction('ADMITTED')">Admitted</button>
          <button class="desk-button" style="flex:1;background:var(--gold);" onclick="stampDossierAction('PENDING')">Pending</button>
          <button class="desk-button" style="flex:1;background:var(--oxblood);" onclick="stampDossierAction('FLAGGED')">Flagged</button>
          <button class="desk-button" style="flex:1;background:var(--ink);" onclick="stampDossierAction('DECLINED')">Declined</button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function stampDossierAction(verdict) {
      playStampThump();
      flickerr.reviewScore += 20;
      showMemoToast("STAMP AFFIXED", `Dossier marked ${verdict}. Review recorded.`);
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 5. DIRECTOR REBALANCE
    function openDirectorRebalanceModal() {
      playClick();
      modalTitle.innerText = "Director Strategy Terminal";
      modalBadge.innerText = "RESERVE PROTOCOL";
      modalInstructions.innerText = "Authorize institutional liquidity allocations across all five books.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:12px;">
          <p style="font-size:12px;line-height:1.5;">
            "Execute automated overnight rebalance across Argon, Bogle, Smaug, Midas, and Vladd books."
          </p>
        </div>
        <button class="desk-button" style="background:var(--oxblood);width:100%;" onclick="executeDirectorRebalance()">
          Authorize Institutional Allocation (+30 Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function executeDirectorRebalance() {
      playStampThump();
      flickerr.reviewScore += 30;
      showMemoToast("ALLOCATION COMPLETE", "Overnight books rebalanced. +30 Review Score.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 6. BOSS: WHAT3VERMAN
    function openWhat3vermanModal() {
      playClick();
      modalTitle.innerText = "Boss Encounter: what3verman";
      modalBadge.innerText = "HEAD OF OPERATIONS";
      modalInstructions.innerText = "what3verman audits your arithmetic from his Oxblood Wingback. Answer his compliance test.";

      modalBody.innerHTML = `
        <div style="display:grid;grid-template-columns:110px 1fr;gap:12px;margin-bottom:14px;">
          <img src="${ASSETS.boss_what3verman}" style="width:100px;height:100px;border:2px solid var(--ink);object-fit:cover;" alt="what3verman">
          <div style="font-size:12px;line-height:1.45;font-style:italic;background:var(--paper-sunken);padding:10px;">
            "The house deals in arithmetic, Flickerr, not enthusiasm. What is the fundamental commandment of house correspondence?"
          </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:6px;">
          <button class="desk-button secondary" onclick="answerWhat3vermanAction(false)">1. The house uses bold em dashes for emphasis.</button>
          <button class="desk-button secondary" onclick="answerWhat3vermanAction(true)">2. The house admits, it never invites, and never uses dashes.</button>
          <button class="desk-button secondary" onclick="answerWhat3vermanAction(false)">3. The house distributes marketing invitations via email.</button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function answerWhat3vermanAction(correct) {
      if (correct) {
        playBell();
        flickerr.reviewScore += 50;
        showMemoToast("WHAT3VERMAN AUDIT PASSED", "The arithmetic is sound. Challenge what3verman to musical chairs for the Green Bankers Chair.");
        closeTaskModal();
        updateHUD();
        saveGame();
      } else {
        playClick();
        showMemoToast("POLICY VIOLATION", "what3verman frowns: 'Incorrect. Re-read brand-guide.md.'");
      }
    }

    // 7. PARTNER VAULT
    function openPartnerVaultModal() {
      playClick();
      modalTitle.innerText = "Private Vault Till";
      modalBadge.innerText = "VAULT 0x48dF...A118";
      modalInstructions.innerText = "Examine the physical gold and on-chain till certificates.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:12px;">
          <p style="font-size:12px;line-height:1.5;">
            "Vault balance: 4,001 total Seats accounted for. Deployer 0x4609...Aa3e verified. Zero discrepancies found."
          </p>
        </div>
        <button class="desk-button" style="background:var(--lamp);width:100%;" onclick="auditVaultAction()">
          Confirm Till Inspection (+40 Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function auditVaultAction() {
      playStampThump();
      flickerr.reviewScore += 40;
      showMemoToast("VAULT VERIFIED", "Till audit certified on-chain. +40 Review Score.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 8. BOARD ROOM QUORUM
    function openBoardQuorumModal() {
      playClick();
      modalTitle.innerText = "The Board of Directors";
      modalBadge.innerText = "THE HIGH TABLE";
      modalInstructions.innerText = "Convene the 12 directors to approve the Continuation Clause.";

      modalBody.innerHTML = `
        <div style="background:#faf6ee;border:1px solid var(--rule);padding:14px;margin-bottom:12px;">
          <p style="font-size:12px;line-height:1.5;">
            "Motion to ratify the permanent charter of The Mutual Fun. Quorum required across all five fund books."
          </p>
        </div>
        <button class="desk-button" style="background:var(--oxblood);width:100%;" onclick="ratifyBoardMotion()">
          Affix Sovereign Quorum Seal (+60 Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function ratifyBoardMotion() {
      playBell();
      flickerr.reviewScore += 60;
      showMemoToast("QUORUM ACHIEVED", "Continuation Clause ratified. Penthouse clearance issued.");
      closeTaskModal();
      updateHUD();
      saveGame();
    }

    // 9. BOSS: KINGPICKLE & SEAT 0
    function openKingpickleModal() {
      playClick();
      modalTitle.innerText = "Final Encounter: Kingpickle & Seat 0";
      modalBadge.innerText = "THE EXECUTIVE ROTUNDA";
      modalInstructions.innerText = "Kingpickle stands before Seat 0. It is 19:59 UTC. Cast the decisive vote before the Closing Bell tolls.";

      modalBody.innerHTML = `
        <div style="display:grid;grid-template-columns:110px 1fr;gap:12px;margin-bottom:14px;">
          <img src="${ASSETS.boss_kingpickle}" style="width:100px;height:100px;border:2px solid var(--gold);object-fit:cover;" alt="Kingpickle">
          <div style="font-size:12px;line-height:1.45;font-style:italic;background:var(--paper-sunken);padding:10px;">
            "Welcome to the rotunda, Flickerr. You climbed from the pavement outside. Seat 0 belongs to the building and is never for sale. Claim The Gilded Throne and become Permanent Trustee."
          </div>
        </div>
        <button class="desk-button" style="background:var(--lamp);width:100%;font-size:13px;padding:10px;" onclick="castFinalVoteAction()">
          Cast Decisive Vote: Preserve the Five Funds in Perpetuity 🔔
        </button>
      `;
      modalEl.classList.add('active');
    }

    function castFinalVoteAction() {
      flickerr.chairName = "The Gilded Throne & Seat 1";
      flickerr.chairTier = "Class IX Sovereign Trustee";
      flickerr.role = "The Chairman";
      flickerr.reviewScore += 100;
      closeTaskModal();
      showMemoToast("CLOSING BELL TOLLS", "All five funds achieve 100% quorum! You are conferred Title to Seat 1!");
      updateTicker("VICTORY: CLOSING BELL TOLLS. FLICKERR CONFIRMED PERMANENT TRUSTEE.");
      updateHUD();
      saveGame();
      setTimeout(openCertModal, 1500);
    }

    // MUSICAL CHAIRS MINI-GAME FIGHT ENGINE
    const arenaModal = document.getElementById('arenaModal');
    const arenaTitle = document.getElementById('arenaTitle');
    const arenaStatus = document.getElementById('arenaStatus');
    const recordSpinner = document.getElementById('recordSpinner');
    const rivalImg = document.getElementById('rivalImg');
    const rivalName = document.getElementById('rivalName');
    const rivalRole = document.getElementById('rivalRole');
    const sitBtn = document.getElementById('sitBtn');

    let arenaTargetFloor = 0;
    let arenaTargetChair = "";
    let arenaTargetTier = "";
    let arenaCutTimeout = null;
    let arenaWindowTimeout = null;
    let arenaMusicPlaying = false;
    let arenaCanSit = false;
    let arenaReactionStartTime = 0;

    function startMusicalChairsContest(floor, chairName, tierName, rivalTitle, rivalAvatar) {
      playClick();
      arenaTargetFloor = floor;
      arenaTargetChair = chairName;
      arenaTargetTier = tierName;

      arenaTitle.innerText = `CHAIR FIGHT: ${chairName.toUpperCase()}`;
      rivalName.innerText = rivalTitle;
      rivalRole.innerText = `Floor ${floor} Contender`;
      rivalImg.src = rivalAvatar || ASSETS.p_bogle_1;

      arenaStatus.className = "arena-status-badge waiting";
      arenaStatus.innerText = "Phonograph Spinning...";
      recordSpinner.classList.add('spinning');

      sitBtn.className = "sit-action-btn disabled";
      sitBtn.innerText = "WAIT FOR THE BELL...";
      arenaCanSit = false;
      arenaMusicPlaying = true;

      arenaModal.classList.add('active');

      startMusicalChairsTune();

      // Random music duration: 2.5 to 5.0 seconds
      const playDuration = 2500 + Math.random() * 2500;
      arenaCutTimeout = setTimeout(triggerMusicCutoff, playDuration);
    }

    function triggerMusicCutoff() {
      if (!arenaMusicPlaying) return;
      stopMusicalChairsTune();
      playBell(); // Bell chimes!

      recordSpinner.classList.remove('spinning');
      arenaStatus.className = "arena-status-badge active";
      arenaStatus.innerText = "THE NEEDLE CUT! SIT DOWN NOW!";

      sitBtn.className = "sit-action-btn ready";
      sitBtn.innerText = "DIVE FOR THE CHAIR! [SPACE]";
      arenaCanSit = true;
      arenaReactionStartTime = Date.now();

      // Rival reaction window: 650ms
      arenaWindowTimeout = setTimeout(() => {
        if (arenaCanSit) {
          rivalWinsContest();
        }
      }, 700);
    }

    function onPlayerSitAction() {
      if (!arenaCanSit) return;
      arenaCanSit = false;
      clearTimeout(arenaWindowTimeout);

      const reactionTime = Date.now() - arenaReactionStartTime;
      playStampThump();

      // Player won!
      flickerr.chairName = arenaTargetChair;
      flickerr.chairTier = arenaTargetTier;
      flickerr.role = ROLES[arenaTargetFloor].title;
      unlockedFloor = Math.max(unlockedFloor, arenaTargetFloor + 1);
      flickerr.reviewScore += 25;

      if (!flickerr.chairsWon.includes(arenaTargetChair)) {
        flickerr.chairsWon.push(arenaTargetChair);
      }

      arenaStatus.className = "arena-status-badge waiting";
      arenaStatus.innerText = `VICTORY! SATE IN ${reactionTime}ms!`;
      sitBtn.className = "sit-action-btn";
      sitBtn.innerText = "CHAIR SECURED!";

      updateTicker(`CHAIR WON: Flickerr claimed ${arenaTargetChair} (${arenaTargetTier})!`);
      showMemoToast("CHAIR SECURED", `Flickerr claimed ${arenaTargetChair}! Promoted to ${flickerr.role}.`);

      updateHUD();
      saveGame();

      setTimeout(() => {
        closeArenaModal();
        openCertModal(); // Show updated certificate
      }, 1200);
    }

    function rivalWinsContest() {
      arenaCanSit = false;
      playClick();
      arenaStatus.className = "arena-status-badge waiting";
      arenaStatus.innerText = "RIVAL SNATCHED THE SEAT!";
      sitBtn.className = "sit-action-btn disabled";
      sitBtn.innerText = "MISSED CHAIR! TRY AGAIN";
      showMemoToast("CONTEST LOST", "Rival seized the chair first. Concentrate on the bell chime.");
    }

    function closeArenaModal() {
      stopMusicalChairsTune();
      clearTimeout(arenaCutTimeout);
      clearTimeout(arenaWindowTimeout);
      arenaCanSit = false;
      arenaMusicPlaying = false;
      arenaModal.classList.remove('active');
    }

    // CERTIFICATE OF EMPLOYMENT GENERATOR (tmforgchart.xyz 1200x675 Canvas)
    const certModal = document.getElementById('certModal');
    const certCanvas = document.getElementById('certCanvas');

    function openCertModal() {
      renderEngravedCertificate();
      certModal.classList.add('active');
    }

    function closeCertModal() {
      playClick();
      certModal.classList.remove('active');
    }

    function renderEngravedCertificate() {
      const W = 1200, H = 675;
      certCanvas.width = W;
      certCanvas.height = H;
      const g = certCanvas.getContext('2d');

      const PAPER = "#f6efe3", INK = "#211b14", MUTED = "#6b5f4e", OX = "#7a2e2e", GOLD = "#b08a3c";
      const F = DEPARTMENTS[flickerr.deptIndex].color;

      const CAS = '"Libre Caslon Text", Georgia, serif';
      const SER = '"Source Serif 4", Georgia, serif';
      const MON = '"IBM Plex Mono", Menlo, monospace';

      // 1. Parchment Background
      g.fillStyle = PAPER;
      g.fillRect(0, 0, W, H);

      // Paper grain noise
      for (let i = 0; i < 4500; i++) {
        g.fillStyle = "rgba(120,95,60," + (Math.random() * 0.05).toFixed(3) + ")";
        g.fillRect(Math.random() * W, Math.random() * H, 1, 1);
      }

      // 2. Engraved Guilloche Border
      g.strokeStyle = OX;
      g.lineWidth = 3;
      g.strokeRect(22, 22, W - 44, H - 44);

      g.lineWidth = 1;
      g.strokeRect(46, 46, W - 92, H - 92);

      const wave = (horiz, fixed, from, to) => {
        for (const ph of [0, Math.PI]) {
          g.beginPath();
          for (let s = from; s <= to; s += 1.5) {
            const o = Math.sin(s / 3 + ph) * 7;
            horiz ? (s === from ? g.moveTo(s, fixed + o) : g.lineTo(s, fixed + o)) : (s === from ? g.moveTo(fixed + o, s) : g.lineTo(fixed + o, s));
          }
          g.stroke();
        }
      };

      g.strokeStyle = "rgba(122,46,46,.5)";
      g.lineWidth = 0.8;
      wave(true, 34, 48, W - 48);
      wave(true, H - 34, 48, W - 48);
      wave(false, 34, 48, H - 48);
      wave(false, W - 34, 48, H - 48);

      // Corner rosettes in department's color
      for (const [x, y] of [[34, 34], [W - 34, 34], [34, H - 34], [W - 34, H - 34]]) {
        g.beginPath();
        g.arc(x, y, 10, 0, Math.PI * 2);
        g.fillStyle = F;
        g.fill();
        g.lineWidth = 1.5;
        g.strokeStyle = OX;
        g.stroke();
      }

      // 3. Header
      g.textAlign = "center";
      g.fillStyle = MUTED;
      g.font = "400 15px " + SER;
      g.fillText("THE MUTUAL FUN  ·  PERSONNEL DEPARTMENT", W / 2, 92);

      g.fillStyle = INK;
      g.font = "700 50px " + CAS;
      g.fillText("Certificate of Employment", W / 2, 150);

      g.strokeStyle = GOLD;
      g.lineWidth = 1;
      g.beginPath();
      g.moveTo(W / 2 - 240, 172);
      g.lineTo(W / 2 + 240, 172);
      g.stroke();

      // 4. Portrait in Oval Ring
      const ox = 250, oy = 360, rx = 95, ry = 118;
      g.save();
      g.beginPath();
      g.ellipse(ox, oy, rx, ry, 0, 0, Math.PI * 2);
      g.fillStyle = "#ede3cf";
      g.fill();
      g.clip();

      // Draw portrait
      const portraitKey = `p_bogle_${Math.min(5, Math.max(1, currentFloor))}`;
      if (ASSETS[portraitKey]) {
        const img = new Image();
        img.src = ASSETS[portraitKey];
        g.drawImage(img, ox - rx, oy - ry, rx * 2, ry * 2);
      } else {
        g.fillStyle = MUTED;
        g.font = "700 80px " + CAS;
        g.fillText("F", ox, oy + 28);
      }
      g.restore();

      g.lineWidth = 4;
      g.strokeStyle = GOLD;
      g.beginPath();
      g.ellipse(ox, oy, rx + 5, ry + 5, 0, 0, Math.PI * 2);
      g.stroke();

      g.lineWidth = 1;
      g.strokeStyle = OX;
      g.beginPath();
      g.ellipse(ox, oy, rx + 11, ry + 11, 0, 0, Math.PI * 2);
      g.stroke();

      // 5. The Words
      const tx = 720;
      g.fillStyle = MUTED;
      g.font = "italic 400 22px " + SER;
      g.fillText("This certifies that", tx, 238);

      g.fillStyle = INK;
      g.font = "700 52px " + CAS;
      g.fillText("@Flickerr", tx, 300);

      g.fillStyle = MUTED;
      g.font = "italic 400 22px " + SER;
      g.fillText("holds the position of", tx, 350);

      g.fillStyle = OX;
      g.font = "700 44px " + CAS;
      g.fillText(flickerr.role, tx, 406);

      g.fillStyle = MUTED;
      g.font = "italic 400 22px " + SER;
      g.fillText("in the department of", tx, 452);

      g.fillStyle = F;
      g.font = "700 34px " + CAS;
      g.fillText(flickerr.department, tx, 496);

      // 6. Ledger Line
      g.strokeStyle = GOLD;
      g.beginPath();
      g.moveTo(90, 526);
      g.lineTo(W - 90, 526);
      g.stroke();

      g.fillStyle = INK;
      g.font = "500 15px " + MON;
      const today = new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
      g.fillText(`EMPLOYEE No. ${String(flickerr.empNo).padStart(4, "0")}   ·   FLOOR ${currentFloor} OF 8   ·   CHAIR: ${flickerr.chairName.toUpperCase()}   ·   ISSUED ${today.toUpperCase()}`, W / 2, 556);

      // 7. Signature Line & Red Seal
      g.textAlign = "left";
      g.fillStyle = INK;
      g.font = "italic 400 26px " + CAS;
      g.fillText("Personnel Department", 108, 592);

      g.strokeStyle = INK;
      g.lineWidth = 0.8;
      g.beginPath();
      g.moveTo(104, 601);
      g.lineTo(344, 601);
      g.stroke();

      g.fillStyle = MUTED;
      g.font = "400 13px " + SER;
      g.fillText("The Mutual Fun · tmforgchart.xyz · 1987", 104, 619);

      const sx = W - 160, sy = 588;
      g.beginPath();
      g.arc(sx, sy, 36, 0, Math.PI * 2);
      g.fillStyle = OX;
      g.fill();

      g.beginPath();
      g.arc(sx, sy, 30, 0, Math.PI * 2);
      g.strokeStyle = "rgba(246,239,227,.8)";
      g.lineWidth = 1.2;
      g.stroke();

      g.fillStyle = PAPER;
      g.textAlign = "center";
      g.font = "700 9px " + CAS;
      g.fillText("OFFICIAL", sx, sy - 1);
      g.font = "400 10px " + SER;
      g.fillText("1987", sx, sy + 13);
    }

    function downloadCert() {
      playClick();
      const a = document.createElement("a");
      a.download = `tmf-certificate-flickerr-${flickerr.role.toLowerCase().replace(/\s+/g, '-')}.png`;
      a.href = certCanvas.toDataURL("image/png");
      a.click();
    }

    function updateHUD() {
      document.getElementById('hudDept').innerText = flickerr.department;
      document.getElementById('hudRank').innerText = `${ROLES[currentFloor].title} (Fl ${currentFloor})`;
      document.getElementById('hudChair').innerText = flickerr.chairName;
      document.getElementById('hudPostage').innerText = `${flickerr.postageETH.toFixed(3)} ETH`;
      document.getElementById('hudDeng').innerText = flickerr.dengCredits.toFixed(2);
      document.getElementById('hudTmf').innerText = flickerr.tmfTokens.toLocaleString();
      document.getElementById('floorIndicatorText').innerText = `CURRENT LEVEL: ${getFloorName(currentFloor).toUpperCase()}`;
    }

    function updateTicker(msg) {
      document.getElementById('tickerText').innerText = `LOBBY TICKER: ${msg.toUpperCase()}`;
    }

    // INPUT CONTROLS (WASD, ARROWS, SPACE, E, Q)
    const keys = {};
    window.addEventListener('keydown', (e) => {
      keys[e.key.toLowerCase()] = true;
      if (e.key === ' ' && arenaCanSit) {
        onPlayerSitAction();
        e.preventDefault();
        return;
      }
      if (e.key === 'e' || e.key === 'E' || e.key === ' ') {
        checkInteractions();
      }
    });

    window.addEventListener('keyup', (e) => {
      keys[e.key.toLowerCase()] = false;
    });

    let cameraAngle = 0;

    function checkInteractions() {
      if (modalEl.classList.contains('active') || arenaModal.classList.contains('active') || certModal.classList.contains('active')) return;
      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist <= obj.radius) {
          obj.action();
          return;
        }
      }
    }

    // ANIMATION & GAME LOOP
    let walkClock = 0;
    const promptEl = document.getElementById('interactPrompt');

    function animate() {
      requestAnimationFrame(animate);

      // Camera orbit (Q / E)
      if (keys['q']) cameraAngle += 0.03;
      if (keys['e'] && !promptEl.style.display.includes('block')) cameraAngle -= 0.03;

      // Player Movement
      let moveX = 0;
      let moveZ = 0;
      if (keys['w'] || keys['arrowup']) moveZ -= 1;
      if (keys['s'] || keys['arrowdown']) moveZ += 1;
      if (keys['a'] || keys['arrowleft']) moveX -= 1;
      if (keys['d'] || keys['arrowright']) moveX += 1;

      const isMoving = (moveX !== 0 || moveZ !== 0);

      const isModalActive = modalEl.classList.contains('active') || arenaModal.classList.contains('active') || certModal.classList.contains('active');

      if (isMoving && !isModalActive) {
        const moveVec = new THREE.Vector3(moveX, 0, moveZ).normalize();
        moveVec.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraAngle);

        const speed = 0.12;
        playerGroup.position.x += moveVec.x * speed;
        playerGroup.position.z += moveVec.z * speed;

        const targetRot = Math.atan2(moveVec.x, moveVec.z);
        playerGroup.rotation.y = targetRot;

        // Limb bobbing animation
        walkClock += 0.2;
        leftLeg.rotation.x = Math.sin(walkClock) * 0.45;
        rightLeg.rotation.x = -Math.sin(walkClock) * 0.45;
        leftArm.rotation.x = -Math.sin(walkClock) * 0.45;
        rightArm.rotation.x = Math.sin(walkClock) * 0.35;
        torso.position.y = 1.0 + Math.abs(Math.sin(walkClock * 2)) * 0.04;

        if (Math.sin(walkClock) > 0.9) playStep();

        // Boundaries
        const boundX = (currentFloor === 0 ? 14 : 10.5);
        const boundZ = (currentFloor === 0 ? 12 : 8.5);
        playerGroup.position.x = Math.max(-boundX, Math.min(boundX, playerGroup.position.x));
        playerGroup.position.z = Math.max(-boundZ, Math.min(boundZ, playerGroup.position.z));
      } else {
        leftLeg.rotation.x = 0;
        rightLeg.rotation.x = 0;
        leftArm.rotation.x = 0;
        rightArm.rotation.x = 0;
        torso.position.y = 1.0;
      }

      // Third-person Smooth Follow Camera
      const camDist = (currentFloor === 0 ? 7.5 : 6.5);
      const camHeight = (currentFloor === 0 ? 4.8 : 4.2);
      const targetCamX = playerGroup.position.x + Math.sin(cameraAngle) * camDist;
      const targetCamZ = playerGroup.position.z + Math.cos(cameraAngle) * camDist;

      camera.position.x += (targetCamX - camera.position.x) * 0.1;
      camera.position.y += (camHeight - camera.position.y) * 0.1;
      camera.position.z += (targetCamZ - camera.position.z) * 0.1;
      camera.lookAt(playerGroup.position.x, 1.2, playerGroup.position.z);

      // Check Proximity for floating prompt
      let nearby = false;
      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist <= obj.radius) {
          promptEl.innerText = `[E] ${obj.label}`;
          promptEl.style.display = 'block';
          nearby = true;
          break;
        }
      }
      if (!nearby) {
        promptEl.style.display = 'none';
      }

      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // STARTUP INITIALIZATION
    loadGame();
    buildFloorEnvironment();
    updateHUD();
    animate();
  </script>
</body>
</html>
'''

# Replace __ASSETS_JSON__ with json dump of assets
final_html = html_content.replace('__ASSETS_JSON__', json.dumps(assets))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

brain_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated full upgraded game successfully in both workspace and brain directory!")
