import os
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

WIDTH, HEIGHT = 1280, 720
FPS = 24

# Fonts
font_title = ImageFont.truetype("C:\\Windows\\Fonts\\georgia.ttf", 34)
font_subtitle = ImageFont.truetype("C:\\Windows\\Fonts\\georgia.ttf", 22)
font_mono = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 18)
font_mono_small = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 15)
font_stamp = ImageFont.truetype("C:\\Windows\\Fonts\\georgia.ttf", 44)

# Colors
C_PAPER = (246, 239, 227)
C_INK = (33, 27, 20)
C_INK_MUTED = (107, 95, 78)
C_OXBLOOD = (122, 46, 46)
C_GOLD = (176, 138, 60)
C_ARGON = (73, 105, 140)
C_BOGLE = (78, 138, 90)
C_SMAUG = (156, 82, 72)
C_MIDAS = (185, 144, 47)
C_VLADD = (110, 93, 140)

def load_fit(path, max_w, max_h):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    scale = min(max_w / w, max_h / h)
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    return img.resize((new_w, new_h), Image.NEAREST)

# Assets
hero_s1 = load_fit("cutouts/argon-02.png", 220, 260) # Candidate in tuxedo
# Scene 2 framed portraits from the actual kit:
p_argon1 = load_fit("portraits/argon-04.png", 200, 200) # Dog in oxblood wingback
p_bogle1 = load_fit("portraits/argon-01.png", 200, 200) # Officer in green bankers chair
p_smaug1 = load_fit("portraits/smaug-02.png", 200, 200) # Smaug throne
p_midas1 = load_fit("portraits/midas-01.png", 200, 200) # Midas bullion officer
p_vladd1 = load_fit("portraits/vladd-02.png", 200, 200) # Vladd officer

# Scene 3: Fez shareholder & Officer with blue briefcase
hero_s3_fez = load_fit("cutouts/smaug-03.png", 260, 310)
hero_s3_officer = load_fit("cutouts/argon-01.png", 260, 310)

# Scene 4: Skeletons
hero_s4_skel1 = load_fit("cutouts/argon-05.png", 270, 330)
hero_s4_skel2 = load_fit("cutouts/bogle-01.png", 270, 330)

# Scene 5: Alien & Elder
hero_s5_alien = load_fit("cutouts/midas-04.png", 260, 320)
hero_s5_elder = load_fit("cutouts/bogle-03.png", 260, 320)

medallion = Image.open("marks/medallion-384.png").convert("RGBA").resize((110, 110), Image.LANCZOS)

# Exact Scene Timing (matches audio/mixed_scene_*.wav exactly)
scene_durations = [17.0, 21.0, 20.0, 23.0, 17.5, 9.5]
total_duration = sum(scene_durations) # 108.0s
total_frames = int(total_duration * FPS)

scene_starts = [0.0]
for d in scene_durations[:-1]:
    scene_starts.append(scene_starts[-1] + d)

subtitles = [
    "\"The house does not invite. The house admits. You begin in the Waiting Room.\nWhen your verdict reads Admitted, you take your TMF Pass to the desk.\"",
    "\"At the Subscription Desk, 0.01 ETH purchases a chair. The chair confers a Seat.\n4,001 positions divided across five syndicates. Mint flows directly into the five vaults.\"",
    "\"Notice the floor beside each chair. That is an ERC 6551 token bound account.\nWhatever the fund earns drops directly into the briefcase, held in kind, unliquidated.\"",
    "\"Holding a chair is not enough. You enroll with TMF tokens to take your Seat.\nEvery Friday at 20:00 UTC (two zero zero zero UTC), the Proxy Ballot opens.\"",
    "\"On Monday, trades settle. Yield arrives in kind, placed directly into your briefcase.\nIf you sell the chair, the briefcase travels with it to the next owner.\"",
    "\"The NFT is not the product. The fund is. Take your seat.\""
]

out_mp4 = "the_mutual_fun_1987.mp4"
cmd = [
    ffmpeg, '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{WIDTH}x{HEIGHT}',
    '-pix_fmt', 'rgb24',
    '-r', str(FPS),
    '-i', '-',
    '-i', 'audio/full_soundtrack.wav',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    out_mp4
]

pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
print(f"Building clean master film: {total_frames} frames ({total_duration}s)...")

for frame_idx in range(total_frames):
    t = frame_idx / FPS
    
    scene_idx = 5
    for s_i in range(5):
        if scene_starts[s_i] <= t < scene_starts[s_i+1]:
            scene_idx = s_i
            break
            
    t_in_scene = t - scene_starts[scene_idx]
    dur_in_scene = scene_durations[scene_idx]
    
    bg = Image.new("RGB", (WIDTH, HEIGHT), (22, 17, 13))
    draw = ImageDraw.Draw(bg)
    
    if scene_idx == 0:
        # Scene 1: The Waiting Room
        zoom = 1.0 + (t_in_scene / dur_in_scene) * 0.08
        pw, ph = int(580 * zoom), int(420 * zoom)
        px = (WIDTH - pw) // 2
        py = (HEIGHT - 120 - ph) // 2
        
        # Mahogany counter + green banker lamp glow
        draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(28, 20, 15))
        draw.ellipse([WIDTH//2 - 380, py - 60, WIDTH//2 + 380, py + ph + 80], fill=(42, 34, 24))
        
        # Certificate paper
        draw.rectangle([px-6, py-6, px+pw+6, py+ph+6], fill=(12, 9, 7))
        draw.rectangle([px, py, px+pw, py+ph], fill=C_PAPER)
        draw.rectangle([px+8, py+8, px+pw-8, py+ph-8], outline=C_INK_MUTED, width=2)
        
        draw.text((px + pw//2, py + 25), "THE MUTUAL FUN", font=font_title, fill=C_INK, anchor="mt")
        draw.text((px + pw//2, py + 70), "ENTRY CERTIFICATE • SEAT NO. 1409", font=font_mono_small, fill=C_INK_MUTED, anchor="mt")
        
        cur_hero_w = int(hero_s1.width * zoom)
        cur_hero_h = int(hero_s1.height * zoom)
        scaled_hero = hero_s1.resize((cur_hero_w, cur_hero_h), Image.NEAREST)
        bg.paste(scaled_hero, (px + (pw - cur_hero_w)//2, py + 105), scaled_hero)
        
        if t_in_scene >= 1.8:
            stamp_img = Image.new("RGBA", (230, 65), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(stamp_img)
            sdraw.rectangle([2, 2, 226, 61], outline=C_OXBLOOD, width=4)
            sdraw.text((115, 32), "ADMITTED", font=font_stamp, fill=C_OXBLOOD, anchor="mm")
            rotated_stamp = stamp_img.rotate(8, expand=True, resample=Image.BICUBIC)
            bg.paste(rotated_stamp, (px + pw - rotated_stamp.width - 25, py + ph - rotated_stamp.height - 20), rotated_stamp)
            
    elif scene_idx == 1:
        # Scene 2: Lateral tracking shot down dim wainscoted hall
        offset_x = int((t_in_scene / dur_in_scene) * 1180)
        panel_w = 380
        funds = [
            (C_ARGON, "THE ARGON FUND", p_argon1, "GOLDEN RETRIEVER • OXBLOOD WINGBACK"),
            (C_BOGLE, "THE BOGLE FUND", p_bogle1, "OFFICER • GREEN BANKERS CHAIR"),
            (C_SMAUG, "THE SMAUG FUND", p_smaug1, "SMAUG SYNDICATE • GILDED THRONE"),
            (C_MIDAS, "THE MIDAS FUND", p_midas1, "MIDAS GOVERNOR • BANKERS CHAIR"),
            (C_VLADD, "THE VLADD FUND", p_vladd1, "VLADD DIRECTOR • BANKERS CHAIR")
        ]
        
        for i, (f_col, f_name, f_portrait, f_desc) in enumerate(funds):
            panel_x = i * panel_w - offset_x + 120
            if -panel_w <= panel_x <= WIDTH + 100:
                draw.rectangle([panel_x, 50, panel_x + panel_w - 20, HEIGHT - 160], fill=f_col)
                draw.rectangle([panel_x, 50, panel_x + panel_w - 20, HEIGHT - 160], outline=(15, 12, 10), width=4)
                
                # Framed portrait
                fx = panel_x + (panel_w - 20 - f_portrait.width)//2
                fy = 80
                bg.paste(f_portrait, (fx, fy), f_portrait)
                
                draw.text((panel_x + (panel_w - 20)//2, fy + f_portrait.height + 25), f_name, font=font_subtitle, fill=C_PAPER, anchor="mt")
                draw.text((panel_x + (panel_w - 20)//2, fy + f_portrait.height + 60), f_desc, font=font_mono_small, fill=C_GOLD, anchor="mt")
                
    elif scene_idx == 2:
        # Scene 3: The Briefcase
        # Split view: Fez shareholder on left, Officer in green chair on right with blue briefcase open
        bg.paste(hero_s3_fez, (100, 140), hero_s3_fez)
        bg.paste(hero_s3_officer, (400, 140), hero_s3_officer)
        
        # Briefcase ledger panel on right
        bx, by = 710, 140
        bw, bh = 500, 340
        draw.rectangle([bx, by, bx + bw, by + bh], fill=(30, 42, 58), outline=(90, 115, 145), width=3)
        draw.rectangle([bx + 60, by - 12, bx + 120, by + 6], fill=C_GOLD, outline=(110, 85, 30), width=2)
        draw.rectangle([bx + bw - 120, by - 12, bx + bw - 60, by + 6], fill=C_GOLD, outline=(110, 85, 30), width=2)
        
        draw.rectangle([bx + 18, by + 18, bx + bw - 18, by + bh - 18], fill=C_PAPER, outline=C_INK_MUTED, width=1)
        ledger_lines = [
            "TOKEN BOUND ACCOUNT // ERC-6551",
            "ACCOUNT HOLDER : 0x8A72...9E10",
            "STATUS         : UNLIQUIDATED (IN KIND)",
            "ALLOCATION     : 20% ARGON / 20% BOGLE",
            "LEDGER LOG #4001 RECORDED.",
            "YIELD DIRECTLY ACCRUED TO BRIEFCASE."
        ]
        for l_i, line in enumerate(ledger_lines):
            draw.text((bx + 32, by + 35 + l_i * 44), line, font=font_mono, fill=C_INK)
            
    elif scene_idx == 3:
        # Scene 4: Symmetrical Boardroom & Proxy Ballot
        draw.rectangle([0, 470, WIDTH, HEIGHT - 130], fill=(42, 30, 22), outline=(22, 16, 12), width=3)
        
        # Skeleton left & right
        bg.paste(hero_s4_skel1, (100, 145), hero_s4_skel1)
        bg.paste(hero_s4_skel2, (WIDTH - 100 - hero_s4_skel2.width, 145), hero_s4_skel2)
        
        # Center Wall Clock ticking to 20:00 UTC
        cx, cy = WIDTH // 2, 220
        r = 85
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(16, 12, 10), outline=(95, 80, 65), width=4)
        draw.text((cx, cy - 40), "UTC TIME", font=font_mono_small, fill=C_GOLD, anchor="mm")
        
        sec_num = int(t_in_scene * 2) % 60
        clock_str = f"19:59:{sec_num:02d}" if t_in_scene < 16 else "20:00:00"
        draw.text((cx, cy), clock_str, font=font_title, fill=C_PAPER, anchor="mm")
        
        draw.rectangle([cx - 125, cy + 50, cx + 125, cy + 95], fill=C_PAPER, outline=C_INK, width=2)
        draw.text((cx, cy + 72), "PROXY BALLOT: OPEN", font=font_mono_small, fill=C_OXBLOOD, anchor="mm")
        
    elif scene_idx == 4:
        # Scene 5: Monday Settlement
        ax = 180
        gx = WIDTH - 180 - hero_s5_elder.width
        bg.paste(hero_s5_alien, (ax, 140), hero_s5_alien)
        bg.paste(hero_s5_elder, (gx, 140), hero_s5_elder)
        
        # Desks
        draw.rectangle([ax - 30, 450, ax + hero_s5_alien.width + 30, 530], fill=(36, 26, 18), outline=(15, 10, 8), width=2)
        draw.rectangle([gx - 30, 450, gx + hero_s5_elder.width + 30, 530], fill=(36, 26, 18), outline=(15, 10, 8), width=2)
        
        # Fresh settlement receipts
        draw.rectangle([ax + 10, 465, ax + 230, 510], fill=C_PAPER, outline=C_INK_MUTED, width=1)
        draw.text((ax + 120, 487), "SETTLEMENT: 0.142 ETH", font=font_mono_small, fill=C_INK, anchor="mm")
        
        draw.rectangle([gx + 10, 465, gx + 230, 510], fill=C_PAPER, outline=C_INK_MUTED, width=1)
        draw.text((gx + 120, 487), "SETTLEMENT: 0.142 ETH", font=font_mono_small, fill=C_INK, anchor="mm")
        
    elif scene_idx == 5:
        # Scene 6: The Wall & Lamp Click
        if t_in_scene < dur_in_scene - 2.5:
            pw, ph = 640, 360
            px, py = (WIDTH - pw) // 2, (HEIGHT - 120 - ph) // 2
            draw.rectangle([px, py, px + pw, py + ph], fill=C_PAPER, outline=(40, 30, 22), width=4)
            draw.rectangle([px + 10, py + 10, px + pw - 10, py + ph - 10], outline=C_INK_MUTED, width=1)
            
            bg.paste(medallion, (px + (pw - medallion.width)//2, py + 30), medallion)
            draw.text((px + pw//2, py + 160), "THE MUTUAL FUN", font=font_title, fill=C_INK, anchor="mt")
            draw.text((px + pw//2, py + 220), "4,001 SEATS. 5 FUNDS.", font=font_subtitle, fill=C_OXBLOOD, anchor="mt")
            draw.text((px + pw//2, py + 270), "themutual.fun", font=font_mono, fill=C_INK_MUTED, anchor="mt")
        else:
            draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(0, 0, 0))

    # Subtitles
    if not (scene_idx == 5 and t_in_scene >= dur_in_scene - 2.5):
        draw.rectangle([40, HEIGHT - 110, WIDTH - 40, HEIGHT - 20], fill=(14, 11, 8), outline=(60, 48, 38), width=2)
        sub_text = subtitles[scene_idx]
        draw.text((WIDTH // 2, HEIGHT - 65), sub_text, font=font_mono_small, fill=C_PAPER, anchor="mm")
    
    pipe.stdin.write(bg.tobytes())

pipe.stdin.close()
pipe.wait()
print(f"SUCCESS: Rendered complete master video -> {out_mp4}")
