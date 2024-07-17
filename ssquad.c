#include <stdio.h>
#include <string.h>
#include <malloc.h>

int xor(unsigned char* data, unsigned int datasize, unsigned char* key, unsigned int keysize) {
  if (datasize <= keysize) return -1;
	unsigned int i, k;
	for (i = 0; i < datasize; i) {
		if(i + keysize > datasize)
			keysize = datasize - i;
		for (k = 0; k < keysize; k++) {
			data[i++] ^= key[k];
		}
	}
	return 1;
}

int main(int argc, char** argv) {
	if (argc == 1 || argc > 2) {
		// usage
		printf("Suicide Squad JSON string crypt tool by LinkOFF.\nUsage: Drag JSON file to decrypt/encrypt it.\n");
		return -1;
	}
	char key[] = {0x29, 0x98, 0xCA, 0xD2, 0x31, 0x6A, 0x67, 0x7D, 0x7A, 0x39, 0x6E, 0x39, 0x99, 0x25};
	FILE* inputFile;
	FILE* out;
	unsigned char* data;
	unsigned int size;

	inputFile = fopen(argc == 1 ? argv[0] : argv[1], "rb");
	if (!inputFile) {
		printf("Could not open %s\n", argv[1]);
		return -2;
	}

	fseek(inputFile, 0, SEEK_END);
	size = ftell(inputFile);
	fseek(inputFile, 0, SEEK_SET);

	data = malloc(size);
	if (!data) {
		printf("malloc error\n");
		return -3;
	}
	fread(data, size, 1, inputFile);
	fclose(inputFile);

	if (!xor(data, size, key, 14)) {
		printf("Decrypting failed.\n");
		return -4;
	}

	out = fopen(argc == 1 ? argv[0] : argv[1], "wb");
	if (!out) {
		printf("Could not open\n");
		return -5;
	}
	fwrite(data, size, 1, out);

	fclose(out);
	free(data);

	printf("Saved to %s\n", argc == 1 ? argv[0] : argv[1]);
}
