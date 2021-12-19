#include <iostream>

#include "interface.h"


int main()
{
    int ret = 0;

    char* filename = "./Resource/D50_HisiRAW_4096x2176_12bits_GBRG_Linear_20191018143802.raw";
    int nWidth = 4096;
    int nHeight = 2176;
    int nImgSize = nWidth * nHeight;

    FILE *pfData = NULL;
    pfData = fopen(filename, "rb");

    unsigned short* pu16RawData = (unsigned short *)malloc(nWidth * nHeight * sizeof(unsigned short));
    ret = fread(pu16RawData, sizeof(unsigned short), nWidth * nHeight, pfData);

    ret = OpenCVShow_unsigned_short(pu16RawData, nWidth, nHeight, 1);

    return 0;
}