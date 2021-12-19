#ifndef _ISP_AWB_
#define _ISP_AWB_


typedef struct tagAWBParam
{
    int Width;
    int Height;

    double RGain;
    double BGain;

    unsigned short Domain;
}TAWBParam;


int IspAWB(TAWBParam tInputParams, unsigned short* pInputBuf, unsigned short* pOutputBuf);


#endif
