#include <stdio.h>
#include <string.h>

const unsigned int table[24] = { 0x1,     0x3,     0x7,      0xf,      0x1f,     0x3f,
                                 0x7f,    0xff,    0x1ff,    0x3ff,    0x7ff,    0xfff,
                                 0x1fff,  0x3fff,  0x7fff,   0xffff,   0x1ffff,  0x3ffff,
                                 0x7ffff, 0xfffff, 0x1fffff, 0x3fffff, 0x7fffff, 0xffffff };

unsigned int    bit_marker;
unsigned int    bit_data;
unsigned int*   bit_next;

unsigned int do_401030() {
    unsigned int sv = 0x200;
    unsigned int retval = 0;

    do {
        unsigned int value = bit_marker & bit_data;
        if (value) {
            retval |= sv;
        }

        bit_marker >>= 1;
        if (bit_marker == 0) {
            bit_marker = 0x80000000;
            bit_data = *bit_next++;
        }

        sv >>= 1;
    } while (sv != 0);

    return retval;
}

unsigned int do_401080() {
    unsigned int count = 0;
    unsigned int sv = 0;
    unsigned int ebx = 0;

    while (1) {
        unsigned int value = bit_marker & bit_data;

        bit_marker >>= 1;
        if (bit_marker == 0) {
            bit_marker = 0x80000000;
            bit_data = *bit_next++;
        }

        if (value == 0) {
            break;
        }

        ++count;
    }

    sv = 1 << count;
    ebx = 0;

    do {
        unsigned int value = bit_marker & bit_data;
        if (value) {
            ebx |= sv;
        }

        bit_marker >>= 1;
        if (bit_marker == 0) {
            bit_marker = 0x80000000;
            bit_data = *bit_next++;
        }

        sv >>= 1;
    } while (sv != 0);

    return table[count] + ebx;
}

bool decompress(unsigned char* data, unsigned int size, unsigned char** ddest, unsigned int* dsize) {
    unsigned int v1;
    unsigned int v2;
    unsigned char* input;
    unsigned int read_data;
    unsigned char* dest, * dest_orig, * dest_end;

    if (memcmp(data, "LZLR", 4)) {
        return 0;
    }

    v1 = ((unsigned int*)data)[1];
    v2 = ((unsigned int*)data)[2];

    bit_marker = 0x80000000;
    bit_next = ((unsigned int*)data) + 3;
    bit_data = *bit_next++;

    input = data + v2;

    dest_orig = new unsigned char[v1 + 0x10000];
    dest = dest_orig;
    dest_end = dest + v1;

    read_data = 0;

    while (read_data < v1) {
        unsigned int value = bit_marker & bit_data;

        bit_marker >>= 1;
        if (bit_marker == 0) {
            bit_marker = 0x80000000;
            bit_data = *bit_next++;
        }

        if (value != 0) {
            unsigned int count1 = do_401080();

            while (count1-- > 0) {
                unsigned int count2 = do_401080();
                unsigned int count3 = do_401030();
                unsigned char* src = dest - (count3 * 4);

                for (unsigned int i = 0; i < count2; ++i) {
                    *(unsigned int*)dest = *(unsigned int*)src;
                    src += 4;
                    dest += 4;
                }

                read_data += count2 * 4;
            }
        }
        else {
            unsigned int count = do_401080();

            memcpy(dest, input, count * 4);
            dest += count * 4;
            input += count * 4;

            read_data += count * 4;
        }
    }

    *ddest = dest_orig;
    *dsize = v1;

    return 1;
}


bool decompress_file(const char* ifilename, const char* ofilename) {
    FILE* inputFile;
    FILE* outputFile;
    unsigned char* data, * uncomp;
    unsigned int size, uncomp_size;
    bool retval = 0;

    inputFile = fopen(ifilename, "rb");
    outputFile = fopen(ofilename, "wb");

    if (!inputFile) {
        printf("Could not open %s\n", ifilename);
        return 0;
    }
    if (!inputFile) {
        printf("Could not create %s\n", ofilename);
        return 0;
    }

    fseek(inputFile, 0, SEEK_END);
    size = ftell(inputFile);
    fseek(inputFile, 0, SEEK_SET);

    if (size <= 16) {
        printf("File too small!\n");
        return 0;
    }

    data = new unsigned char[size];

    fread(data, size, 1, inputFile);

    fclose(inputFile);

    if (decompress(data, size, &uncomp, &uncomp_size)) {
        retval = 1;
    }
    fwrite(uncomp, uncomp_size, 1, outputFile);

    fclose(outputFile);

    delete[] data;
    delete[] uncomp;

    return retval;
}

int main(int argc, char** argv) {
    if (argc == 2) {
        char name[128];
        strcat(name, argv[1]);
        strcat(name, ".dec");
        if (decompress_file(argv[1], name)) {
            printf("Extracted to %s\n", name);
            return 1;
        } else {
            printf("Extraction failed!\n");
            return 0;
        }
    }
    else if (argc == 3) {
        if (decompress_file(argv[1], argv[2])) {
            printf("Extracted to %s\n", argv[2]);
            return 1;
        }
        else {
            printf("Extraction failed!\n");
            return 0;
        }
    } else {
        printf("LZLR decompressor (Entergram games)\nUsage: %s inputfile <outputfile>\n", argv[0]);
        return 0;
    }
}
