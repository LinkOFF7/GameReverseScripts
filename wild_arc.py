# Wild Hearts .arc extraction
# Incomplete: unknown encryption

import os
import struct
import sys

def read(file):
    with open(file, "rb") as f:
        magic, unk1, start_pos, entry_length, count, unk2 = struct.unpack('<IIQIIQ', f.read(32))
        if magic != 0x9186A482:
            print('Unknown magic.')
            return -1
        outdir = os.path.splitext(file)[0]
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        for i in range(count):
            f.read(16) # skipping unknown 8 bytes and type
            size, offset = struct.unpack('<QQ', f.read(16))
            cur = f.tell()
            f.seek(offset)
            data = f.read(size)
            f.seek(cur)
            with open(f"{outdir}/{i}.dat", "wb") as d:
                print(f"[{i+1}/{count}]{outdir}/{i}.dat")
                d.write(data) # obfuscated
                
read(sys.argv[1])
