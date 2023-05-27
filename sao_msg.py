import os
import struct
import sys

alltext = []
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

def read(file):
    with open(file, "rb") as f:
        magic, start, unk, fullsize, count = struct.unpack("<IIIII", f.read(0x14))
        for i in range(count):
            pos, index = struct.unpack("<II", f.read(8))
            alltext.append("#%s#%s" % (index, readcstr(f, pos + start)))
            
            
def savetext(outfile):
    with open(outfile, "w", encoding="utf-8") as f:
        for line in alltext:
            f.write(line.replace('\n', '<lf>') + '\n')
        print("Text saved to %s" % outfile)

read(sys.argv[1])
savetext("%s.txt" % sys.argv[1])