#ifndef _ISP_ISP_GAIN_H_
#define _ISP_ISP_GAIN_H_


typedef struct tagIspGainParam
{
    int Width;
    int Height;

    double isp_gain;

    unsigned short Domain;
}TIspGainParam;


int IspIspGain(TIspGainParam tInputParams, unsigned short *pBuf);


#endif
