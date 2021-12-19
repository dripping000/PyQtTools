#ifndef _ISP_CCM_
#define _ISP_CCM_


typedef struct tagCCMParam
{
    int Width;
    int Height;

    unsigned short Domain;
}TCCMParam;


int IspCCM(double(*ccm)[3], unsigned char sat_level, TCCMParam tInputParams, unsigned short* pBuf);


#endif
