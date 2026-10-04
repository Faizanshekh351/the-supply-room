import json
import base64
import os

print("Generating Custom 1987 Chair Arbitrage Arena with Multi-Track Music & Canvas-Rendered Countdown...")

with open("assets_encoded.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

print(f"Loaded {len(assets)} assets.")

# Build HTML template
html_template = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>The Supply Room · 1987 Corporate Odyssey</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=IBM+Plex+Mono:ital,wght@0,400;0,600;0,700;1,400&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <style>
    :root {
      --ink: #211b14;
      --ink-muted: #6b5f4e;
      --paper: #f4ecdc;
      --paper-raised: #fbf7ee;
      --paper-dim: #e4d8c1;
      --rule: #c8b99c;
      --rule-subtle: #dbcfb7;
      --oxblood: #7a2e2e;
      --oxblood-soft: #a84848;
      --lamp: #b08a3c;
      --green: #2f6b3d;
      --green-soft: #425440;
      --edge: #3d2314;
      --bogle: #57a671;
      --argon: #5b8ac2;
      --smaug: #c97258;
      --midas: #d19a19;
      --vladd: #977bc4;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #0d0a07;
      font-family: 'Libre Caslon Text', Georgia, serif;
      color: var(--ink);
    }

    .hidden { display: none !important; }

    #canvas3d {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
    }

    /* CRT SCANLINE OVERLAY */
    .crt-overlay {
      position: absolute;
      inset: 0;
      pointer-events: none;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%),
                  linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
      background-size: 100% 3px, 4px 100%;
      z-index: 10;
      opacity: 0.5;
    }

    /* HUD TOP BAR */
    .hud-panel {
      position: absolute;
      top: 16px;
      left: 16px;
      background: var(--paper-raised);
      border: 3px solid var(--ink);
      box-shadow: 0 8px 24px rgba(0,0,0,0.6), inset 0 0 0 1px var(--rule);
      padding: 12px 18px;
      z-index: 20;
      max-width: 440px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .hud-medallion {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      border: 2px solid var(--lamp);
      box-shadow: 0 0 8px rgba(176, 138, 60, 0.5);
      flex-shrink: 0;
      background: #110c08;
      object-fit: cover;
    }
    .hud-details h1 {
      font-family: 'Cinzel', serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: var(--oxblood);
      text-transform: uppercase;
      line-height: 1.2;
    }
    .hud-details .sub {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: var(--ink-muted);
      margin-top: 2px;
    }
    .hud-stats-row {
      display: flex;
      gap: 12px;
      margin-top: 6px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 600;
    }
    .hud-stat-badge {
      background: var(--paper-dim);
      border: 1px solid var(--rule);
      padding: 2px 7px;
      border-radius: 2px;
    }

    /* TOP RIGHT CONTROLS */
    .hud-controls-top {
      position: absolute;
      top: 16px;
      right: 16px;
      display: flex;
      gap: 8px;
      z-index: 20;
    }
    .hud-btn {
      background: var(--paper-raised);
      border: 2px solid var(--ink);
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 8px 14px;
      cursor: pointer;
      color: var(--ink);
      box-shadow: 0 4px 10px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }
    .hud-btn:hover {
      background: var(--ink);
      color: var(--paper-raised);
      transform: translateY(-1px);
    }

    /* FLOATING INTERACTION PROMPT */
    .interact-prompt {
      position: absolute;
      bottom: 40px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--ink);
      color: var(--paper);
      font-family: 'IBM Plex Mono', monospace;
      font-size: 13px;
      padding: 10px 22px;
      border: 2px solid var(--lamp);
      box-shadow: 0 6px 20px rgba(0,0,0,0.8);
      z-index: 20;
      display: none;
      letter-spacing: 0.5px;
      animation: promptPulse 1.4s infinite alternate ease-in-out;
    }
    @keyframes promptPulse {
      0% { transform: translateX(-50%) scale(1); }
      100% { transform: translateX(-50%) scale(1.04); }
    }

    /* TOAST NOTIFICATION */
    .toast-memo {
      position: absolute;
      bottom: 24px;
      right: 24px;
      background: var(--paper-raised);
      border-left: 5px solid var(--oxblood);
      border-top: 2px solid var(--ink);
      border-right: 2px solid var(--ink);
      border-bottom: 2px solid var(--ink);
      padding: 12px 18px;
      max-width: 340px;
      z-index: 50;
      box-shadow: 0 10px 30px rgba(0,0,0,0.7);
      font-size: 12px;
      display: none;
      animation: slideToast 0.3s ease;
    }
    @keyframes slideToast {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* GENERAL MODAL BACKDROP */
    .modal-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(10, 8, 6, 0.88);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 60;
      padding: 20px;
    }
    .modal-backdrop.active { display: flex; }

    .modal-window {
      background: var(--paper-raised);
      border: 4px solid var(--ink);
      box-shadow: 0 25px 60px rgba(0,0,0,0.9), inset 0 0 0 1px var(--rule);
      max-width: 620px;
      width: 100%;
      padding: 24px;
      position: relative;
    }
    .modal-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--rule);
      padding-bottom: 10px;
      margin-bottom: 14px;
    }
    .modal-header-row h3 {
      font-family: 'Cinzel', serif;
      font-size: 18px;
      color: var(--oxblood);
      letter-spacing: 1px;
    }

    .desk-button {
      background: var(--ink);
      color: var(--paper);
      border: none;
      padding: 10px 18px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 0 #000;
      transition: all 0.1s;
    }
    .desk-button:hover { background: var(--oxblood); }
    .desk-button:active { transform: translateY(2px); box-shadow: 0 2px 0 #000; }
    .desk-button.secondary {
      background: var(--paper-dim);
      color: var(--ink);
      border: 1px solid var(--ink);
      box-shadow: 0 3px 0 var(--rule);
    }
    .desk-button.secondary:hover { background: #d7c9ad; }

    /* ==========================================================================
       CUSTOM 1987 CHAIR ARBITRAGE ARENA (The Mutual Fun Private Chamber)
       Unique bespoke design with brass marquetry, needle scratch & phonograph
       ========================================================================== */
    .musical-arena-overlay {
      position: absolute;
      inset: 0;
      background: rgba(6, 4, 3, 0.94);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 70;
      padding: 14px;
    }
    .musical-arena-overlay.active { display: flex; }

    .chamber-cabinet {
      width: 1140px;
      max-width: 98vw;
      max-height: 94vh;
      display: flex;
      flex-direction: column;
      background: #fbf7ee;
      border: 6px solid var(--edge);
      box-shadow: 0 0 0 3px #b08a3c, 0 0 0 7px #2a150c, 16px 20px 0 rgba(10, 6, 4, 0.88);
      position: relative;
      overflow: hidden;
    }

    .chamber-header {
      min-height: 70px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 24px;
      background: #2a160d;
      border-bottom: 4px solid var(--lamp);
      box-shadow: inset 0 2px #54311c, inset 0 -2px #150904;
    }
    .chamber-brand {
      display: flex;
      align-items: center;
      gap: 14px;
      color: #f7e7bd;
    }
    .chamber-seal {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      border: 2px solid var(--lamp);
      object-fit: cover;
      background: #110b06;
      flex-shrink: 0;
    }
    .chamber-title-text h2 {
      font-family: 'Cinzel', serif;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: #ffd875;
      text-transform: uppercase;
      line-height: 1.2;
    }
    .chamber-title-text small {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      color: #d1bda2;
      display: block;
      margin-top: 2px;
    }
    .chamber-head-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .chamber-btn {
      padding: 8px 16px;
      background: #efe4d0;
      border: 2px solid #3d2314;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      color: #2a160d;
      box-shadow: 2px 2px #150904;
      transition: all 0.1s;
    }
    .chamber-btn:hover { background: #fff; transform: translateY(-1px); }
    .chamber-btn:active { transform: translateY(1px); }

    .chamber-body {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 290px;
      gap: 14px;
      padding: 14px;
      background: #442a1b;
      overflow-y: auto;
    }

    .chamber-stage {
      min-width: 0;
      border: 4px solid var(--edge);
      background: #fdfaf2;
      box-shadow: 0 8px 24px rgba(0,0,0,0.4);
      display: flex;
      flex-direction: column;
    }

    .chamber-stage-top {
      min-height: 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 8px 18px;
      color: #ffd875;
      background: #1f1008;
      border-bottom: 3px solid var(--lamp);
      font-family: 'IBM Plex Mono', monospace;
      font-size: 12px;
      letter-spacing: 0.5px;
    }

    .chamber-signal-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 3px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
    .chamber-signal-pill.waiting {
      background: #382419;
      color: #d1bda2;
      border: 1px solid #6b4c37;
    }
    .chamber-signal-pill.green {
      background: #1e4526;
      color: #bdf2c7;
      border: 1px solid #3ca851;
      animation: pulseGreenPill 0.8s infinite alternate;
    }
    .chamber-signal-pill.red {
      background: #6e1c1c;
      color: #ffc4c4;
      border: 1px solid #c73636;
      animation: pulseRedPill 0.25s infinite alternate;
    }
    @keyframes pulseGreenPill { 0% { opacity: 0.75; } 100% { opacity: 1; filter: brightness(1.2); } }
    @keyframes pulseRedPill { 0% { opacity: 0.8; } 100% { opacity: 1; filter: brightness(1.35); } }

    .chamber-scene-wrap {
      position: relative;
      aspect-ratio: 16/9;
      background: #1c110b;
      overflow: hidden;
    }
    #chamberCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .scene-canvas-flash {
      animation: arenaFlashBorder 0.15s 2;
    }
    @keyframes arenaFlashBorder {
      50% { filter: brightness(1.3) contrast(1.2); }
    }

    /* SCENE OVERLAYS (Intro, Result) */
    .chamber-overlay {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(14, 9, 6, 0.75);
      z-index: 5;
      padding: 18px;
    }

    .chamber-card {
      width: 460px;
      max-width: 95%;
      padding: 24px 22px;
      text-align: center;
      background: #fbf6ec;
      border: 4px solid var(--ink);
      box-shadow: inset 0 0 0 3px var(--lamp), 0 15px 40px rgba(0,0,0,0.8);
    }
    .chamber-card-eyebrow {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: var(--oxblood);
      text-transform: uppercase;
    }
    .chamber-card h2 {
      font-family: 'Cinzel', serif;
      font-size: 20px;
      line-height: 1.3;
      margin: 10px 0 12px;
      color: var(--ink);
      letter-spacing: 1px;
    }
    .chamber-card p {
      font-size: 13px;
      line-height: 1.45;
      color: var(--ink-muted);
      margin-bottom: 16px;
    }
    .chamber-contenders-preview {
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-bottom: 18px;
    }
    .chamber-thumb {
      width: 52px;
      height: 52px;
      border-radius: 50%;
      border: 2px solid var(--lamp);
      background: #110b06;
      object-fit: cover;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .primary-chamber-btn {
      width: 100%;
      background: var(--oxblood);
      border: 2px solid #381212;
      color: #fff;
      padding: 14px;
      font-family: 'Cinzel', serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 5px 0 #2b0b0b;
      transition: all 0.1s;
    }
    .primary-chamber-btn:hover { background: #943939; }
    .primary-chamber-btn:active { transform: translateY(3px); box-shadow: 0 2px 0 #2b0b0b; }

    /* CONTROL DECK */
    .chamber-control-deck {
      min-height: 84px;
      padding: 12px 20px;
      display: flex;
      gap: 16px;
      align-items: center;
      border-top: 3px solid var(--rule);
      background: #f4ecd9;
    }
    .chamber-control-deck > div { flex: 1; }
    .deck-hint {
      font-size: 13px;
      line-height: 1.35;
      color: var(--ink);
      margin-top: 3px;
    }
    .deck-eyebrow {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 1px;
      color: var(--ink-muted);
      text-transform: uppercase;
    }

    #chamberSitBtn {
      background: var(--oxblood);
      color: #fff;
      border: 3px solid #3b1212;
      box-shadow: 0 5px 0 #240a0a;
      min-width: 190px;
      padding: 12px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      font-family: 'Cinzel', serif;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.1s;
    }
    #chamberSitBtn kbd {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      padding: 2px 8px;
      border: 1px solid #ff9999;
      background: #541414;
      color: #ffe6e6;
      border-radius: 2px;
    }
    #chamberSitBtn:not(:disabled):active {
      transform: translateY(3px);
      box-shadow: 0 2px 0 #240a0a;
    }
    #chamberSitBtn:disabled {
      filter: grayscale(0.8);
      opacity: 0.55;
      cursor: not-allowed;
      box-shadow: none;
    }

    /* ASIDE SIDEBAR */
    .chamber-aside {
      padding: 16px 14px;
      background: #efe5d1;
      border: 3px solid var(--edge);
      box-shadow: inset 0 0 0 1px var(--rule);
    }
    .aside-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      margin-bottom: 14px;
      border-bottom: 2px solid var(--rule);
    }
    .aside-title-row h4 {
      font-family: 'Cinzel', serif;
      font-size: 12px;
      color: var(--oxblood);
      letter-spacing: 1px;
    }
    .aside-count-badge {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      background: var(--ink);
      padding: 2px 8px;
      color: #fff;
      border-radius: 2px;
    }

    .roster-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .roster-person {
      display: flex;
      gap: 10px;
      align-items: center;
      background: #fbf7ee;
      padding: 6px 10px;
      border: 1px solid var(--rule);
    }
    .roster-person img {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid var(--lamp);
    }
    .roster-person strong {
      display: block;
      font-family: 'Libre Caslon Text', serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--ink);
    }
    .roster-person small {
      display: block;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: var(--ink-muted);
    }
    .roster-person .you-tag {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      color: #fff;
      background: var(--green);
      padding: 2px 6px;
      margin-left: auto;
      border-radius: 2px;
    }
    .roster-person.out {
      opacity: 0.45;
      text-decoration: line-through;
      background: #e2d6c1;
    }
    .roster-person.out img {
      filter: grayscale(1);
    }

    .chamber-rules-box {
      margin-top: 18px;
      padding-top: 14px;
      border-top: 2px solid var(--rule);
      font-size: 12px;
    }
    .rules-item {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      margin: 8px 0;
      line-height: 1.35;
      color: var(--ink-muted);
    }
    .dot-green, .dot-red {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
      margin-top: 3px;
    }
    .dot-green { background: #2f6b3d; }
    .dot-red { background: #8a2424; }

    .chamber-reflex-stat {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 2px solid var(--rule);
      margin-top: 14px;
      padding-top: 12px;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
    }
    .chamber-reflex-stat strong {
      font-size: 13px;
      color: var(--oxblood);
    }

    /* ==========================================================================
       CERTIFICATE OF EMPLOYMENT (1200x675 Canvas Modal)
       ========================================================================== */
    .cert-modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(10, 8, 6, 0.94);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 80;
      padding: 16px;
    }
    .cert-modal-overlay.active { display: flex; }
    .cert-container {
      max-width: 1060px;
      width: 100%;
      text-align: center;
    }
    #certCanvas {
      width: 100%;
      height: auto;
      max-height: 80vh;
      border: 4px solid var(--lamp);
      box-shadow: 0 20px 60px rgba(0,0,0,0.9);
      background: #fbf7ee;
      margin-bottom: 14px;
      display: block;
    }
  </style>
</head>
<body>
  <!-- Three.js 3D Viewport -->
  <canvas id="canvas3d"></canvas>
  <div class="crt-overlay"></div>

  <!-- HUD Top Left -->
  <div class="hud-panel">
    <img id="hudMedallion" class="hud-medallion" alt="TMF Seal">
    <div class="hud-details">
      <h1 id="hudRole">Applicant</h1>
      <div class="sub" id="hudFloor">The Pavement · Outside Gate</div>
      <div class="hud-stats-row">
        <span class="hud-stat-badge" id="hudDept">The Bogle Fund</span>
        <span class="hud-stat-badge" id="hudChair">No Chair Secured</span>
        <span class="hud-stat-badge" id="hudScore">0 Pts</span>
      </div>
    </div>
  </div>

  <!-- HUD Top Right Controls -->
  <div class="hud-controls-top">
    <button class="hud-btn" onclick="openElevatorModal()">
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
    </button>
  </div>

  <!-- Floating Proximity Prompt -->
  <div class="interact-prompt" id="interactPrompt">[E] Inspect Gate</div>

  <!-- Toast Memo -->
  <div class="toast-memo" id="toastMemo">
    <strong id="toastTitle">MEMORANDUM</strong>
    <p id="toastBody" style="margin-top:4px;color:var(--ink-muted);"></p>
  </div>

  <!-- Standard Office Modal -->
  <div class="modal-backdrop" id="taskModal">
    <div class="modal-window">
      <div class="modal-header-row">
        <h3 id="modalTitle">DISPATCH TERMINAL</h3>
        <span style="font-family:'IBM Plex Mono';font-size:10px;color:var(--ink-muted);" id="modalSubtitle">REF: 1987-TMF</span>
      </div>
      <div id="modalBody"></div>
      <div style="margin-top:18px;display:flex;justify-content:flex-end;gap:10px;">
        <button class="desk-button secondary" onclick="closeTaskModal()">Step Back</button>
      </div>
    </div>
  </div>

  <!-- Elevator Concourse Modal -->
  <div class="modal-backdrop" id="elevatorModal">
    <div class="modal-window">
      <div class="modal-header-row">
        <h3>ELEVATOR CONCOURSE</h3>
        <span style="font-family:'IBM Plex Mono';font-size:11px;color:var(--lamp);">BRASS CAR C-4</span>
      </div>
      <p style="font-size:13px;color:var(--ink-muted);margin-bottom:14px;">
        Floor clearance is governed by review points and chair ownership. Select an authorized destination:
      </p>
      <div id="elevatorFloorList" style="display:flex;flex-direction:column;gap:8px;max-height:360px;overflow-y:auto;padding-right:6px;"></div>
      <div style="margin-top:18px;display:flex;justify-content:flex-end;">
        <button class="desk-button secondary" onclick="closeElevatorModal()">Remain on Floor</button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       CUSTOM 1987 CHAIR ARBITRAGE CHAMBER (BESPOKE CHAIR DISPUTE ARENA)
       ========================================================================== -->
  <div class="musical-arena-overlay" id="arenaModal">
    <div class="chamber-cabinet">
      <!-- Cabinet Header -->
      <div class="chamber-header">
        <div class="chamber-brand">
          <img class="chamber-seal" id="chamberSealImg" alt="Seal">
          <div class="chamber-title-text">
            <h2>THE CHAIR ARBITRAGE CHAMBER</h2>
            <small id="chamberSubTitle">FLOOR 1 DISPUTE · THE INTERN'S FOLDING CHAIR</small>
          </div>
        </div>
        <div class="chamber-head-actions">
          <button class="chamber-btn" id="chamberSoundBtn" onclick="toggleChamberSound()">AUDIO: ON</button>
          <button class="chamber-btn" onclick="closeArenaModal()">CONCEDE ✕</button>
        </div>
      </div>

      <!-- Cabinet Layout -->
      <div class="chamber-body">
        <!-- Play Section -->
        <div class="chamber-stage">
          <div class="chamber-stage-top">
            <span id="arenaRoundLabel">ROUND 01 / 03</span>
            <div class="chamber-signal-pill waiting" id="arenaSignal">
              PHONOGRAPH READY
            </div>
            <div>
              STOPWATCH: <strong id="arenaReactionDisplay" style="color:#ffd875;">-- MS</strong>
            </div>
          </div>

          <div class="chamber-scene-wrap" id="arenaSceneWrap">
            <canvas id="chamberCanvas" width="960" height="540"></canvas>

            <!-- Intro / Guide Screen Overlay -->
            <div class="chamber-overlay" id="arenaIntroOverlay">
              <div class="chamber-card">
                <div class="chamber-card-eyebrow" id="introFloorEyebrow">FLOOR 1 CHAIR DISPUTE</div>
                <h2 id="introChairTitle">THE INTERN'S FOLDING CHAIR</h2>
                <p id="introGuideBody">
                  Circle the parquet marquetry while the department phonograph spins. When the needle scratches and the boardroom bell tolls, seize an available seat immediately.
                </p>
                <div class="chamber-contenders-preview" id="introContendersPreview"></div>
                <button class="primary-chamber-btn" onclick="startArenaMatch()">
                  ENTER CHAMBER [SPACE]
                </button>
              </div>
            </div>

            <!-- Result Overlay -->
            <div class="chamber-overlay hidden" id="arenaResultOverlay">
              <div class="chamber-card">
                <div class="chamber-card-eyebrow" id="resultKicker">ROUND COMPLETE</div>
                <h2 id="resultTitle">SEAT SECURED</h2>
                <p id="resultBody">
                  Rival eliminated. Next up: 3 contenders, 2 chairs.
                </p>
                <button class="primary-chamber-btn" id="resultBtn" onclick="onResultBtnClick()">
                  NEXT ROUND [SPACE]
                </button>
              </div>
            </div>
          </div>

          <!-- Control Deck -->
          <div class="chamber-control-deck">
            <div>
              <div class="deck-eyebrow">CHAIR ARBITRAGE CONTROLS</div>
              <p class="deck-hint" id="deckHintText">Hold your nerve. Listen for the needle scratch.</p>
            </div>
            <button id="chamberSitBtn" onclick="onSitClicked()" disabled>
              SEIZE SEAT <kbd>SPACE</kbd>
            </button>
          </div>
        </div>

        <!-- Aside Sidebar -->
        <div class="chamber-aside">
          <div class="aside-title-row">
            <h4>BOARD CONTENDERS</h4>
            <span class="aside-count-badge" id="rosterCount">04</span>
          </div>

          <div class="roster-list" id="rosterList"></div>

          <div class="chamber-rules-box">
            <div style="font-family:'Cinzel',serif;font-size:11px;font-weight:700;color:var(--ink);margin-bottom:6px;">HOUSE PROTOCOL</div>
            <div class="rules-item">
              <div class="dot-green"></div>
              <div><strong>Turntable active:</strong> Circle the seats while the phonograph plays.</div>
            </div>
            <div class="rules-item">
              <div class="dot-red"></div>
              <div><strong>Needle cuts:</strong> Strike SPACE or click SEIZE SEAT instantly.</div>
            </div>
            <div class="rules-item" style="color:var(--oxblood);">
              <div>⚠️</div>
              <div><strong>False start:</strong> Sitting while phonograph plays results in immediate forfeiture.</div>
            </div>
          </div>

          <div class="chamber-reflex-stat">
            <span>TARGET WINDOW:</span>
            <strong id="floorDifficultyStat">~460 ms</strong>
          </div>
          <div class="chamber-reflex-stat" style="margin-top:6px;">
            <span>SOUNDTRACK:</span>
            <strong id="floorTrackName" style="color:var(--ink-muted);font-size:10px;">Mailroom Rag</strong>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Certificate of Employment Modal -->
  <div class="cert-modal-overlay" id="certModal">
    <div class="cert-container">
      <canvas id="certCanvas" width="1200" height="675"></canvas>
      <div style="display:flex;justify-content:center;gap:12px;">
        <button class="desk-button" style="background:var(--lamp);padding:10px 22px;" onclick="downloadCert()">
          Download Official Certificate (PNG)
        </button>
        <button class="desk-button secondary" onclick="closeCertModal()">
          Close Registry
        </button>
      </div>
    </div>
  </div>

  <!-- Script for 3D Engine & Game Logic -->
  <script>
    const ASSETS = __ASSETS_JSON__;

    if (ASSETS.medallion) {
      document.getElementById('hudMedallion').src = ASSETS.medallion;
      document.getElementById('chamberSealImg').src = ASSETS.medallion;
    }

    // ==========================================================================
    // CUSTOM MULTI-TRACK AUDIO ENGINE (Unique 1987 Corporate Music per Floor)
    // ==========================================================================
    let audioCtx = null;
    let chamberSound = true;

    function initAudio() {
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx && audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
      } catch(e) {}
    }

    function tone(freq, duration = 0.12, type = 'square', volume = 0.04) {
      if (!chamberSound) return;
      try {
        initAudio();
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(volume, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    // AUTHENTIC VINYL NEEDLE SCRATCH + BOARDROOM BELL CHIME
    function playNeedleScratchAndBell() {
      if (!chamberSound) return;
      try {
        initAudio();
        if (!audioCtx) return;

        // 1. Vinyl Needle Scratch Noise Burst
        const bufferSize = audioCtx.sampleRate * 0.15;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
        }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(1400, audioCtx.currentTime);
        filter.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.14);
        const noiseGain = audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.25, audioCtx.currentTime);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(audioCtx.destination);
        noise.start();

        // 2. Resonant Boardroom Bell Chime (440Hz + 880Hz + 1320Hz)
        [440, 880, 1320].forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + 0.05);
          const vol = 0.18 / (idx + 1);
          gain.gain.setValueAtTime(vol, audioCtx.currentTime + 0.05);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.9);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + 0.05);
          osc.stop(audioCtx.currentTime + 0.95);
        });
      } catch(e) {}
    }

    function playStampThump() {
      if (!chamberSound) return;
      try {
        initAudio();
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(140, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(35, audioCtx.currentTime + 0.18);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.22);
      } catch(e) {}
    }

    function playElevatorDing() {
      if (!chamberSound) return;
      try {
        initAudio();
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.18, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.65);
      } catch(e) {}
    }

    function playStep() {
      tone(90, 0.04, 'triangle', 0.02);
    }

    function playClick() {
      tone(440, 0.05, 'square', 0.03);
    }

    function toggleChamberSound() {
      chamberSound = !chamberSound;
      document.getElementById('chamberSoundBtn').innerText = `AUDIO: ${chamberSound ? 'ON' : 'OFF'}`;
      if (chamberSound) tone(440, 0.1);
    }

    // ==========================================================================
    // MULTI-TRACK 1987 PHONOGRAPH MUSIC (Different Themes per Floor)
    // ==========================================================================
    let musicInterval = null;
    let musicStep = 0;

    // 1. Floor 1: Mailroom Phonograph Rag (Upbeat C Major corporate ragtime)
    const TRACK_MAILROOM_RAG = {
      name: "Mailroom Rag",
      tempoMs: 230,
      melody: [261.63, 329.63, 392.00, 440.00, 392.00, 329.63, 293.66, 329.63, 261.63, 293.66, 329.63, 392.00, 523.25, 440.00, 392.00, 329.63],
      bass: [130.81, 164.81, 196.00, 130.81]
    };

    // 2. Floors 2-4: The Trading Bullpen Swing (Driving F Major jazz swing)
    const TRACK_BULLPEN_SWING = {
      name: "Bullpen Swing",
      tempoMs: 200,
      melody: [349.23, 440.00, 523.25, 587.33, 523.25, 466.16, 440.00, 392.00, 349.23, 415.30, 440.00, 523.25, 698.46, 587.33, 523.25, 440.00],
      bass: [174.61, 220.00, 261.63, 174.61]
    };

    // 3. Floors 5-7: Executive Chamber Waltz (Tense D Minor classical baroque)
    const TRACK_EXECUTIVE_WALTZ = {
      name: "Executive Waltz",
      tempoMs: 190,
      melody: [293.66, 349.23, 440.00, 587.33, 523.25, 493.88, 440.00, 392.00, 440.00, 523.25, 587.33, 698.46, 659.25, 587.33, 523.25, 440.00],
      bass: [146.83, 174.61, 220.00, 146.83]
    };

    // 4. Floors 8-9: Sovereign Hymn of Seat 0 (Grand, ceremonial C Minor cathedral synth)
    const TRACK_SOVEREIGN_HYMN = {
      name: "Sovereign Hymn",
      tempoMs: 220,
      melody: [261.63, 311.13, 392.00, 523.25, 466.16, 392.00, 311.13, 349.23, 392.00, 466.16, 523.25, 622.25, 523.25, 392.00, 311.13, 261.63],
      bass: [65.41, 77.78, 98.00, 65.41]
    };

    function getFloorTrack(floor) {
      if (floor <= 1) return TRACK_MAILROOM_RAG;
      if (floor <= 4) return TRACK_BULLPEN_SWING;
      if (floor <= 7) return TRACK_EXECUTIVE_WALTZ;
      return TRACK_SOVEREIGN_HYMN;
    }

    function startChamberPhonographTune(floor) {
      stopChamberPhonographTune();
      const track = getFloorTrack(floor);
      musicStep = 0;

      musicInterval = setInterval(() => {
        if (arenaPhase !== 'green') {
          stopChamberPhonographTune();
          return;
        }

        const mNote = track.melody[musicStep % track.melody.length];
        const bNote = track.bass[Math.floor(musicStep / 4) % track.bass.length];
        musicStep++;

        // Play melody note
        tone(mNote, 0.14, 'triangle', 0.045);
        // Play deep bass note on beats
        if (musicStep % 2 === 0) {
          tone(bNote, 0.18, 'sine', 0.06);
        }
      }, track.tempoMs);
    }

    function stopChamberPhonographTune() {
      if (musicInterval) {
        clearInterval(musicInterval);
        musicInterval = null;
      }
    }

    // ==========================================================================
    // GAME STATE & FLICKERR PROGRESSION (Matching tmforgchart.xyz)
    // ==========================================================================
    const ROLES = [
      { floor: 0, title: "Applicant", minPts: 0, chair: "The Pavement", tier: "Unadmitted" },
      { floor: 1, title: "Intern", minPts: 15, chair: "The Intern's Folding Chair", tier: "Class I Intern" },
      { floor: 2, title: "Analyst", minPts: 29, chair: "The Typist Stool", tier: "Class II Analyst" },
      { floor: 3, title: "Associate", minPts: 59, chair: "Creaking Wooden Swivel", tier: "Class III Associate" },
      { floor: 4, title: "Vice President", minPts: 118, chair: "Beige Task Chair", tier: "Class IV Vice President" },
      { floor: 5, title: "Director", minPts: 221, chair: "High-Back Leather Desk Chair", tier: "Class V Director" },
      { floor: 6, title: "Managing Director", minPts: 358, chair: "Green Banker's Chair", tier: "Class VI Managing Director" },
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

    const SAVE_KEY = "tmf_odyssey_save_v6";

    function saveGame(showToast = false) {
      const data = {
        currentFloor,
        unlockedFloor,
        flickerr,
        timestamp: Date.now()
      };
      localStorage.setItem(SAVE_KEY, JSON.stringify(data));
      if (showToast) {
        showMemoToast("PROGRESS COMMITTED", `Registry saved to local device. Current floor: ${currentFloor}, Review: ${flickerr.reviewScore} pts.`);
      }
    }

    function loadGame() {
      const saved = localStorage.getItem(SAVE_KEY);
      if (saved) {
        try {
          const data = JSON.parse(saved);
          if (data && data.flickerr) {
            currentFloor = data.currentFloor || 0;
            unlockedFloor = data.unlockedFloor || 0;
            flickerr = Object.assign(flickerr, data.flickerr);
            console.log("Loaded game from local device persistence:", flickerr);
          }
        } catch (e) {
          console.warn("Failed to load save data:", e);
        }
      }
    }

    function confirmResetGame() {
      if (confirm("Reset career history and return to the sunny pavement outside the gate?")) {
        localStorage.removeItem(SAVE_KEY);
        location.reload();
      }
    }

    function updateHUD() {
      document.getElementById('hudRole').innerText = `You · ${flickerr.role}`;
      document.getElementById('hudFloor').innerText = getFloorName(currentFloor);
      document.getElementById('hudDept').innerText = flickerr.department;
      document.getElementById('hudDept').style.borderColor = DEPARTMENTS[flickerr.deptIndex].color;
      document.getElementById('hudChair').innerText = flickerr.chairName;
      document.getElementById('hudScore').innerText = `${flickerr.reviewScore} Pts | ${flickerr.dengCredits} Deng`;
    }

    // ==========================================================================
    // THREE.JS 3D SCENE SETUP
    // ==========================================================================
    const canvas3d = document.getElementById('canvas3d');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas3d, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x8ab4f8);

    const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.1, 150);

    // ==========================================
    // REVAMPED FLICKERR 3D MODEL (The 1987 Corporate Clerk)
    // Distinct Front (Face, Glasses, Tie, Lapels, ID Badge, Shoes) vs Back (Full Hair, Jacket Seam, Heels)
    // ==========================================
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // Color Palette
    const suitMat = new THREE.MeshLambertMaterial({ color: 0x1d2738 }); // 1987 Navy Wool
    const lapelMat = new THREE.MeshLambertMaterial({ color: 0x141b27 }); // Dark Navy Lapel / Seam
    const shirtMat = new THREE.MeshLambertMaterial({ color: 0xf7f4ef }); // Starched White Poplin
    const tieMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });   // Authentic Oxblood Silk
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.85, roughness: 0.25 }); // Gold Accents
    const skinMat = new THREE.MeshLambertMaterial({ color: 0xebb992 });  // Fair Complexion
    const hairMat = new THREE.MeshLambertMaterial({ color: 0x2e1d13 });  // Chestnut Hair
    const glassesMat = new THREE.MeshLambertMaterial({ color: 0x1f140e }); // Tortoiseshell Frame
    const lensMat = new THREE.MeshLambertMaterial({ color: 0xcde8f7, transparent: true, opacity: 0.5 }); // Lenses
    const eyeMat = new THREE.MeshLambertMaterial({ color: 0x110e0c });   // Dark Iris
    const shoeMat = new THREE.MeshStandardMaterial({ color: 0x111116, roughness: 0.35 }); // Oxford Leather
    const caseMat = new THREE.MeshStandardMaterial({ color: 0x3d2012, roughness: 0.5 });  // Briefcase Leather

    // --- TORSO GROUP ---
    const torso = new THREE.Group();
    torso.position.y = 1.0;
    playerGroup.add(torso);

    // Jacket Core (0.68W x 0.76H x 0.38D)
    const jacket = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.76, 0.38), suitMat);
    jacket.castShadow = true;
    torso.add(jacket);

    // FRONT DETAILS (+Z):
    // White shirt V-placket (FRONT ONLY, z > 0.18)
    const shirtPlacket = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.32, 0.02), shirtMat);
    shirtPlacket.position.set(0, 0.18, 0.191);
    torso.add(shirtPlacket);

    // Oxblood Silk Tie (FRONT ONLY, z > 0.19)
    const tieMesh = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.36, 0.025), tieMat);
    tieMesh.position.set(0, 0.10, 0.205);
    torso.add(tieMesh);

    const tieKnot = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.09, 0.035), tieMat);
    tieKnot.position.set(0, 0.29, 0.205);
    torso.add(tieKnot);

    // Gold Tie Clip (Mid-chest)
    const tieClip = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.02, 0.02), goldMat);
    tieClip.position.set(0, 0.14, 0.22);
    torso.add(tieClip);

    // Notched Lapels (Front only)
    const leftLapel = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.32, 0.03), lapelMat);
    leftLapel.position.set(-0.14, 0.16, 0.195);
    leftLapel.rotation.z = -0.12;
    torso.add(leftLapel);

    const rightLapel = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.32, 0.03), lapelMat);
    rightLapel.position.set(0.14, 0.16, 0.195);
    rightLapel.rotation.z = 0.12;
    torso.add(rightLapel);

    // Breast pocket & TMF Employee Pass (Left chest, FRONT ONLY)
    const welt = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.02, 0.02), lapelMat);
    welt.position.set(-0.20, 0.18, 0.195);
    torso.add(welt);

    const tmfPass = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.015), shirtMat);
    tmfPass.position.set(-0.20, 0.22, 0.198);
    torso.add(tmfPass);

    const passHeader = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.02, 0.018), tieMat);
    passHeader.position.set(-0.20, 0.25, 0.199);
    torso.add(passHeader);

    // Gold jacket buttons (FRONT ONLY)
    const btn1 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.02), goldMat);
    btn1.position.set(0.02, -0.05, 0.195);
    torso.add(btn1);
    const btn2 = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.02), goldMat);
    btn2.position.set(0.02, -0.18, 0.195);
    torso.add(btn2);

    // Belt & Brass Buckle (Waist)
    const belt = new THREE.Mesh(new THREE.BoxGeometry(0.69, 0.08, 0.39), shoeMat);
    belt.position.set(0, -0.34, 0);
    torso.add(belt);

    const beltBuckle = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.07, 0.02), goldMat);
    beltBuckle.position.set(0, -0.34, 0.20);
    torso.add(beltBuckle);

    // BACK DETAILS (-Z, REAR ONLY):
    // Tailored center spine vent seam
    const backSeam = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.68, 0.02), lapelMat);
    backSeam.position.set(0, 0, -0.192);
    torso.add(backSeam);

    // --- HEAD GROUP ---
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 1.62, 0);
    playerGroup.add(headGroup);

    // Neck
    const neck = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.18, 0.20), skinMat);
    neck.position.set(0, -0.16, 0);
    headGroup.add(neck);

    // Shirt Collar wrapping neck (higher in back, open in front)
    const collarFront = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.09, 0.03), shirtMat);
    collarFront.position.set(0, -0.14, 0.11);
    headGroup.add(collarFront);

    // Head Core (0.38 x 0.40 x 0.36)
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.40, 0.36), skinMat);
    head.castShadow = true;
    headGroup.add(head);

    // FRONT FACE DETAILS (+Z, FRONT ONLY):
    // Chiseled corporate nose
    const nose = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.09, 0.08), skinMat);
    nose.position.set(0, -0.01, 0.21);
    headGroup.add(nose);

    // Dry corporate mouth line
    const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.018, 0.02), lapelMat);
    mouth.position.set(0, -0.08, 0.185);
    headGroup.add(mouth);

    // Eyes (Pupils behind glasses)
    const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.04, 0.02), eyeMat);
    eyeL.position.set(-0.09, 0.03, 0.185);
    headGroup.add(eyeL);
    const eyeR = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.04, 0.02), eyeMat);
    eyeR.position.set(0.09, 0.03, 0.185);
    headGroup.add(eyeR);

    // Eyebrows
    const browL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.02, 0.025), hairMat);
    browL.position.set(-0.09, 0.08, 0.19);
    headGroup.add(browL);
    const browR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.02, 0.025), hairMat);
    browR.position.set(0.09, 0.08, 0.19);
    headGroup.add(browR);

    // 1987 Tortoiseshell Spectacles
    const glassRimL = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.09, 0.03), glassesMat);
    glassRimL.position.set(-0.09, 0.03, 0.198);
    headGroup.add(glassRimL);

    const lensL = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.07, 0.01), lensMat);
    lensL.position.set(-0.09, 0.03, 0.20);
    headGroup.add(lensL);

    const glassRimR = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.09, 0.03), glassesMat);
    glassRimR.position.set(0.09, 0.03, 0.198);
    headGroup.add(glassRimR);

    const lensR = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.07, 0.01), lensMat);
    lensR.position.set(0.09, 0.03, 0.20);
    headGroup.add(lensR);

    const glassBridge = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.02, 0.025), glassesMat);
    glassBridge.position.set(0, 0.03, 0.205);
    headGroup.add(glassBridge);

    // Glasses temples (running back along side of head)
    const stemL = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.02, 0.22), glassesMat);
    stemL.position.set(-0.195, 0.03, 0.07);
    headGroup.add(stemL);
    const stemR = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.02, 0.22), glassesMat);
    stemR.position.set(0.195, 0.03, 0.07);
    headGroup.add(stemR);

    // Ears on sides
    const earL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.10, 0.08), skinMat);
    earL.position.set(-0.20, 0, 0);
    headGroup.add(earL);
    const earR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.10, 0.08), skinMat);
    earR.position.set(0.20, 0, 0);
    headGroup.add(earR);

    // HAIR ARCHITECTURE (Distinct Front vs Back):
    // Top Hair
    const hairTop = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.10, 0.38), hairMat);
    hairTop.position.set(0, 0.21, -0.01);
    headGroup.add(hairTop);

    // Front executive side-part bangs
    const hairBangs = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.08, 0.08), hairMat);
    hairBangs.position.set(0.04, 0.16, 0.18);
    headGroup.add(hairBangs);

    // Side hair
    const hairSideL = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.24, 0.34), hairMat);
    hairSideL.position.set(-0.195, 0.06, -0.03);
    headGroup.add(hairSideL);
    const hairSideR = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.24, 0.34), hairMat);
    hairSideR.position.set(0.195, 0.06, -0.03);
    headGroup.add(hairSideR);

    // BACK HAIR (COVERS ENTIRE REAR OF SKULL DOWN TO COLLAR - CRITICAL FOR BACK VIEW)
    const hairBack = new THREE.Mesh(new THREE.BoxGeometry(0.40, 0.38, 0.08), hairMat);
    hairBack.position.set(0, 0.02, -0.185);
    headGroup.add(hairBack);

    // --- LEGS & FORWARD-POINTING OXFORD SHOES ---
    // Left Leg Group (Hip Joint at x=-0.17, y=0.62)
    const leftLeg = new THREE.Group();
    leftLeg.position.set(-0.17, 0.62, 0);
    playerGroup.add(leftLeg);

    const leftPants = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.58, 0.22), suitMat);
    leftPants.position.set(0, -0.29, 0);
    leftPants.castShadow = true;
    leftLeg.add(leftPants);

    // Left Shoe: Black Oxford pointing FORWARD (+Z)
    const leftShoeBody = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.08, 0.26), shoeMat);
    leftShoeBody.position.set(0, -0.56, 0.04);
    leftShoeBody.castShadow = true;
    leftLeg.add(leftShoeBody);

    const leftToeCap = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.06, 0.08), shoeMat);
    leftToeCap.position.set(0, -0.57, 0.18);
    leftLeg.add(leftToeCap);

    const leftHeel = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.04, 0.10), shoeMat);
    leftHeel.position.set(0, -0.58, -0.08);
    leftLeg.add(leftHeel);

    // Right Leg Group (Hip Joint at x=+0.17, y=0.62)
    const rightLeg = new THREE.Group();
    rightLeg.position.set(0.17, 0.62, 0);
    playerGroup.add(rightLeg);

    const rightPants = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.58, 0.22), suitMat);
    rightPants.position.set(0, -0.29, 0);
    rightPants.castShadow = true;
    rightLeg.add(rightPants);

    // Right Shoe: Black Oxford pointing FORWARD (+Z)
    const rightShoeBody = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.08, 0.26), shoeMat);
    rightShoeBody.position.set(0, -0.56, 0.04);
    rightShoeBody.castShadow = true;
    rightLeg.add(rightShoeBody);

    const rightToeCap = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.06, 0.08), shoeMat);
    rightToeCap.position.set(0, -0.57, 0.18);
    rightLeg.add(rightToeCap);

    const rightHeel = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.04, 0.10), shoeMat);
    rightHeel.position.set(0, -0.58, -0.08);
    rightLeg.add(rightHeel);

    // --- ARMS, GOLD WATCH & BRIEFCASE ---
    // Left Arm Group (Shoulder Joint at x=-0.44, y=1.35)
    const leftArm = new THREE.Group();
    leftArm.position.set(-0.44, 1.35, 0);
    playerGroup.add(leftArm);

    const leftSleeve = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.52, 0.18), suitMat);
    leftSleeve.position.set(0, -0.26, 0);
    leftSleeve.castShadow = true;
    leftArm.add(leftSleeve);

    const leftCuff = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.17), shirtMat);
    leftCuff.position.set(0, -0.53, 0);
    leftArm.add(leftCuff);

    // 1987 Gold Executive Dress Watch
    const watchBand = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.03, 0.18), shoeMat);
    watchBand.position.set(0, -0.56, 0);
    leftArm.add(watchBand);

    const watchFace = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.04, 0.06), goldMat);
    watchFace.position.set(-0.08, -0.56, 0);
    leftArm.add(watchFace);

    const leftHand = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.13), skinMat);
    leftHand.position.set(0, -0.63, 0);
    leftArm.add(leftHand);

    // Right Arm Group (Shoulder Joint at x=+0.44, y=1.35)
    const rightArm = new THREE.Group();
    rightArm.position.set(0.44, 1.35, 0);
    playerGroup.add(rightArm);

    const rightSleeve = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.52, 0.18), suitMat);
    rightSleeve.position.set(0, -0.26, 0);
    rightSleeve.castShadow = true;
    rightArm.add(rightSleeve);

    const rightCuff = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.17), shirtMat);
    rightCuff.position.set(0, -0.53, 0);
    rightArm.add(rightCuff);

    const rightHand = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.13), skinMat);
    rightHand.position.set(0, -0.63, 0);
    rightArm.add(rightHand);

    // AUTHENTIC 1987 VINTAGE LEATHER BRIEFCASE (Carried in Right Hand, swings naturally with arm stride!)
    const caseGroup = new THREE.Group();
    caseGroup.position.set(0.06, -0.80, 0.04);
    rightArm.add(caseGroup);

    const caseBody = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.36, 0.44), caseMat);
    caseBody.castShadow = true;
    caseGroup.add(caseBody);

    const caseHandle = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.14, 0.16), caseMat);
    caseHandle.position.set(0, 0.20, 0);
    caseGroup.add(caseHandle);

    // Dual Brass Latches (FRONT ONLY, +Z)
    const latch1 = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.02), goldMat);
    latch1.position.set(0, 0.08, 0.225);
    caseGroup.add(latch1);

    const latch2 = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.02), goldMat);
    latch2.position.set(0, -0.08, 0.225);
    caseGroup.add(latch2);

    let interactiveObjects = [];
    let roomGroup = new THREE.Group();
    scene.add(roomGroup);

    function loadTextureB64(b64) {
      if (!b64) return null;
      const img = new Image();
      img.src = b64;
      const tex = new THREE.Texture(img);
      img.onload = () => { tex.needsUpdate = true; };
      return tex;
    }

    // ==========================================================================
    // PROCEDURAL 3D CHAIR BUILDER (Distinct detailed model for each floor)
    // ==========================================================================
    function createChair(x, y, z, floorTier = 1, rotY = 0) {
      const chairGroup = new THREE.Group();

      if (floorTier === 1) {
        // FLOOR 1: THE INTERN'S FOLDING CHAIR (Tubular steel X-frame with beige vinyl pad)
        const steelMat = new THREE.MeshLambertMaterial({ color: 0x9e9e9e });
        const vinylMat = new THREE.MeshLambertMaterial({ color: 0xd5bd82 });

        const leg1 = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.65), steelMat);
        leg1.rotation.z = 0.32;
        leg1.position.set(-0.25, 0.28, 0);
        chairGroup.add(leg1);

        const leg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.65), steelMat);
        leg2.rotation.z = -0.32;
        leg2.position.set(0.25, 0.28, 0);
        chairGroup.add(leg2);

        const cross = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.52), steelMat);
        cross.rotation.x = Math.PI / 2;
        cross.position.set(0, 0.12, 0);
        chairGroup.add(cross);

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.56, 0.04, 0.52), vinylMat);
        seat.position.set(0, 0.48, 0);
        chairGroup.add(seat);

        const backArch = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.55), steelMat);
        backArch.position.set(0, 0.78, -0.24);
        chairGroup.add(backArch);

        const backPad = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.24, 0.03), vinylMat);
        backPad.position.set(0, 0.82, -0.23);
        chairGroup.add(backPad);

      } else if (floorTier === 2) {
        // FLOOR 2: THE TYPIST STOOL (Turned oak round seat with circular brass footring)
        const oakMat = new THREE.MeshLambertMaterial({ color: 0x8a5229 });
        const brassMat = new THREE.MeshLambertMaterial({ color: 0xd4af37 });
        const ironMat = new THREE.MeshLambertMaterial({ color: 0x333333 });

        const seat = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.06, 24), oakMat);
        seat.position.set(0, 0.5, 0);
        chairGroup.add(seat);

        const screw = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.35), ironMat);
        screw.position.set(0, 0.32, 0);
        chairGroup.add(screw);

        for (let i = 0; i < 4; i++) {
          const ang = (i * Math.PI) / 2 + Math.PI / 4;
          const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.02, 0.5), oakMat);
          leg.position.set(Math.cos(ang) * 0.18, 0.22, Math.sin(ang) * 0.18);
          leg.rotation.z = Math.cos(ang) * 0.22;
          leg.rotation.x = -Math.sin(ang) * 0.22;
          chairGroup.add(leg);
        }

        const ring = new THREE.Mesh(new THREE.TorusGeometry(0.24, 0.016, 8, 24), brassMat);
        ring.rotation.x = Math.PI / 2;
        ring.position.set(0, 0.18, 0);
        chairGroup.add(ring);

        const spine = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.42), ironMat);
        spine.position.set(0, 0.68, -0.22);
        chairGroup.add(spine);

        const lumbarPad = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.15, 0.04), oakMat);
        lumbarPad.position.set(0, 0.82, -0.21);
        chairGroup.add(lumbarPad);

      } else if (floorTier === 3) {
        // FLOOR 3: CREAKING WOODEN SWIVEL (Solid dark oak with slat back)
        const darkOak = new THREE.MeshLambertMaterial({ color: 0x5a3518 });
        const brassMat = new THREE.MeshLambertMaterial({ color: 0xd4af37 });

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.07, 0.64), darkOak);
        seat.position.set(0, 0.5, 0);
        chairGroup.add(seat);

        for (let i = 0; i < 5; i++) {
          const ang = (i * Math.PI * 2) / 5;
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.05, 0.32), darkOak);
          leg.position.set(Math.sin(ang) * 0.18, 0.12, Math.cos(ang) * 0.18);
          leg.rotation.y = ang;
          chairGroup.add(leg);

          const wheel = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), brassMat);
          wheel.position.set(Math.sin(ang) * 0.34, 0.04, Math.cos(ang) * 0.34);
          chairGroup.add(wheel);
        }

        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.38), darkOak);
        hub.position.set(0, 0.28, 0);
        chairGroup.add(hub);

        const topRail = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.08, 0.06), darkOak);
        topRail.position.set(0, 1.05, -0.3);
        chairGroup.add(topRail);

        for (let i = -2; i <= 2; i++) {
          const slat = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 0.48), darkOak);
          slat.position.set(i * 0.12, 0.78, -0.3);
          chairGroup.add(slat);
        }

      } else if (floorTier === 4) {
        // FLOOR 4: BEIGE TASK CHAIR (1980s executive task chair)
        const beigeMat = new THREE.MeshLambertMaterial({ color: 0xcbb082 });
        const blackPlastic = new THREE.MeshLambertMaterial({ color: 0x1e1e1e });

        for (let i = 0; i < 5; i++) {
          const ang = (i * Math.PI * 2) / 5;
          const armMesh = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.04, 0.34), blackPlastic);
          armMesh.position.set(Math.sin(ang) * 0.18, 0.12, Math.cos(ang) * 0.18);
          armMesh.rotation.y = ang;
          chairGroup.add(armMesh);
        }

        const column = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.36, 12), blackPlastic);
        column.position.set(0, 0.28, 0);
        chairGroup.add(column);

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.1, 0.64), beigeMat);
        seat.position.set(0, 0.52, 0);
        chairGroup.add(seat);

        const back = new THREE.Mesh(new THREE.BoxGeometry(0.64, 0.62, 0.08), beigeMat);
        back.position.set(0, 0.9, -0.28);
        chairGroup.add(back);

      } else if (floorTier === 5) {
        // FLOOR 5: HIGH-BACK LEATHER DESK CHAIR (Channel-tufted deep black leather)
        const leatherMat = new THREE.MeshLambertMaterial({ color: 0x141414 });
        const chromeMat = new THREE.MeshLambertMaterial({ color: 0xd8d8d8 });

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.12, 0.68), leatherMat);
        seat.position.set(0, 0.54, 0);
        chairGroup.add(seat);

        for (let i = 0; i < 5; i++) {
          const rib = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.16, 0.09), leatherMat);
          rib.position.set(0, 0.74 + i * 0.17, -0.3);
          chairGroup.add(rib);
        }

      } else if (floorTier === 6) {
        // FLOOR 6: GREEN BANKER'S CHAIR (Managing Director what3verman chair)
        const mahogMat = new THREE.MeshLambertMaterial({ color: 0x3d1b10 });
        const greenLeather = new THREE.MeshLambertMaterial({ color: 0x1b432a });
        const brassStudMat = new THREE.MeshLambertMaterial({ color: 0xd4af37 });

        for (let i = 0; i < 4; i++) {
          const ang = (i * Math.PI) / 2;
          const leg = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.06, 0.36), mahogMat);
          leg.position.set(Math.sin(ang) * 0.2, 0.12, Math.cos(ang) * 0.2);
          leg.rotation.y = ang;
          chairGroup.add(leg);
        }

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.12, 0.68), greenLeather);
        seat.position.set(0, 0.52, 0);
        chairGroup.add(seat);

        const backRail = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.08, 0.08), mahogMat);
        backRail.position.set(0, 1.02, -0.32);
        chairGroup.add(backRail);

        for (let i = -3; i <= 3; i++) {
          const spindle = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.44), mahogMat);
          spindle.position.set(i * 0.11, 0.76, -0.32);
          chairGroup.add(spindle);
        }

      } else if (floorTier === 7) {
        // FLOOR 7: OXBLOOD WINGBACK CHAIR (Partner)
        const oxbloodMat = new THREE.MeshLambertMaterial({ color: 0x691717 });
        const cabrioleMat = new THREE.MeshLambertMaterial({ color: 0x30160a });

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.16, 0.74), oxbloodMat);
        seat.position.set(0, 0.44, 0);
        chairGroup.add(seat);

        const back = new THREE.Mesh(new THREE.BoxGeometry(0.76, 0.95, 0.12), oxbloodMat);
        back.position.set(0, 0.95, -0.32);
        chairGroup.add(back);

      } else if (floorTier === 8) {
        // FLOOR 8: BOARD OF DIRECTORS HIGH SEAT (Monumental throne in navy velvet & gold)
        const navyMat = new THREE.MeshLambertMaterial({ color: 0x0f1c3a });
        const goldMat = new THREE.MeshLambertMaterial({ color: 0xd4af37 });
        const mahogMat = new THREE.MeshLambertMaterial({ color: 0x2e150a });

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.16, 0.76), navyMat);
        seat.position.set(0, 0.42, 0);
        chairGroup.add(seat);

        const back = new THREE.Mesh(new THREE.BoxGeometry(0.78, 1.35, 0.1), navyMat);
        back.position.set(0, 1.08, -0.34);
        chairGroup.add(back);

      } else {
        // FLOOR 9: THE GILDED THRONE & SEAT 0 (Kingpickle Penthouse Sovereign Throne)
        const goldLeafMat = new THREE.MeshLambertMaterial({ color: 0xffd700 });
        const royalCrimson = new THREE.MeshLambertMaterial({ color: 0x8b0000 });

        const dais = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.22, 1.1), goldLeafMat);
        dais.position.set(0, 0.11, 0);
        chairGroup.add(dais);

        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.84, 0.18, 0.8), royalCrimson);
        seat.position.set(0, 0.35, 0);
        chairGroup.add(seat);

        const back = new THREE.Mesh(new THREE.BoxGeometry(0.84, 1.5, 0.12), royalCrimson);
        back.position.set(0, 1.2, -0.36);
        chairGroup.add(back);

        const crownCrest = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.45, 0.28, 16), goldLeafMat);
        crownCrest.rotation.x = Math.PI / 2;
        crownCrest.position.set(0, 2.02, -0.36);
        chairGroup.add(crownCrest);

        const throneGlow = new THREE.PointLight(0xffd700, 1.8, 5);
        throneGlow.position.set(0, 2.1, -0.2);
        chairGroup.add(throneGlow);
      }

      chairGroup.position.set(x, y, z);
      chairGroup.rotation.y = rotY;
      chairGroup.castShadow = true;
      roomGroup.add(chairGroup);
      return chairGroup;
    }

    // ==========================================================================
    // 3D ENVIRONMENT BUILDERS (Floors 0 to 9)
    // ==========================================================================
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
    }

    // LEVEL 0: SUNNY MORNING OUTDOOR PAVEMENT (Security Gate)
    function buildExteriorStreet() {
      scene.background = new THREE.Color(0x8ab4f8);
      scene.fog = new THREE.FogExp2(0x8ab4f8, 0.007);

      const morningSun = new THREE.DirectionalLight(0xfffaed, 2.2);
      morningSun.position.set(16, 24, 18);
      morningSun.castShadow = true;
      morningSun.shadow.mapSize.width = 2048;
      morningSun.shadow.mapSize.height = 2048;
      morningSun.shadow.camera.near = 0.5;
      morningSun.shadow.camera.far = 60;
      morningSun.shadow.camera.left = -20;
      morningSun.shadow.camera.right = 20;
      morningSun.shadow.camera.top = 20;
      morningSun.shadow.camera.bottom = -20;
      roomGroup.add(morningSun);

      const skyAmb = new THREE.AmbientLight(0xcde0f7, 1.3);
      roomGroup.add(skyAmb);

      const road = new THREE.Mesh(new THREE.PlaneGeometry(40, 18), new THREE.MeshLambertMaterial({ color: 0x33363d }));
      road.rotation.x = -Math.PI / 2;
      road.position.set(0, 0, 7);
      road.receiveShadow = true;
      roomGroup.add(road);

      const curb = new THREE.Mesh(new THREE.BoxGeometry(40, 0.25, 14), new THREE.MeshLambertMaterial({ color: 0x8a847c }));
      curb.position.set(0, 0.125, -5);
      curb.receiveShadow = true;
      roomGroup.add(curb);

      const wallMat = new THREE.MeshLambertMaterial({ color: 0x7a3e2e });
      const facade = new THREE.Mesh(new THREE.BoxGeometry(40, 18, 2), wallMat);
      facade.position.set(0, 9, -12);
      facade.receiveShadow = true;
      roomGroup.add(facade);

      const archMat = new THREE.MeshLambertMaterial({ color: 0xc49e4d });
      const arch = new THREE.Mesh(new THREE.BoxGeometry(6.5, 6.5, 2.2), archMat);
      arch.position.set(0, 3.25, -12);
      arch.castShadow = true;
      roomGroup.add(arch);

      const gateMat = new THREE.MeshLambertMaterial({ color: 0x181818 });
      const gateL = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.2, 0.15), gateMat);
      gateL.position.set(-1.3, 2.1, -10.9);
      roomGroup.add(gateL);

      const gateR = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.2, 0.15), gateMat);
      gateR.position.set(1.3, 2.1, -10.9);
      roomGroup.add(gateR);

      const booth = new THREE.Mesh(new THREE.BoxGeometry(2.6, 3.4, 2.6), new THREE.MeshLambertMaterial({ color: 0x4a3424 }));
      booth.position.set(5.5, 1.7, -7);
      booth.castShadow = true;
      booth.receiveShadow = true;
      roomGroup.add(booth);

      const guardMesh = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.7, 0.4), new THREE.MeshLambertMaterial({ color: 0x223654 }));
      guardMesh.position.set(4, 0.85, -6);
      guardMesh.castShadow = true;
      roomGroup.add(guardMesh);

      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 4.5), new THREE.MeshLambertMaterial({ color: 0x222222 }));
      post.position.set(-6, 2.25, -4);
      post.castShadow = true;
      roomGroup.add(post);

      const lampHead = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), new THREE.MeshLambertMaterial({ color: 0xe8e4dc }));
      lampHead.position.set(-6, 4.5, -4);
      roomGroup.add(lampHead);

      playerGroup.position.set(0, 0.25, 2);
      playerGroup.rotation.y = Math.PI;

      interactiveObjects.push({
        id: "gatekeeper",
        label: "Security Gatekeeper: Seek Admission & Department Assignment",
        pos: new THREE.Vector3(4, 0, -6),
        radius: 2.5,
        action: openGatekeeperModal
      });

      interactiveObjects.push({
        id: "headquarters_entry",
        label: "Headquarters Entrance: Step Inside to Floor 1 (Intern Concourse)",
        pos: new THREE.Vector3(0, 0, -10.5),
        radius: 2.2,
        action: () => {
          if (!flickerr.gateAdmitted) {
            showMemoToast("ACCESS DENIED", "Speak with the Security Gatekeeper to complete admissions and fund assignment.");
            tone(120, 0.3);
          } else {
            rideElevatorTo(1);
          }
        }
      });
    }

    // INTERIOR OFFICE FLOOR (Floors 1-9)
    function buildInteriorOfficeFloor() {
      scene.background = new THREE.Color(0x140f0b);
      scene.fog = new THREE.FogExp2(0x140f0b, 0.018);

      const ambLight = new THREE.AmbientLight(0xd4af37, 0.65);
      roomGroup.add(ambLight);

      const ceilingLight = new THREE.PointLight(0xffe6b0, 1.8, 25);
      ceilingLight.position.set(0, 5.2, 0);
      ceilingLight.castShadow = true;
      roomGroup.add(ceilingLight);

      const floorMat = new THREE.MeshLambertMaterial({ color: 0x3d2719 });
      const floorMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), floorMat);
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
    }

    // AUTHENTIC ART DEPARTMENT WALLS (themutual.fun/art-department)
    function buildArchitecturalWalls() {
      const wallTex = loadTextureB64(ASSETS.art_wall);
      if (wallTex) {
        wallTex.wrapS = THREE.RepeatWrapping;
        wallTex.wrapT = THREE.RepeatWrapping;
        wallTex.repeat.set(3, 1.5);
        wallTex.magFilter = THREE.NearestFilter;
        wallTex.minFilter = THREE.NearestFilter;
      }

      const upperWallMat = new THREE.MeshLambertMaterial({ 
        map: wallTex || null,
        color: wallTex ? 0xffffff : 0xdcc48d
      });

      const wainMat = new THREE.MeshLambertMaterial({ color: 0xc8ad72 });
      const railMat = new THREE.MeshLambertMaterial({ color: 0xae9259 });

      buildArtWallSegment(0, -10, 24, false, wainMat, upperWallMat, railMat);
      buildArtWallSegment(-12, 0, 20, true, wainMat, upperWallMat, railMat, true);
      buildArtWallSegment(12, 0, 20, true, wainMat, upperWallMat, railMat, true);
    }

    function buildArtWallSegment(x, z, length, isSide, wainMat, topMat, railMat, hasWindow = false) {
      const group = new THREE.Group();
      const w = isSide ? 0.3 : length;
      const d = isSide ? length : 0.3;

      const bottom = new THREE.Mesh(new THREE.BoxGeometry(w, 2.0, d), wainMat);
      bottom.position.y = 1.0;
      bottom.receiveShadow = true;
      group.add(bottom);

      const rail = new THREE.Mesh(new THREE.BoxGeometry(w * 1.04, 0.14, d * 1.04), railMat);
      rail.position.y = 2.07;
      group.add(rail);

      const top = new THREE.Mesh(new THREE.BoxGeometry(w, 3.6, d), topMat);
      top.position.y = 3.9;
      top.receiveShadow = true;
      group.add(top);

      if (hasWindow) {
        const winGroup = new THREE.Group();
        const frameWood = new THREE.MeshLambertMaterial({ color: 0x453629 });
        const skyGlass = new THREE.MeshBasicMaterial({ color: 0x8ab4f8 });

        const frame = new THREE.Mesh(new THREE.BoxGeometry(0.35, 2.2, 2.2), frameWood);
        winGroup.add(frame);

        for (let row = -1; row <= 1; row += 2) {
          for (let col = -1; col <= 1; col += 2) {
            const pane = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.88, 0.88), skyGlass);
            pane.position.set(0, row * 0.5, col * 0.5);
            winGroup.add(pane);
          }
        }

        winGroup.position.set(0, 3.8, 0);
        group.add(winGroup);

        const winLight = new THREE.PointLight(0xfffaed, 0.8, 8);
        winLight.position.set(isSide ? (x > 0 ? -1 : 1) : 0, 3.8, isSide ? 0 : 1);
        group.add(winLight);
      }

      group.position.set(x, 0, z);
      roomGroup.add(group);
    }

    function hangFloorPortraits() {
      const portraits = [
        ASSETS.flickerr_human || ASSETS.p_bogle_3,
        ASSETS.p_argon_1,
        ASSETS.p_smaug_1,
        ASSETS.p_midas_1
      ].filter(Boolean);

      for (let i = 0; i < 4; i++) {
        if (portraits[i]) {
          createWallPortrait(-7.5 + i * 5, 3.2, -9.8, 0, portraits[i]);
        }
      }
    }

    function createWallPortrait(x, y, z, rotY, b64) {
      const frameGroup = new THREE.Group();
      const frameMesh = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.8, 0.1), new THREE.MeshLambertMaterial({ color: 0xb08a3c }));
      frameGroup.add(frameMesh);

      const tex = loadTextureB64(b64);
      if (tex) {
        const art = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 1.6), new THREE.MeshBasicMaterial({ map: tex }));
        art.position.z = 0.06;
        frameGroup.add(art);
      }
      frameGroup.position.set(x, y, z);
      frameGroup.rotation.y = rotY;
      roomGroup.add(frameGroup);
    }

    function buildElevatorConcourse() {
      const doorMat = new THREE.MeshLambertMaterial({ color: 0xb08a3c });
      const leftDoor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.6, 0.2), doorMat);
      leftDoor.position.set(-0.9, 1.8, 9.8);
      roomGroup.add(leftDoor);

      const rightDoor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.6, 0.2), doorMat);
      rightDoor.position.set(0.9, 1.8, 9.8);
      roomGroup.add(rightDoor);

      const dial = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.1, 16), doorMat);
      dial.rotation.x = Math.PI / 2;
      dial.position.set(0, 4.0, 9.75);
      roomGroup.add(dial);

      interactiveObjects.push({
        id: "elevator_panel",
        label: "Elevator Concourse: Travel Between Floors",
        pos: new THREE.Vector3(0, 0, 8.5),
        radius: 2.2,
        action: openElevatorModal
      });
    }

    function createDesk(x, y, z, w, d, color) {
      const deskGroup = new THREE.Group();
      const top = new THREE.Mesh(new THREE.BoxGeometry(w, 0.14, d), new THREE.MeshLambertMaterial({ color: color }));
      top.position.y = 1.25;
      top.castShadow = true;
      top.receiveShadow = true;
      deskGroup.add(top);

      const legGeo = new THREE.BoxGeometry(0.12, 1.2, 0.12);
      const offsets = [[-w/2 + 0.15, -d/2 + 0.15], [w/2 - 0.15, -d/2 + 0.15], [-w/2 + 0.15, d/2 - 0.15], [w/2 - 0.15, d/2 - 0.15]];
      offsets.forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(legGeo, new THREE.MeshLambertMaterial({ color: 0x221309 }));
        leg.position.set(lx, 0.6, lz);
        deskGroup.add(leg);
      });

      // Briefcase prop from Art Department
      const caseBody = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.16, 0.38), new THREE.MeshLambertMaterial({ color: 0x3d1f0f }));
      caseBody.position.set(-w/2 + 0.4, 1.45, 0);
      deskGroup.add(caseBody);

      const latchMat = new THREE.MeshLambertMaterial({ color: 0xd4af37 });
      const latch1 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.17, 0.04), latchMat);
      latch1.position.set(-w/2 + 0.28, 1.46, 0.19);
      deskGroup.add(latch1);

      const latch2 = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.17, 0.04), latchMat);
      latch2.position.set(-w/2 + 0.52, 1.46, 0.19);
      deskGroup.add(latch2);

      deskGroup.position.set(x, y, z);
      roomGroup.add(deskGroup);

      const lampBase = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.05), new THREE.MeshLambertMaterial({ color: 0xb08a3c }));
      lampBase.position.set(x + w * 0.28, y + 1.35, z);
      roomGroup.add(lampBase);

      const lampShade = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 0.16, 12), new THREE.MeshLambertMaterial({ color: 0x2f6b3d }));
      lampShade.rotation.z = Math.PI / 2;
      lampShade.position.set(x + w * 0.28, y + 1.55, z);
      roomGroup.add(lampShade);

      const lampLight = new THREE.PointLight(0x90ff90, 1.1, 4);
      lampLight.position.set(x + w * 0.28, y + 1.45, z);
      roomGroup.add(lampLight);
    }

    // 1. FLOOR 1: INTERN
    function buildFloor1Intern() {
      createDesk(0, 0, 0, 6, 1.6, 0x3d2719);

      const chuteColors = [0x5b8ac2, 0x57a671, 0xc97258, 0xd19a19, 0x977bc4];
      for (let i = 0; i < 5; i++) {
        const cMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 3.2, 16), new THREE.MeshLambertMaterial({ color: chuteColors[i] }));
        cMesh.position.set(-11.5, 1.8, -6 + i * 2.8);
        roomGroup.add(cMesh);
      }

      const consoleMesh = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.1, 1.2), new THREE.MeshLambertMaterial({ color: 0x573e13 }));
      consoleMesh.position.set(7, 0.55, 2);
      roomGroup.add(consoleMesh);

      const lever = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.8), new THREE.MeshLambertMaterial({ color: 0xd4af37 }));
      lever.position.set(7, 1.3, 2);
      lever.rotation.z = 0.3;
      roomGroup.add(lever);

      interactiveObjects.push({
        id: "mailroom_chutes",
        label: "Pneumatic Mail Chutes: Route Department Dispatches",
        pos: new THREE.Vector3(-11, 0, 0),
        radius: 2.8,
        action: openMailroomChuteModal
      });

      interactiveObjects.push({
        id: "dispatch_lever",
        label: "Master Dispatch Lever: Tender Outgoing Mail",
        pos: new THREE.Vector3(7, 0, 2),
        radius: 2.2,
        action: pullDispatchLever
      });

      createChair(8, 0, -6, 1);
      interactiveObjects.push({
        id: "chair_intern",
        label: "Musical Chair Dispute: The Intern's Folding Chair",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(1)
      });
    }

    // 2. FLOOR 2: ANALYST
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
    }

    // 3. FLOOR 3: ASSOCIATE
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
    }

    // 4. FLOOR 4: VICE PRESIDENT
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
    }

    // 5. FLOOR 5: DIRECTOR
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
    }

    // 6. FLOOR 6: MANAGING DIRECTOR (Boss: what3verman)
    function buildFloor6MD() {
      createDesk(0, 0, -1.5, 9, 2.6, 0x24140b);

      const bossTex = loadTextureB64(ASSETS.boss_what3verman);
      const bossMat = new THREE.MeshBasicMaterial({ map: bossTex, transparent: true });
      const bossQuad = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 2.4), bossMat);
      bossQuad.position.set(0, 2.4, -3.2);
      roomGroup.add(bossQuad);

      createChair(0, 0, -3.2, 6);

      const lamp = new THREE.PointLight(0x2f6b3d, 1.8, 6);
      lamp.position.set(1.5, 1.6, -2);
      roomGroup.add(lamp);

      interactiveObjects.push({
        id: "md_boss_talk",
        label: "Audience with Managing Director (what3verman)",
        pos: new THREE.Vector3(0, 0, -1.5),
        radius: 2.8,
        action: openWhat3vermanModal
      });

      createChair(-6, 0, 2, 6);
      interactiveObjects.push({
        id: "chair_md",
        label: "Musical Chair Dispute: Green Banker's Chair (Boss Showdown)",
        pos: new THREE.Vector3(-6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(6)
      });
    }

    // 7. FLOOR 7: PARTNER
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
    }

    // 8. FLOOR 8: BOARD OF DIRECTORS
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
    }

    // 9. FLOOR 9: THE PENTHOUSE (The Chairman: Kingpickle)
    function buildFloor9Penthouse() {
      const skyGlow = new THREE.PointLight(0xffdf80, 2.5, 30);
      skyGlow.position.set(0, 5, 0);
      roomGroup.add(skyGlow);

      const kpTex = loadTextureB64(ASSETS.boss_kingpickle);
      const kpMat = new THREE.MeshBasicMaterial({ map: kpTex, transparent: true });
      const kpQuad = new THREE.Mesh(new THREE.PlaneGeometry(3.0, 3.0), kpMat);
      kpQuad.position.set(0, 2.8, -4.5);
      roomGroup.add(kpQuad);

      createDesk(0, 0, -2.8, 10, 3.2, 0x180b05);

      interactiveObjects.push({
        id: "kingpickle_audience",
        label: "The Chairman (Kingpickle): Audience at The Gilded Seat",
        pos: new THREE.Vector3(0, 0, -2.5),
        radius: 3.2,
        action: openKingpickleModal
      });

      createChair(-5, 0, -2, 9);
      interactiveObjects.push({
        id: "chair_throne",
        label: "Musical Chair Dispute: The Gilded Sovereign Throne (Final Showdown)",
        pos: new THREE.Vector3(-5, 0, -2),
        radius: 2.6,
        action: () => triggerMusicalChairsArena(9)
      });
    }

    function getFloorName(f) {
      if (f === 0) return "The Pavement · Security Gate";
      if (f === 1) return "Floor 1 · The Interns (Mailroom)";
      if (f === 2) return "Floor 2 · The Analysts (Ledgers)";
      if (f === 3) return "Floor 3 · The Associates (Deng Credit)";
      if (f === 4) return "Floor 4 · The Vice Presidents (Subscriptions)";
      if (f === 5) return "Floor 5 · The Directors (Archives)";
      if (f === 6) return "Floor 6 · Managing Director (what3verman)";
      if (f === 7) return "Floor 7 · The Partners (Syndicate)";
      if (f === 8) return "Floor 8 · The Board of Directors";
      if (f === 9) return "The Penthouse · The Chairman (Kingpickle)";
      return `Floor ${f}`;
    }

    // ==========================================================================
    // UI MODAL CONTROLLERS & INTERACTION DIALOGUES
    // ==========================================================================
    const modalEl = document.getElementById('taskModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalSubtitle = document.getElementById('modalSubtitle');
    const modalBody = document.getElementById('modalBody');

    function closeTaskModal() {
      playClick();
      modalEl.classList.remove('active');
    }

    function showMemoToast(title, body) {
      const t = document.getElementById('toastMemo');
      document.getElementById('toastTitle').innerText = title;
      document.getElementById('toastBody').innerText = body;
      t.style.display = 'block';
      setTimeout(() => { t.style.display = 'none'; }, 4000);
    }

    const elevModal = document.getElementById('elevatorModal');
    const elevList = document.getElementById('elevatorFloorList');

    function openElevatorModal() {
      playElevatorDing();
      elevList.innerHTML = "";

      for (let i = 0; i <= 9; i++) {
        const r = ROLES[i];
        const isCurrent = (i === currentFloor);
        const isUnlocked = (i <= unlockedFloor || flickerr.reviewScore >= r.minPts);

        const row = document.createElement('div');
        row.style.display = "flex";
        row.style.justifyContent = "space-between";
        row.style.alignItems = "center";
        row.style.padding = "10px 14px";
        row.style.background = isCurrent ? "#dfcfb0" : (isUnlocked ? "#f0e6d2" : "#ddceb8");
        row.style.border = isCurrent ? "2px solid var(--oxblood)" : "1px solid var(--rule)";
        row.style.opacity = isUnlocked ? "1" : "0.55";

        row.innerHTML = `
          <div>
            <strong style="font-family:'Cinzel';font-size:13px;color:${isCurrent ? 'var(--oxblood)' : 'var(--ink)'};">
              ${i === 0 ? 'LEVEL 0' : (i === 9 ? 'PENTHOUSE' : 'FLOOR ' + i)} · ${r.title.toUpperCase()}
            </strong>
            <div style="font-family:'IBM Plex Mono';font-size:10px;color:var(--ink-muted);">
              Chair: ${r.chair} | Required: ${r.minPts} Review Pts
            </div>
          </div>
          <div>
            ${isCurrent ? '<span style="font-family:\'IBM Plex Mono\';font-size:11px;font-weight:700;color:var(--oxblood);">[HERE]</span>' :
              (isUnlocked ? `<button class="desk-button" onclick="rideElevatorTo(${i})" style="padding:6px 12px;font-size:11px;">RIDE CAR</button>` :
                `<span style="font-family:'IBM Plex Mono';font-size:11px;color:#8a4040;">LOCKED (${r.minPts} pts)</span>`)}
          </div>
        `;
        elevList.appendChild(row);
      }
      elevModal.classList.add('active');
    }

    function closeElevatorModal() {
      playClick();
      elevModal.classList.remove('active');
    }

    function rideElevatorTo(targetFloor) {
      closeElevatorModal();
      playElevatorDing();
      currentFloor = targetFloor;
      buildFloorEnvironment();
      updateHUD();
      saveGame();
      showMemoToast("CAR DISPATCHED", `Arrived at ${getFloorName(currentFloor)}.`);
    }

    function openGatekeeperModal() {
      playClick();
      modalTitle.innerText = "SECURITY GATEKEEPER";
      modalSubtitle.innerText = "ADMISSIONS DESK · WEST GATE";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          The gatekeeper looks up over wire-rimmed glasses in the morning sun.
        </p>
        <blockquote style="font-style:italic;border-left:3px solid var(--lamp);padding-left:12px;margin-bottom:14px;color:var(--ink-muted);font-size:12px;">
          "Every applicant who enters these doors is sworn to a department fund. Choose your covenant carefully. You are now within The Mutual Fun. It operates with clockwork precision. Zero em dashes. Exact ledger entries."
        </blockquote>
        <div style="margin-bottom:14px;">
          <label style="font-family:'IBM Plex Mono';font-size:11px;font-weight:700;display:block;margin-bottom:6px;">SELECT YOUR DEPARTMENT COVENANT:</label>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            ${DEPARTMENTS.map((d, idx) => `
              <button class="desk-button" style="background:${d.color};color:#fff;text-align:left;padding:8px 12px;" onclick="enrollAtGate('${d.name}', ${idx})">
                ${d.name}
              </button>
            `).join('')}
          </div>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function enrollAtGate(deptName, deptIdx) {
      playStampThump();
      flickerr.department = deptName;
      flickerr.deptIndex = deptIdx;
      flickerr.gateAdmitted = true;
      flickerr.reviewScore = Math.max(flickerr.reviewScore, 15);
      unlockedFloor = Math.max(unlockedFloor, 1);
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("ADMISSION GRANTED", `Sworn to ${deptName}. Walk through the wrought iron turnstiles to Floor 1.`);
    }

    function openMailroomChuteModal() {
      playClick();
      modalTitle.innerText = "PNEUMATIC CHUTE DISPATCH";
      modalSubtitle.innerText = "DEPARTMENT LOGISTICS TUBE";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          Five brass cylinders feed into pressurized conduits. Route correspondence to your department:
        </p>
        <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:14px;">
          ${DEPARTMENTS.map((d, idx) => `
            <div style="display:flex;justify-content:space-between;align-items:center;background:#f5efe3;padding:8px 12px;border:1px solid ${d.color};">
              <span style="font-family:'IBM Plex Mono';font-size:11px;font-weight:700;color:${d.color};">${d.name}</span>
              <button class="desk-button" style="background:${d.color};padding:5px 12px;font-size:10px;" onclick="routeMailChute('${d.name}')">
                Send Capsule (0.015 ETH)
              </button>
            </div>
          `).join('')}
        </div>
      `;
      modalEl.classList.add('active');
    }

    function routeMailChute(fund) {
      playStampThump();
      flickerr.postsOnFile += 1;
      flickerr.postageETH += 0.015;
      flickerr.reviewScore += 5;
      flickerr.dengCredits += 25.0;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("PNEUMATIC TUBE FIRED", `Capsule routed to ${fund}. +5 Review Points, +25 Deng Credits.`);
    }

    function pullDispatchLever() {
      playStampThump();
      flickerr.reviewScore += 8;
      flickerr.dengCredits += 15.0;
      updateHUD();
      saveGame();
      showMemoToast("DISPATCH LEVER PULLED", "Master valve engaged. Outgoing ledger dispatches cleared. +8 Review Points.");
    }

    function openAnalystLedgerModal() {
      playClick();
      modalTitle.innerText = "LEDGER BALANCE SHEET";
      modalSubtitle.innerText = "FLOOR 2 · ANALYST BULLPEN";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          Cross-examine debit columns against vault receipts (0x48dF...A118). Balance the allocation:
        </p>
        <button class="desk-button" style="width:100%;" onclick="auditLedgerAction()">
          Certify Column Balances (+14 Review Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function auditLedgerAction() {
      playStampThump();
      flickerr.reviewScore += 14;
      flickerr.dengCredits += 35.0;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("LEDGER CERTIFIED", "Columns reconcile to the exact digit. +14 Review Points.");
    }

    function openDengModal() {
      playClick();
      modalTitle.innerText = "CASHIER WINDOW: DENG CREDITS";
      modalSubtitle.innerText = "FLOOR 3 · THE ASSOCIATE CONCOURSE";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          Tender Deng credit notes for settlement or convert corporate postage into certified slips:
        </p>
        <div style="display:flex;gap:10px;margin-bottom:14px;">
          <button class="desk-button" style="flex:1;" onclick="tenderDengSlip(50)">
            Deposit 50 Deng
          </button>
          <button class="desk-button" style="flex:1;" onclick="tenderDengSlip(100)">
            Deposit 100 Deng
          </button>
        </div>
      `;
      modalEl.classList.add('active');
    }

    function tenderDengSlip(cr) {
      playStampThump();
      flickerr.dengCredits += cr;
      flickerr.reviewScore += Math.floor(cr / 4);
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("DENG SLIP ACCEPTED", `Deposited ${cr} Deng credits. Review points increased.`);
    }

    function forgePassAction() {
      playStampThump();
      flickerr.hasPass = true;
      flickerr.reviewScore += 25;
      updateHUD();
      saveGame();
      showMemoToast("TMF PASS EMBOSSED", "Golden seal pressed into wax. Contract 0xED37...751a verified.");
    }

    function openSubscriptionModal() {
      playClick();
      modalTitle.innerText = "SHAREHOLDER SUBSCRIPTION ROLL";
      modalSubtitle.innerText = "FLOOR 4 · VICE PRESIDENT SUITE";

      modalBody.innerHTML = `
        <button class="desk-button" style="width:100%;" onclick="auditSubscriptionsAction()">
          Reconcile Share Allotments (+20 Review Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function auditSubscriptionsAction() {
      playStampThump();
      flickerr.reviewScore += 20;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("SUBSCRIPTIONS AUDITED", "Shareholder allotments balanced. +20 Review Points.");
    }

    function openDossierArchiveModal() {
      playClick();
      modalTitle.innerText = "FLAGGED DOSSIER ARCHIVE";
      modalSubtitle.innerText = "FLOOR 5 · DIRECTORATE";

      modalBody.innerHTML = `
        <button class="desk-button" style="width:100%;" onclick="signDossierAction()">
          Sign Off Compliance Clearance (+30 Review Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function signDossierAction() {
      playStampThump();
      flickerr.reviewScore += 30;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("DOSSIER APPROVED", "Compliance record closed with red wax seal. +30 Review Points.");
    }

    function openWhat3vermanModal() {
      playClick();
      modalTitle.innerText = "MANAGING DIRECTOR: WHAT3VERMAN";
      modalSubtitle.innerText = "FLOOR 6 · EXECUTIVE SUITE";

      modalBody.innerHTML = `
        <div style="display:flex;gap:14px;align-items:center;margin-bottom:14px;">
          <img src="${ASSETS.boss_what3verman}" style="width:72px;height:72px;border-radius:50%;border:2px solid var(--lamp);object-fit:cover;">
          <div>
            <h4 style="font-family:'Cinzel';font-size:15px;color:var(--oxblood);">WHAT3VERMAN</h4>
            <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--ink-muted);">Managing Director · Floor 6 Overseer</div>
          </div>
        </div>
        <blockquote style="font-style:italic;border-left:3px solid var(--green);padding-left:12px;margin-bottom:14px;color:var(--ink-muted);font-size:12px;">
          "You climb fast. But my green banker's chair is not given away on review points alone. You must out-reflex me in the arbitrage chamber when the needle scratches."
        </blockquote>
        <button class="desk-button" style="width:100%;background:var(--green);" onclick="closeTaskModal(); triggerMusicalChairsArena(6);">
          Challenge what3verman in The Chair Chamber (Floor 6)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function openPartnerSyndicateModal() {
      playClick();
      modalTitle.innerText = "PARTNERSHIP SYNDICATE";
      modalSubtitle.innerText = "FLOOR 7 · EXECUTIVE CHAMBER";

      modalBody.innerHTML = `
        <button class="desk-button" style="width:100%;" onclick="underwriteSyndicateAction()">
          Underwrite Quarterly Distribution (+45 Review Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function underwriteSyndicateAction() {
      playStampThump();
      flickerr.reviewScore += 45;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("SYNDICATE UNDERWRITTEN", "Partnership agreement signed in fountain ink. +45 Review Points.");
    }

    function openBoardConclaveModal() {
      playClick();
      modalTitle.innerText = "BOARD OF DIRECTORS CONCLAVE";
      modalSubtitle.innerText = "FLOOR 8 · HIGH COUNCIL";

      modalBody.innerHTML = `
        <button class="desk-button" style="width:100%;" onclick="conferBoardAction()">
          Receive Boardroom Clearance (+60 Review Pts)
        </button>
      `;
      modalEl.classList.add('active');
    }

    function conferBoardAction() {
      playStampThump();
      flickerr.reviewScore += 60;
      updateHUD();
      saveGame();
      closeTaskModal();
      showMemoToast("BOARDROOM CONCURRENCE", "The Governors affirm your standing. +60 Review Points.");
    }

    function openKingpickleModal() {
      playClick();
      modalTitle.innerText = "THE CHAIRMAN: KINGPICKLE";
      modalSubtitle.innerText = "PENTHOUSE · SEAT 0 & SEAT 1";

      modalBody.innerHTML = `
        <div style="display:flex;gap:14px;align-items:center;margin-bottom:14px;">
          <img src="${ASSETS.boss_kingpickle}" style="width:76px;height:76px;border-radius:50%;border:2px solid var(--lamp);object-fit:cover;">
          <div>
            <h4 style="font-family:'Cinzel';font-size:16px;color:var(--oxblood);">KINGPICKLE</h4>
            <div style="font-family:'IBM Plex Mono';font-size:11px;color:var(--lamp);">The Chairman · Sovereign Trustee</div>
          </div>
        </div>
        <blockquote style="font-style:italic;border-left:3px solid var(--lamp);padding-left:12px;margin-bottom:14px;color:var(--ink-muted);font-size:12px;">
          "Welcome to Seat 0. You started outside on the pavement. Now, you stand before the gilded throne. Win the final dispute, and the entire institution is yours."
        </blockquote>
        <button class="desk-button" style="width:100%;background:var(--lamp);color:#110b06;" onclick="closeTaskModal(); triggerMusicalChairsArena(9);">
          The Final Dispute: Challenge Kingpickle for The Gilded Throne
        </button>
      `;
      modalEl.classList.add('active');
    }

    // ==========================================================================
    // CUSTOM CHAIR ARBITRAGE ARENA ENGINE
    // ==========================================================================
    const arenaModal = document.getElementById('arenaModal');
    const chamberSubTitle = document.getElementById('chamberSubTitle');
    const arenaRoundLabel = document.getElementById('arenaRoundLabel');
    const arenaSignal = document.getElementById('arenaSignal');
    const arenaReactionDisplay = document.getElementById('arenaReactionDisplay');
    const arenaIntroOverlay = document.getElementById('arenaIntroOverlay');
    const arenaResultOverlay = document.getElementById('arenaResultOverlay');
    const deckHintText = document.getElementById('deckHintText');
    const chamberSitBtn = document.getElementById('chamberSitBtn');
    const rosterCount = document.getElementById('rosterCount');
    const rosterList = document.getElementById('rosterList');
    const floorDifficultyStat = document.getElementById('floorDifficultyStat');
    const floorTrackName = document.getElementById('floorTrackName');
    const chamberCanvas = document.getElementById('chamberCanvas');
    const ctx = chamberCanvas.getContext('2d');

    let arenaFloor = 1;
    let arenaChairName = "";
    let arenaChairTier = "";
    let arenaRound = 1;
    let arenaPhase = 'idle'; // 'idle', 'intro', 'countdown', 'green', 'red', 'resolving', 'won', 'lost'
    let arenaActive = [0, 1, 2, 3];
    let arenaChairs = [];
    let arenaSeated = {};
    let arenaMoves = {};
    let arenaAngle = 0;
    let arenaPhaseAt = 0;
    let arenaRedAt = 0;
    let arenaGreenFor = 0;
    let arenaFinishAt = 0;
    let arenaBots = [];
    let arenaLastReaction = null;
    let arenaLoser = null;
    let arenaEarly = false;
    let arenaContenders = [];
    let arenaAnimFrame = null;
    let canvasCountdownVal = 0;
    let countdownInterval = null;

    const FLOOR_REFLEX_DIFFICULTY = {
      1: { base: 460, spread: 130, label: "~460 ms" },
      2: { base: 410, spread: 120, label: "~410 ms" },
      3: { base: 360, spread: 110, label: "~360 ms" },
      4: { base: 310, spread: 100, label: "~310 ms" },
      5: { base: 260, spread: 90,  label: "~260 ms" },
      6: { base: 220, spread: 80,  label: "~220 ms (Boss: what3verman)" },
      7: { base: 195, spread: 70,  label: "~195 ms" },
      8: { base: 175, spread: 60,  label: "~175 ms" },
      9: { base: 155, spread: 50,  label: "~155 ms (Boss: Kingpickle)" }
    };

    function triggerMusicalChairsArena(floor) {
      arenaFloor = floor;
      const role = ROLES[floor];
      arenaChairName = role.chair;
      arenaChairTier = role.tier;

      chamberSubTitle.innerText = `FLOOR ${floor} DISPUTE · ${arenaChairName.toUpperCase()}`;
      floorDifficultyStat.innerText = FLOOR_REFLEX_DIFFICULTY[floor].label;
      floorTrackName.innerText = getFloorTrack(floor).name;

      setupArenaContenders();

      arenaRound = 1;
      arenaActive = [0, 1, 2, 3];
      arenaPhase = 'intro';
      arenaLastReaction = null;
      arenaReactionDisplay.innerText = "-- MS";

      document.getElementById('introFloorEyebrow').innerText = `FLOOR ${floor} CHAIR DISPUTE`;
      document.getElementById('introChairTitle').innerText = arenaChairName.toUpperCase();
      document.getElementById('introGuideBody').innerText =
        `There is always one chair too few. Circle the parquet marquetry while the phonograph spins. When the needle cuts and the boardroom bell tolls, seize an available seat immediately. Press SPACE to sit. Beware: sitting on green results in immediate forfeiture.`;

      const previewDiv = document.getElementById('introContendersPreview');
      previewDiv.innerHTML = arenaContenders.map(c => `<img class="chamber-thumb" src="${c.avatar}" title="${c.name}">`).join('');

      arenaIntroOverlay.classList.remove('hidden');
      arenaResultOverlay.classList.add('hidden');

      renderRoster();
      setArenaSignal('waiting', 'PHONOGRAPH READY');
      setDeckHint("Read house protocol. Press ENTER CHAMBER or [SPACE] to begin.");
      chamberSitBtn.disabled = true;

      arenaModal.classList.add('active');

      if (!arenaAnimFrame) {
        lastFrameTime = performance.now();
        arenaAnimFrame = requestAnimationFrame(arenaTick);
      }
    }

    function setupArenaContenders() {
      const flickerrAvatar = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      arenaContenders = [
        { id: 0, name: "You", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color }
      ];

      if (arenaFloor === 6) {
        arenaContenders.push({ id: 1, name: "what3verman", role: "Managing Director", fund: "Executive Desk", avatar: ASSETS.boss_what3verman, color: "#2f6b3d" });
        arenaContenders.push({ id: 2, name: "Smaug Arbitrageur", role: "Contender", fund: "The Smaug Fund", avatar: ASSETS.p_smaug_1, color: "#c97258" });
        arenaContenders.push({ id: 3, name: "Argon Auditor", role: "Contender", fund: "The Argon Fund", avatar: ASSETS.p_argon_1, color: "#5b8ac2" });
      } else if (arenaFloor === 9) {
        arenaContenders.push({ id: 1, name: "Kingpickle", role: "The Chairman", fund: "Seat 0 Trustee", avatar: ASSETS.boss_kingpickle, color: "#d4af37" });
        arenaContenders.push({ id: 2, name: "Board Governor A", role: "Governor", fund: "The Midas Fund", avatar: ASSETS.p_midas_1, color: "#d19a19" });
        arenaContenders.push({ id: 3, name: "Board Governor B", role: "Governor", fund: "The Vladd Fund", avatar: ASSETS.p_vladd_1, color: "#977bc4" });
      } else {
        const pool = [
          { name: "Bogle Senior Clerk", role: "Contender", fund: "The Bogle Fund", avatar: ASSETS.p_bogle_2, color: "#57a671" },
          { name: "Smaug Auditor", role: "Contender", fund: "The Smaug Fund", avatar: ASSETS.p_smaug_1, color: "#c97258" },
          { name: "Midas Analyst", role: "Contender", fund: "The Midas Fund", avatar: ASSETS.p_midas_1, color: "#d19a19" },
          { name: "Argon Specialist", role: "Contender", fund: "The Argon Fund", avatar: ASSETS.p_argon_1, color: "#5b8ac2" },
          { name: "Vladd Dispatcher", role: "Contender", fund: "The Vladd Fund", avatar: ASSETS.p_vladd_1, color: "#977bc4" }
        ];
        arenaContenders.push(Object.assign({ id: 1 }, pool[(arenaFloor * 2) % pool.length]));
        arenaContenders.push(Object.assign({ id: 2 }, pool[(arenaFloor * 2 + 1) % pool.length]));
        arenaContenders.push(Object.assign({ id: 3 }, pool[(arenaFloor * 2 + 2) % pool.length]));
      }
    }

    function renderRoster() {
      rosterCount.innerText = String(arenaActive.length).padStart(2, '0');
      rosterList.innerHTML = arenaContenders.map((c, i) => `
        <div class="roster-person ${arenaActive.includes(c.id) ? '' : 'out'}" style="border-left:4px solid ${c.color};">
          <img src="${c.avatar}" alt="${c.name}">
          <div>
            <strong>${c.name}</strong>
            <small>${arenaActive.includes(c.id) ? (c.id === 0 ? 'Your Aspirant' : c.fund) : 'Eliminated'}</small>
          </div>
          ${c.id === 0 ? '<span class="you-tag">YOU</span>' : ''}
        </div>
      `).join('');
    }

    function setArenaSignal(kind, text) {
      arenaSignal.className = `chamber-signal-pill ${kind}`;
      arenaSignal.innerText = text;
    }

    function setDeckHint(text) {
      deckHintText.innerText = text;
    }

    function layoutChairs() {
      const chairCount = arenaActive.length - 1;
      arenaChairs = Array.from({ length: chairCount }, (_, i) => ({
        x: 480 + (i - (chairCount - 1) / 2) * 120,
        y: 280
      }));
    }

    function startArenaMatch() {
      hideArenaOverlays();
      arenaActive = [0, 1, 2, 3];
      arenaRound = 1;
      arenaReactionDisplay.innerText = "-- MS";
      startArenaRound();
    }

    // CANVAS-RENDERED COUNTDOWN (No stuck DOM elements!)
    function startArenaRound() {
      hideArenaOverlays();
      if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
      }

      arenaPhase = 'countdown';
      arenaSeated = {};
      arenaMoves = {};
      arenaLoser = null;
      arenaEarly = false;
      arenaBots = [];
      arenaFinishAt = 0;
      arenaGreenFor = 3200 + Math.random() * 4200;
      layoutChairs();

      arenaRoundLabel.innerText = `ROUND 0${arenaRound} / 03`;
      chamberSitBtn.disabled = true;
      setArenaSignal('waiting', 'GET READY');
      setDeckHint("Three, two, one… Watch the turntable.");
      renderRoster();

      canvasCountdownVal = 3;
      tone(440, 0.09, 'sine', 0.05);

      countdownInterval = setInterval(() => {
        canvasCountdownVal--;
        if (canvasCountdownVal > 0) {
          tone(440, 0.09, 'sine', 0.05);
        } else {
          clearInterval(countdownInterval);
          countdownInterval = null;
          canvasCountdownVal = 0;
          arenaGoGreen(performance.now());
        }
      }, 820);
    }

    function hideArenaOverlays() {
      arenaIntroOverlay.classList.add('hidden');
      arenaResultOverlay.classList.add('hidden');
    }

    function arenaGoGreen(now) {
      arenaPhase = 'green';
      arenaPhaseAt = now;
      setArenaSignal('green', 'PHONOGRAPH ACTIVE');
      chamberSitBtn.disabled = false;
      setDeckHint("Hold your nerve. Turntable is spinning. Await the needle scratch.");

      startChamberPhonographTune(arenaFloor);
    }

    function calculateRivalDelay(botId, round) {
      const diff = FLOOR_REFLEX_DIFFICULTY[arenaFloor] || { base: 400, spread: 100 };
      const rng = (Math.random() + Math.random()) * 0.5;
      const reaction = diff.base + (rng - 0.5) * diff.spread - (round - 1) * 14;
      return Math.round(Math.max(130, reaction));
    }

    function arenaGoRed(now) {
      stopChamberPhonographTune();
      arenaPhase = 'red';
      arenaPhaseAt = now;
      arenaRedAt = now;

      const sceneWrap = document.getElementById('arenaSceneWrap');
      sceneWrap.classList.remove('scene-canvas-flash');
      void sceneWrap.offsetWidth;
      sceneWrap.classList.add('scene-canvas-flash');

      // Schedule rival bot reactions based on floor difficulty
      arenaBots = arenaActive.filter(id => id !== 0).map(id => ({
        id,
        at: now + calculateRivalDelay(id, arenaRound)
      })).sort((a, b) => a.at - b.at);

      setArenaSignal('red', 'NEEDLE CUT: SIT NOW');
      setDeckHint("Press SPACE or tap SEIZE SEAT to secure a chair.");
      
      // Play authentic vinyl scratch + boardroom bell chime
      playNeedleScratchAndBell();
    }

    function getContenderPosition(id) {
      const idx = arenaActive.indexOf(id);
      const angle = arenaAngle + (idx * Math.PI * 2) / arenaActive.length;
      return {
        x: 480 + Math.cos(angle) * 280,
        y: 280 + Math.sin(angle) * 98,
        angle
      };
    }

    function claimSeat(id) {
      if (arenaSeated[id] !== undefined) return false;
      const taken = Object.values(arenaSeated);
      const free = arenaChairs.map((c, i) => i).filter(i => !taken.includes(i));
      if (!free.length) return false;

      const p = getContenderPosition(id);
      free.sort((a, b) => Math.hypot(arenaChairs[a].x - p.x, arenaChairs[a].y - p.y) -
                          Math.hypot(arenaChairs[b].x - p.x, arenaChairs[b].y - p.y));

      arenaMoves[id] = { from: p, at: performance.now() };
      arenaSeated[id] = free[0];

      if (id === 0) {
        chamberSitBtn.disabled = true;
        setDeckHint("Seat secured. Hold your position.");
        tone(660, 0.12, 'sine', 0.06);
        setTimeout(() => tone(880, 0.16, 'sine', 0.08), 110);
      }

      if (Object.keys(arenaSeated).length === arenaChairs.length) {
        arenaLoser = arenaActive.find(i => arenaSeated[i] === undefined);
        arenaPhase = 'resolving';
        arenaFinishAt = performance.now() + 1000;
        chamberSitBtn.disabled = true;
      }
      return true;
    }

    function onSitClicked() {
      if (arenaPhase === 'green') {
        // FALSE START
        stopChamberPhonographTune();
        arenaLoser = 0;
        arenaPhase = 'resolving';
        arenaFinishAt = performance.now() + 700;
        arenaActive.filter(i => i !== 0).forEach((id, i) => { arenaSeated[id] = i; });
        chamberSitBtn.disabled = true;
        setDeckHint("Too soon. You moved while phonograph was still playing.");
        setArenaSignal('red', 'FALSE START');
        tone(110, 0.45, 'sawtooth', 0.1);
        arenaEarly = true;
        return;
      }

      if (arenaPhase !== 'red') return;

      const now = performance.now();
      for (const bot of arenaBots) {
        if (bot.at <= now && arenaSeated[bot.id] === undefined && arenaPhase === 'red') {
          claimSeat(bot.id);
        }
      }

      if (arenaPhase !== 'red') return;

      arenaLastReaction = Math.round(now - arenaRedAt);
      arenaReactionDisplay.innerText = `${arenaLastReaction} MS`;
      claimSeat(0);
    }

    function finishArenaRound() {
      const eliminated = arenaLoser;
      arenaActive = arenaActive.filter(i => i !== eliminated);
      renderRoster();

      const playerLost = (eliminated === 0);
      const playerWon = (!playerLost && arenaActive.length === 1);
      arenaPhase = playerLost ? 'lost' : (playerWon ? 'won' : 'between');

      const kicker = document.getElementById('resultKicker');
      const title = document.getElementById('resultTitle');
      const body = document.getElementById('resultBody');
      const btn = document.getElementById('resultBtn');

      if (playerLost) {
        kicker.innerText = "CHAIR FORFEITURE";
        title.innerText = arenaEarly ? "FALSE START." : "LEFT STANDING.";
        body.innerText = arenaEarly ?
          "You moved before the needle scratched. Wait for the bell and oxblood signal before making your move." :
          `Your rivals seized all remaining seats. (Your reaction: ${arenaLastReaction || '-'} ms). Train your reflexes and challenge again.`;
        btn.innerHTML = "TRY AGAIN [SPACE]";
        setArenaSignal('red', 'FORFEITED');
        tone(140, 0.4, 'sawtooth', 0.08);
      } else if (playerWon) {
        kicker.innerText = "CHAMPIONSHIP VICTORY";
        title.innerText = "THE LAST CHAIR IS YOURS";
        body.innerText = `Three rounds. Three flawless moves. You secure lawful title to ${arenaChairName} on Floor ${arenaFloor}.`;
        btn.innerHTML = "CLAIM CERTIFICATE & ADVANCE [SPACE]";
        setArenaSignal('green', 'TITLE SECURED');

        // Victory fanfare
        [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => tone(f, 0.22, 'sine', 0.08), i * 130));

        flickerr.chairName = arenaChairName;
        flickerr.chairTier = arenaChairTier;
        flickerr.role = ROLES[arenaFloor].title;
        unlockedFloor = Math.max(unlockedFloor, arenaFloor + 1);
        flickerr.reviewScore += (arenaFloor * 30);
        flickerr.dengCredits += (arenaFloor * 50);
        if (!flickerr.chairsWon.includes(arenaChairName)) {
          flickerr.chairsWon.push(arenaChairName);
        }
        updateHUD();
        saveGame();
      } else {
        const eliminatedName = arenaContenders[eliminated] ? arenaContenders[eliminated].name : "Rival";
        kicker.innerText = "ROUND COMPLETE";
        title.innerText = "SEAT SECURED";
        body.innerText = `${eliminatedName} is out. Next up: ${arenaActive.length} contenders, ${arenaActive.length - 1} chairs.`;
        btn.innerHTML = "NEXT ROUND [SPACE]";
        setArenaSignal('green', 'ROUND CLEARED');
      }

      arenaResultOverlay.classList.remove('hidden');
      arenaEarly = false;
    }

    function onResultBtnClick() {
      if (arenaPhase === 'between') {
        arenaRound++;
        startArenaRound();
      } else if (arenaPhase === 'won') {
        closeArenaModal();
        openCertModal();
      } else {
        startArenaMatch();
      }
    }

    function closeArenaModal() {
      stopChamberPhonographTune();
      if (countdownInterval) {
        clearInterval(countdownInterval);
        countdownInterval = null;
      }
      arenaModal.classList.remove('active');
      arenaPhase = 'idle';
    }

    // ==========================================================================
    // 2D CANVAS ARENA RENDERING (Parquet Marquetry, Inlaid Medallion, Turntable)
    // ==========================================================================
    let lastFrameTime = performance.now();

    function arenaTick(now) {
      try {
        const dt = Math.min((now - lastFrameTime) / 1000, 0.05);
        lastFrameTime = now;

        if (arenaModal.classList.contains('active')) {
          if (arenaPhase === 'intro' || arenaPhase === 'green') {
            arenaAngle += dt * (arenaPhase === 'intro' ? 0.22 : 0.75 + arenaRound * 0.12);
          }

          if (arenaPhase === 'green') {
            if (now - arenaPhaseAt >= arenaGreenFor) {
              arenaGoRed(now);
            }
          }

          if (arenaPhase === 'red') {
            for (const b of arenaBots) {
              if (now >= b.at && arenaPhase === 'red') {
                claimSeat(b.id);
              }
            }
            if (now - arenaRedAt > 2400 && arenaPhase === 'red') {
              arenaLoser = arenaActive.find(i => arenaSeated[i] === undefined) || 0;
              arenaPhase = 'resolving';
              arenaFinishAt = now + 600;
            }
          }

          if (arenaPhase === 'resolving' && now >= arenaFinishAt) {
            finishArenaRound();
          }

          drawChamberArenaCanvas(now);
        }
      } catch(e) {
        console.warn("Error in arenaTick:", e);
      }

      arenaAnimFrame = requestAnimationFrame(arenaTick);
    }

    function drawChamberArenaCanvas(now) {
      ctx.imageSmoothingEnabled = true;

      // 1. Concentric Marquetry Parquet Flooring
      ctx.fillStyle = "#331c10";
      ctx.fillRect(0, 0, 960, 540);

      // Radial wood planks
      ctx.save();
      ctx.translate(480, 280);
      for (let i = 0; i < 24; i++) {
        const ang = (i * Math.PI * 2) / 24;
        ctx.strokeStyle = (i % 2 === 0 ? "#3d2214" : "#2a160c");
        ctx.lineWidth = 14;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(ang) * 440, Math.sin(ang) * 220);
        ctx.stroke();
      }
      ctx.restore();

      // Outer inlaid brass ring
      ctx.strokeStyle = "#b08a3c";
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.ellipse(480, 280, 420, 190, 0, 0, Math.PI * 2);
      ctx.stroke();

      // Inner parquet disc
      ctx.fillStyle = "#4a2917";
      ctx.beginPath();
      ctx.ellipse(480, 280, 360, 160, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "#8a5f2a";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Central Golden TMF Medallion Inlaid in Floor
      ctx.save();
      ctx.translate(480, 280);
      ctx.fillStyle = "rgba(176, 138, 60, 0.22)";
      ctx.beginPath();
      ctx.ellipse(0, 0, 190, 80, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "rgba(212, 175, 55, 0.55)";
      ctx.lineWidth = 2;
      ctx.stroke();

      // Draw TMF Compass Star
      ctx.fillStyle = "rgba(212, 175, 55, 0.35)";
      for (let s = 0; s < 8; s++) {
        const sa = (s * Math.PI * 2) / 8;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(sa) * 160, Math.sin(sa) * 65);
        ctx.lineTo(Math.cos(sa + 0.2) * 50, Math.sin(sa + 0.2) * 20);
        ctx.closePath();
        ctx.fill();
      }
      ctx.restore();

      // 2. Animated 1987 Corporate Phonograph Turntable in Upper-Left Corner
      drawCornerPhonograph(85, 75, now);

      const items = [];

      // 3. Draw Chairs in the Center (matching the current floor)
      arenaChairs.forEach((ch, idx) => {
        items.push({
          y: ch.y,
          draw: () => {
            drawCustomFloorChair(ch.x, ch.y, arenaFloor);

            // Check if someone is sitting on this chair
            const occupantId = Object.keys(arenaSeated).find(k => arenaSeated[k] === idx);
            if (occupantId !== undefined) {
              const move = arenaMoves[occupantId];
              const t = move ? Math.min(1, Math.max(0, (now - move.at) / 180)) : 1;
              const ease = 1 - Math.pow(1 - t, 3);
              const curX = move ? move.from.x + (ch.x - move.from.x) * ease : ch.x;
              const curY = move ? move.from.y + (ch.y - 10 - move.from.y) * ease : ch.y - 10;

              drawAnimatedContender(+occupantId, curX, curY, false, now);
            }
          }
        });
      });

      // 4. Draw Walking Contenders
      const displayActive = (arenaPhase === 'intro') ? [0, 1, 2, 3] :
        [...new Set([...arenaActive, ...Object.keys(arenaSeated).map(Number), ...(arenaLoser === null ? [] : [arenaLoser])])];

      displayActive.forEach(id => {
        if (arenaSeated[id] !== undefined) return;

        let p = arenaActive.includes(id) ? getContenderPosition(id) : { x: 820, y: 390, angle: 0 };
        const isWalking = (arenaPhase === 'intro' || arenaPhase === 'green');

        items.push({
          y: p.y,
          draw: () => {
            // Natural drop shadow
            ctx.fillStyle = "rgba(10, 6, 4, 0.4)";
            ctx.beginPath();
            ctx.ellipse(p.x, p.y + 4, 22, 7, 0, 0, Math.PI * 2);
            ctx.fill();

            drawAnimatedContender(id, p.x, p.y, isWalking, now);
          }
        });
      });

      // Depth sort items by Y
      items.sort((a, b) => a.y - b.y).forEach(i => i.draw());

      // 5. Render Canvas Countdown (No stuck DOM elements!)
      if (arenaPhase === 'countdown' && canvasCountdownVal > 0) {
        ctx.save();
        ctx.fillStyle = "rgba(10, 6, 4, 0.6)";
        ctx.fillRect(0, 0, 960, 540);

        ctx.font = "bold 88px 'Cinzel', serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "#ffd875";
        ctx.shadowColor = "#000";
        ctx.shadowBlur = 16;
        ctx.fillText(canvasCountdownVal, 480, 260);

        ctx.font = "16px 'IBM Plex Mono', monospace";
        ctx.fillStyle = "#f5ebd5";
        ctx.shadowBlur = 4;
        ctx.fillText("PREPARE TO CIRCLE THE CHAIRS", 480, 320);
        ctx.restore();
      }

      // 6. Red Border Flash during RED phase
      if (arenaPhase === 'red') {
        ctx.strokeStyle = "#8a2424";
        ctx.lineWidth = 10;
        ctx.strokeRect(5, 5, 950, 530);
      }
    }

    // DRAW ANIMATED CORNER PHONOGRAPH
    function drawCornerPhonograph(cx, cy, now) {
      ctx.save();
      ctx.translate(cx, cy);

      // Wooden housing
      ctx.fillStyle = "#2e180d";
      ctx.fillRect(-55, -45, 110, 90);
      ctx.strokeStyle = "#b08a3c";
      ctx.lineWidth = 2;
      ctx.strokeRect(-55, -45, 110, 90);

      // Brass turntable platter
      ctx.fillStyle = "#d4af37";
      ctx.beginPath();
      ctx.arc(-10, 0, 34, 0, Math.PI * 2);
      ctx.fill();

      // Spinning vinyl record
      const spinAngle = (arenaPhase === 'green' ? now * 0.006 : 0);
      ctx.save();
      ctx.translate(-10, 0);
      ctx.rotate(spinAngle);

      ctx.fillStyle = "#16120e";
      ctx.beginPath();
      ctx.arc(0, 0, 31, 0, Math.PI * 2);
      ctx.fill();

      // Vinyl groove rings
      ctx.strokeStyle = "#2c241c";
      ctx.lineWidth = 1;
      [14, 20, 26].forEach(r => {
        ctx.beginPath();
        ctx.arc(0, 0, r, 0, Math.PI * 2);
        ctx.stroke();
      });

      // Center record label
      ctx.fillStyle = (arenaFloor === 6 ? "#2f6b3d" : (arenaFloor === 9 ? "#d4af37" : "#7a2e2e"));
      ctx.beginPath();
      ctx.arc(0, 0, 10, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Brass tone arm
      const armRot = (arenaPhase === 'green' ? 0.35 : 0.05);
      ctx.strokeStyle = "#b08a3c";
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(35, -28);
      ctx.lineTo(35 + Math.cos(armRot) * -34, -28 + Math.sin(armRot) * 42);
      ctx.stroke();

      ctx.fillStyle = "#8a5f2a";
      ctx.beginPath();
      ctx.arc(35, -28, 6, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();
    }

    // DRAW CUSTOM ANIMATED CONTENDER (Walking limbs, briefcase, seated posture)
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
      ctx.strokeRect(-12, -42 - walkBob, 24, 26);

      // Head
      ctx.fillStyle = "#eabf98";
      ctx.beginPath();
      ctx.arc(0, -52 - walkBob, 11, 0, Math.PI * 2);
      ctx.fill();

      // Hair
      ctx.fillStyle = (id === 1 && arenaFloor === 9 ? "#ffffff" : "#3d2719");
      ctx.beginPath();
      ctx.arc(0, -56 - walkBob, 11, Math.PI, Math.PI * 2);
      ctx.fill();

      // Crown for Kingpickle on Penthouse!
      if (arenaFloor === 9 && id === 1) {
        ctx.fillStyle = "#ffd700";
        ctx.beginPath();
        ctx.moveTo(-10, -64 - walkBob);
        ctx.lineTo(-10, -72 - walkBob);
        ctx.lineTo(-4, -67 - walkBob);
        ctx.lineTo(0, -74 - walkBob);
        ctx.lineTo(4, -67 - walkBob);
        ctx.lineTo(10, -72 - walkBob);
        ctx.lineTo(10, -64 - walkBob);
        ctx.closePath();
        ctx.fill();
      }

      // Leather Briefcase
      ctx.fillStyle = "#4a2412";
      ctx.fillRect(14, -30 - walkBob + legCycle * 0.3, 14, 11);
      ctx.fillStyle = "#d4af37";
      ctx.fillRect(17, -25 - walkBob + legCycle * 0.3, 3, 3);
      ctx.fillRect(22, -25 - walkBob + legCycle * 0.3, 3, 3);

      // Name Tag Badge
      if (id === 0) {
        ctx.fillStyle = "#2f6b3d";
        ctx.fillRect(-26, -74 - walkBob, 52, 16);
        ctx.fillStyle = "#fff";
        ctx.font = "bold 9px 'IBM Plex Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("YOU", 0, -62 - walkBob);
      } else if (id === 1 && (arenaFloor === 6 || arenaFloor === 9)) {
        ctx.fillStyle = "#7a2e2e";
        ctx.fillRect(-22, -74 - walkBob, 44, 16);
        ctx.fillStyle = "#ffd875";
        ctx.font = "bold 9px 'IBM Plex Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText("BOSS", 0, -62 - walkBob);
      }

      ctx.restore();
    }

    // DRAW CUSTOM CHAIRS PROCEDURALLY IN 2D
    function drawCustomFloorChair(x, y, floor) {
      ctx.save();
      ctx.translate(x, y);

      if (floor === 1) {
        // Floor 1: Intern's Folding Chair
        ctx.fillStyle = "#888";
        ctx.fillRect(-20, -12, 4, 38);
        ctx.fillRect(16, -12, 4, 38);
        ctx.fillStyle = "#cbb082";
        ctx.fillRect(-24, 6, 48, 10);
        ctx.fillStyle = "#aaa";
        ctx.fillRect(-18, -32, 36, 5);
        ctx.fillStyle = "#cbb082";
        ctx.fillRect(-16, -27, 32, 16);
      } else if (floor === 2) {
        // Floor 2: Typist Stool
        ctx.fillStyle = "#444";
        ctx.fillRect(-16, 10, 4, 26);
        ctx.fillRect(12, 10, 4, 26);
        ctx.strokeStyle = "#d4af37";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.ellipse(0, 24, 18, 6, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.fillStyle = "#8a5229";
        ctx.beginPath();
        ctx.ellipse(0, 8, 22, 10, 0, 0, Math.PI * 2);
        ctx.fill();
      } else if (floor === 3) {
        // Floor 3: Wooden Swivel
        ctx.fillStyle = "#4a2a12";
        ctx.fillRect(-22, 8, 44, 8);
        ctx.fillRect(-24, -30, 48, 6);
        for (let i = -16; i <= 16; i += 8) ctx.fillRect(i, -24, 3, 26);
        ctx.fillStyle = "#222";
        ctx.fillRect(-14, 26, 28, 5);
      } else if (floor === 4) {
        // Floor 4: Beige Task Chair
        ctx.fillStyle = "#1e1e1e";
        ctx.fillRect(-20, 26, 40, 5);
        ctx.fillRect(-3, 14, 6, 14);
        ctx.fillStyle = "#c4a36f";
        ctx.fillRect(-24, 6, 48, 12);
        ctx.fillRect(-20, -28, 40, 32);
      } else if (floor === 5) {
        // Floor 5: Leather Desk Chair
        ctx.fillStyle = "#ccc";
        ctx.fillRect(-22, 26, 44, 4);
        ctx.fillRect(-3, 12, 6, 16);
        ctx.fillStyle = "#111";
        ctx.fillRect(-26, 6, 52, 12);
        for (let i = -36; i <= -4; i += 8) {
          ctx.fillStyle = "#1c1c1c";
          ctx.fillRect(-22, i, 44, 6);
        }
      } else if (floor === 6) {
        // Floor 6: Green Banker's Chair
        ctx.fillStyle = "#3e180d";
        ctx.fillRect(-24, 24, 48, 6);
        ctx.fillStyle = "#1b432a";
        ctx.fillRect(-26, 6, 52, 14);
        ctx.fillStyle = "#d4af37";
        for (let i = -20; i <= 20; i += 10) ctx.fillRect(i, 16, 3, 3);
        ctx.fillStyle = "#3e180d";
        ctx.fillRect(-28, -26, 56, 6);
        ctx.fillRect(-28, -20, 6, 24);
        ctx.fillRect(22, -20, 6, 24);
      } else if (floor === 7) {
        // Floor 7: Oxblood Wingback Chair
        ctx.fillStyle = "#221108";
        ctx.fillRect(-22, 22, 6, 14);
        ctx.fillRect(16, 22, 6, 14);
        ctx.fillStyle = "#691717";
        ctx.fillRect(-28, 4, 56, 18);
        ctx.fillRect(-24, -38, 48, 40);
        ctx.fillRect(-34, -32, 10, 30);
        ctx.fillRect(24, -32, 10, 30);
      } else if (floor === 8) {
        // Floor 8: Boardroom High Seat
        ctx.fillStyle = "#2e150a";
        ctx.fillRect(-26, 18, 52, 16);
        ctx.fillStyle = "#0f1c3a";
        ctx.fillRect(-28, 4, 56, 16);
        ctx.fillRect(-26, -46, 52, 48);
        ctx.fillStyle = "#d4af37";
        ctx.fillRect(-30, -50, 60, 6);
      } else {
        // Floor 9: Gilded Sovereign Throne
        ctx.fillStyle = "#ffd700";
        ctx.fillRect(-32, 16, 64, 18);
        ctx.fillStyle = "#8b0000";
        ctx.fillRect(-28, 2, 56, 16);
        ctx.fillRect(-26, -52, 52, 52);
        ctx.fillStyle = "#ffd700";
        ctx.fillRect(-34, -14, 10, 20);
        ctx.fillRect(24, -14, 10, 20);
        ctx.beginPath();
        ctx.arc(0, -54, 14, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }

    // ==========================================================================
    // KEYBOARD INPUT & SPACEBAR INTEGRATION
    // ==========================================================================
    const keys = {};
    window.addEventListener('keydown', (e) => {
      const code = e.code.toLowerCase();
      keys[code] = true;

      if (arenaModal.classList.contains('active')) {
        if (e.code === 'Space') {
          e.preventDefault();
          if (!arenaIntroOverlay.classList.contains('hidden')) {
            startArenaMatch();
          } else if (!arenaResultOverlay.classList.contains('hidden')) {
            onResultBtnClick();
          } else if (arenaPhase === 'green' || arenaPhase === 'red') {
            onSitClicked();
          }
        }
        if (e.code === 'Escape') {
          closeArenaModal();
        }
        return;
      }

      if (e.code === 'KeyE') {
        checkInteractions();
      }
      if (e.code === 'Escape') {
        closeTaskModal();
        closeElevatorModal();
        closeCertModal();
      }
    });

    window.addEventListener('keyup', (e) => {
      keys[e.code.toLowerCase()] = false;
    });

    let cameraAngle = 0;

    function checkInteractions() {
      if (modalEl.classList.contains('active') || elevModal.classList.contains('active') ||
          arenaModal.classList.contains('active') || certModal.classList.contains('active')) return;

      for (const obj of interactiveObjects) {
        const dist = playerGroup.position.distanceTo(obj.pos);
        if (dist <= obj.radius) {
          obj.action();
          return;
        }
      }
    }

    // ==========================================================================
    // 3D ANIMATION LOOP (Third-person follow camera, walking bobbing)
    // ==========================================================================
    let walkClock = 0;
    let idleClock = 0;
    const promptEl = document.getElementById('interactPrompt');

    function animate() {
      requestAnimationFrame(animate);

      if (keys['keyq']) cameraAngle += 0.03;
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
      camera.lookAt(playerGroup.position.x, 1.2, playerGroup.position.z);

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

    // ==========================================================================
    // CERTIFICATE OF EMPLOYMENT (1200x675 Canvas Generator matching tmforgchart)
    // ==========================================================================
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

      g.fillStyle = PAPER;
      g.fillRect(0, 0, W, H);

      g.strokeStyle = INK;
      g.lineWidth = 4;
      g.strokeRect(20, 20, W - 40, H - 40);

      g.strokeStyle = GOLD;
      g.lineWidth = 2;
      g.strokeRect(26, 26, W - 52, H - 52);

      g.strokeStyle = F;
      g.lineWidth = 1;
      g.strokeRect(32, 32, W - 64, H - 64);

      g.fillStyle = OX;
      g.font = "bold 26px 'Cinzel', serif";
      g.textAlign = "center";
      g.fillText("THE MUTUAL FUN · CERTIFICATE OF APPOINTMENT", W / 2, 75);

      g.fillStyle = MUTED;
      g.font = "italic 13px 'Libre Caslon Text', serif";
      g.fillText("Incorporated under the Provisions of the General Syndicate Trust · Established 1987", W / 2, 98);

      const px = 160, py = 250, pr = 80;
      g.save();
      g.beginPath();
      g.arc(px, py, pr, 0, Math.PI * 2);
      g.clip();

      const memberImg = new Image();
      memberImg.src = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      if (memberImg.complete && memberImg.naturalWidth) {
        g.drawImage(memberImg, px - pr, py - pr, pr * 2, pr * 2);
      } else {
        g.fillStyle = "#e0d5be";
        g.fillRect(px - pr, py - pr, pr * 2, pr * 2);
      }
      g.restore();

      g.strokeStyle = GOLD;
      g.lineWidth = 4;
      g.beginPath();
      g.arc(px, py, pr, 0, Math.PI * 2);
      g.stroke();

      g.fillStyle = INK;
      g.font = "bold 12px 'IBM Plex Mono', monospace";
      g.fillText("YOU", px, py + pr + 22);
      g.fillStyle = MUTED;
      g.font = "11px 'IBM Plex Mono', monospace";
      g.fillText(`EMP NO. 401`, px, py + pr + 38);

      const cx = 640;
      g.fillStyle = INK;
      g.font = "16px 'Libre Caslon Text', serif";
      g.textAlign = "center";
      g.fillText("This official instrument certifies that the aspirant named herein has demonstrated faithful compliance,", cx, 160);
      g.fillText("having contested the company seats and secured lawful title to the office of:", cx, 184);

      g.fillStyle = F;
      g.font = "bold 34px 'Cinzel', serif";
      g.fillText(flickerr.role.toUpperCase(), cx, 235);

      g.fillStyle = OX;
      g.font = "italic 20px 'Libre Caslon Text', serif";
      g.fillText(`Occupant of ${flickerr.chairName}`, cx, 268);

      g.fillStyle = "#efe6d4";
      g.fillRect(320, 295, 640, 120);
      g.strokeStyle = GOLD;
      g.lineWidth = 1.5;
      g.strokeRect(320, 295, 640, 120);

      g.fillStyle = INK;
      g.font = "bold 12px 'IBM Plex Mono', monospace";
      g.textAlign = "left";
      g.fillText(`DEPARTMENT CONVENANT:   ${flickerr.department.toUpperCase()}`, 340, 325);
      g.fillText(`RANK CLASSIFICATION:   ${flickerr.chairTier.toUpperCase()}`, 340, 350);
      g.fillText(`REVIEW CREDITS:        ${flickerr.reviewScore} POINTS ON RECORD`, 340, 375);
      g.fillText(`DENG SETTLEMENT:       ${flickerr.dengCredits.toFixed(2)} CREDITS HELD`, 340, 400);

      const sigY = 540;
      g.strokeStyle = INK;
      g.lineWidth = 1;
      g.beginPath();
      g.moveTo(340, sigY);
      g.lineTo(540, sigY);
      g.moveTo(740, sigY);
      g.lineTo(940, sigY);
      g.stroke();

      g.fillStyle = INK;
      g.font = "italic 13px 'Libre Caslon Text', serif";
      g.textAlign = "center";
      g.fillText("what3verman", 440, sigY - 8);
      g.fillText("Kingpickle", 840, sigY - 8);

      g.font = "10px 'IBM Plex Mono', monospace";
      g.fillStyle = MUTED;
      g.fillText("MANAGING DIRECTOR (FLOOR 6)", 440, sigY + 16);
      g.fillText("THE CHAIRMAN (SEAT 0)", 840, sigY + 16);

      g.font = "9px 'IBM Plex Mono', monospace";
      g.fillStyle = "#8a7e6d";
      g.fillText("DEPLOYER: 0x4609585Ac28c827678B1554DfcE3bc6b411dAa3e | PASS: 0xED37605FF0e513e46d50B26244DEb2024189751a | VAULT: 0x48dF666dA1D12c952aFfCda214e30958a512A118", W / 2, 645);
    }

    function downloadCert() {
      const link = document.createElement('a');
      link.download = `TMF_Certificate_You_${flickerr.role.replace(/\\s+/g, '_')}.png`;
      link.href = certCanvas.toDataURL('image/png');
      link.click();
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    loadGame();
    buildFloorEnvironment();
    updateHUD();
    animate();
  </script>
</body>
</html>
'''

final_html = html_template.replace('__ASSETS_JSON__', json.dumps(assets))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

brain_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated Custom 1987 Chair Arbitrage Arena successfully!")
