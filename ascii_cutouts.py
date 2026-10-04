import zlib
import struct
import glob
import os

def get_image_rgba(path):
    with open(path, 'rb') as f:
        data = f.read()
    pos = 8
    width = height = None
    idat = []
    while pos < len(data):
        length, chunk_type = struct.unpack('>I4s', data[pos:pos+8])
        pos += 8
        chunk_data = data[pos:pos+length]
        pos += length + 4
        if chunk_type == b'IHDR':
            width, height, bit_depth, color_type = struct.unpack('>IIBB', chunk_data[:10])
        elif chunk_type == b'IDAT':
            idat.append(chunk_data)
        elif chunk_type == b'IEND':
            break
    
    decomp = zlib.decompress(b''.join(idat))
    # It is RGBA, width x height
    # row size = 1 filter byte + width * 4
    stride = 1 + width * 4
    pixels = []
    # reconstruct unfilter
    prev_row = bytearray(width * 4)
    for y in range(height):
        filter_type = decomp[y * stride]
        row = bytearray(decomp[y * stride + 1 : (y + 1) * stride])
        if filter_type == 0:
            pass
        elif filter_type == 1: # Sub
            for i in range(4, len(row)):
                row[i] = (row[i] + row[i-4]) & 0xFF
        elif filter_type == 2: # Up
            for i in range(len(row)):
                row[i] = (row[i] + prev_row[i]) & 0xFF
        elif filter_type == 3: # Average
            for i in range(len(row)):
                left = row[i-4] if i >= 4 else 0
                up = prev_row[i]
                row[i] = (row[i] + ((left + up) >> 1)) & 0xFF
        elif filter_type == 4: # Paeth
            for i in range(len(row)):
                a = row[i-4] if i >= 4 else 0
                b = prev_row[i]
                c = prev_row[i-4] if i >= 4 else 0
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                if pa <= pb and pa <= pc: pr = a
                elif pb <= pc: pr = b
                else: pr = c
                row[i] = (row[i] + pr) & 0xFF
        prev_row = row
        pixels.append(row)
    return width, height, pixels

# Let's inspect a few cutouts
for f in sorted(glob.glob('cutouts/*.png')):
    key = os.path.basename(f).replace('.png', '')
    w, h, rows = get_image_rgba(f)
    # sample grid 32x32 ascii
    lines = []
    for y in range(0, h, h // 24):
        line = []
        for x in range(0, w, w // 40):
            idx = x * 4
            if idx + 3 < len(rows[y]):
                r, g, b, a = rows[y][idx:idx+4]
                if a < 128:
                    line.append(' ')
                else:
                    lum = (r * 299 + g * 587 + b * 114) // 1000
                    if lum > 200: line.append('#')
                    elif lum > 140: line.append('*')
                    elif lum > 70: line.append(':')
                    else: line.append('.')
        lines.append(''.join(line))
    print(f"=== {key} ({w}x{h}) ===")
    print('\n'.join(lines[:14])) # print head/upper body
