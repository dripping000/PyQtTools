#ifndef _ISP_BLC_H_
#define _ISP_BLC_H_


#include "isp_raw.h"


typedef struct tagBLCParam
{
    int Width;
    int Height;

    EBayerPatternType Pattern;

    unsigned short R_blc;
    unsigned short Gr_blc;
    unsigned short Gb_blc;
    unsigned short B_blc;

    unsigned short Domain;
}TBLCParam;


int IspBLC(TBLCParam tInputParams, unsigned short *pBuf);


#endif
