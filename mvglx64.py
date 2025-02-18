import struct
import os
import lz4.block

class MDB1Header:
    def __init__(self, f):
        self.magic, self.file_entry_count, self.file_name_count, self.data_entry_count, self.data_start, self.total_size = \
            struct.unpack('<4I2Q', f.read(32))

class FileEntry:
    def __init__(self, f):
        self.compare_bit, self.data_id, self.left, self.right = \
            struct.unpack('<4i', f.read(16))

class NameEntry:
    def __init__(self, f):
        name_buf = f.read(0x80)
        self.extension = str(name_buf[:4], 'ascii').strip('\0')
        self.name = str(name_buf[4:], 'ascii').strip('\0')

    def get_string(self) -> str:
        return self.name + '.' + self.extension.strip(' ')

class DataEntry:
    def __init__(self, f):
        self.offset, self.size, self.comp_size = \
            struct.unpack('<3Q', f.read(0x18))


def extract(mvgl_file: str, output_dir: str) -> int:
    f = open(mvgl_file, 'rb')
    header = MDB1Header(f)
    file_entries = []
    name_entries = []
    data_entries = []
    for i in range(header.file_entry_count): file_entries.append(FileEntry(f))
    for i in range(header.file_name_count): name_entries.append(NameEntry(f))
    for i in range(header.data_entry_count): data_entries.append(DataEntry(f))
    for i in range(len(file_entries)):
        if file_entries[i].compare_bit == -1 and file_entries[i].data_id == -1:
            continue
        print('Extracting: %s' % (name_entries[i].get_string()))
        data_entry = data_entries[file_entries[i].data_id]
        f.seek(header.data_start + data_entry.offset)
        dir = output_dir + '/' +os.path.dirname(name_entries[i].get_string())
        if not os.path.exists(dir): os.makedirs(dir)
        with open(output_dir + '/' + name_entries[i].get_string(), 'wb') as r:
            raw_data = f.read(data_entry.comp_size)
            decompressed = lz4.block.decompress(raw_data, data_entry.size) \
                if data_entry.size > data_entry.comp_size else raw_data
            r.write(decompressed)


extract('app_0.dx11.mvgl', 'app_0')
