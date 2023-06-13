# Ghost Trick Phantom Detective DEMO re_chunk_000.pak
# based on Ekey's tool: https://github.com/Ekey/REE.PAK.Tool

import sys
import os
import struct
import zlib


def get_comp(flag):
    if flag & 0xf == 1:
        return 'deflate'
    else:
        return 'none'
        
def get_ext(data):
    # i am too lazy to copy-paste all signatures =(
    sign = int.from_bytes(data[:4], byteorder='little')
    if sign == 0x584554:
        return '.tex'
    elif sign == 0x4F464246:
        return '.oft'
    else:
        sign = int.from_bytes(data[4:8], byteorder='little')
        if sign == 0x47534D47:
            return '.msg'
        else:
            return '.dat'

def extract(pakfile):
    with open(pakfile, 'rb') as f:
        magic, version, num_of_files, crc = struct.unpack('<4I', f.read(16))
        if magic != 0x414B504B:
            print('Invalid magic number')
            return
        for i in range(num_of_files):
            low_hash, high_hash, offset, comp_size, uncomp_size, comp_flag, dependency = struct.unpack('<IIqqqqQ', f.read(48))
            compression = get_comp(comp_flag)
            save = f.tell()
            f.seek(offset)
            raw_data = f.read(comp_size)
            if compression == 'deflate':
                data = zlib.decompress(raw_data, -15)
            else:
                data = raw_data
            f.seek(save)
            ext = get_ext(data)
            path = os.path.splitext(pakfile)[0]
            if not os.path.exists(path):
                os.makedirs(path)
            print('[%d/%d] %s\%d%s (%s)' % (i+1, num_of_files, path, i, ext, compression))
            with open(f'{path}\{str(i)}{ext}', 'wb') as r:
                r.write(data)
                    
extract(sys.argv[1])