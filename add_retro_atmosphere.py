with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add high-grade 1987 retro corporate CRT / scanline vignette overlay
crt_css = """
    /* Authentic 1987 Corporate CRT Scanline & Warm Vignette Environment */
    .retro-crt-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 90;
      background: linear-gradient(rgba(18, 16, 12, 0) 50%, rgba(0, 0, 0, 0.14) 50%),
                  radial-gradient(circle at center, transparent 65%, rgba(18, 10, 4, 0.42) 100%);
      background-size: 100% 3px, 100% 100%;
      mix-blend-mode: multiply;
      opacity: 0.85;
    }
"""

if '</style>' in text and '.retro-crt-overlay' not in text:
    text = text.replace('</style>', crt_css + '\n  </style>')

if 'class="retro-crt-overlay"' not in text and '<body>' in text:
    text = text.replace('<body>', '<body>\n  <div class="retro-crt-overlay"></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added authentic 1987 retro CRT scanlines and warm vignette environment!')
