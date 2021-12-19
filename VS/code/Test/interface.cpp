#include "interface.h"


typedef struct tagStruct
{
    int width;
    int height;
    unsigned char* data;

}TStruct;


class Interface
{
public:
    int test(int width, int height, unsigned char* data);
    int test(TStruct* tStruct);

};


int Interface::test(int width, int height, unsigned char* data)
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = 0; k < 3; k++)
            {
                std::cout << (int)data[i*width * 3 + j * 3 + k] << std::endl;
            }
        }
    }

    return 0;
}


int Interface::test(TStruct* tStruct)
{
    for (int i = 0; i < tStruct->height; i++)
    {
        for (int j = 0; j < tStruct->width; j++)
        {
            for (int k = 0; k < 3; k++)
            {
                std::cout << (int)tStruct->data[i*tStruct->width * 3 + j * 3 + k] << std::endl;
            }
        }
    }

    return 0;
}


int uint16_rrrgggbbb2bgrbgrbgr(int width, int height, unsigned short *pBuf)
{
    unsigned short *u16Data = (unsigned short*)malloc(width * height * 3 * sizeof(unsigned short));
    memset(u16Data, 0, width * height * 3 * sizeof(unsigned short));
    memcpy(u16Data, pBuf, width * height * 3 * sizeof(unsigned short));

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            pBuf[i*width * 3 + j * 3 + 0] = u16Data[i*width + j + width*height * 2];  // b
            pBuf[i*width * 3 + j * 3 + 1] = u16Data[i*width + j + width*height];
            pBuf[i*width * 3 + j * 3 + 2] = u16Data[i*width + j];
        }
    }

    free(u16Data);
    u16Data = NULL;

    return 0;
}


int uint16_bgrbgrbgr2rrrgggbbb(int width, int height, unsigned short *pBuf)
{
    unsigned short *u16Data = (unsigned short*)malloc(width * height * 3 * sizeof(unsigned short));
    memset(u16Data, 0, width * height * 3 * sizeof(unsigned short));
    memcpy(u16Data, pBuf, width * height * 3 * sizeof(unsigned short));

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            pBuf[i*width + j + width*height * 2]        = u16Data[i*width * 3 + j * 3 + 0];  // b
            pBuf[i*width + j + width*height]            = u16Data[i*width * 3 + j * 3 + 1];
            pBuf[i*width + j]                           = u16Data[i*width * 3 + j * 3 + 2];
        }
    }

    free(u16Data);
    u16Data = NULL;

    return 0;
}


extern "C"
{
    Interface interface;
    DLLEXPORT int test(int width, int height, unsigned char* data)
    {
        return interface.test(width, height, data);
    }

    DLLEXPORT int test_struct(TStruct* tStruct)
    {
        return interface.test(tStruct);
    }


    DLLEXPORT int interface_BLC(TBLCParam tInputParams, unsigned short *pBuf)
    {
        return IspBLC(tInputParams, pBuf);
    }


    DLLEXPORT int interface_interpolation(TInterpolationParam tInputParams, unsigned short * pInputBuf, unsigned short *pOutputBuf)
    {
        int ret = 0;

        ret = IspInterpolation(tInputParams, pInputBuf, pOutputBuf);
        ret = uint16_rrrgggbbb2bgrbgrbgr(tInputParams.Width, tInputParams.Height, pOutputBuf);

        return ret;
    }


    DLLEXPORT int interface_AWB(TAWBParam tInputParams, unsigned short* pInputBuf, unsigned short* pOutputBuf)
    {
        int ret = 0;

        ret = uint16_bgrbgrbgr2rrrgggbbb(tInputParams.Width, tInputParams.Height, pInputBuf);
        ret = IspAWB(tInputParams, pInputBuf, pOutputBuf);
        ret = uint16_rrrgggbbb2bgrbgrbgr(tInputParams.Width, tInputParams.Height, pOutputBuf);

        return ret;
    }
}
