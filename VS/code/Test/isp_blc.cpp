#include "isp_blc.h"

#include "common.h"


int IspBLC(TBLCParam tInputParams, unsigned short *pBuf)
{
    int Width = tInputParams.Width;
    int Height = tInputParams.Height;
    int ImgSize = tInputParams.Width * tInputParams.Height;

    unsigned short Domain = tInputParams.Domain;

    unsigned short BlockBlc[2][2] = { 0 };

    switch (tInputParams.Pattern)
    {
        case RGGB:
            BlockBlc[0][0] = tInputParams.R_blc;
            BlockBlc[0][1] = tInputParams.Gr_blc;
            BlockBlc[1][0] = tInputParams.Gb_blc;
            BlockBlc[1][1] = tInputParams.B_blc;
            printf_DEBUGMK("RGGB\n");
            break;

        case GRBG:
            BlockBlc[0][0] = tInputParams.Gr_blc;
            BlockBlc[0][1] = tInputParams.R_blc;
            BlockBlc[1][0] = tInputParams.B_blc;
            BlockBlc[1][1] = tInputParams.Gb_blc;
            printf_DEBUGMK("GRBG\n");
            break;

        case GBRG:
            BlockBlc[0][0] = tInputParams.Gb_blc;
            BlockBlc[0][1] = tInputParams.B_blc;
            BlockBlc[1][0] = tInputParams.R_blc;
            BlockBlc[1][1] = tInputParams.Gr_blc;
            printf_DEBUGMK("GBRG\n");
            break;

        case BGGR:
            BlockBlc[0][0] = tInputParams.B_blc;
            BlockBlc[0][1] = tInputParams.Gb_blc;
            BlockBlc[1][0] = tInputParams.Gr_blc;
            BlockBlc[1][1] = tInputParams.R_blc;
            printf_DEBUGMK("BGGR\n");
            break;

        default:
            printf_DEBUGMK("This pattern is illegal!\n");
            return FUNCTION_ERROR;
    }

    for (int row = 0; row < Height / 2; row++)
    {
        for (int col = 0; col < Width / 2; col++)
        {
            pBuf[row * 2 * Width + col * 2] = CLIP(unsigned short(pBuf[row * 2 * Width + col * 2] - BlockBlc[0][0]), 0, Domain);
            pBuf[row * 2 * Width + col * 2 + 1] = CLIP(unsigned short(pBuf[row * 2 * Width + col * 2 + 1] - BlockBlc[0][1]), 0, Domain);
            pBuf[(row * 2 + 1) * Width + col * 2] = CLIP(unsigned short(pBuf[(row * 2 + 1) * Width + col * 2] - BlockBlc[1][0]), 0, Domain);
            pBuf[(row * 2 + 1) * Width + col * 2 + 1] = CLIP(unsigned short(pBuf[(row * 2 + 1) * Width + col * 2 + 1] - BlockBlc[1][1]), 0, Domain);
        }
    }

    return FUNCTION_OK;
}
