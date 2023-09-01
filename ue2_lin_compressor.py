# Land of the Dead: Road to Fiddler's Green XBOX .lin compressor (Unreal Engine 2)

import struct
import os
import sys
import zlib

CHUNK_SIZE = 16384

def compress_lin(file):
    result_filename = os.path.splitext(file)[0] + '.lin'
    with open(file, 'rb') as f, open (result_filename, 'wb') as r:
        fsize = os.path.getsize(file)
        chunk_num = (fsize // CHUNK_SIZE) + 1
        for i in range(chunk_num):
            data_decomp = f.read(CHUNK_SIZE)
            data_comp = zlib.compress(data_decomp)
            r.write(len(data_decomp).to_bytes(4, byteorder='little'))
            r.write(len(data_comp).to_bytes(4, byteorder='little'))
            r.write(data_comp)
        print('%s compressed to %s' % (file, result_filename))

def decompress_lin(file):
    result_filename = os.path.splitext(file)[0] + '.dz'
    with open(file, 'rb') as f, open (result_filename, 'wb') as r:
        fsize = os.path.getsize(file)
        cur = 0
        while(cur < fsize):
            size, zsize = struct.unpack('<2I', f.read(8))
            data = zlib.decompress(f.read(zsize))
            r.write(data)
            cur = f.tell()
        print('%s decompressed to %s' % (file, result_filename))
                
if len(sys.argv) < 2:
    exit()
ext = os.path.splitext(sys.argv[1])[1]
if ext == '.lin':
    decompress_lin(sys.argv[1])
elif ext == '.dz':
    compress_lin(sys.argv[1])