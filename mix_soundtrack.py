import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

scene_durations = [17.0, 21.0, 20.0, 23.0, 17.5, 9.5]

# Scene 1: VO + Stamp thump at t=1.8s, total dur = 17.0s
cmd1 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_1.mp3',
    '-i', 'audio/sfx_stamp_thump.wav',
    '-filter_complex',
    '[1:a]adelay=1800|1800,volume=1.2[thump];[0:a][thump]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=17.0[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_1.wav'
]
subprocess.run(cmd1, check=True)

# Scene 2: VO + Typewriter, total dur = 21.0s
cmd2 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_2.mp3',
    '-i', 'audio/sfx_typewriter.wav',
    '-filter_complex',
    '[1:a]volume=0.25[type];[0:a][type]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=21.0[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_2.wav'
]
subprocess.run(cmd2, check=True)

# Scene 3: VO + Latches at t=0.8s, total dur = 20.0s
cmd3 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_3.mp3',
    '-i', 'audio/sfx_brass_latches.wav',
    '-filter_complex',
    '[1:a]adelay=800|800,volume=1.0[latches];[0:a][latches]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=20.0[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_3.wav'
]
subprocess.run(cmd3, check=True)

# Scene 4: VO + Clock ticking, total dur = 23.0s
cmd4 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_4.mp3',
    '-i', 'audio/sfx_clock_ticking.wav',
    '-filter_complex',
    '[1:a]volume=0.35[clock];[0:a][clock]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=23.0[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_4.wav'
]
subprocess.run(cmd4, check=True)

# Scene 5: VO + Paper rustle, total dur = 17.5s
cmd5 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_5.mp3',
    '-i', 'audio/sfx_paper_rustle.wav',
    '-filter_complex',
    '[1:a]volume=0.35[paper];[0:a][paper]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=17.5[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_5.wav'
]
subprocess.run(cmd5, check=True)

# Scene 6: VO + toggle click at t=6.5s, then darkness and silence, total dur = 9.5s
cmd6 = [
    ffmpeg, '-y',
    '-i', 'audio/scene_6.mp3',
    '-i', 'audio/sfx_toggle_click.wav',
    '-filter_complex',
    '[1:a]adelay=6500|6500,volume=0.9[toggle];[0:a]apad=whole_dur=9.5[vopad];[vopad][toggle]amix=inputs=2:duration=first[mix];[mix]apad=whole_dur=9.5[aout]',
    '-map', '[aout]',
    '-c:a', 'pcm_s16le',
    'audio/mixed_scene_6.wav'
]
subprocess.run(cmd6, check=True)

with open('audio/concat_list.txt', 'w') as f:
    for i in range(1, 7):
        f.write(f"file 'mixed_scene_{i}.wav'\n")

cmd_cat = [
    ffmpeg, '-y',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'audio/concat_list.txt',
    '-c:a', 'pcm_s16le',
    'audio/full_soundtrack.wav'
]
subprocess.run(cmd_cat, check=True)
print("Built clean master soundtrack with exact timings:", scene_durations)
