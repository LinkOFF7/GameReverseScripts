#Touhou Genso Wanderer archives (AQUA) PS Vita

import os
import sys
import struct
import zstandard

def decompress(data):
    decomp = zstandard.ZstdDecompressor()
    return decomp.decompress(data)

def readstring(f, pos, ln):
    cur = f.tell()
    f.seek(pos)
    string = ''
    for i in range(ln):
        string += str(f.read(1), "utf-8")
    f.seek(cur)
    return string

def extract(file):
    with open(file, "rb") as f:
        magic, unk, count = struct.unpack("<IIH", f.read(10))
        if magic != 0x41555141: # AQUA
            return -1
        f.seek(16) # idk what is 6-bytes at 0xA
        start = struct.unpack("<Q", f.read(8)) # offsets always unsigned long value
        outdir = os.path.splitext(file)[0]
        
        for i in range(count):
            compsize, size, unk, compflag, namelen, nameoffset, offset = struct.unpack("<IIIIIIQ", f.read(32))
            filename = readstring(f, nameoffset, namelen)
            cur = f.tell()
            f.seek(offset)
            rawdata = f.read(size)
            if compflag == 1: # zstd
                decompressed = decompress(rawdata)
            f.seek(cur)
            print(f'[{offset}] {filename} ({size}/{compsize})')
            path = outdir + "/" + os.path.dirname(filename)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(outdir + "/" + filename, "wb") as out:
                if compflag == 1:
                    out.write(decompressed)
                if compflag == 0:
                    out.write(rawdata)
                
                
extract(sys.argv[1])