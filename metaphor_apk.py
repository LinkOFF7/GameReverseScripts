import os
import sys
import struct
import lz4.block

class ZZZ0:
    def __init__(self, f):
        self.magic, self.var04, self.var08, self.uncompressed_size = struct.unpack('<4I', f.read(16))
        self.data_size, self.var14, self.var18, self.var1C = struct.unpack('<4I', f.read(16))
        self.compressed_size, self.compressed_offset, self.var18, self.var1C = struct.unpack('<4I', f.read(16))
        
    def decompress(self, f) -> bytes:
        compressed = f.read(self.compressed_size)
        return lz4.block.decompress(compressed, self.uncompressed_size)

class TOCEntry:
    def __init__(self, f):
        self.file_name = str(f.read(256), 'ascii').strip('\0')
        self.size, self.rev1, self.rev2, self.offset = struct.unpack('4Q', f.read(32))

def extract(apk_file):
    output_dir = os.path.splitext(os.path.basename(apk_file))[0]
    f = open(apk_file, 'rb')
    magic, var04, files, var0C = struct.unpack('<4i', f.read(16))
    toc = []
    for i in range(files):
        toc.append(TOCEntry(f))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for entry in toc:
        print('Extracting: %s' % entry.file_name)
        r = open('%s/%s' % (output_dir, entry.file_name), 'wb')
        f.seek(entry.offset)
        data = ZZZ0(f)
        r.write(data.decompress(f))
        r.close()
    
extract(sys.argv[1])