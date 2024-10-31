import os, struct

class DirEntry:
    def __init__(self, f):
        self.index, self.var04, self.var08, self.var0C = struct.unpack('<4i',  f.read(0x10))
        self.var10, self.var14, self.var18 = struct.unpack('<iiI',  f.read(0xC))

class FileEntry:
    def __init__(self, f):
        self.offset, self.compressedSize, self.decompressedSize = struct.unpack('<3Q',  f.read(0x18))
        self.unk18, self.filenameIndex, self.dirIndex, self.unk24, self.unk26 = struct.unpack('<3I2h',  f.read(0x10))
        
def readcstr(f):
    cstr = bytearray()
    while True:
        ch = f.read(2)
        if(ch == b'\x00\x00'):
            return str(cstr, "utf-16")
        cstr += ch
        
def align(var):
    if var % 16 != 0:
        return var + (16 - var % 16)
    return var
        
def read_filenames(f, offset):
    cur = f.tell()
    f.seek(offset)
    file_count = struct.unpack('<I', f.read(4))[0]
    dirs = []
    files = []
    for i in range(file_count):
        files.append(readcstr(f))
    dir_count = struct.unpack('<I', f.read(4))[0]
    for i in range(dir_count):
        dirs.append(readcstr(f))
    f.seek(cur)
    return (files, dirs)

def extract(vfs_file):
    f = open(vfs_file, 'rb')
    magic, start_offset, dir_count, pad = struct.unpack('<4I', f.read(16))
    if magic != 0x33534656:
        exit()
    dirs = []
    for i in range(dir_count):
        dirs.append(DirEntry(f))
    count = dirs[len(dirs)-1].var18
    data_start = f.tell() + (count * 0x28) + (0x8 * 3)
    data_start = align(data_start)
    print(data_start)
    entries = []
    for i in range(count):
        entries.append(FileEntry(f))
    f.read(16)
    filename_offset = struct.unpack('<Q', f.read(8))[0]
    filenames, dirnames = read_filenames(f, filename_offset)
    for entry in entries:
        if not os.path.exists(dirnames[entry.dirIndex]):
            os.makedirs(dirnames[entry.dirIndex])
        filepath = '%s/%s' % (dirnames[entry.dirIndex], filenames[entry.filenameIndex])
        print('Processing: %s' % (filepath))
        f.seek(data_start + entry.offset)
        data = f.read(entry.decompressedSize)
        r = open(filepath, 'wb')
        r.write(data)
        r.close()
    f.close()
    
extract('data.vfs')
