#include "isp_isp_gain.h"

#include "common.h"


int IspIspGain(TIspGainParam tInputParams, unsigned short *pBuf)
{
    int Width = tInputParams.Width;
    int Height = tInputParams.Height;
    int ImgSize = tInputParams.Width * tInputParams.Height;

    double isp_gain = tInputParams.isp_gain;
    unsigned short Domain = tInputParams.Domain;

    for (int row = 0; row < Height; row++)
    {
        for (int col = 0; col < Width; col++)
        {
            pBuf[row * Width + col] = CLIP(unsigned short(pBuf[row * Width + col] * isp_gain), 0, Domain);
        }
    }

    return FUNCTION_OK;
}
