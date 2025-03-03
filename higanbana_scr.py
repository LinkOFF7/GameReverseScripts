# higanbana no saku yoru ni 3ds scriptdata%d.dat

import os, sys

opcodes = {
    0x00: 'mes',
    0x01: 'bg',
    0x02: 'ld',
    0x03: 'cl',
    0x04: 'wait',
    0x05: 'br',
    0x06: 'me1',
    0x07: 'me2',
    0x08: 'me3',
    0x09: 'me4',
    0x0A: 'me5',
    0x0B: 'me1v',
    0x0C: 'me2v',
    0x0D: 'me3v',
    0x0E: 'me4v',
    0x0F: 'me5v',
    0x10: 'se1',
    0x11: 'se2',
    0x12: 'se3',
    0x13: 'se1v',
    0x14: 'se2v',
    0x15: 'se3v',
    0x16: 'bgm1',
    0x18: 'E_A',
    0x19: 'E_B',
    0x1A: 'E_M1',
    0x1B: 'E_M2',
    0x1C: 'E_M3',
    0x1D: 'E_M4',
    0x1F: 'E_MA',
    0x20: 'fede',
    0x21: 'fedexx',
    0x22: 'movie',
    0x23: 'mono',
    0x24: 'nega',
    0x25: 'ld_p',
    0x26: 'csp2',
    0x27: 'print',
    0x28: 'mld',
    0x29: 'mcl',
    0x2A: 'mbg',
    0x2B: 'mcbg',
    0x2C: 'dllefe',
    0x2D: 'dllefe_off',
    0x2E: 'lsp',
    0x2F: 'csp',
    0x30: 'quake',
    0x31: 'quakex',
    0x32: 'quakey',
    0x33: 'mevol',
    0x34: 'bgmvol',
    0x35: 'texton',
    0x36: 'textoff',
    0x37: 'locate',
    0x38: 'bgcopy',
    0x39: 'bgmonce',
    0x3A: 'prnumclear',
    0x3B: 'com_at',
    0x3C: 'mov',
    0xFF: 'eoi'
}

def read_single_instr(f) -> bytes:
    buf = bytearray()
    while True:
        b = f.read(1)
        if b == b'\x00' and len(buf) != 0:
            f.seek(-1, os.SEEK_CUR)
            return buf
        elif b == b'\xFF' and len(buf) > 1:
            return buf
        buf.extend(b)
            

def script_factory(f):
    result = ''
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)
    pos = 0
    while pos < size:
        b = f.read(1)
        pos += 1
        if b == b'\x00':
            instr = read_single_instr(f)
            pos += len(instr)
            if len(instr) > 0:
                result += opcodes[instr[0]] + str(instr[1:], 'shift-jis').replace('\n', '\\n') + '\n'
            else:
                result += '\n'
    return result
        
def read(file):
    with open(file, 'rb') as f:
        scr = script_factory(f)
    with open(file + '.txt', 'w', encoding='utf-8') as f:
        f.write(scr)

read(sys.argv[1] if len(sys.argv) == 2 else sys.argv[0])