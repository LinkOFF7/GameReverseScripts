# Fate Extella Link PS Vita archive (.pfs, .pkh, .pk) BIG-ENDIAN
# Not figured out how names works. There is 24-bytes entities in folder section:
# 4 - index
# 4 - ?
# 4 - ?
# 4 - contains folders?
# 4 - index of file in filelist
# 4 - files in folder

import os
import struct
import zlib

filenames = []
def readcstr(f, pos):
    cur = f.tell()
    f.seek(pos)
    cstr = bytearray()
    while True:
        ch = f.read(1)
        if(ch == b'\x00'):
            f.seek(cur)
            return str(cstr, "utf-8")
        cstr.append(ord(ch))
        
def readnames(pfsfile = "archive.pfs"):
    with open(pfsfile, "rb") as f:
        f.seek(8)
        folders_num, files_num = struct.unpack(">II", f.read(8))
        text_start = (folders_num * 24) + ((folders_num + files_num) * 4) + 16
        for i in range(folders_num):
            idx, unk2, unk3, unk4, file_idx, num_of_files = struct.unpack(">iiiiii", f.read(24))
        for i in range(files_num):
            offset = int(struct.unpack(">I", f.read(4))[0])
            filenames.append(readcstr(f, text_start + offset))
        i = 0
        for filename in filenames:
            if i >= folders_num: # skip folders
                filenames.append(filename)
            i += 1
                
def extract(pkhfile = "archive.pkh", pkfile = "archive.pk"):
    #readnames()
    with open(pkhfile, "rb") as pkh, open(pkfile, "rb") as pk:
        count = int(struct.unpack(">I", pkh.read(4))[0])
        if not os.path.exists("archive"):
            os.makedirs("archive")
        for i in range(count):
            unk1, zero1, zero2, offset, size, zsize = struct.unpack(">IIIIII", pkh.read(24))
            pk.seek(offset)
            if zsize > 0:
                zobj = zlib.decompressobj()
                data = zobj.decompress(pk.read(zsize))
            else:
                data = pk.read(size)
            with open(f"archive/{unk1}.dat", "wb") as out:
                print(f"[{i+1}/{count}] {unk1}.dat {offset} {size} {zsize}")
                out.write(data)
        
extract()