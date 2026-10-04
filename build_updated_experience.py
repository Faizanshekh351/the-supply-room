import json
import base64
import os

print("Building updated experience with Art Department walls, Sunny morning outdoor, Real animated sprites, and Fixed countdown...")

# Load assets
with open("assets_encoded.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

print(f"Loaded {len(assets)} encoded assets.")

html_template = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>The Supply Room · 1987 corporate Odyssey</title>
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
      --edge: #503820;
      --bogle: #57a671;
      --argon: #5b8ac2;
      --smaug: #c97258;
      --midas: #d19a19;
      --vladd: #977bc4;
      --pixel: 'Press Start 2P', monospace;
      --retro: 'VT323', monospace;
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
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.18) 50%),
                  linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
      background-size: 100% 3px, 4px 100%;
      z-index: 10;
      opacity: 0.55;
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
       LAST CHAIR RETRO ARCADE CABINET (Musical Chairs Fight Engine)
       Faithfully matching https://last-chair-five.vercel.app/
       ========================================================================== */
    .musical-arena-overlay {
      position: absolute;
      inset: 0;
      background: rgba(8, 5, 4, 0.95);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 70;
      padding: 16px;
    }
    .musical-arena-overlay.active { display: flex; }

    .lastchair-cabinet {
      width: 1100px;
      max-width: 98vw;
      max-height: 94vh;
      display: flex;
      flex-direction: column;
      background: #e8d6a5;
      border: 5px solid var(--edge);
      box-shadow: 0 0 0 4px #d9bd7d, 0 0 0 8px #574228, 12px 18px 0 rgba(20, 15, 10, 0.85);
      position: relative;
      overflow: hidden;
      font-family: var(--retro);
    }

    .lastchair-header {
      min-height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 24px;
      background: #485641;
      border-bottom: 5px solid var(--edge);
      box-shadow: inset 0 3px #708160, inset 0 -3px #293a2e;
    }
    .lastchair-brand {
      display: flex;
      align-items: center;
      gap: 14px;
      color: #f1d999;
      font-family: var(--pixel);
      font-size: 15px;
      letter-spacing: -0.5px;
      text-shadow: 2px 2px #282e26;
    }
    .lastchair-brand small {
      font-family: var(--retro);
      font-size: 15px;
      letter-spacing: 1.5px;
      color: #c4c9a2;
      display: block;
      margin-top: 2px;
      text-shadow: none;
    }
    .lastchair-mark {
      width: 44px;
      height: 44px;
      line-height: 38px;
      text-align: center;
      background: #7c3038;
      border: 3px solid #b7955e;
      color: #e8d6a5;
      font-family: var(--pixel);
      font-size: 14px;
      box-shadow: inset 0 0 0 3px #4e2926, 3px 3px #273327;
      flex-shrink: 0;
    }
    .lastchair-head-actions {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .cabinet-btn {
      padding: 8px 14px;
      background: #d4bf85;
      border: 3px solid #382c21;
      box-shadow: inset 2px 2px #f0dfab, inset -2px -2px #aa884b, 2px 2px #29392c;
      font-family: var(--pixel);
      font-size: 10px;
      cursor: pointer;
      color: #382a20;
    }
    .cabinet-btn:hover { background: #dfcb93; }
    .cabinet-btn:active { transform: translateY(2px); }

    .lastchair-body {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: 12px;
      padding: 12px;
      background: #b79a62;
      overflow-y: auto;
    }

    .lastchair-stage {
      min-width: 0;
      border: 4px solid var(--edge);
      background: #e8d6a5;
      box-shadow: 3px 3px #80643c;
      display: flex;
      flex-direction: column;
    }

    .lastchair-stage-top {
      min-height: 48px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      padding: 8px 16px;
      color: #e5d8b0;
      background: #40392b;
      border-bottom: 4px solid var(--edge);
      box-shadow: inset 0 2px #65543a;
      font-family: var(--retro);
      font-size: 18px;
      letter-spacing: 1px;
    }

    .lastchair-signal {
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: var(--pixel);
      font-size: 11px;
      color: #e1ca8c;
    }
    .lastchair-signal i {
      display: block;
      width: 14px;
      height: 14px;
      background: #92886a;
      box-shadow: 0 0 0 2px #252e23, 2px 2px 0 2px #30291f;
    }
    .lastchair-signal.green { color: #b5d28c; }
    .lastchair-signal.green i {
      background: #a3c47c;
      box-shadow: 0 0 0 2px #252e23, 0 0 0 5px #617e46;
      animation: pulseGreenLed 0.8s infinite alternate;
    }
    .lastchair-signal.red { color: #ffd094; }
    .lastchair-signal.red i {
      background: #e5664c;
      box-shadow: 0 0 0 2px #252e23, 0 0 0 5px #ab443b;
      animation: pulseRedLed 0.3s infinite alternate;
    }
    @keyframes pulseGreenLed { 0% { opacity: 0.7; } 100% { opacity: 1; filter: brightness(1.2); } }
    @keyframes pulseRedLed { 0% { opacity: 0.8; } 100% { opacity: 1; filter: brightness(1.4); } }

    .lastchair-scene-wrap {
      position: relative;
      aspect-ratio: 16/10;
      background: #3a4732;
      overflow: hidden;
    }
    #lastchairCanvas {
      width: 100%;
      height: 100%;
      display: block;
      image-rendering: pixelated;
    }
    .scene-crt-scan {
      position: absolute;
      inset: 0;
      pointer-events: none;
      background: repeating-linear-gradient(transparent 0 3px, rgba(27, 34, 8, 0.08) 3px 4px);
      box-shadow: inset 0 0 0 3px rgba(68, 46, 36, 0.4);
    }
    .scene-canvas-flash {
      animation: arenaFlashBorder 0.15s 2;
    }
    @keyframes arenaFlashBorder {
      50% { filter: brightness(1.3) contrast(1.2); }
    }

    /* SCENE OVERLAYS (Intro, Countdown, Result) */
    .scene-overlay {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(41, 50, 37, 0.65);
      z-index: 5;
      padding: 16px;
    }
    .scene-overlay.hidden { display: none !important; }

    .intro-card {
      width: 440px;
      max-width: 95%;
      padding: 22px 20px;
      text-align: center;
      background: #e5d3a0;
      border: 4px solid #533a25;
      box-shadow: inset 0 0 0 4px #f7e7b8, 0 0 0 4px #b59557, 0 0 0 8px #4b3522, 10px 14px rgba(48, 39, 31, 0.6);
      font-family: var(--retro);
    }
    .intro-eyebrow {
      font-size: 15px;
      letter-spacing: 1.5px;
      color: #705330;
      text-transform: uppercase;
    }
    .intro-card h2 {
      font-family: var(--pixel);
      font-size: 15px;
      line-height: 1.6;
      margin: 10px 0 12px;
      color: #63312b;
      text-shadow: 2px 2px #c4ac74;
    }
    .intro-card p {
      font-size: 19px;
      line-height: 1.25;
      color: #4b3a24;
      margin-bottom: 16px;
    }
    .intro-card-contenders-preview {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-bottom: 16px;
    }
    .intro-contender-thumb {
      width: 48px;
      height: 48px;
      border: 2px solid #533a25;
      background: #baa270;
      object-fit: cover;
      box-shadow: 2px 2px rgba(0,0,0,0.3);
    }

    .primary-arcade-btn {
      width: 100%;
      background: #526644;
      border: 3px solid #2c392b;
      color: #f5e5b8;
      padding: 14px;
      font-family: var(--pixel);
      font-size: 11px;
      text-align: center;
      cursor: pointer;
      box-shadow: inset 2px 2px #839260, inset -2px -2px #364b32, 0 4px #2b3728;
    }
    .primary-arcade-btn:hover { background: #61774d; }
    .primary-arcade-btn:active { transform: translateY(3px); box-shadow: inset 2px 2px #364b32, 0 1px #2b3728; }

    .countdown-number {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--pixel);
      font-size: 84px;
      color: #f7e7bd;
      text-shadow: 6px 6px #443422;
      pointer-events: none;
      z-index: 6;
      animation: pulseCount 0.4s ease-out;
    }
    @keyframes pulseCount {
      0% { transform: scale(1.4); opacity: 0; }
      100% { transform: scale(1.0); opacity: 1; }
    }

    /* CONTROL DECK */
    .lastchair-control-deck {
      min-height: 84px;
      padding: 12px 18px;
      display: flex;
      gap: 14px;
      align-items: center;
      border-top: 4px solid var(--edge);
      background: #dcc38c;
      box-shadow: inset 0 3px #f0dca7;
      font-family: var(--retro);
    }
    .lastchair-control-deck > div { flex: 1; }
    .deck-hint {
      font-size: 20px;
      line-height: 1.15;
      color: #443422;
      margin-top: 3px;
    }
    .deck-eyebrow {
      font-size: 14px;
      letter-spacing: 1px;
      color: #725835;
      text-transform: uppercase;
    }

    #lastchairSitBtn {
      background: #863c3e;
      color: #ffe4ad;
      border: 4px solid #492a26;
      box-shadow: inset 3px 3px #b95d54, inset -3px -3px #602c30, 0 5px #4b3326;
      min-width: 170px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      font-family: var(--pixel);
      font-size: 13px;
      cursor: pointer;
    }
    #lastchairSitBtn kbd {
      font-family: var(--retro);
      font-size: 18px;
      padding: 2px 7px;
      border: 2px solid #cf9b73;
      background: #572b2b;
      color: #e9cd9d;
    }
    #lastchairSitBtn:not(:disabled):active {
      transform: translateY(3px);
      box-shadow: inset 3px 3px #602c30, 0 2px #4b3326;
    }
    #lastchairSitBtn:disabled {
      filter: saturate(0.3);
      opacity: 0.6;
      cursor: not-allowed;
    }

    /* ASIDE SIDEBAR */
    .lastchair-aside {
      padding: 14px 12px;
      background: #c4c9a4;
      border: 4px solid var(--edge);
      box-shadow: inset 0 0 0 2px #e2dfb4, 3px 3px #80643c;
      font-family: var(--retro);
    }
    .aside-title-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 10px;
      margin-bottom: 12px;
      border-bottom: 3px solid #7c805e;
    }
    .aside-title-row h4 {
      font-family: var(--pixel);
      font-size: 10px;
      color: #382a20;
    }
    .aside-count-badge {
      font-size: 19px;
      background: #526044;
      padding: 1px 7px;
      color: #e6dcae;
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
    }
    .roster-person img {
      width: 44px;
      height: 44px;
      object-fit: cover;
      border: 2px solid #6e5433;
      box-shadow: 2px 2px #8b8e65;
    }
    .roster-person strong {
      display: block;
      font-size: 20px;
      font-weight: normal;
      color: #382a20;
    }
    .roster-person small {
      display: block;
      font-size: 15px;
      color: #606344;
      margin-top: 1px;
    }
    .roster-person .you-tag {
      font-family: var(--pixel);
      font-size: 9px;
      color: #e9deb6;
      background: #596746;
      padding: 2px 4px;
      margin-left: auto;
    }
    .roster-person.out {
      opacity: 0.45;
      text-decoration: line-through;
    }
    .roster-person.out img {
      filter: grayscale(1);
    }

    .cabinet-rules-box {
      margin-top: 16px;
      padding-top: 12px;
      border-top: 3px solid #7c805e;
    }
    .rules-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      margin: 8px 0;
      font-size: 16px;
      line-height: 1.15;
      color: #4b4f35;
    }
    .dot-green, .dot-red {
      width: 10px;
      height: 10px;
      flex-shrink: 0;
      margin-top: 4px;
      box-shadow: 1px 1px #222;
    }
    .dot-green { background: #6f884e; }
    .dot-red { background: #a64f42; }

    .cabinet-reflex-stat {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 3px solid #7c805e;
      margin-top: 14px;
      padding-top: 10px;
      font-size: 15px;
      letter-spacing: 0.5px;
    }
    .cabinet-reflex-stat strong {
      font-size: 24px;
      color: #29392c;
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
       THE LAST CHAIR MUSICAL CHAIRS ARENA (CABINET OVERLAY)
       ========================================================================== -->
  <div class="musical-arena-overlay" id="arenaModal">
    <div class="lastchair-cabinet">
      <!-- Cabinet Header -->
      <div class="lastchair-header">
        <div class="lastchair-brand">
          <span class="lastchair-mark">TMF</span>
          <div>
            THE SUPPLY ROOM · MUSICAL CHAIRS
            <small id="cabinetSubTitle">FLOOR 1 DISPUTE · THE INTERN'S FOLDING CHAIR</small>
          </div>
        </div>
        <div class="lastchair-head-actions">
          <button class="cabinet-btn" id="cabinetSoundBtn" onclick="toggleCabinetSound()">SOUND: ON</button>
          <button class="cabinet-btn" onclick="closeArenaModal()">CONCEDE ✕</button>
        </div>
      </div>

      <!-- Cabinet Layout -->
      <div class="lastchair-body">
        <!-- Play Section -->
        <div class="lastchair-stage">
          <div class="lastchair-stage-top">
            <span id="arenaRoundLabel">ROUND 01 / 03</span>
            <div class="lastchair-signal" id="arenaSignal">
              <i></i>
              <span>GET READY</span>
            </div>
            <div style="font-family:'VT323';font-size:22px;">
              REFLEX: <strong id="arenaReactionDisplay" style="color:#f7e7bd;">-- ms</strong>
            </div>
          </div>

          <div class="lastchair-scene-wrap" id="arenaSceneWrap">
            <canvas id="lastchairCanvas" width="960" height="600"></canvas>
            <div class="scene-crt-scan"></div>

            <!-- Countdown Overlay -->
            <div class="countdown-number hidden" id="arenaCountdown">3</div>

            <!-- Intro / Loading Screen Overlay -->
            <div class="scene-overlay" id="arenaIntroOverlay">
              <div class="intro-card">
                <div class="intro-eyebrow" id="introFloorEyebrow">FLOOR 1 CHAIR DISPUTE</div>
                <h2 id="introChairTitle">THE INTERN'S FOLDING CHAIR</h2>
                <p id="introGuideBody">
                  There is always one chair too few. Circle the seats while the corporate turntable plays. When the needle cuts and the screen flashes RED, dive for a chair instantly.
                </p>
                <div class="intro-card-contenders-preview" id="introContendersPreview"></div>
                <button class="primary-arcade-btn" onclick="startArenaMatch()">
                  ENTER ARENA [SPACE]
                </button>
              </div>
            </div>

            <!-- Result Overlay -->
            <div class="scene-overlay hidden" id="arenaResultOverlay">
              <div class="intro-card">
                <div class="intro-eyebrow" id="resultKicker">ROUND COMPLETE</div>
                <h2 id="resultTitle">SEAT SECURED</h2>
                <p id="resultBody">
                  Rival eliminated. Next up: 3 contenders, 2 chairs.
                </p>
                <button class="primary-arcade-btn" id="resultBtn" onclick="onResultBtnClick()">
                  NEXT ROUND [SPACE]
                </button>
              </div>
            </div>
          </div>

          <!-- Control Deck -->
          <div class="lastchair-control-deck">
            <div>
              <div class="deck-eyebrow">CHAIR CONTEST CONTROLS</div>
              <p class="deck-hint" id="deckHintText">Hold your nerve. Wait for the needle to cut.</p>
            </div>
            <button id="lastchairSitBtn" onclick="onSitClicked()" disabled>
              SIT <kbd>SPACE</kbd>
            </button>
          </div>
        </div>

        <!-- Aside Sidebar -->
        <div class="lastchair-aside">
          <div class="aside-title-row">
            <h4>CONTENDERS</h4>
            <span class="aside-count-badge" id="rosterCount">04</span>
          </div>

          <div class="roster-list" id="rosterList"></div>

          <div class="cabinet-rules-box">
            <div style="font-family:'Press Start 2P';font-size:9px;color:#382a20;margin-bottom:8px;">HOUSE RULES</div>
            <div class="rules-item">
              <div class="dot-green"></div>
              <div><strong>Walk on green:</strong> Circle the seats while turntable plays.</div>
            </div>
            <div class="rules-item">
              <div class="dot-red"></div>
              <div><strong>Sit on red:</strong> When the needle cuts, press SPACE or tap SIT!</div>
            </div>
            <div class="rules-item" style="color:#7a2e2e;">
              <div>⚠️</div>
              <div><strong>Too soon:</strong> Sitting on green triggers immediate disqualification!</div>
            </div>
          </div>

          <div class="cabinet-reflex-stat">
            <span>RIVAL DIFFICULTY:</span>
            <strong id="floorDifficultyStat">~460 ms</strong>
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

    // Medallion HUD setup
    if (ASSETS.medallion) {
      document.getElementById('hudMedallion').src = ASSETS.medallion;
    }

    // ==========================================================================
    // AUDIO ENGINE (Web Audio API Synthesizer)
    // ==========================================================================
    let audioCtx = null;
    let cabinetSound = true;

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
      if (!cabinetSound) return;
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

    function playStampThump() {
      if (!cabinetSound) return;
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
      if (!cabinetSound) return;
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

    function toggleCabinetSound() {
      cabinetSound = !cabinetSound;
      document.getElementById('cabinetSoundBtn').innerText = `SOUND: ${cabinetSound ? 'ON' : 'OFF'}`;
      if (cabinetSound) tone(440, 0.1);
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

    // LOCAL STORAGE PERSISTENCE
    const SAVE_KEY = "tmf_odyssey_save_v5";

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
      document.getElementById('hudRole').innerText = `Flickerr · ${flickerr.role}`;
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
    scene.background = new THREE.Color(0x8ab4f8); // Sunny morning default

    const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.1, 150);

    // Player group (Flickerr)
    const playerGroup = new THREE.Group();
    scene.add(playerGroup);

    // Flickerr character mesh (Stylized 1987 corporate clerk in navy business suit with tie)
    const suitMat = new THREE.MeshLambertMaterial({ color: 0x222a38 });
    const shirtMat = new THREE.MeshLambertMaterial({ color: 0xf5f0ea });
    const tieMat = new THREE.MeshLambertMaterial({ color: 0x7a2e2e });
    const skinMat = new THREE.MeshLambertMaterial({ color: 0xeabf98 }); // Clean human skin tone matching bogle-03!
    const hairMat = new THREE.MeshLambertMaterial({ color: 0x332218 }); // Neat brown hair

    // Torso
    const torso = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.85, 0.4), suitMat);
    torso.position.y = 1.0;
    torso.castShadow = true;
    playerGroup.add(torso);

    // Shirt collar
    const collar = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.28, 0.41), shirtMat);
    collar.position.set(0, 1.3, 0);
    playerGroup.add(collar);

    // Tie
    const tie = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.4, 0.42), tieMat);
    tie.position.set(0, 1.15, 0);
    playerGroup.add(tie);

    // Head (Clean human features, no monkey!)
    const head = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.42, 0.4), skinMat);
    head.position.set(0, 1.62, 0);
    head.castShadow = true;
    playerGroup.add(head);

    // Hair
    const hair = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.16, 0.42), hairMat);
    hair.position.set(0, 1.83, 0);
    playerGroup.add(hair);

    // Limbs
    const legGeo = new THREE.BoxGeometry(0.22, 0.65, 0.24);
    const leftLeg = new THREE.Mesh(legGeo, suitMat);
    leftLeg.position.set(-0.18, 0.35, 0);
    leftLeg.castShadow = true;
    playerGroup.add(leftLeg);

    const rightLeg = new THREE.Mesh(legGeo, suitMat);
    rightLeg.position.set(0.18, 0.35, 0);
    rightLeg.castShadow = true;
    playerGroup.add(rightLeg);

    const armGeo = new THREE.BoxGeometry(0.18, 0.65, 0.2);
    const leftArm = new THREE.Mesh(armGeo, suitMat);
    leftArm.position.set(-0.46, 0.95, 0);
    leftArm.castShadow = true;
    playerGroup.add(leftArm);

    const rightArm = new THREE.Mesh(armGeo, suitMat);
    rightArm.position.set(0.46, 0.95, 0);
    rightArm.castShadow = true;
    playerGroup.add(rightArm);

    // Interactive object tracking
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
        // FLOOR 3: CREAKING WOODEN SWIVEL (Solid dark oak with slat back & brass casters)
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
        // FLOOR 4: BEIGE TASK CHAIR (1980s ergonomic executive task chair)
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
        // FLOOR 6: GREEN BANKER'S CHAIR (Managing Director / what3verman Boss chair)
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
      // CRISP BRIGHT SUNNY MORNING ATMOSPHERE
      scene.background = new THREE.Color(0x8ab4f8); // Bright morning blue sky
      scene.fog = new THREE.FogExp2(0x8ab4f8, 0.007); // Subtle morning haze

      // Morning Sun: Bright warm directional sunlight with crisp shadows
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

      // Morning ambient light
      const skyAmb = new THREE.AmbientLight(0xcde0f7, 1.3);
      roomGroup.add(skyAmb);

      // Sunny Asphalt Road
      const road = new THREE.Mesh(new THREE.PlaneGeometry(40, 18), new THREE.MeshLambertMaterial({ color: 0x33363d }));
      road.rotation.x = -Math.PI / 2;
      road.position.set(0, 0, 7);
      road.receiveShadow = true;
      roomGroup.add(road);

      // Sunny Morning Stone Sidewalk
      const curb = new THREE.Mesh(new THREE.BoxGeometry(40, 0.25, 14), new THREE.MeshLambertMaterial({ color: 0x8a847c }));
      curb.position.set(0, 0.125, -5);
      curb.receiveShadow = true;
      roomGroup.add(curb);

      // Brick facade of 1987 corporate headquarters in morning sun
      const wallMat = new THREE.MeshLambertMaterial({ color: 0x7a3e2e });
      const facade = new THREE.Mesh(new THREE.BoxGeometry(40, 18, 2), wallMat);
      facade.position.set(0, 9, -12);
      facade.receiveShadow = true;
      roomGroup.add(facade);

      // Grand Entrance Archway
      const archMat = new THREE.MeshLambertMaterial({ color: 0xc49e4d });
      const arch = new THREE.Mesh(new THREE.BoxGeometry(6.5, 6.5, 2.2), archMat);
      arch.position.set(0, 3.25, -12);
      arch.castShadow = true;
      roomGroup.add(arch);

      // Wrought iron gate with brass finials
      const gateMat = new THREE.MeshLambertMaterial({ color: 0x181818 });
      const gateL = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.2, 0.15), gateMat);
      gateL.position.set(-1.3, 2.1, -10.9);
      roomGroup.add(gateL);

      const gateR = new THREE.Mesh(new THREE.BoxGeometry(2.4, 4.2, 0.15), gateMat);
      gateR.position.set(1.3, 2.1, -10.9);
      roomGroup.add(gateR);

      // Security Gatekeeper Booth in warm polished wood
      const booth = new THREE.Mesh(new THREE.BoxGeometry(2.6, 3.4, 2.6), new THREE.MeshLambertMaterial({ color: 0x4a3424 }));
      booth.position.set(5.5, 1.7, -7);
      booth.castShadow = true;
      booth.receiveShadow = true;
      roomGroup.add(booth);

      // Gatekeeper NPC
      const guardMesh = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.7, 0.4), new THREE.MeshLambertMaterial({ color: 0x223654 }));
      guardMesh.position.set(4, 0.85, -6);
      guardMesh.castShadow = true;
      roomGroup.add(guardMesh);

      // Streetlamp (off during sunny morning, gleaming brass & black iron)
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 4.5), new THREE.MeshLambertMaterial({ color: 0x222222 }));
      post.position.set(-6, 2.25, -4);
      post.castShadow = true;
      roomGroup.add(post);

      const lampHead = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), new THREE.MeshLambertMaterial({ color: 0xe8e4dc }));
      lampHead.position.set(-6, 4.5, -4);
      roomGroup.add(lampHead);

      // Player starting position outside gate on sunny morning
      playerGroup.position.set(0, 0.25, 2);
      playerGroup.rotation.y = Math.PI;

      // Interactive Station: Gatekeeper Admissions
      interactiveObjects.push({
        id: "gatekeeper",
        label: "Security Gatekeeper: Seek Admission & Department Assignment",
        pos: new THREE.Vector3(4, 0, -6),
        radius: 2.5,
        action: openGatekeeperModal
      });

      // Interactive Station: Wrought Iron Turnstile
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

      // Corporate Herringbone Parquet Floor
      const floorMat = new THREE.MeshLambertMaterial({ color: 0x3d2719 });
      const floorMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), floorMat);
      floorMesh.rotation.x = -Math.PI / 2;
      floorMesh.receiveShadow = true;
      roomGroup.add(floorMesh);

      // Coffered Ceiling
      const ceilMat = new THREE.MeshLambertMaterial({ color: 0xede0cb });
      const ceilMesh = new THREE.Mesh(new THREE.PlaneGeometry(24, 20), ceilMat);
      ceilMesh.rotation.x = Math.PI / 2;
      ceilMesh.position.y = 5.8;
      roomGroup.add(ceilMesh);

      // Walls with Art Department Pixel Wallpaper & 3D Windows
      buildArchitecturalWalls();

      // Elevator Concourse along South Wall
      buildElevatorConcourse();

      // Hang member portraits from ASSETS
      hangFloorPortraits();

      // Floor-specific layout
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
      // Exact pixel-art wallpaper texture from the user's uploaded art-department asset
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
        color: wallTex ? 0xffffff : 0xdcc48d // Warm art department tan
      });

      // Wainscot baseboard in matching #c8ad72 with dentil base
      const wainMat = new THREE.MeshLambertMaterial({ color: 0xc8ad72 });
      const railMat = new THREE.MeshLambertMaterial({ color: 0xae9259 });

      // North Wall (Z = -10)
      buildArtWallSegment(0, -10, 24, false, wainMat, upperWallMat, railMat);
      // West Wall (X = -12) with 3D Window
      buildArtWallSegment(-12, 0, 20, true, wainMat, upperWallMat, railMat, true);
      // East Wall (X = 12) with 3D Window
      buildArtWallSegment(12, 0, 20, true, wainMat, upperWallMat, railMat, true);
    }

    function buildArtWallSegment(x, z, length, isSide, wainMat, topMat, railMat, hasWindow = false) {
      const group = new THREE.Group();
      const w = isSide ? 0.3 : length;
      const d = isSide ? length : 0.3;

      // Bottom wainscot (Art department lower wall with dentils)
      const bottom = new THREE.Mesh(new THREE.BoxGeometry(w, 2.0, d), wainMat);
      bottom.position.y = 1.0;
      bottom.receiveShadow = true;
      group.add(bottom);

      // Horizontal dentil moulding
      const rail = new THREE.Mesh(new THREE.BoxGeometry(w * 1.04, 0.14, d * 1.04), railMat);
      rail.position.y = 2.07;
      group.add(rail);

      // Upper wall with the exact art department pixel pattern
      const top = new THREE.Mesh(new THREE.BoxGeometry(w, 3.6, d), topMat);
      top.position.y = 3.9;
      top.receiveShadow = true;
      group.add(top);

      // Add 3D Wooden Window matching the user's uploaded art-department window
      if (hasWindow) {
        const winGroup = new THREE.Group();
        const frameWood = new THREE.MeshLambertMaterial({ color: 0x453629 });
        const skyGlass = new THREE.MeshBasicMaterial({ color: 0x8ab4f8 });

        // Outer wooden frame
        const frame = new THREE.Mesh(new THREE.BoxGeometry(0.35, 2.2, 2.2), frameWood);
        winGroup.add(frame);

        // 4 Panes of sunny blue morning sky
        for (let row = -1; row <= 1; row += 2) {
          for (let col = -1; col <= 1; col += 2) {
            const pane = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.88, 0.88), skyGlass);
            pane.position.set(0, row * 0.5, col * 0.5);
            winGroup.add(pane);
          }
        }

        winGroup.position.set(0, 3.8, 0);
        group.add(winGroup);

        // Morning light entering window
        const winLight = new THREE.PointLight(0xfffaed, 0.8, 8);
        winLight.position.set(isSide ? (x > 0 ? -1 : 1) : 0, 3.8, isSide ? 0 : 1);
        group.add(winLight);
      }

      group.position.set(x, 0, z);
      roomGroup.add(group);
    }

    function hangFloorPortraits() {
      // Use clean human clerk portraits (no monkey weirdos)
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

      // Place the 3D Briefcase (from art department) beside the desk!
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

      // Banker's lamp
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

    // 1. FLOOR 1: INTERN (Mailroom & Pneumatic Chutes)
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
        label: "Musical Chair Contest: The Intern's Folding Chair",
        pos: new THREE.Vector3(8, 0, -6),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(1)
      });
    }

    // 2. FLOOR 2: ANALYST (Typist Bullpen & Ledgers)
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
        label: "Musical Chair Contest: The Typist Stool",
        pos: new THREE.Vector3(7, 0, -5),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(2)
      });
    }

    // 3. FLOOR 3: ASSOCIATE (Deng Credit Window & Forge)
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
        label: "Musical Chair Contest: Creaking Wooden Swivel",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(3)
      });
    }

    // 4. FLOOR 4: VICE PRESIDENT (Subscription Registry)
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
        label: "Musical Chair Contest: Beige Task Chair",
        pos: new THREE.Vector3(0, 0, -4),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(4)
      });
    }

    // 5. FLOOR 5: DIRECTOR (Flagged Dossier Archive)
    function buildFloor5Director() {
      createDesk(0, 0, -1, 8, 2.4, 0x2e1a0d);

      for (let i = -3; i <= 3; i += 2) {
        const cab = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.5, 1.2), new THREE.MeshLambertMaterial({ color: 0x485641 }));
        cab.position.set(i * 3, 1.75, -8.5);
        roomGroup.add(cab);
      }

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
        label: "Musical Chair Contest: High-Back Leather Desk Chair",
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
        label: "Musical Chair Contest: Green Banker's Chair (Boss Showdown)",
        pos: new THREE.Vector3(-6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(6)
      });
    }

    // 7. FLOOR 7: PARTNER (Syndicate Executive Chamber)
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
        label: "Musical Chair Contest: Oxblood Wingback Chair",
        pos: new THREE.Vector3(6, 0, 2),
        radius: 2.4,
        action: () => triggerMusicalChairsArena(7)
      });
    }

    // 8. FLOOR 8: BOARD OF DIRECTORS (Round Mahogany Table)
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
        label: "Musical Chair Contest: Board of Directors High Seat",
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
        label: "Musical Chair Contest: The Gilded Sovereign Throne (Final Showdown)",
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

    // ELEVATOR CONCOURSE
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

    // GATEKEEPER ADMISSION (Level 0)
    function openGatekeeperModal() {
      playClick();
      modalTitle.innerText = "SECURITY GATEKEEPER";
      modalSubtitle.innerText = "ADMISSIONS DESK · WEST GATE";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          The gatekeeper looks up over wire-rimmed glasses in the morning sun.
        </p>
        <blockquote style="font-style:italic;border-left:3px solid var(--lamp);padding-left:12px;margin-bottom:14px;color:var(--ink-muted);font-size:12px;">
          "Every applicant who enters these doors is sworn to a department fund. Choose your covenant carefully, Flickerr. The Mutual Fun operates with clockwork precision. Zero em dashes. Exact ledger entries."
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

    // FLOOR 1: MAILROOM & PNEUMATIC CHUTES
    function openMailroomChuteModal() {
      playClick();
      modalTitle.innerText = "PNEUMATIC CHUTE DISPATCH";
      modalSubtitle.innerText = "DEPARTMENT LOGISTICS TUBE";

      modalBody.innerHTML = `
        <p style="font-size:13px;color:var(--ink);margin-bottom:12px;">
          Five brass cylinders feed into pressurized brass pneumatic conduits. Route correspondence to your department:
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

    // FLOOR 2: AUDIT LEDGER
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

    // FLOOR 3: DENG WINDOW & FORGE
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

    // FLOOR 4: SUBSCRIPTION ROLL
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

    // FLOOR 5: DOSSIER ARCHIVE
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

    // FLOOR 6: WHAT3VERMAN AUDIENCE
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
          "You climb fast, Flickerr. But my green banker's chair is not given away on review points alone. You must out-reflex me in musical chairs when the needle cuts."
        </blockquote>
        <button class="desk-button" style="width:100%;background:var(--green);" onclick="closeTaskModal(); triggerMusicalChairsArena(6);">
          Challenge what3verman to Musical Chairs (Floor 6)
        </button>
      `;
      modalEl.classList.add('active');
    }

    // FLOOR 7: PARTNER SYNDICATE
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

    // FLOOR 8: BOARDROOM CONCLAVE
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

    // FLOOR 9: KINGPICKLE AUDIENCE
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
          "Welcome to Seat 0, Flickerr. You started outside on the pavement. Now, you stand before the gilded throne. Win the final dispute, and the entire institution is yours."
        </blockquote>
        <button class="desk-button" style="width:100%;background:var(--lamp);color:#110b06;" onclick="closeTaskModal(); triggerMusicalChairsArena(9);">
          The Final Dispute: Challenge Kingpickle for The Gilded Throne
        </button>
      `;
      modalEl.classList.add('active');
    }

    // ==========================================================================
    // THE LAST CHAIR MUSICAL CHAIRS ENGINE (with Real Sprite Animations & Robust Timer)
    // ==========================================================================
    const arenaModal = document.getElementById('arenaModal');
    const cabinetSubTitle = document.getElementById('cabinetSubTitle');
    const arenaRoundLabel = document.getElementById('arenaRoundLabel');
    const arenaSignal = document.getElementById('arenaSignal');
    const arenaReactionDisplay = document.getElementById('arenaReactionDisplay');
    const arenaCountdown = document.getElementById('arenaCountdown');
    const arenaIntroOverlay = document.getElementById('arenaIntroOverlay');
    const arenaResultOverlay = document.getElementById('arenaResultOverlay');
    const deckHintText = document.getElementById('deckHintText');
    const lastchairSitBtn = document.getElementById('lastchairSitBtn');
    const rosterCount = document.getElementById('rosterCount');
    const rosterList = document.getElementById('rosterList');
    const floorDifficultyStat = document.getElementById('floorDifficultyStat');
    const lastchairCanvas = document.getElementById('lastchairCanvas');
    const ctx = lastchairCanvas.getContext('2d');

    // Load Last Chair Sprites & Room
    let atlasImg = new Image();
    let roomImg = new Image();
    let lastchairSprites = null;

    if (ASSETS.lastchair_sprites) {
      atlasImg.src = ASSETS.lastchair_sprites;
      atlasImg.onload = () => {
        try {
          const source = document.createElement('canvas');
          source.width = atlasImg.width;
          source.height = atlasImg.height;
          const sc = source.getContext('2d', { willReadFrequently: true });
          sc.drawImage(atlasImg, 0, 0);
          const pixels = sc.getImageData(0, 0, source.width, source.height);
          // Key out green screen background
          for (let i = 0; i < pixels.data.length; i += 4) {
            let r = pixels.data[i], g = pixels.data[i+1], b = pixels.data[i+2];
            if (g > 90 && g > r * 1.4 && g > b * 1.4) {
              pixels.data[i+3] = 0;
            }
          }
          sc.putImageData(pixels, 0, 0);

          // 3 rows: row 0 = walking, row 1 = seated, row 2 = chair
          lastchairSprites = [0, 1, 2].map((row) => [0, 1, 2, 3].map((col) => {
            const out = document.createElement('canvas');
            out.width = (row === 2 ? 42 : 36);
            out.height = (row === 2 ? 64 : 86);
            const oc = out.getContext('2d');
            oc.imageSmoothingEnabled = false;
            const boxes = [[24, 42, 214, 529], [24, 620, 214, 494], [25, 1165, 214, 319]];
            const [bx, by, bw, bh] = boxes[row];
            oc.drawImage(
              source,
              (col * 256 + bx) * atlasImg.width / 1024,
              by * atlasImg.height / 1536,
              bw * atlasImg.width / 1024,
              bh * atlasImg.height / 1536,
              0, 0, out.width, out.height
            );
            return out;
          }));
          console.log("Successfully extracted Last Chair animated walking & sitting sprites!");
        } catch(e) {
          console.warn("Could not process sprites atlas:", e);
        }
      };
    }

    if (ASSETS.lastchair_room) {
      roomImg.src = ASSETS.lastchair_room;
    }

    const melody = [261.63, 329.63, 392, 329.63, 293.66, 349.23, 440, 349.23, 261.63, 329.63, 392, 523.25, 440, 392, 349.23, 293.66];
    let melodyNoteIndex = 0;
    let melodyInterval = null;
    let countdownTimer = null;

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

      cabinetSubTitle.innerText = `FLOOR ${floor} DISPUTE · ${arenaChairName.toUpperCase()}`;
      floorDifficultyStat.innerText = FLOOR_REFLEX_DIFFICULTY[floor].label;

      setupArenaContenders();

      arenaRound = 1;
      arenaActive = [0, 1, 2, 3];
      arenaPhase = 'intro';
      arenaLastReaction = null;
      arenaReactionDisplay.innerText = "-- ms";

      document.getElementById('introFloorEyebrow').innerText = `FLOOR ${floor} CHAIR DISPUTE`;
      document.getElementById('introChairTitle').innerText = arenaChairName.toUpperCase();
      document.getElementById('introGuideBody').innerText =
        `There is always one chair too few. Circle the seats while the 1987 turntable plays. When the needle cuts and the screen flashes RED, dive for a chair instantly! Press SPACE to sit. Beware: sitting on green results in immediate disqualification.`;

      const previewDiv = document.getElementById('introContendersPreview');
      previewDiv.innerHTML = arenaContenders.map(c => `<img class="intro-contender-thumb" src="${c.avatar}" title="${c.name}">`).join('');

      arenaIntroOverlay.classList.remove('hidden');
      arenaResultOverlay.classList.add('hidden');
      arenaCountdown.classList.add('hidden');

      renderRoster();
      setArenaSignal('', 'GET READY');
      setDeckHint("Read house rules carefully. Press ENTER ARENA or [SPACE] to begin.");
      lastchairSitBtn.disabled = true;

      arenaModal.classList.add('active');

      if (!arenaAnimFrame) {
        lastFrameTime = performance.now();
        arenaAnimFrame = requestAnimationFrame(arenaTick);
      }
    }

    function setupArenaContenders() {
      // Flickerr is a human corporate clerk (bogle-03, NO MONKEY!)
      const flickerrAvatar = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      arenaContenders = [
        { id: 0, name: "Flickerr", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar }
      ];

      if (arenaFloor === 6) {
        arenaContenders.push({ id: 1, name: "what3verman", role: "Managing Director", fund: "Executive Desk", avatar: ASSETS.boss_what3verman });
        arenaContenders.push({ id: 2, name: "Smaug Arbitrageur", role: "Contender", fund: "The Smaug Fund", avatar: ASSETS.p_smaug_1 });
        arenaContenders.push({ id: 3, name: "Argon Auditor", role: "Contender", fund: "The Argon Fund", avatar: ASSETS.p_argon_1 });
      } else if (arenaFloor === 9) {
        arenaContenders.push({ id: 1, name: "Kingpickle", role: "The Chairman", fund: "Seat 0 Trustee", avatar: ASSETS.boss_kingpickle });
        arenaContenders.push({ id: 2, name: "Board Governor A", role: "Governor", fund: "The Midas Fund", avatar: ASSETS.p_midas_1 });
        arenaContenders.push({ id: 3, name: "Board Governor B", role: "Governor", fund: "The Vladd Fund", avatar: ASSETS.p_vladd_1 });
      } else {
        const pool = [
          { name: "Bogle Senior Clerk", role: "Contender", fund: "The Bogle Fund", avatar: ASSETS.p_bogle_2 },
          { name: "Smaug Auditor", role: "Contender", fund: "The Smaug Fund", avatar: ASSETS.p_smaug_1 },
          { name: "Midas Analyst", role: "Contender", fund: "The Midas Fund", avatar: ASSETS.p_midas_1 },
          { name: "Argon Specialist", role: "Contender", fund: "The Argon Fund", avatar: ASSETS.p_argon_1 },
          { name: "Vladd Dispatcher", role: "Contender", fund: "The Vladd Fund", avatar: ASSETS.p_vladd_1 }
        ];
        arenaContenders.push(Object.assign({ id: 1 }, pool[(arenaFloor * 2) % pool.length]));
        arenaContenders.push(Object.assign({ id: 2 }, pool[(arenaFloor * 2 + 1) % pool.length]));
        arenaContenders.push(Object.assign({ id: 3 }, pool[(arenaFloor * 2 + 2) % pool.length]));
      }
    }

    function renderRoster() {
      rosterCount.innerText = String(arenaActive.length).padStart(2, '0');
      rosterList.innerHTML = arenaContenders.map((c, i) => `
        <div class="roster-person ${arenaActive.includes(c.id) ? '' : 'out'}">
          <img src="${c.avatar}" alt="${c.name}">
          <div>
            <strong>${c.name}</strong>
            <small>${arenaActive.includes(c.id) ? (c.id === 0 ? 'Your character' : c.fund) : 'Eliminated'}</small>
          </div>
          ${c.id === 0 ? '<span class="you-tag">YOU</span>' : ''}
        </div>
      `).join('');
    }

    function setArenaSignal(kind, text) {
      arenaSignal.className = `lastchair-signal ${kind}`;
      arenaSignal.querySelector('span').innerText = text;
    }

    function setDeckHint(text) {
      deckHintText.innerText = text;
    }

    function layoutChairs() {
      const chairCount = arenaActive.length - 1;
      arenaChairs = Array.from({ length: chairCount }, (_, i) => ({
        x: 480 + (i - (chairCount - 1) / 2) * 115,
        y: 417
      }));
    }

    function startArenaMatch() {
      hideArenaOverlays();
      arenaActive = [0, 1, 2, 3];
      arenaRound = 1;
      arenaReactionDisplay.innerText = "-- ms";
      startArenaRound();
    }

    // FIXED COUNTDOWN: Bulletproof interval timer that transitions 3 -> 2 -> 1 -> Green!
    function startArenaRound() {
      hideArenaOverlays();
      if (countdownTimer) {
        clearInterval(countdownTimer);
        countdownTimer = null;
      }

      arenaPhase = 'countdown';
      arenaSeated = {};
      arenaMoves = {};
      arenaLoser = null;
      arenaEarly = false;
      arenaBots = [];
      arenaFinishAt = 0;
      arenaGreenFor = 3200 + Math.random() * 4200; // 3.2s to 7.4s green
      layoutChairs();

      arenaRoundLabel.innerText = `ROUND 0${arenaRound} / 03`;
      lastchairSitBtn.disabled = true;
      setArenaSignal('', 'GET READY');
      setDeckHint("Three, two, one… Watch the signal light.");
      renderRoster();

      let count = 3;
      arenaCountdown.innerText = count;
      arenaCountdown.classList.remove('hidden');
      tone(440, 0.08, 'square', 0.04);

      countdownTimer = setInterval(() => {
        count--;
        if (count > 0) {
          arenaCountdown.innerText = count;
          tone(440, 0.08, 'square', 0.04);
        } else {
          clearInterval(countdownTimer);
          countdownTimer = null;
          arenaCountdown.classList.add('hidden');
          arenaGoGreen(performance.now());
        }
      }, 820);
    }

    function hideArenaOverlays() {
      arenaIntroOverlay.classList.add('hidden');
      arenaResultOverlay.classList.add('hidden');
      arenaCountdown.classList.add('hidden');
    }

    function arenaGoGreen(now) {
      arenaPhase = 'green';
      arenaPhaseAt = now;
      setArenaSignal('green', 'KEEP WALKING');
      lastchairSitBtn.disabled = false;
      arenaCountdown.classList.add('hidden');
      setDeckHint("Hold your nerve. Turntable is playing. Wait for RED.");

      melodyNoteIndex = 0;
      startTurntableMelody();
    }

    function startTurntableMelody() {
      stopTurntableMelody();
      melodyInterval = setInterval(() => {
        if (arenaPhase !== 'green') {
          stopTurntableMelody();
          return;
        }
        const freq = melody[melodyNoteIndex % melody.length];
        melodyNoteIndex++;
        tone(freq, 0.12, 'triangle', 0.04);
      }, 270);
    }

    function stopTurntableMelody() {
      if (melodyInterval) {
        clearInterval(melodyInterval);
        melodyInterval = null;
      }
    }

    function calculateRivalDelay(botId, round) {
      const diff = FLOOR_REFLEX_DIFFICULTY[arenaFloor] || { base: 400, spread: 100 };
      const rng = (Math.random() + Math.random()) * 0.5;
      const reaction = diff.base + (rng - 0.5) * diff.spread - (round - 1) * 14;
      return Math.round(Math.max(130, reaction));
    }

    function arenaGoRed(now) {
      stopTurntableMelody();
      arenaPhase = 'red';
      arenaPhaseAt = now;
      arenaRedAt = now;

      const sceneWrap = document.getElementById('arenaSceneWrap');
      sceneWrap.classList.remove('scene-canvas-flash');
      void sceneWrap.offsetWidth;
      sceneWrap.classList.add('scene-canvas-flash');

      arenaBots = arenaActive.filter(id => id !== 0).map(id => ({
        id,
        at: now + calculateRivalDelay(id, arenaRound)
      })).sort((a, b) => a.at - b.at);

      setArenaSignal('red', 'SIT NOW!');
      setDeckHint("NOW! Press SPACE or tap SIT to take a chair!");
      tone(160, 0.28, 'sawtooth', 0.08);
    }

    function getContenderPosition(id) {
      const idx = arenaActive.indexOf(id);
      const angle = arenaAngle + (idx * Math.PI * 2) / arenaActive.length;
      return {
        x: 480 + Math.cos(angle) * 282,
        y: 421 + Math.sin(angle) * 101,
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
        lastchairSitBtn.disabled = true;
        setDeckHint("Seat secured! Hold tight.");
        tone(660, 0.12);
        setTimeout(() => tone(880, 0.16), 110);
      }

      if (Object.keys(arenaSeated).length === arenaChairs.length) {
        arenaLoser = arenaActive.find(i => arenaSeated[i] === undefined);
        arenaPhase = 'resolving';
        arenaFinishAt = performance.now() + 1000;
        lastchairSitBtn.disabled = true;
      }
      return true;
    }

    function onSitClicked() {
      if (arenaPhase === 'green') {
        stopTurntableMelody();
        arenaLoser = 0;
        arenaPhase = 'resolving';
        arenaFinishAt = performance.now() + 700;
        arenaActive.filter(i => i !== 0).forEach((id, i) => { arenaSeated[id] = i; });
        lastchairSitBtn.disabled = true;
        setDeckHint("Too soon! You sat on green. False start disqualification.");
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
      arenaReactionDisplay.innerText = `${arenaLastReaction} ms`;
      claimSeat(0);
    }

    function finishArenaRound() {
      const eliminated = arenaLoser;
      arenaActive = arenaActive.filter(i => i !== eliminated);
      renderRoster();
      arenaCountdown.classList.add('hidden');

      const playerLost = (eliminated === 0);
      const playerWon = (!playerLost && arenaActive.length === 1);
      arenaPhase = playerLost ? 'lost' : (playerWon ? 'won' : 'between');

      const kicker = document.getElementById('resultKicker');
      const title = document.getElementById('resultTitle');
      const body = document.getElementById('resultBody');
      const btn = document.getElementById('resultBtn');

      if (playerLost) {
        kicker.innerText = "BETTER LUCK NEXT TIME";
        title.innerText = arenaEarly ? "TOO SOON." : "LEFT STANDING.";
        body.innerText = arenaEarly ?
          "You sat down on green. Wait for the needle to cut and the signal to turn RED before moving." :
          `Your rivals snatched every seat. (Your reaction: ${arenaLastReaction || '-'} ms). Train your reflexes and try again.`;
        btn.innerHTML = "TRY AGAIN [SPACE]";
        setArenaSignal('', 'GAME OVER');
        tone(140, 0.4);
      } else if (playerWon) {
        kicker.innerText = "THE LAST ONE SEATED";
        title.innerText = "THE LAST CHAIR IS YOURS!";
        body.innerText = `Three rounds. Three flawless moves. Flickerr leaves Floor ${arenaFloor} holding ${arenaChairName}!`;
        btn.innerHTML = "CLAIM CERTIFICATE & ADVANCE [SPACE]";
        setArenaSignal('', 'YOU WIN');

        [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => tone(f, 0.22), i * 130));

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
        title.innerText = "SEAT SECURED!";
        body.innerText = `${eliminatedName} is out. Next up: ${arenaActive.length} contenders, ${arenaActive.length - 1} chairs.`;
        btn.innerHTML = "NEXT ROUND [SPACE]";
        setArenaSignal('', 'ONE LESS CHAIR');
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
      stopTurntableMelody();
      if (countdownTimer) {
        clearInterval(countdownTimer);
        countdownTimer = null;
      }
      arenaModal.classList.remove('active');
      arenaPhase = 'idle';
    }

    // ==========================================================================
    // 2D CANVAS DRAWING (Using Authenticated Last Chair Sprites & Walking Engine)
    // ==========================================================================
    let lastFrameTime = performance.now();

    function arenaTick(now) {
      try {
        const dt = Math.min((now - lastFrameTime) / 1000, 0.05);
        lastFrameTime = now;

        if (arenaModal.classList.contains('active')) {
          if (arenaPhase === 'intro' || arenaPhase === 'green') {
            arenaAngle += dt * (arenaPhase === 'intro' ? 0.2 : 0.72 + arenaRound * 0.12);
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

          drawArenaCanvas(now);
        }
      } catch(e) {
        console.warn("Error in arenaTick:", e);
      }

      arenaAnimFrame = requestAnimationFrame(arenaTick);
    }

    function drawSprite(col, row, x, y, height) {
      if (lastchairSprites) {
        const sp = lastchairSprites[row][col % 4];
        const w = height * sp.width / sp.height;
        ctx.drawImage(sp, Math.round(x - w / 2), Math.round(y - height), Math.round(w), height);
      } else {
        // Fallback procedural sprite
        ctx.fillStyle = row === 1 ? "#7a2e2e" : (col === 0 ? "#57a671" : "#5b8ac2");
        ctx.fillRect(x - 18, y - height, 36, height);
      }
    }

    function drawArenaCanvas(now) {
      ctx.imageSmoothingEnabled = false;

      // 1. Draw 1987 Room Background
      if (roomImg.complete && roomImg.naturalWidth) {
        ctx.drawImage(roomImg, 0, 0, 960, 600);
      } else {
        ctx.fillStyle = "#a7b694";
        ctx.fillRect(0, 0, 960, 600);
      }

      const items = [];

      // 2. Draw Chairs & Seated Contenders
      arenaChairs.forEach((ch, i) => {
        items.push({
          y: ch.y,
          draw: () => {
            // Draw authentic chair sprite
            drawSprite(i % 4, 2, ch.x, ch.y, 150);

            // Check if occupant is seated
            const occupant = Object.keys(arenaSeated).find(k => arenaSeated[k] === i);
            if (occupant !== undefined) {
              const move = arenaMoves[occupant];
              const t = move ? Math.min(1, Math.max(0, (now - move.at) / 160)) : 1;
              const ease = 1 - Math.pow(1 - t, 3);
              const x = move ? move.from.x + (ch.x - move.from.x) * ease : ch.x;
              const y = move ? move.from.y + (ch.y - 2 - move.from.y) * ease : ch.y - 2;

              // Smooth transition from walking (row 0) to sitting (row 1)
              drawSprite(+occupant, t < 0.8 ? 0 : 1, x, y, t < 0.8 ? 188 : 180);
              drawPlayerLabel(+occupant, x, y + 19);
            }
          }
        });
      });

      // 3. Draw Walking Contenders with real walk cycle bob
      const displayActive = (arenaPhase === 'intro') ? [0, 1, 2, 3] :
        [...new Set([...arenaActive, ...Object.keys(arenaSeated).map(Number), ...(arenaLoser === null ? [] : [arenaLoser])])];

      displayActive.forEach(id => {
        if (arenaSeated[id] !== undefined) return;

        let p = arenaActive.includes(id) ? getContenderPosition(id) : { x: 810, y: 455, angle: 0 };
        const moving = ['intro', 'green'].includes(arenaPhase);
        const bob = moving ? Math.abs(Math.sin(now / 125 + id)) * 5 : 0;

        items.push({
          y: p.y,
          draw: () => {
            // Drop shadow
            ctx.fillStyle = '#2f241c35';
            ctx.beginPath();
            ctx.ellipse(p.x, p.y + 1, 26, 8, 0, 0, Math.PI * 2);
            ctx.fill();

            // Real walking sprite (row 0)
            drawSprite(id, 0, p.x, p.y - bob, 188);
            drawPlayerLabel(id, p.x, p.y + 21);
          }
        });
      });

      // Sort items by Y for isometric depth sorting
      items.sort((a, b) => a.y - b.y).forEach(i => i.draw());

      // Red border flash during RED phase
      if (arenaPhase === 'red') {
        ctx.strokeStyle = '#a53532';
        ctx.lineWidth = 8;
        ctx.strokeRect(4, 4, 952, 592);
      }
    }

    function drawPlayerLabel(id, x, y) {
      if (id !== 0) return;
      ctx.font = 'bold 14px monospace';
      ctx.textAlign = 'center';
      ctx.fillStyle = '#2d4534';
      ctx.fillRect(x - 22, y - 12, 44, 19);
      ctx.fillStyle = '#f0e8ca';
      ctx.fillText('YOU', x, y + 2);
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
        leftLeg.rotation.x = 0;
        rightLeg.rotation.x = 0;
        leftArm.rotation.x = 0;
        rightArm.rotation.x = 0;
        torso.position.y = 1.0;
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
      // Use clean human clerk portrait!
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
      g.fillText("FLICKERR", px, py + pr + 22);
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
      link.download = `TMF_Certificate_Flickerr_${flickerr.role.replace(/\\s+/g, '_')}.png`;
      link.href = certCanvas.toDataURL('image/png');
      link.click();
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

# Replace __ASSETS_JSON__ with assets JSON
final_html = html_template.replace('__ASSETS_JSON__', json.dumps(assets))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

brain_path = r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html'
with open(brain_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated upgraded game with Art Department walls, Sunny outdoor morning, Real sprites, and Fixed countdown successfully!")
