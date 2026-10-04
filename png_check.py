import zlib
import struct
import glob
import os

def read_png(path):
    with open(path, 'rb') as f:
        data = f.read()
    # Check signature
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Not a PNG file")
    pos = 8
    chunks = []
    width = height = bit_depth = color_type = None
    idat = []
    palette = []
    trns = []
    while pos < len(data):
        length, chunk_type = struct.unpack('>I4s', data[pos:pos+8])
        pos += 8
        chunk_data = data[pos:pos+length]
        pos += length
        crc = data[pos:pos+4]
        pos += 4
        if chunk_type == b'IHDR':
            width, height, bit_depth, color_type = struct.unpack('>IIBB', chunk_data[:10])
        elif chunk_type == b'PLTE':
            palette = [chunk_data[i:i+3] for i in range(0, len(chunk_data), 3)]
        elif chunk_type == b'tRNS':
            trns = list(chunk_data)
        elif chunk_type == b'IDAT':
            idat.append(chunk_data)
        elif chunk_type == b'IEND':
            break

    raw_data = zlib.decompress(b''.join(idat))
    return width, height, color_type, palette, trns, raw_data

# Let's test reading one cutout
w, h, ctype, pal, trns, raw = read_png('cutouts/argon-01.png')
print(f"Argon-01: {w}x{h}, color_type={ctype}, pal_len={len(pal)}, trns_len={len(trns)}")
