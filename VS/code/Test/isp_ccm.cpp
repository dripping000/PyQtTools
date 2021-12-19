#include "isp_ccm.h"

#include "common.h"


double Saturation[10][9] =
{
    { 0.3008,   0.5859,   0.1133,   0.2969,   0.5898,   0.1133,   0.2969,   0.5859,   0.1172 },  // level 1
    { 0.4727,   0.4414,   0.0859,   0.2227,   0.6914,   0.0859,   0.2227,   0.4414,   0.3359 },  // level 2
    { 0.6484,   0.2930,   0.0586,   0.1484,   0.7930,   0.0586,   0.1484,   0.2930,   0.5586 },  // level 3
    { 0.8242,   0.1484,   0.0273,   0.0742,   0.8984,   0.0273,   0.0742,   0.1484,   0.7773 },  // level 4
    { 1.0000,   0.0000,   0.0000,   0.0000,   1.0000,   0.0000,   0.0000,   0.0000,   1.0000 },  // level 5
    { 1.1641,  -0.1406,  -0.0234,  -0.0703,   1.0938,  -0.0234,  -0.0703,  -0.1406,   1.2109 },  // level 6
    { 1.2539,  -0.2148,  -0.0391,  -0.1055,   1.1445,  -0.0391,  -0.1055,  -0.2148,   1.3203 },  // level 7
    { 1.4297,  -0.3633,  -0.0664,  -0.1797,   1.2461,  -0.0664,  -0.1797,  -0.3633,   1.5430 },  // level 8
    { 1.5156,  -0.4336,  -0.0820,  -0.2188,   1.3008,  -0.0820,  -0.2188,  -0.4336,   1.6523 },  // level 9
    { 1.6875,  -0.5781,  -0.1094,  -0.2891,   1.3984,  -0.1094,  -0.2891,  -0.5781,   1.8672 }   // level 10
};


int IspCCM(double(*ccm)[3], unsigned char sat_level, TCCMParam tInputParams, unsigned short* pBuf)
{
    int Width = tInputParams.Width;
    int Height = tInputParams.Height;
    int ImgSize = Width * Height;

    double r, g, b;
    double ccm_re[3][3] = { 0 };

    double ccm_sat[9] = { 0 };
    memcpy(ccm_sat, Saturation[sat_level - 1], sizeof(double)*(9));

    ccm_re[0][0] = ccm[0][0] * ccm_sat[0] + ccm[0][1] * ccm_sat[3] + ccm[0][2] * ccm_sat[6];
    ccm_re[0][1] = ccm[0][0] * ccm_sat[1] + ccm[0][1] * ccm_sat[4] + ccm[0][2] * ccm_sat[7];
    ccm_re[0][2] = ccm[0][0] * ccm_sat[2] + ccm[0][1] * ccm_sat[5] + ccm[0][2] * ccm_sat[8];
    ccm_re[1][0] = ccm[1][0] * ccm_sat[0] + ccm[1][1] * ccm_sat[3] + ccm[1][2] * ccm_sat[6];
    ccm_re[1][1] = ccm[1][0] * ccm_sat[1] + ccm[1][1] * ccm_sat[4] + ccm[1][2] * ccm_sat[7];
    ccm_re[1][2] = ccm[1][0] * ccm_sat[2] + ccm[1][1] * ccm_sat[5] + ccm[1][2] * ccm_sat[8];
    ccm_re[2][0] = ccm[2][0] * ccm_sat[0] + ccm[2][1] * ccm_sat[3] + ccm[2][2] * ccm_sat[6];
    ccm_re[2][1] = ccm[2][0] * ccm_sat[1] + ccm[2][1] * ccm_sat[4] + ccm[2][2] * ccm_sat[7];
    ccm_re[2][2] = ccm[2][0] * ccm_sat[2] + ccm[2][1] * ccm_sat[5] + ccm[2][2] * ccm_sat[8];


    for (int i = 0; i < Height; i++)
    {
        for (int j = 0; j < Width; j++)
        {
            r = pBuf[i * Width + j] * ccm_re[0][0] + pBuf[i * Width + j + ImgSize] * ccm_re[0][1] + pBuf[i * Width + j + 2 * ImgSize] * ccm_re[0][2];
            g = pBuf[i * Width + j] * ccm_re[1][0] + pBuf[i * Width + j + ImgSize] * ccm_re[1][1] + pBuf[i * Width + j + 2 * ImgSize] * ccm_re[1][2];
            b = pBuf[i * Width + j] * ccm_re[2][0] + pBuf[i * Width + j + ImgSize] * ccm_re[2][1] + pBuf[i * Width + j + 2 * ImgSize] * ccm_re[2][2];

            pBuf[i * Width + j] = (unsigned short)CLIP_12bit(round(r));
            pBuf[i * Width + j + 1 * ImgSize] = (unsigned short)CLIP_12bit(round(g));
            pBuf[i * Width + j + 2 * ImgSize] = (unsigned short)CLIP_12bit(round(b));
        }
    }

    return FUNCTION_OK;
}
