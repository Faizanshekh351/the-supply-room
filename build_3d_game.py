import os
import json
import base64

# 1. Load assets
assets = {}

if os.path.exists('marks/medallion-384.png'):
    with open('marks/medallion-384.png', 'rb') as f:
        assets['medallion'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

if os.path.exists('85cAnf-p_400x400.jpg'):
    with open('85cAnf-p_400x400.jpg', 'rb') as f:
        assets['boss_what3verman'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

if os.path.exists('iYRjRGYm_400x400.jpg'):
    with open('iYRjRGYm_400x400.jpg', 'rb') as f:
        assets['boss_kingpickle'] = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

for fund in ['argon', 'bogle', 'smaug', 'midas', 'vladd']:
    for i in range(1, 6):
        p_path = f'portraits/{fund}-0{i}.png'
        c_path = f'cutouts/{fund}-0{i}.png'
        if os.path.exists(p_path):
            with open(p_path, 'rb') as f:
                assets[f'p_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')
        if os.path.exists(c_path):
            with open(c_path, 'rb') as f:
                assets[f'c_{fund}_{i}'] = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

print(f"Loaded {len(assets)} assets.")

# 2. Build complete 3D game HTML
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Mutual Fun: Flickerr's 3D Office Odyssey (1987)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Libre+Caslon+Text:wght@400;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
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
      --argon: #49698C;
      --bogle: #4E8A5A;
      --smaug: #9C5248;
      --midas: #B9902F;
      --vladd: #6E5D8C;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

    body {
      background: #0d0a08;
      color: var(--ink);
      font-family: 'Source Serif 4', Georgia, serif;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      position: relative;
    }

    #gameCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    /* 3D Vignette overlay */
    .vignette {
      position: absolute;
      inset: 0;
      pointer-events: none;
      background: radial-gradient(circle at 50% 50%, transparent 55%, rgba(10, 7, 5, 0.75) 100%);
      z-index: 5;
    }

    /* Top HUD Plaque */
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
      flex-wrap: wrap;
      gap: 10px;
    }

    .brass-badge {
      background: linear-gradient(180deg, #c79b4b 0%, #8f6826 40%, #573e13 100%);
      border: 2px solid #e5c178;
      border-radius: 4px;
      padding: 6px 16px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      gap: 12px;
      pointer-events: auto;
    }

    .brass-badge h1 {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 15px;
      letter-spacing: 2px;
      color: #1a1207;
      text-transform: uppercase;
      font-weight: 700;
    }

    .status-ribbon {
      display: flex;
      gap: 10px;
      background: rgba(22, 16, 12, 0.92);
      border: 1px solid #3d2d20;
      padding: 6px 14px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: #bfaea0;
      align-items: center;
      pointer-events: auto;
    }

    .status-ribbon b { color: #e5c178; }

    .character-pill {
      background: var(--oxblood);
      color: var(--paper-raised);
      padding: 2px 7px;
      font-weight: 600;
      border-radius: 2px;
    }

    /* Floor Indicator Strip */
    .floor-indicator {
      position: absolute;
      top: 68px;
      left: 18px;
      background: rgba(22, 16, 12, 0.88);
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
      background: rgba(246, 239, 227, 0.95);
      border: 2px solid var(--ink);
      box-shadow: 0 6px 20px rgba(0,0,0,0.6);
      padding: 8px 20px;
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

    /* Controls Guide at Bottom Left */
    .controls-guide {
      position: absolute;
      bottom: 14px;
      left: 18px;
      background: rgba(18, 13, 10, 0.85);
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
      background: rgba(18, 13, 10, 0.85);
      border: 1px solid #33261c;
      padding: 6px 12px;
      border-radius: 4px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: #c9a86a;
      z-index: 10;
      pointer-events: none;
      max-width: 500px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Modal Sheet for Task Interaction */
    .task-modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(10, 7, 5, 0.85);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 50;
      padding: 20px;
    }

    .task-modal-overlay.active { display: flex; }

    .modal-paper-sheet {
      background: var(--paper);
      border: 3px solid var(--ink);
      max-width: 620px;
      width: 100%;
      padding: 24px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      position: relative;
      background-image: repeating-linear-gradient(0deg, transparent, transparent 23px, rgba(216, 204, 180, 0.3) 24px);
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
      color: var(--ink);
    }

    .desk-button {
      background: var(--ink);
      color: var(--paper-raised);
      border: 1px solid var(--ink);
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 12px;
      padding: 7px 14px;
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .desk-button:hover {
      background: var(--oxblood);
      border-color: var(--oxblood);
    }

    .desk-button.secondary {
      background: transparent;
      color: var(--ink);
      border-color: var(--rule);
    }

    .desk-button.secondary:hover {
      background: var(--paper-sunken);
      border-color: var(--ink);
    }

    /* Elevator Selector Modal */
    .elevator-panel {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin: 14px 0;
    }

    .elevator-floor-btn {
      display: flex;
      justify-content: space-between;
      padding: 10px 14px;
      background: #faf6ee;
      border: 1px solid var(--rule);
      cursor: pointer;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 12px;
      transition: all 0.12s ease;
    }

    .elevator-floor-btn:hover {
      border-color: var(--ink);
      background: #fff;
      box-shadow: 2px 2px 0 var(--ink);
    }

    .elevator-floor-btn.locked {
      opacity: 0.45;
      cursor: not-allowed;
      background: #ece3d3;
    }

    /* In-game Memorandum Notification Toast */
    .memo-toast {
      position: absolute;
      top: 70px;
      left: 50%;
      transform: translateX(-50%) translateY(-140px);
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

    /* Full-screen Victory Certificate Modal */
    .victory-modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(10, 7, 5, 0.92);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 70;
      padding: 20px;
    }
    .victory-modal-overlay.active { display: flex; }
    .victory-certificate {
      background: var(--paper-raised);
      border: 6px double var(--ink);
      box-shadow: 0 25px 60px rgba(0,0,0,0.9);
      max-width: 680px;
      width: 100%;
      padding: 32px;
      text-align: center;
      position: relative;
    }
    .cert-medallion {
      width: 64px;
      height: 64px;
      margin: 0 auto 10px auto;
      display: block;
    }
    .cert-title {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 22px;
      font-weight: 700;
      color: var(--oxblood);
      letter-spacing: 2px;
      text-transform: uppercase;
      margin: 0;
    }
    .cert-sub {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: var(--ink-muted);
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-top: 4px;
      border-bottom: 1px solid var(--rule);
      padding-bottom: 12px;
    }
    .cert-body {
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 13px;
      color: var(--ink);
      line-height: 1.6;
      margin: 16px 0;
    }
    .cert-name {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 24px;
      font-weight: 700;
      color: var(--ink);
      letter-spacing: 3px;
      text-transform: uppercase;
      margin: 6px 0;
    }
    .cert-chair {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--gold);
      background: #faf3e3;
      border: 1px solid var(--gold);
      display: inline-block;
      padding: 6px 18px;
      margin: 8px 0;
    }
    .cert-signatures {
      display: grid;
      grid-template-columns: 1fr 100px 1fr;
      gap: 12px;
      align-items: center;
      margin-top: 20px;
      border-top: 1px solid var(--rule);
      padding-top: 16px;
    }
    .sig-block {
      text-align: center;
    }
    .sig-pic {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 2px solid var(--ink);
      object-fit: cover;
      margin: 0 auto 4px auto;
      display: block;
    }
    .sig-line {
      font-family: 'Libre Caslon Text', Georgia, serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--oxblood);
      font-style: italic;
    }
    .sig-title {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 9px;
      color: var(--ink-muted);
      text-transform: uppercase;
    }
    .seal-circle {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      border: 3px double var(--oxblood);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 9px;
      font-weight: 700;
      color: var(--oxblood);
      text-align: center;
      line-height: 1.1;
      margin: 0 auto;
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
      <img src="__MEDALLION_B64__" style="width:28px;height:28px;object-fit:contain;" alt="Seal">
      <div>
        <h1>The Mutual Fun</h1>
      </div>
    </div>

    <div class="status-ribbon">
      <span class="character-pill">FLICKERR</span>
      <span>Floor: <b id="hudFloor">B (Mailroom)</b></span>
      <span>Chair: <b id="hudChair">The Pavement</b></span>
      <span>Postage: <b id="hudPostage">0.000 ETH</b></span>
      <span>Deng: <b id="hudDeng">0.00</b></span>
      <span>$TMF: <b id="hudTmf">0</b></span>
    </div>
  </div>

  <div class="floor-indicator" id="floorIndicatorText">
    CURRENT FLOOR: BASEMENT MAILROOM · OBJECTIVE: EARN 0.050 ETH POSTAGE
  </div>

  <!-- Proximity Interaction Badge -->
  <div class="interact-prompt" id="interactPrompt">
    [E] Interact
  </div>

  <!-- Controls Guide -->
  <div class="controls-guide">
    <b>WASD / ARROWS:</b> Move Flickerr · <b>[E] / SPACE:</b> Interact with Stations & Chairs · <b>Q / E:</b> Orbit Camera
  </div>

  <!-- Bottom Ticker -->
  <div class="bottom-ticker" id="tickerText">
    LOBBY TICKER: FLICKERR ENTERS 1987 HEADQUARTERS.
  </div>

  <!-- Task & Interaction Modal -->
  <div class="task-modal-overlay" id="taskModal">
    <div class="modal-paper-sheet">
      <div class="modal-header-row">
        <h3 id="modalTitle">Station Title</h3>
        <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--ink-muted);" id="modalBadge">OFFICIAL DESK</span>
      </div>

      <div class="modal-instruction-box" id="modalInstructions">
        Instructions go here.
      </div>

      <div id="modalBody">
        <!-- Dynamic content injected by JS -->
      </div>

      <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:16px;">
        <button class="desk-button secondary" onclick="closeTaskModal()">Step Back</button>
      </div>
    </div>
  </div>

  <!-- In-Game Memorandum Notification Toast -->
  <div class="memo-toast" id="memoToast">
    <div class="memo-toast-title" id="memoToastTitle">INTERNAL MEMORANDUM</div>
    <div class="memo-toast-body" id="memoToastBody">House instructions updated.</div>
  </div>

  <!-- Full-screen Victory Certificate Modal -->
  <div class="victory-modal-overlay" id="victoryModal">
    <div class="victory-certificate">
      <img src="__MEDALLION_B64__" class="cert-medallion" alt="Medallion">
      <h2 class="cert-title">The Mutual Fun</h2>
      <div class="cert-sub">CONFIRMATION OF ADMISSION IN PERPETUITY · 1987</div>
      <div class="cert-body">
        <p>Be it known to all books, ledgers, and pneumatic conduits that</p>
        <h1 class="cert-name">FLICKERR</h1>
        <p>having successfully navigated all five floors of the institution, routed the pneumatic chutes, verified ApeChain Deng slips, audited the shareholder admissions counter, and answered the Head of Operations,</p>
        <p>is hereby conferred Title to</p>
        <div>
          <span class="cert-chair">THE GILDED THRONE & SEAT 1</span>
        </div>
        <p style="font-size:12px;color:var(--ink-muted);margin-top:10px;">
          Admitted with permanent trustee privileges under The Bogle Fund. Briefcase bound on-chain with 401,000 $TMF tokens and sovereign clearance on ApeChain.
        </p>
        <div class="cert-signatures">
          <div class="sig-block">
            <img id="sigImgWhat3verman" class="sig-pic" alt="what3verman">
            <div class="sig-line">what3verman</div>
            <div class="sig-title">Head of Operations</div>
          </div>
          <div class="seal-circle">
            OFFICIALLY<br>ADMITTED<br>1987
          </div>
          <div class="sig-block">
            <img id="sigImgKingpickle" class="sig-pic" alt="Kingpickle">
            <div class="sig-line">Kingpickle</div>
            <div class="sig-title">Chairman & Architect</div>
          </div>
        </div>
      </div>
      <div style="margin-top:16px;">
        <button class="desk-button" style="background:var(--oxblood);padding:10px 24px;font-size:13px;" onclick="closeVictoryModal()">Return to Floor 4 Rotunda</button>
      </div>
    </div>
  </div>

  <!-- Script for 3D Game Engine -->
  <script>
    const ASSETS = __ASSETS_JSON__;

    // PROCEDURAL AUDIO ENGINE
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
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
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
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.15);
          gain.gain.setValueAtTime(0.35, audioCtx.currentTime + idx * 0.15);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + idx * 0.15 + 1.8);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.15);
          osc.stop(audioCtx.currentTime + idx * 0.15 + 1.9);
        });
      } catch(e) {}
    }

    // GAME STATE
    let currentFloor = 0; // 0 = Basement, 1 = Deng, 2 = Waiting, 3 = Operations, 4 = Penthouse
    let unlockedFloor = 0;

    let flickerr = {
      postageETH: 0.000,
      dengCredits: 0.0,
      tmfTokens: 0,
      reputation: 100,
      hasPass: false,
      chairName: "The Pavement",
      chairTier: "Unadmitted",
      seatsOwned: 0,
      briefcaseBalance: 0
    };

    // THREE.JS SETUP
    const canvas = document.getElementById('gameCanvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x2a1e16);
    scene.fog = new THREE.FogExp2(0x2a1e16, 0.012);

    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, 4.5, 9);

    // WARM 1987 CORPORATE LIGHTING
    const hemiLight = new THREE.HemisphereLight(0xfff5e6, 0x4a3222, 0.55);
    scene.add(hemiLight);

    const ambientLight = new THREE.AmbientLight(0xffeedd, 0.45);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xfffae6, 0.75);
    dirLight.position.set(8, 16, 8);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    scene.add(dirLight);

    // FLICKERR 3D CHARACTER
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // Character body construction
    const suitMat = new THREE.MeshLambertMaterial({ color: 0x2b221b }); // Charcoal/tweed suit
    const shirtMat = new THREE.MeshLambertMaterial({ color: 0xf6efe3 }); // Cream shirt
    const tieMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });   // Oxblood tie
    const skinMat = new THREE.MeshLambertMaterial({ color: 0xd4a373 });  // Skin
    const leatherMat = new THREE.MeshLambertMaterial({ color: 0x5a3619 }); // Briefcase leather

    // Torso
    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.75, 0.35), suitMat);
    torso.position.y = 1.0;
    torso.castShadow = true;
    playerGroup.add(torso);

    // Tie
    const tie = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.45, 0.05), tieMat);
    tie.position.set(0, 1.0, 0.18);
    playerGroup.add(tie);

    // Head
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.38), skinMat);
    head.position.y = 1.6;
    head.castShadow = true;
    playerGroup.add(head);

    // Hair
    const hairMat = new THREE.MeshLambertMaterial({ color: 0x1f140e });
    const hair = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.15, 0.4), hairMat);
    hair.position.y = 1.8;
    playerGroup.add(hair);

    // Legs
    const leftLeg = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.65, 0.22), suitMat);
    leftLeg.position.set(-0.16, 0.35, 0);
    leftLeg.castShadow = true;
    playerGroup.add(leftLeg);

    const rightLeg = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.65, 0.22), suitMat);
    rightLeg.position.set(0.16, 0.35, 0);
    rightLeg.castShadow = true;
    playerGroup.add(rightLeg);

    // Arms & Briefcase
    const leftArm = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.6, 0.18), suitMat);
    leftArm.position.set(-0.4, 0.95, 0);
    leftArm.castShadow = true;
    playerGroup.add(leftArm);

    const rightArm = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.6, 0.18), suitMat);
    rightArm.position.set(0.4, 0.95, 0);
    rightArm.castShadow = true;
    playerGroup.add(rightArm);

    // Briefcase in right hand
    const briefcase = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.38, 0.48), leatherMat);
    briefcase.position.set(0.48, 0.65, 0);
    briefcase.castShadow = true;
    playerGroup.add(briefcase);

    playerGroup.position.set(0, 0, 5);

    // INTERACTIVE OBJECTS & ROOM REGISTRY
    let interactiveObjects = [];
    let roomGroup = new THREE.Group();
    scene.add(roomGroup);

    // Textures builder from base64
    function loadTextureB64(b64) {
      const img = new Image();
      img.src = b64;
      const tex = new THREE.Texture(img);
      img.onload = () => { tex.needsUpdate = true; };
      tex.magFilter = THREE.NearestFilter;
      tex.minFilter = THREE.NearestFilter;
      return tex;
    }

    // BOSS BILLBOARDS
    let bossTextureWhat3verman = loadTextureB64(ASSETS.boss_what3verman);
    let bossTextureKingpickle = loadTextureB64(ASSETS.boss_kingpickle);

    // REBUILD 3D ENVIRONMENT FOR CURRENT FLOOR
    function buildFloorEnvironment() {
      // Clear previous room
      while(roomGroup.children.length > 0) {
        roomGroup.remove(roomGroup.children[0]);
      }
      interactiveObjects = [];

      // Ground plane (Rich walnut parquet, oxblood marble, or deep green executive marble)
      let floorColor = 0x482d1c; // Rich walnut
      if (currentFloor === 2) floorColor = 0x38201a; // Oxblood executive marble
      if (currentFloor === 4) floorColor = 0x1a3325; // Deep 1987 executive green marble

      const floorMat = new THREE.MeshLambertMaterial({ color: floorColor });
      const floorGeo = new THREE.PlaneGeometry(30, 30);
      const floorMesh = new THREE.Mesh(floorGeo, floorMat);
      floorMesh.rotation.x = -Math.PI / 2;
      floorMesh.receiveShadow = true;
      roomGroup.add(floorMesh);

      // Warm overhead chandelier
      const ceilingLight = new THREE.PointLight(0xfff7e8, 0.7, 22);
      ceilingLight.position.set(0, 3.8, 0);
      roomGroup.add(ceilingLight);

      // Walls (Warm corporate parchment paper)
      const wallMat = new THREE.MeshLambertMaterial({ color: (currentFloor === 0 ? 0xded2c1 : 0xf7f2e7) });
      
      // North Wall (with Elevator)
      const nWallLeft = new THREE.Mesh(new THREE.BoxGeometry(11, 4, 0.4), wallMat);
      nWallLeft.position.set(-7, 2, -10);
      nWallLeft.receiveShadow = true;
      roomGroup.add(nWallLeft);

      const nWallRight = new THREE.Mesh(new THREE.BoxGeometry(11, 4, 0.4), wallMat);
      nWallRight.position.set(7, 2, -10);
      nWallRight.receiveShadow = true;
      roomGroup.add(nWallRight);

      // North Wall Top Lintel above Elevator Doors
      const nWallTop = new THREE.Mesh(new THREE.BoxGeometry(4, 0.8, 0.4), wallMat);
      nWallTop.position.set(0, 3.6, -10);
      roomGroup.add(nWallTop);

      // Elevator Doors (North Center)
      const elevMat = new THREE.MeshStandardMaterial({ color: 0x9c7a3c, metalness: 0.8, roughness: 0.3 });
      const elevDoors = new THREE.Mesh(new THREE.BoxGeometry(3.5, 3.2, 0.3), elevMat);
      elevDoors.position.set(0, 1.6, -9.9);
      roomGroup.add(elevDoors);

      // Elevator Floor Indicator Light
      const lightMesh = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), new THREE.MeshBasicMaterial({ color: 0xe5c178 }));
      lightMesh.position.set(0, 3.4, -9.8);
      roomGroup.add(lightMesh);

      // Register Elevator trigger
      interactiveObjects.push({
        id: "elevator",
        label: "Take Elevator to Another Floor",
        pos: new THREE.Vector3(0, 0, -8.5),
        radius: 2.2,
        action: openElevatorModal
      });

      // Side Walls (South wall removed for clear diorama view)
      const wWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, 4, 20), wallMat);
      wWall.position.set(-12, 2, 0);
      roomGroup.add(wWall);

      const eWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, 4, 20), wallMat);
      eWall.position.set(12, 2, 0);
      roomGroup.add(eWall);

      // FLOOR-SPECIFIC PROPS
      if (currentFloor === 0) {
        buildBasementMailroom();
      } else if (currentFloor === 1) {
        buildFloor1Deng();
      } else if (currentFloor === 2) {
        buildFloor2Waiting();
      } else if (currentFloor === 3) {
        buildFloor3Operations();
      } else if (currentFloor === 4) {
        buildFloor4Penthouse();
      }

      updateTicker(`Flickerr stepped onto ${getFloorName(currentFloor)}.`);
    }

    // 1. BASEMENT MAILROOM
    function buildBasementMailroom() {
      // Historical Member Wall Portraits
      createWallPortrait(-6, 2.2, -9.7, 0, 'p_argon_1');
      createWallPortrait(6, 2.2, -9.7, 0, 'p_bogle_1');

      // Sorting Counter Desk
      createDesk(0, 0, 0, 6, 1.6, 0x3d2719);

      // Pneumatic Chutes along West Wall
      const chuteColors = [0x49698C, 0x4E8A5A, 0x9C5248, 0xB9902F, 0x6E5D8C];
      const chuteNames = ["Argon", "Bogle", "Smaug", "Midas", "Vladd"];
      for (let i = 0; i < 5; i++) {
        const cMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 3.2, 16), new THREE.MeshLambertMaterial({ color: chuteColors[i] }));
        cMesh.position.set(-11.5, 1.8, -6 + i * 2.8);
        roomGroup.add(cMesh);
      }

      // Public Errand Dispatch Lever Console
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

      // Secure First Chair: The Intern's Folding Chair in corner
      createChair(8, 0, -6, 0x6b5f4e, "Folding Chair");
      interactiveObjects.push({
        id: "chair_folding",
        label: "Secure The Intern's Folding Chair",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.0,
        action: () => secureChairOnFloor("The Interns Folding Chair", "Class I Intern")
      });
    }

    // 2. FLOOR 1: DENG DESK
    function buildFloor1Deng() {
      // Historical Member Wall Portraits
      createWallPortrait(-6, 2.2, -9.7, 0, 'p_smaug_1');
      createWallPortrait(6, 2.2, -9.7, 0, 'p_midas_1');
      createWallPortrait(-11.7, 2.2, 0, Math.PI/2, 'p_vladd_1');

      createDesk(0, 0, -1, 7, 2.0, 0x4a3222);

      // ApeChain CRT Terminal with Green Phosphor Glow
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
        label: "Examine Deng Desk ApeChain Slips & Forge Pass",
        pos: new THREE.Vector3(0, 0, 1.2),
        radius: 2.5,
        action: openDengModal
      });

      // Swivel Chair to secure
      createChair(6, 0, 2, 0x7a5835, "Creaking Wooden Swivel");
      interactiveObjects.push({
        id: "chair_swivel",
        label: "Secure Creaking Wooden Swivel Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.0,
        action: () => secureChairOnFloor("Creaking Wooden Swivel", "Class II Clerk")
      });
    }

    // 3. FLOOR 2: WAITING ROOM & ADMISSIONS
    function buildFloor2Waiting() {
      // Historical Member Wall Portraits
      createWallPortrait(-6, 2.2, -9.7, 0, 'p_argon_2');
      createWallPortrait(6, 2.2, -9.7, 0, 'p_bogle_2');
      createWallPortrait(-11.7, 2.2, -2, Math.PI/2, 'p_smaug_2');
      createWallPortrait(11.7, 2.2, -2, -Math.PI/2, 'p_midas_2');

      // Subscription Desk (West)
      createDesk(-6, 0, 0, 4, 1.8, 0x422a1b);
      // Admissions Counter (East)
      createDesk(6, 0, 0, 4, 1.8, 0x422a1b);

      // Oxblood leather benches
      const benchMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });
      const bench = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.6, 5), benchMat);
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

      // Task Chair to secure
      createChair(0, 0, -4, 0xb08a3c, "Beige Task Chair");
      interactiveObjects.push({
        id: "chair_task",
        label: "Secure Beige Task Chair",
        pos: new THREE.Vector3(0, 0, -4),
        radius: 2.0,
        action: () => secureChairOnFloor("Beige Task Chair", "Class III Executive")
      });
    }

    // 4. FLOOR 3: OPERATIONS FLOOR (BOSS: WHAT3VERMAN)
    function buildFloor3Operations() {
      // Historical Member Wall Portraits
      createWallPortrait(-6, 2.2, -9.7, 0, 'p_midas_2');
      createWallPortrait(6, 2.2, -9.7, 0, 'p_vladd_2');
      createWallPortrait(-11.7, 2.2, 0, Math.PI/2, 'p_argon_3');
      createWallPortrait(11.7, 2.2, 0, -Math.PI/2, 'p_bogle_3');

      createDesk(0, 0, -2, 6, 2.2, 0x2e1c12);

      // what3verman Boss Billboard
      const bossMat = new THREE.MeshBasicMaterial({ map: bossTextureWhat3verman });
      const bossQuad = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.8), bossMat);
      bossQuad.position.set(0, 1.8, -3.2);
      roomGroup.add(bossQuad);

      // Oxblood Wingback behind desk
      createChair(0, 0, -3.2, 0x7a2e2e, "Oxblood Wingback");

      // Banker's Lamp with Green Glow
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

      // Green Banker's Chair reward
      createChair(-6, 0, 2, 0x2f6b3d, "Green Bankers Chair");
      interactiveObjects.push({
        id: "chair_bankers",
        label: "Secure Green Bankers Chair",
        pos: new THREE.Vector3(-6, 0, 2),
        radius: 2.0,
        action: () => secureChairOnFloor("Green Bankers Chair", "Class IV Officer")
      });
    }

    // 5. FLOOR 4: EXECUTIVE ROTUNDA (FINAL BOSS: KINGPICKLE & SEAT 0)
    function buildFloor4Penthouse() {
      // Historical Member Wall Portraits
      createWallPortrait(-6, 2.2, -9.7, 0, 'p_smaug_3');
      createWallPortrait(6, 2.2, -9.7, 0, 'p_midas_3');
      createWallPortrait(-11.7, 2.2, 0, Math.PI/2, 'p_vladd_3');
      createWallPortrait(11.7, 2.2, 0, -Math.PI/2, 'p_argon_4');

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
      const seat0Mat = new THREE.MeshLambertMaterial({ color: 0x5e2222 }); // Deep oxblood mahogany
      const seat0 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.6, 1.2), seat0Mat);
      seat0.position.set(0, 1.1, 0);
      roomGroup.add(seat0);

      // Seat 0 Heavenly Skylight Glow
      const seat0Light = new THREE.PointLight(0xfffae6, 1.2, 8);
      seat0Light.position.set(0, 3.5, 0);
      roomGroup.add(seat0Light);

      // Kingpickle Boss Billboard standing beside dais
      const kpMat = new THREE.MeshBasicMaterial({ map: bossTextureKingpickle });
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
      createChair(-5, 0, -2, 0xd4af37, "The Gilded Throne");
      interactiveObjects.push({
        id: "chair_throne",
        label: "Ascend to The Gilded Throne (Class VII)",
        pos: new THREE.Vector3(-5, 0, -2),
        radius: 2.2,
        action: () => secureChairOnFloor("The Gilded Throne", "Class VII Sovereign")
      });
    }

    // HELPER: BUILD WALL-MOUNTED GILDED PORTRAIT
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

    // HELPER: BUILD 3D DESK
    function createDesk(x, y, z, w, d, color) {
      const deskMat = new THREE.MeshLambertMaterial({ color: color });
      const top = new THREE.Mesh(new THREE.BoxGeometry(w, 0.15, d), deskMat);
      top.position.set(x, y + 1.0, z);
      top.castShadow = true;
      roomGroup.add(top);

      const leg1 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.0, 0.2), deskMat);
      leg1.position.set(x - w/2 + 0.2, y + 0.5, z - d/2 + 0.2);
      roomGroup.add(leg1);

      const leg2 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.0, 0.2), deskMat);
      leg2.position.set(x + w/2 - 0.2, y + 0.5, z - d/2 + 0.2);
      roomGroup.add(leg2);

      const leg3 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.0, 0.2), deskMat);
      leg3.position.set(x - w/2 + 0.2, y + 0.5, z + d/2 - 0.2);
      roomGroup.add(leg3);

      const leg4 = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.0, 0.2), deskMat);
      leg4.position.set(x + w/2 - 0.2, y + 0.5, z + d/2 - 0.2);
      roomGroup.add(leg4);

      // 1987 Green Banker's Lamp
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
    function createChair(x, y, z, color, label) {
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
    }

    function getFloorName(f) {
      if (f === 0) return "Floor B (Mailroom)";
      if (f === 1) return "Floor 1 (The Deng Desk)";
      if (f === 2) return "Floor 2 (Subscription & Admissions)";
      if (f === 3) return "Floor 3 (Operations - Boss: what3verman)";
      if (f === 4) return "Floor 4 (Rotunda - Boss: Kingpickle & Seat 0)";
      return `Floor ${f}`;
    }

    // INTERACTION MODALS
    const modalEl = document.getElementById('taskModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBadge = document.getElementById('modalBadge');
    const modalInstructions = document.getElementById('modalInstructions');
    const modalBody = document.getElementById('modalBody');

    // IN-GAME NOTIFICATION & VICTORY MODAL HANDLERS
    function showMemoToast(title, body) {
      const toast = document.getElementById('memoToast');
      document.getElementById('memoToastTitle').innerText = title;
      document.getElementById('memoToastBody').innerText = body;
      toast.classList.add('show');
      playStampThump();
      setTimeout(() => {
        toast.classList.remove('show');
      }, 4500);
    }

    function showVictoryModal() {
      playBell();
      if (document.getElementById('sigImgWhat3verman')) document.getElementById('sigImgWhat3verman').src = ASSETS.boss_what3verman;
      if (document.getElementById('sigImgKingpickle')) document.getElementById('sigImgKingpickle').src = ASSETS.boss_kingpickle;
      document.getElementById('victoryModal').style.display = 'flex';
    }

    function closeVictoryModal() {
      playClick();
      document.getElementById('victoryModal').style.display = 'none';
    }

    function openElevatorModal() {
      playElevatorDing();
      modalTitle.innerText = "Elevator Concourse";
      modalBadge.innerText = "BRASS ELEVATOR DIAL";
      modalInstructions.innerText = "Select a floor to ride the elevator. Floors unlock as you complete tasks and promotions.";

      let buttonsHtml = '';
      for (let i = 0; i <= 4; i++) {
        const unlocked = i <= unlockedFloor;
        buttonsHtml += `
          <div class="elevator-floor-btn ${unlocked ? '' : 'locked'}" onclick="${unlocked ? `rideElevatorTo(${i})` : `showMemoToast('FLOOR RESTRICTED', 'Floor locked. Complete current floor duties to unlock elevator access.')`}">
            <span>${getFloorName(i)}</span>
            <span>${unlocked ? 'OPEN ➔' : 'LOCKED 🔒'}</span>
          </div>
        `;
      }

      modalBody.innerHTML = `<div class="elevator-panel">${buttonsHtml}</div>`;
      modalEl.classList.add('active');
    }

    function rideElevatorTo(f) {
      closeTaskModal();
      playElevatorDing();
      currentFloor = f;
      playerGroup.position.set(0, 0, -6.5);
      buildFloorEnvironment();
      updateHUD();
      showMemoToast("ELEVATOR ARRIVAL", `Flickerr stepped onto ${getFloorName(currentFloor)}.`);
    }

    // MODAL: MAILROOM CHUTES
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
        mailroomIndex++;
        updateTicker(`CHUTE ROUTED: Successfully deposited into ${fund.toUpperCase()} book. +0.010 ETH Postage.`);
      } else {
        playClick();
        updateTicker(`CHUTE REJECT: Incorrect philosophy match.`);
      }

      if (flickerr.postageETH >= 0.050 && unlockedFloor < 1) {
        unlockedFloor = 1;
        showMemoToast("ELEVATOR CLEARANCE", "You earned 0.050 ETH in Postage tips. Floor 1 (The Deng Desk) is now unlocked.");
      }

      openMailroomChuteModal();
      updateHUD();
    }

    function pullDispatchLever() {
      playStampThump();
      flickerr.postageETH += 0.010;
      updateTicker("DISPATCH PULLED: Public rebalance errand run on-chain. +0.010 ETH.");
      if (flickerr.postageETH >= 0.050 && unlockedFloor < 1) {
        unlockedFloor = 1;
        showMemoToast("ELEVATOR CLEARANCE", "You earned 0.050 ETH in Postage tips. Floor 1 (The Deng Desk) is now unlocked.");
      }
      updateHUD();
    }

    // MODAL: DENG DESK
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
          <button class="desk-button" style="flex:1;background:var(--lamp);" onclick="tenderDengSlip(1.5)">
            Audit & Tender Verified Deng Slip (+1.50 Credits)
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
      updateTicker(`DENG CREDITED: Tendered ApeChain voucher. +${cr} Credits.`);
      openDengModal();
      updateHUD();
    }

    function forgePassAction() {
      if (flickerr.dengCredits < 10.0) {
        playClick();
        showMemoToast("TENDER DEFICIT", "The Deng Desk requires at least 10.00 credits to forge a TMF Pass.");
        return;
      }
      playBell();
      flickerr.hasPass = true;
      unlockedFloor = Math.max(unlockedFloor, 2);
      showMemoToast("TMF PASS FORGED", "A soulbound pass has been minted into Flickerr's satchel. Floor 2 (Admissions) is now unlocked.");
      closeTaskModal();
      updateHUD();
    }

    // MODAL: SUBSCRIPTION
    function openSubscriptionModal() {
      playClick();
      modalTitle.innerText = "Subscription Desk";
      modalBadge.innerText = "BURNING KILN";
      modalInstructions.innerText = "Burn your soulbound TMF Pass at 0.01 ETH to mint 2 Seats and bind your ERC-6551 Briefcase.";

      modalBody.innerHTML = `
        <div style="text-align:center;padding:16px;">
          <p style="font-size:13px;margin-bottom:14px;">
            ${flickerr.hasPass ? 'You hold a soulbound TMF Pass. Ready for consumption.' : 'You do not hold a TMF Pass. Visit Floor 1.'}
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
        showMemoToast("PASS REQUIRED", "You must forge a TMF Pass at the Deng Desk on Floor 1 first.");
        return;
      }
      playStampThump();
      flickerr.seatsOwned = 2;
      flickerr.tmfTokens = 401000;
      flickerr.chairName = "The Interns Folding Chair";
      flickerr.chairTier = "Class I Intern";
      showMemoToast("PASS CONSUMED", "2 Seats minted into The Bogle Fund. Briefcase bound on-chain.");
      closeTaskModal();
      updateHUD();
    }

    // MODAL: ADMISSIONS DESK
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
      unlockedFloor = Math.max(unlockedFloor, 3);
      showMemoToast("STAMP AFFIXED", `Dossier marked ${verdict}. Operations floor (Floor 3) is now unlocked.`);
      closeTaskModal();
      updateHUD();
    }

    // MODAL: WHAT3VERMAN (BOSS 1)
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
        unlockedFloor = 4;
        flickerr.chairName = "Green Bankers Chair";
        flickerr.chairTier = "Class IV Officer";
        showMemoToast("WHAT3VERMAN AUDIT PASSED", "The arithmetic is sound. Brass keycard to Floor 4 Rotunda issued.");
        closeTaskModal();
        updateHUD();
      } else {
        playClick();
        showMemoToast("POLICY VIOLATION", "what3verman frowns: 'Incorrect. Re-read brand-guide.md.'");
      }
    }

    // MODAL: KINGPICKLE & SEAT 0 (FINAL BOSS)
    function openKingpickleModal() {
      playClick();
      modalTitle.innerText = "Final Boss: Kingpickle & Seat 0";
      modalBadge.innerText = "THE EXECUTIVE ROTUNDA";
      modalInstructions.innerText = "Kingpickle stands before Seat 0. It is 19:59 UTC. Cast the decisive vote before the Closing Bell tolls.";

      modalBody.innerHTML = `
        <div style="display:grid;grid-template-columns:110px 1fr;gap:12px;margin-bottom:14px;">
          <img src="${ASSETS.boss_kingpickle}" style="width:100px;height:100px;border:2px solid var(--gold);object-fit:cover;" alt="Kingpickle">
          <div style="font-size:12px;line-height:1.45;font-style:italic;background:var(--paper-sunken);padding:10px;">
            "Welcome to the top, Flickerr. The market cracked at 19:45 UTC. The five books need quorum before the 20:00 bell tolls. Cast your briefcase vote for the Continuation Clause."
          </div>
        </div>
        <button class="desk-button" style="background:var(--lamp);width:100%;font-size:13px;padding:10px;" onclick="castFinalVoteAction()">
          Cast Decisive Vote: Preserve the Five Funds in Perpetuity 🔔
        </button>
      `;
      modalEl.classList.add('active');
    }

    function castFinalVoteAction() {
      flickerr.chairName = "The Gilded Throne";
      flickerr.chairTier = "Class VII Sovereign";
      closeTaskModal();
      showVictoryModal();
      updateTicker("VICTORY: CLOSING BELL TOLLS. FLICKERR CONFIRMED PERMANENT TRUSTEE.");
      updateHUD();
    }

    // SECURE CHAIR ACTION
    function secureChairOnFloor(name, tier) {
      playStampThump();
      flickerr.chairName = name;
      flickerr.chairTier = tier;
      updateTicker(`CHAIR SECURED: Flickerr claimed ${name} (${tier})!`);
      showMemoToast("CHAIR CLAIMED", `Flickerr claimed ${name} (${tier}). Building status elevated.`);
      updateHUD();
    }

    function closeTaskModal() {
      playClick();
      modalEl.classList.remove('active');
    }

    function updateHUD() {
      document.getElementById('hudFloor').innerText = getFloorName(currentFloor);
      document.getElementById('hudChair').innerText = flickerr.chairName;
      document.getElementById('hudPostage').innerText = `${flickerr.postageETH.toFixed(3)} ETH`;
      document.getElementById('hudDeng').innerText = flickerr.dengCredits.toFixed(2);
      document.getElementById('hudTmf').innerText = flickerr.tmfTokens.toLocaleString();
      document.getElementById('floorIndicatorText').innerText = `CURRENT FLOOR: ${getFloorName(currentFloor).toUpperCase()}`;
    }

    function updateTicker(msg) {
      document.getElementById('tickerText').innerText = `LOBBY TICKER: ${msg.toUpperCase()}`;
    }

    // INPUT & 3D CONTROLS
    const keys = {};
    window.addEventListener('keydown', (e) => {
      keys[e.key.toLowerCase()] = true;
      if (e.key === 'e' || e.key === 'E' || e.key === ' ') {
        checkInteractions();
      }
    });
    window.addEventListener('keyup', (e) => {
      keys[e.key.toLowerCase()] = false;
    });

    let cameraAngle = 0;

    function checkInteractions() {
      if (modalEl.classList.contains('active')) return;
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

      // Camera rotation controls (Q / E)
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

      if (isMoving && !modalEl.classList.contains('active')) {
        const moveVec = new THREE.Vector3(moveX, 0, moveZ).normalize();
        moveVec.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraAngle);

        const speed = 0.12;
        playerGroup.position.x += moveVec.x * speed;
        playerGroup.position.z += moveVec.z * speed;

        // Player rotation towards movement direction
        const targetRot = Math.atan2(moveVec.x, moveVec.z);
        playerGroup.rotation.y = targetRot;

        // Walking leg & arm bobbing animation
        walkClock += 0.2;
        leftLeg.rotation.x = Math.sin(walkClock) * 0.45;
        rightLeg.rotation.x = -Math.sin(walkClock) * 0.45;
        leftArm.rotation.x = -Math.sin(walkClock) * 0.45;
        rightArm.rotation.x = Math.sin(walkClock) * 0.35;
        torso.position.y = 1.0 + Math.abs(Math.sin(walkClock * 2)) * 0.04;

        if (Math.sin(walkClock) > 0.9) playStep();

        // Boundaries
        playerGroup.position.x = Math.max(-10.5, Math.min(10.5, playerGroup.position.x));
        playerGroup.position.z = Math.max(-8.5, Math.min(8.5, playerGroup.position.z));
      } else {
        // Reset limbs
        leftLeg.rotation.x = 0;
        rightLeg.rotation.x = 0;
        leftArm.rotation.x = 0;
        rightArm.rotation.x = 0;
        torso.position.y = 1.0;
      }

      // Smooth Follow Camera
      const camDist = 6.5;
      const camHeight = 4.2;
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

    // WINDOW RESIZE
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // STARTUP
    buildFloorEnvironment();
    updateHUD();
    animate();
  </script>
</body>
</html>
"""

# Replace placeholders
final_html = html_template.replace('__MEDALLION_B64__', assets.get('medallion', ''))
final_html = final_html.replace('__ASSETS_JSON__', json.dumps(assets))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

brain_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated full 3D moveable game index.html successfully.")
