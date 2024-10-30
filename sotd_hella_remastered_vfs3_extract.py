import os, struct

class FileEntry:
    def __init__(self, f):
        self.offset, self.compressedSize, self.decompressedSize = struct.unpack('<3Q',  f.read(0x18))
        self.unk18, self.filenameIndex, self.unk20, self.unk24, self.unk26 = struct.unpack('<3I2h',  f.read(0x10))
        
def readcstr(f):
    cstr = bytearray()
    while True:
        ch = f.read(2)
        if(ch == b'\x00\x00'):
            return str(cstr, "utf-16")
        cstr += ch
        
def read_filenames(f, offset):
    cur = f.tell()
    f.seek(offset)
    count = struct.unpack('<I', f.read(4))[0]
    filenames = []
    for i in range(count):
        filenames.append(readcstr(f))
    f.seek(cur)
    return filenames

def extract(vfs_file):
    f = open(vfs_file, 'rb')
    f.seek(0x7c)
    count = struct.unpack('<I', f.read(4))[0]
    data_start = f.tell() + (count * 0x28) + (0x8 * 3)
    entries = []
    for i in range(count):
        entries.append(FileEntry(f))
    f.read(16)
    filename_offset = struct.unpack('<Q', f.read(8))[0]
    filenames = read_filenames(f, filename_offset)
    out_dir = os.path.splitext(vfs_file)[0]
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for entry in entries:
        filename = filenames[entry.filenameIndex]
        print('Processing: %s' % filename)
        f.seek(data_start + entry.offset)
        data = f.read(entry.decompressedSize)
        r = open('%s/%s' % (out_dir, filenames[entry.filenameIndex]), 'wb')
        r.write(data)
        r.close()
    f.close()
    
extract('data.vfs')