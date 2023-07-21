# Xenosaga Episode 1 JavaClass text export script (0xCAFEBABE)

import os
import sys
import struct

idx = []
dicts = []
        
def readstring(f, ln):
    return str(f.read(ln), "euc-jp")

def get_const_item_len(tag):
    if tag == 5 or tag == 6:
        return 8
    elif tag == 7 or tag == 8 or tag == 16:
        return 2
    else:
        return 4
        
def save(output_file):
    with open(output_file, 'w', encoding='utf-8') as r:
        for i in idx:
            for dct in dicts:
                if dct['index'] == i:
                    r.write(dct['content'] + '\n')
        print('Saved to %s' % output_file)
                    
def read(file):
    with open(file, 'rb') as f:
        magic, ver_major, ver_minor, constantNum = struct.unpack('>I3H', f.read(10))
        if magic != 0xCAFEBABE:
            print('Unknown file type.')
            return
        for i in range(constantNum-1):
            tag = int.from_bytes(f.read(1), byteorder='big')
            if tag == 1: # string
                strlen = int.from_bytes(f.read(2), byteorder='big')
                string = readstring(f, strlen).rstrip('\x00').replace('\n', '<lf>')
                dicts.append(dict(index=i, content=string))
            elif tag == 8: # string index
                stridx = int.from_bytes(f.read(2), byteorder='big')
                idx.append(stridx - 1)
            else:
                f.read(get_const_item_len(tag))
        
read(sys.argv[1])
save(sys.argv[1] + '.txt')