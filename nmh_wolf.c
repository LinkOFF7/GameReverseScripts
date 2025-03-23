#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>

#define QUICK_PUTi32(X,Y)   (X)[0]=(Y);      (X)[1]= (Y)>> 8;    (X)[2]= (Y)>>16;     (X)[3]= (Y)>> 24;

int dewolf(unsigned char * src, int srclen, unsigned char * dest, int destlen, int set_ps) {
    unsigned char m;
    if(!set_ps) m = 0xff;
    else if(set_ps == 1) m = src[0];
    else m = src[8];
    int ps = set_ps, pd = 0;
    while(ps < srclen && pd < destlen)
    {
        //if(ps>=0x422)
        //    ps=ps;
        if(src[ps] == m)
        {
            ps++;
            if(src[ps] == m)
                dest[pd++] = src[ps++];
            else
            {
                if(src[ps] >= m)
                    src[ps]--;
                int pos = 0, len = (src[ps] >> 3) + 4;
                unsigned char type1 = src[ps++] & 7;
                unsigned char type2 = type1 >> 2;
                type1 &= 3;
                if(type2)
                    len += src[ps++] << 5;
 
                if(type1 == 0)
                    pos = src[ps++] + 1;
                else if(type1 == 1)
                {
                    pos = src[ps] + (src[ps + 1] << 8) + 1;
                    ps += 2;
                }
                else if(type1 == 2)
                {
                    pos = src[ps] + (src[ps + 1] << 8) + (src[ps + 2] << 16) + 1;
                    ps += 3;
                }
                else
                    type1 = type1;
 
                int k;
                for(k = 0; k < len; ++k)
                    dest[pd + k] = dest[pd - pos + k];
                pd += len;
            }
        }
        else
        {
            dest[pd++] = src[ps++];
        }
    }
    return(pd);
}

int dewolf_compress_fake(unsigned char *in, int insz, unsigned char *out) {
    unsigned char* inl = in + insz;
    unsigned char* o = out;

    unsigned char m = 0xff;
    o = out + 9;
    while (in < inl) {
        if (*in == m) {
            *o++ = m;
            *o++ = *in++;
        }
        else {
            *o++ = *in++;
        }
    }
    QUICK_PUTi32(out + 0, insz);
    QUICK_PUTi32(out + 4, o - out);
    out[8] = m;
    return o - out;
}

int main(int argc, char* argv[]){
    FILE* fp;
    unsigned char* cmp;
    unsigned char* dec;
    int size, zsize, r;

    if (argc != 4){
        printf("WOLF Decompression/Fake compression Tool.\n");
        printf("Usage: %s [-d/-c] <input file path> <output file path>\n", argv[0]);
        return 0;
    }
    if (!memcmp(argv[1], "-d", 2)) {
        fp = fopen(argv[2], "rb");

        if (!fp) return(-1);

        fread(&size, sizeof(int), 1, fp);
        fread(&zsize, sizeof(int), 1, fp);
        zsize -= 8;

        cmp = (unsigned char*)malloc(zsize);
        fread(cmp, zsize, 1, fp);
        fclose(fp);

        dec = (unsigned char*)malloc(size);

        printf("Decompressing %s\n", argv[2]);

        if (r = dewolf(cmp, zsize, dec, size, 1) != size) {
            printf("Decompression error: %d\n", r);
        }
        else {
            printf("Decompressed to %s\n", argv[3]);
            fp = fopen(argv[3], "wb");
            if (!fp) return(-1);
            fwrite(dec, size, 1, fp);
            fclose(fp);
        }
    }
    else if(!memcmp(argv[1], "-c", 2)){
        fp = fopen(argv[2], "rb");

        if (!fp) return(-1);

        fseek(fp, 0, SEEK_END);
        size = ftell(fp);
        fseek(fp, 0, SEEK_SET);

        dec = (unsigned char*)malloc(size);
        fread(dec, size, 1, fp);
        fclose(fp);

        cmp = (unsigned char*)malloc(size * 2);

        
        if (zsize = dewolf_compress_fake(dec, size, cmp)) {
            printf("Saved to %s\n", argv[3]);
            fp = fopen(argv[3], "wb");
            if (!fp) return(-1);
            fwrite(cmp, zsize, 1, fp);
            fclose(fp);
        }
        else {
            printf("dewolf_compress_fake returns error %d.\n", zsize);
        }
        
    }

    free(cmp);
    free(dec);
    return 0;
}