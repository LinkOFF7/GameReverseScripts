#include <cstdio>
#include <stdlib.h>

// sub_1402F2890 (Journey.exe)
int main(int argc, char** argv) {
	if (argc != 3) {
		printf("Journey XMB to XML decrypt\n");
		printf("Usage: program.exe Strings.xme Strings.xml\n");
		return(0);
	}
	FILE* fl;
	int* buf;
	size_t size; // always 32-bit aligned because of int xor key
	int i, c;
	int key = 0x6341F337;

	fl = fopen(argv[1], "rb");
	if (!fl) return (-1);
	fseek(fl, 0, SEEK_END);
	size = ftell(fl);
	fseek(fl, 0, SEEK_SET);
	
	buf = (int*)malloc(size);
	if (!buf) return (-2);
	fread(buf, size, 1, fl);
	fclose(fl);

	for (i = 0; i < size / sizeof(int); i++) {
		c = buf[i];
		buf[i] ^= key;
		key += c;
	}

	fl = fopen(argv[2], "wb");
	if (!fl) return (-1);
	fwrite(buf, size, 1, fl);
	fclose(fl);
	free(buf);

	return 0;
}
