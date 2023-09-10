// Mortal Kombat Shaolin Monks GAMEDATA.WAD (PWF\x20)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define getInt16High(n)(n & 0xffff)
#define getInt16Low(n)((n >> 16) & 0xffff)
#define getInt32High(n)(n & 0xffffffff)
#define getInt32Low(n)((n >> 32) & 0xffffffff)

unsigned getBits(unsigned value, unsigned offset, unsigned n)
{
	const unsigned max_n = CHAR_BIT * sizeof(unsigned);
	if (offset >= max_n)
		return 0;
	value >>= offset;
	if (n >= max_n)
		return value;
	const unsigned mask = (1u << n) - 1;
	return value & mask;
}

typedef struct{
	unsigned char 	magic[4];
	unsigned char 	unknown04[4];
	unsigned int 	  version;
	unsigned int 	  files;
	unsigned int 	  unknown10;
	unsigned int 	  align;
	unsigned int 	  unknown18;
	unsigned int 	  unknown1C;
} shaolin_header;

typedef struct{
	unsigned int   offset;
	unsigned int   size;
	char           flags;
	unsigned int   pos;
} shaolin_entry;


int main(int argc, char** argv){
	shaolin_header	  *header;
	shaolin_entry	    *entries;
	FILE			        *in;
	char 			        *header_buf;
	unsigned int	    size;
	unsigned int	    i;
	
	in = fopen(argv[1], "rb");
	if(!in){
		printf("File %s can't be opened.", argv[1]);
		return 0;
	};
	
	// read header
	header_buf = malloc(sizeof(shaolin_header));
	fread(header_buf, sizeof(shaolin_header), 1, in);
	header = (shaolin_header *)header_buf;
	if(memcmp(header->magic, "PWF ", 4)){
		printf("Unknown file signature.");
		return 0;
	}
	
	// read entries
	entries = malloc(header->files * sizeof(shaolin_entry));
	for(i = 0; i < header->files; i++){
		entries[i].pos = ftell(in);
		
		unsigned long long check;
		unsigned int off, sz;
		fread(&check, sizeof(long long), 1, in);
		off = getInt32High(check);
		sz = getInt32Low(check);
		if(off >> 24 == 0 && sz >> 24 == 0){
			entries[i].offset = off;
			entries[i].size = sz;
		} else {
			// bits according bms script
			unsigned offset = getBits(check, 0, 22);
			unsigned size = getBits(check, 24, 20);
			unsigned flags = getBits(check, 56, 8);
			
			entries[i].offset = offset * header->align;
			entries[i].size = size * 4;
			entries[i].flags = flags;
		}
			
	}
	for(i = 0; i < header->files; i++){
		if(entries[i].size != 0)
			printf("%06d: 0x%08x (0x%08x) (0x%01x) (0x%08x)\n", i, entries[i].offset, entries[i].size, entries[i].flags, entries[i].pos);
	}
	
	fclose(in);
	free(header_buf);
	free(entries);
};
