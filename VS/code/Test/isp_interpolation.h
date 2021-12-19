#ifndef _ISP_INTERPOLATION_
#define _ISP_INTERPOLATION_


#include "isp_raw.h"


typedef struct tagInterpolationParam
{
    int Width;
    int Height;

    EBayerPatternType Pattern;

    unsigned short Domain;
}TInterpolationParam;


int IspInterpolation(TInterpolationParam tInputParams, unsigned short * pInputBuf, unsigned short *pOutputBuf);


#endif
