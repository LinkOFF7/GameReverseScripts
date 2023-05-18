import sys
import struct

def readcstr(f, pos):
    cur = f.tell()
    f.seek(pos)
    cstr = bytearray()
    while True:
        ch = f.read(1)
        if(ch == b'\x00'):
            f.seek(cur)
            try:
                return str(cstr, "utf-8")
            except UnicodeDecodeError:
                return '<UNIERR>'
        cstr.append(ord(ch))
    

def read(file):
    text = []
    with open(file, "rb") as f:
        f.seek(0x120)
        count = struct.unpack("<I", f.read(4))
        for i in range(*count):
            f.read(4) #skip id
            offset = int(struct.unpack("<I", f.read(4))[0]) + 0x120
            line = readcstr(f, offset)
            text.append(line)
        with open(file + ".txt", "w", encoding="utf-8") as t:
            for line in text:
                t.write(line.replace('\n', '<lb>') + '\n')
            print(f'Saved to {file}.txt')

read(sys.argv[1])
