#include "isp_awb.h"

#include "common.h"


int IspAWB(TAWBParam tInputParams, unsigned short* pInputBuf, unsigned short* pOutputBuf)
{
    int Width = tInputParams.Width;
    int Height = tInputParams.Height;
    int ImgSize = Width * Height;

    double RG = tInputParams.RGain;
    double BG = tInputParams.BGain;

    unsigned short Domain = tInputParams.Domain;

    float sum_R = 0.0, sum_G = 0.0, sum_B = 0.0;
    float RG_cal = 0.0, BG_cal = 0.0;
    for (int i = 0; i < Height; i = i + 1)
    {
        for (int j = 0; j < Width; j = j + 1)
        {
            sum_R += 1.0f * pInputBuf[i * Width + j] / ImgSize;
            sum_G += 1.0f * pInputBuf[i * Width + j + ImgSize * 1] / ImgSize;
            sum_B += 1.0f * pInputBuf[i * Width + j + ImgSize * 2] / ImgSize;
        }
    }

    RG_cal = sum_R / sum_G;
    BG_cal = sum_B / sum_G;
    printf_DEBUGMK("[awb] GR_cal:%f; GB_cal:%f\n", RG_cal, BG_cal);
    printf_DEBUGMK("[awb] GR:%f; GB:%f\n", RG, BG);
    //RG = RG_cal;
    //BG = BG_cal;

    //double blc_com = 4095.0 / (4095 - blc);
    double blc_com = 4095.0 / 4095;

    for (int i = 0; i < Height; i = i + 1)
    {
        for (int j = 0; j < Width; j = j + 1)
        {
            pOutputBuf[i * Width + j] = CLIP(unsigned short(round(pInputBuf[i * Width + j] / RG * blc_com)), 0, Domain);
            pOutputBuf[i * Width + j + ImgSize * 1] = CLIP(unsigned short(round(pInputBuf[i * Width + j + ImgSize * 1] * blc_com)), 0, Domain);
            pOutputBuf[i * Width + j + ImgSize * 2] = CLIP(unsigned short(round(pInputBuf[i * Width + j + ImgSize * 2] / BG * blc_com)), 0, Domain);
        }
    }

    return FUNCTION_OK;
}
