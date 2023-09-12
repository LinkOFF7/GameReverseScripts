// Mortal Kombat Shaolin Monks GAMEDATA.WAD (PWF\x20)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define GET_BITS(number, offbits, nbits) (((number) >> (offbits)) & ((1 << (nbits)) - 1))

typedef struct{
	unsigned char 	signature[4];
	unsigned int 	virtualSize;
	unsigned int 	version;
	unsigned int 	files;
	unsigned int 	maxSize;
	unsigned int 	align;
	unsigned int 	zero1;
	unsigned int 	zero2;
} shaolin_header;

typedef struct{
	unsigned int 	offset;
	unsigned int 	value2;
	unsigned int 	size;
	unsigned int 	value4;
	unsigned int	flags;
} shaolin_entry;


int main(int argc, char** argv){
	shaolin_header	*header;
	shaolin_entry	*entries;
	FILE			*in;
	FILE			*log;
	char 			*header_buf;
	unsigned int	i;
	
	in = fopen(argv[1], "rb");
	log = fopen("log.txt", "w");
	if(!in){
		printf("File %s can't be opened.", argv[1]);
		return 0;
	};
	
	// read header
	header_buf = malloc(sizeof(shaolin_header));
	fread(header_buf, sizeof(shaolin_header), 1, in);
	header = (shaolin_header *)header_buf;
	if(memcmp(header->signature, "PWF ", 4)){
		printf("Unknown file signature.");
		return 0;
	}
	
	// read entries
	entries = malloc(header->files * sizeof(shaolin_entry));
	for(i = 0; i < header->files; i++){
		unsigned long long value;
		unsigned int off, v2, sz, v4, fl;
		
		fread(&value, 8, 1, in);
		off = GET_BITS(value, 0, 22);
		v2 = GET_BITS(value, 22, 2);
		sz = GET_BITS(value, 24, 20);
		v4 = GET_BITS(value, 44, 12);
		fl = GET_BITS(value, 56, 8);
		
		if(fl == 0x00){
			entries[i].offset = off;
			entries[i].value2 = -1;
			entries[i].size = sz;
			entries[i].value4 = 0xff;
			entries[i].flags = 0xff;
		} else {
			entries[i].offset = off * header->align;
			entries[i].value2 = v2;
			entries[i].size = sz * 4;
			entries[i].value4 = v4;
			entries[i].flags = fl;
		}
	}
	for(i = 0; i < header->files; i++){
		//printf("%06d: 0x%08x (0x%08x) (%i) (0x%06x) (0x%02x)\n", i, entries[i].offset, entries[i].size, entries[i].value2, entries[i].value4, entries[i].flags);
		fprintf(log, "%06d: 0x%08x (0x%08x) (%i) (0x%06x) (0x%02x)\n", i, entries[i].offset, entries[i].size, entries[i].value2, entries[i].value4, entries[i].flags);
	}
	
	fclose(in);
	fclose(log);
	free(header_buf);
	free(entries);
};
