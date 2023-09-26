import os
import struct

def get_size(f):
    save = f.tell()
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(save)
    return size

def dump_to_txt(metadataFile):
    with open(metadataFile, 'rb') as f:
        signature, header_size, string_info_table_offset, string_info_table_length, string_table_offset, string_table_length = struct.unpack('6I', f.read(0x18))
        if signature != 0xFAB11BAF:
            print('Unknown signature')
            exit()
        if header_size > 0x20:
            print('File is obfuscated.')
            exit()
        sizes = []
        offsets = []
        strings = []
        count = string_info_table_length // 8
        f.seek(string_info_table_offset)
        for i in range(0, count):
            sizes.append(int.from_bytes(f.read(4), byteorder='little'))
            offsets.append(int.from_bytes(f.read(4), byteorder='little'))
        for i in range(0, count):
            f.seek(string_table_offset + offsets[i])
            string = f.read(sizes[i]).decode('utf-8')
            if string == '':
                strings.append('<empty>')
            elif string == ' ':
                strings.append('<space>')
            elif string == '    ':
                strings.append('<tab>')
            else:
                strings.append(string.replace('\r', '<cr>').replace('\n', '<lf>'))
        with open('%s.txt' % metadataFile, 'w', encoding='utf-8') as t:
            for string in strings:
                t.write(string + '\n')
                
def import_new_string_table(metadataFile, textFile):
    with open(metadataFile, 'r+b') as f, open(textFile, 'r', encoding='utf-8') as t:
        strings = t.readlines()
        signature, header_size, string_info_table_offset, string_info_table_length, string_table_offset, string_table_length = struct.unpack('6I', f.read(0x18))
        if signature != 0xFAB11BAF:
            print('Unknown signature')
            exit()
        if header_size > 0x20:
            print('File is obfuscated.')
            exit()
            
        # check number of strings
        count = string_info_table_length // 8
        if count != len(strings):
            print('String count error: metadata: %d\ttext file: %d\n' % (count, len(strings)))
            exit()
            
        sizes = []
        offsets = []
        cur = 0
        end = get_size(f)
        f.seek(end)
        if end % 0x10 != 0: # align if necessary
            f.seek((0x10 - end % 0x10) + end)
            end = f.tell()
        
        
        for string in strings:
            if string == '<empty>':
                offsets.append(cur)
                sizes.append(0)
            else:
                string = string.strip('\n').replace('<cr>', '\r').replace('<lf>', '\n').replace('tab>', '\t').replace('<space>', ' ')
                strbytes = string.encode('utf-8')
                offsets.append(cur)
                strlen = len(strbytes)
                sizes.append(strlen)
                f.write(strbytes)
                cur += strlen
                
        string_table_offset = end
        string_info_table_length = get_size(f) - end
        # header
        f.seek(0x10)
        f.write(string_table_offset.to_bytes(4, byteorder='little'))
        f.write(string_info_table_length.to_bytes(4, byteorder='little'))
        #info
        f.seek(string_info_table_offset)
        for i in range(0, count):
            f.write(sizes[i].to_bytes(4, byteorder='little'))
            f.write(offsets[i].to_bytes(4, byteorder='little'))
            
        print('Done.')
        
dump_to_txt('global-metadata.dat')
#import_new_string_table('global-metadata.dat', 'global-metadata.dat.txt')