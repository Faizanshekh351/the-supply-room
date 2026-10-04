import wave
import struct
import math
import random
import os

os.makedirs("audio", exist_ok=True)
SAMPLE_RATE = 44100

def write_wav(filename, samples):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # mono
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        # clamp
        int_samples = [max(-32767, min(32767, int(s * 32767))) for s in samples]
        raw = struct.pack(f'<{len(int_samples)}h', *int_samples)
        wav_file.writeframes(raw)

# 1. Stamp Thump (heavy wooden & rubber thump)
thump_duration = 0.4
thump_samples = []
for i in range(int(SAMPLE_RATE * thump_duration)):
    t = i / SAMPLE_RATE
    env = math.exp(-t * 18)
    # pitch drops from 95Hz to 30Hz
    freq = 30 + 65 * math.exp(-t * 25)
    s = math.sin(2 * math.pi * freq * t) * env
    # low frequency thud noise
    noise = (random.random() * 2 - 1) * math.exp(-t * 35) * 0.4
    thump_samples.append((s + noise) * 0.85)
write_wav("audio/sfx_stamp_thump.wav", thump_samples)

# 2. Typewriter Keystroke sequence (IBM Selectric)
type_duration = 20.5
type_samples = [0.0] * int(SAMPLE_RATE * type_duration)
# rhythm strikes
for strike_t in [0.2, 0.45, 0.7, 1.1, 1.35, 1.6, 2.0, 2.3, 2.7, 3.1, 3.4, 3.8, 4.2, 4.6, 5.0, 5.5, 6.0, 6.4, 7.0, 7.5, 8.2, 8.8, 9.4, 10.1, 10.8, 11.5, 12.2, 13.0, 14.0, 15.0, 16.2, 17.5, 18.5, 19.5]:
    start_idx = int(strike_t * SAMPLE_RATE)
    for j in range(int(0.08 * SAMPLE_RATE)):
        t = j / SAMPLE_RATE
        if start_idx + j < len(type_samples):
            # sharp metallic clack + paper slap
            f = 1200 + random.uniform(-100, 100)
            click = math.sin(2 * math.pi * f * t) * math.exp(-t * 90)
            noise = (random.random() * 2 - 1) * math.exp(-t * 70) * 0.6
            type_samples[start_idx + j] += (click + noise) * 0.35
write_wav("audio/sfx_typewriter.wav", type_samples)

# 3. Twin Brass Latches (sharp clack-clack)
latch_duration = 0.5
latch_samples = [0.0] * int(SAMPLE_RATE * latch_duration)
for t_offset in [0.05, 0.16]:
    start_idx = int(t_offset * SAMPLE_RATE)
    for j in range(int(0.06 * SAMPLE_RATE)):
        t = j / SAMPLE_RATE
        click = math.sin(2 * math.pi * 2200 * t) * math.exp(-t * 120)
        noise = (random.random() * 2 - 1) * math.exp(-t * 100) * 0.7
        latch_samples[start_idx + j] += (click + noise) * 0.6
write_wav("audio/sfx_brass_latches.wav", latch_samples)

# 4. Clock Escapement Ticking (tock... tock... tock)
clock_duration = 22.0
clock_samples = [0.0] * int(SAMPLE_RATE * clock_duration)
for sec in range(int(clock_duration)):
    start_idx = int(sec * SAMPLE_RATE)
    for j in range(int(0.07 * SAMPLE_RATE)):
        t = j / SAMPLE_RATE
        freq = 680 if (sec % 2 == 0) else 540
        tick = math.sin(2 * math.pi * freq * t) * math.exp(-t * 80)
        noise = (random.random() * 2 - 1) * math.exp(-t * 110) * 0.3
        if start_idx + j < len(clock_samples):
            clock_samples[start_idx + j] += (tick + noise) * 0.4
write_wav("audio/sfx_clock_ticking.wav", clock_samples)

# 5. Paper Rustle
paper_duration = 17.0
paper_samples = [0.0] * int(SAMPLE_RATE * paper_duration)
for rustle_t in [1.5, 4.0, 7.5, 11.0, 14.2]:
    start_idx = int(rustle_t * SAMPLE_RATE)
    for j in range(int(0.4 * SAMPLE_RATE)):
        t = j / SAMPLE_RATE
        env = math.sin(math.pi * (j / (0.4 * SAMPLE_RATE)))
        noise = (random.random() * 2 - 1) * env * 0.18
        if start_idx + j < len(paper_samples):
            paper_samples[start_idx + j] += noise
write_wav("audio/sfx_paper_rustle.wav", paper_samples)

# 6. Brass Toggle Switch Click (snap)
toggle_duration = 0.3
toggle_samples = []
for i in range(int(SAMPLE_RATE * toggle_duration)):
    t = i / SAMPLE_RATE
    click = math.sin(2 * math.pi * 1400 * t) * math.exp(-t * 140)
    noise = (random.random() * 2 - 1) * math.exp(-t * 120) * 0.5
    toggle_samples.append((click + noise) * 0.7)
write_wav("audio/sfx_toggle_click.wav", toggle_samples)

print("Generated all Foley sound effects successfully.")
