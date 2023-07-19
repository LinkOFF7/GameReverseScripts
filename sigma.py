# Ninja Gaiden Sigma 1 (steam) databin extraction script

import os
import struct
import zlib

def get_ext(data):
    # there is filelist in the .exe, but its not sorted
    sign = int.from_bytes(data[:4], byteorder='little')
    if sign == 0x79727473:
        return '.sty'
    elif sign == 0x434d54:
        return '.tmc'
    elif sign == 0x4c787456:
        return '.xmc'
    elif sign == 0x47315447:
        return '.g1t'
    elif sign == 0x5f726863:
        return '.chr'
    elif sign == 0x5f6d7469:
        return '.itm'
    elif sign == 0x5f6c7462:
        return '.btl'
    elif sign == 0x5f6d7472:
        return '.rtm'
    elif sign == 0x474e5089:
        return '.png'
    elif sign == 0x444e53:
        return '.snd'
    elif sign == 0x69727073:
        return '.spr'
    elif sign == 0x61706474:
        return '.tdp'
    else:
        return '.dat'

def extract(file):
    with open(file, 'rb') as f:
        f.seek(16) # bunch of unk values
        ptrs_start, data_start, unk3, unk4, count, counter_start, count2, unk8 = struct.unpack('<8I', f.read(32))
        ptrs = []
        for i in range(count):
            ptrs.append(int.from_bytes(f.read(4), byteorder='little'))
        outdir = os.path.splitext(file)[0] + '_extracted'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        c = 0
        for ptr in ptrs:
            f.seek(ptr + 0x1c) # actual bias is 28 bytes, not 32 bytes. dunno why
            zero, offset, size, zsize, unk14, unk18, unk1c = struct.unpack('<IQ5I', f.read(32))
            if zsize == 0: # single entry is blank
                c += 1
                continue
            f.seek(data_start + ptrs_start + offset)
            compressed = f.read(zsize)
            data = zlib.decompress(compressed)
            path = '%s/%s%s' % (outdir, c, get_ext(data))
            print('[%i/%i] Extracting: %s' % (c+1, count, path))
            with open(path, 'wb') as r:
                r.write(data)
            c += 1
        print('Done!')
        
        
extract('databin')
