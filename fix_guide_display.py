with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix retro guide box styling to clean retro white styling
old_css = """    .retro-guide-box {
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
    }"""

new_css = """    .retro-guide-box {
      position: fixed;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%) translateY(0);
      width: min(860px, 94vw);
      background: #fdfaf2;
      border: 4px solid #211b14;
      border-radius: 4px;
      box-shadow: 0 10px 28px rgba(0,0,0,0.7), inset 0 0 0 2px #b9902f;
      padding: 12px 20px 14px 20px;
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
      margin-bottom: 6px;
    }
    .retro-guide-badge {
      background: #7a2e2e;
      color: #fdfaf2;
      font-size: 10px;
      font-weight: 700;
      padding: 2px 7px;
      letter-spacing: 1px;
      text-transform: uppercase;
      border-radius: 2px;
    }
    .retro-guide-sub {
      color: #6b5f4e;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .retro-guide-content {
      color: #211b14;
      font-size: 14px;
      line-height: 1.5;
      font-weight: 500;
      padding-right: 28px;
      letter-spacing: normal;
      word-spacing: normal;
      white-space: pre-wrap;
    }
    .retro-guide-cursor {
      position: absolute;
      right: 18px;
      bottom: 10px;
      color: #7a2e2e;
      font-size: 11px;
      font-family: 'IBM Plex Mono', monospace;
      font-weight: 600;
      opacity: 0;
      animation: retroBlink 0.7s infinite alternate ease-in-out;
    }"""

assert old_css in text, "old_css not found"
text = text.replace(old_css, new_css)

# 2. Fix _typeGuideChar to use textContent and prompt to Press [E] to continue only
old_typewriter = """    function _typeGuideChar(textEl, cursor) {
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
    }"""

new_typewriter = """    function _typeGuideChar(textEl, cursor) {
      if (_guideCharIdx < _guideFullText.length) {
        const ch = _guideFullText[_guideCharIdx];
        textEl.textContent += ch;
        _guideCharIdx++;
        const delay = (ch === '.' || ch === ',') ? 85 : 18;
        _guideTypeTimer = setTimeout(() => _typeGuideChar(textEl, cursor), delay);
      } else {
        _guideTypeTimer = null;
        if (cursor) { cursor.textContent = 'Press [E] to continue'; cursor.style.opacity = '1'; }
      }
    }"""

assert old_typewriter in text, "old_typewriter not found"
text = text.replace(old_typewriter, new_typewriter)

# 3. Fix advanceGuide prompt and textContent
old_advance = """    function advanceGuide() {
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
    }"""

new_advance = """    function advanceGuide() {
      if (!guideLocked) return;
      const textEl = document.getElementById('retroGuideText');
      const cursor = document.getElementById('retroGuideCursor');
      if (_guideCharIdx < _guideFullText.length) {
        if (_guideTypeTimer) { clearTimeout(_guideTypeTimer); _guideTypeTimer = null; }
        textEl.textContent = _guideFullText;
        _guideCharIdx = _guideFullText.length;
        if (cursor) { cursor.textContent = 'Press [E] to continue'; cursor.style.opacity = '1'; }
      } else {
        _dismissGuide();
      }
    }"""

assert old_advance in text, "old_advance not found"
text = text.replace(old_advance, new_advance)

# 4. In setRetroGuide, also use textContent
text = text.replace("textEl.innerText = '';", "textEl.textContent = '';")
text = text.replace("if (cursor) { cursor.innerText = ''; cursor.style.opacity = '0'; }", "if (cursor) { cursor.textContent = ''; cursor.style.opacity = '0'; }")

# 5. Fix keydown to ONLY trigger on KeyE
old_kd_check = """      // Guide advance: E, Space or Enter dismisses/skips guide
      if (typeof guideLocked !== 'undefined' && guideLocked &&
          (e.code === 'KeyE' || e.code === 'Space' || e.code === 'Enter')) {
        e.preventDefault();
        if (typeof advanceGuide === 'function') advanceGuide();
        return;
      }"""

new_kd_check = """      // Guide advance: only Press [E] to continue
      if (typeof guideLocked !== 'undefined' && guideLocked && e.code === 'KeyE') {
        e.preventDefault();
        if (typeof advanceGuide === 'function') advanceGuide();
        return;
      }"""

assert old_kd_check in text, "old_kd_check not found"
text = text.replace(old_kd_check, new_kd_check)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Successfully patched index.html and artifact!')
