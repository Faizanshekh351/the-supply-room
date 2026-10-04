with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update setupArenaContenders to map specific assets to each floor holder and keep ONLY [player, holder]
new_setup_block = """    const ARENA_FLOOR_HOLDERS = {
      1: { name: "Chief Mail Clerk",        role: "Head of Couriers",     avatar: ASSETS.p_bogle_1, color: "#4e8a5a", hasCrown: false },
      2: { name: "Senior Ledger Archivist", role: "Auditing Lead",        avatar: ASSETS.p_smaug_1, color: "#8a4a2a", hasCrown: false },
      3: { name: "Head Trading Associate",  role: "Floor Broker",         avatar: ASSETS.p_midas_1, color: "#b08a3c", hasCrown: false },
      4: { name: "Senior Market Analyst",   role: "Vice President Desk",  avatar: ASSETS.p_argon_1, color: "#4a6b8c", hasCrown: false },
      5: { name: "Chief Compliance Dir.",   role: "Director of Records",  avatar: ASSETS.p_vladd_1, color: "#6e5d8c", hasCrown: false },
      6: { name: "what3verman",             role: "Managing Director",    avatar: ASSETS.boss_what3verman, color: "#1f4728", hasCrown: false },
      7: { name: "General Counsel",         role: "Syndicate Trustee",    avatar: ASSETS.p_bogle_4, color: "#7a2e2e", hasCrown: false },
      8: { name: "Governor of Board",       role: "Executive Governor",   avatar: ASSETS.p_midas_4, color: "#967822", hasCrown: false },
      9: { name: "The Chairman Kingpickle", role: "Chairman of the Board",avatar: ASSETS.boss_kingpickle, color: "#110b06", hasCrown: true }
    };

    function setupArenaContenders() {
      const flickerrAvatar = ASSETS.flickerr_human || ASSETS.p_bogle_3;
      const holder = ARENA_FLOOR_HOLDERS[arenaFloor] || { name: "Floor Holder", role: "Seat Holder", avatar: ASSETS.p_argon_1, color: "#5a3518", hasCrown: false };
      arenaContenders = [
        { id: 0, name: "You", role: flickerr.role, fund: flickerr.department, avatar: flickerrAvatar, color: DEPARTMENTS[flickerr.deptIndex].color },
        { id: 1, name: holder.name, role: holder.role, fund: `Floor ${arenaFloor} Seat Holder`, avatar: holder.avatar || ASSETS.p_argon_1, color: holder.color, hasCrown: holder.hasCrown }
      ];
    }"""

idx_start = text.find('const ARENA_FLOOR_HOLDERS = {')
if idx_start == -1:
    idx_start = text.find('function setupArenaContenders() {')

idx_end = text.find('function renderRoster() {')
text = text[:idx_start] + new_setup_block + '\n\n    ' + text[idx_end:]

# 2. Fix promptEl display in animate loop so it HIDES whenever any modal is active
old_prompt_check = """      let nearby = false;
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
      }"""

new_prompt_check = """      let nearby = false;
      const anyModalActive = modalEl.classList.contains('active') || elevModal.classList.contains('active') ||
                             arenaModal.classList.contains('active') || certModal.classList.contains('active') ||
                             (typeof guideLocked !== 'undefined' && guideLocked);

      if (!anyModalActive) {
        for (const obj of interactiveObjects) {
          const dist = playerGroup.position.distanceTo(obj.pos);
          if (dist <= obj.radius) {
            promptEl.innerText = `[E] ${obj.label}`;
            promptEl.style.display = 'block';
            nearby = true;
            break;
          }
        }
      }
      if (!nearby || anyModalActive) {
        promptEl.style.display = 'none';
      }"""

assert old_prompt_check in text, 'old_prompt_check not found'
text = text.replace(old_prompt_check, new_prompt_check)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'C:\Users\faizan\.gemini\antigravity\brain\ce014d9d-f09e-4a92-b7cf-58ca3be8d0d3\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated 1v1 arena contenders and modal prompt hiding!')
