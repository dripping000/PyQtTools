#include "isp_interpolation.h"

#include "common.h"


int IspInterpolation(TInterpolationParam tInputParams, unsigned short * pInputBuf, unsigned short *pOutputBuf)
{
    int Width = tInputParams.Width;
    int Height = tInputParams.Height;
    int ImgSize = Height * Width;

    int pattern = tInputParams.Pattern;

    unsigned short *RChannel = (unsigned short *)malloc(ImgSize * sizeof(unsigned short));
    unsigned short *GChannel = (unsigned short *)malloc(ImgSize * sizeof(unsigned short));
    unsigned short *BChannel = (unsigned short *)malloc(ImgSize * sizeof(unsigned short));
    memset(RChannel, 0, ImgSize * sizeof(unsigned short));
    memset(GChannel, 0, ImgSize * sizeof(unsigned short));
    memset(BChannel, 0, ImgSize * sizeof(unsigned short));

    if (pattern == GBRG)
    {
        //G interpolation

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }


                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                //recover G in B
                unsigned short V = abs(pInputBuf[top * Width + j * 2 + 1] - pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2 + 1] - pInputBuf[top_2 * Width + j * 2 + 1] - pInputBuf[bot * Width + j * 2 + 1]);

                unsigned short H = abs(pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[(i * 2) * Width + rig]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2 + 1] - pInputBuf[(i * 2) * Width + lef] - pInputBuf[(i * 2) * Width + rig_2]);



                if (V > H)
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[top * Width + j * 2 + 1] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig] + pInputBuf[top * Width + j * 2 + 1] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 4.0));
                }

                //recover G in R
                V = abs(pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[bot * Width + j * 2]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[top * Width + j * 2] - pInputBuf[bot_2 * Width + j * 2]);

                H = abs(pInputBuf[(i * 2 + 1) * Width + lef] - pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[(i * 2 + 1) * Width + lef_2] - pInputBuf[(i * 2 + 1) * Width + rig]);


                if (V > H)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[bot * Width + j * 2]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] + pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[bot * Width + j * 2]) / 4.0));
                }




                GChannel[(i * 2) * Width + j * 2] = pInputBuf[(i * 2) * Width + j * 2];
                GChannel[(i * 2 + 1) * Width + j * 2 + 1] = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];
                //GChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)(pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig] + pInputBuf[top * Width + j * 2 + 1] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 4;
                //GChannel[(i * 2 + 1) * Width + j * 2] = (unsigned short)(pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] + pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[bot * Width + j * 2]) / 4;

            }
        }

        //recover R in G

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2 - 1;
                int bot = i * 2 + 1;
                int lef = j * 2;
                int rig = j * 2 + 2;

                if (top < 0)
                {
                    top = 1;
                }
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }


                //recover R in G
                RChannel[(i * 2) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[top * Width + j * 2] + pInputBuf[bot * Width + j * 2]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(top_G)* Width + j * 2]) / 4.0));

                //RChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)(pInputBuf[top * Width + lef] + pInputBuf[top * Width + rig] + pInputBuf[bot * Width + lef] + pInputBuf[bot * Width + rig]) / 4;
                RChannel[(i * 2 + 1) * Width + j * 2] = pInputBuf[(i * 2 + 1) * Width + j * 2];

                RChannel[(i * 2 + 1) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + rig]) / 2.0 +
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2 + 1) * Width + rig_G]) / 4.0));



            }
        }



        //recover B in G 
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2;
                int bot = i * 2 + 2;
                int lef = j * 2 - 1;
                int rig = j * 2 + 1;

                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }

                BChannel[(i * 2) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(i * 2) * Width + lef_G] - GChannel[(i * 2) * Width + j * 2 + 1]) / 4.0));



                BChannel[(i * 2) * Width + j * 2 + 1] = pInputBuf[(i * 2) * Width + j * 2 + 1];

                BChannel[(i * 2 + 1) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2 + 1] + pInputBuf[bot * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(bot_G)* Width + j * 2 + 1]) / 4.0));
            }
        }


        //recover B in R
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2;
                int bot = i * 2 + 2;
                int lef = j * 2 - 1;
                int rig = j * 2 + 1;

                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                unsigned short B00 = pInputBuf[top * Width + lef];
                unsigned short B01 = pInputBuf[top * Width + rig];
                unsigned short B10 = pInputBuf[bot * Width + lef];
                unsigned short B11 = pInputBuf[bot * Width + rig];

                unsigned short D45 = abs(B01 - B10) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(bot_G)* Width + lef_G]);
                unsigned short D135 = abs(B00 - B11) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + lef_G] - GChannel[(bot_G)* Width + rig]);


                if (D45 > D135)
                {
                    BChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((B00 + B11) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + lef_G] - GChannel[(bot_G)* Width + rig]) / 4.0));
                }
                else if (D45 < D135)
                {
                    BChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((B01 + B10) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(bot_G)* Width + lef_G]) / 4.0));
                }
                else
                {
                    BChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((B00 + B11 + B01 + B10) / 4.0 + (4 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + lef_G] - GChannel[(bot_G)* Width + rig] - GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(bot_G)* Width + lef_G]) / 8.0));
                }


            }
        }

        //recover R in B
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2 - 1;
                int bot = i * 2 + 1;
                int lef = j * 2;
                int rig = j * 2 + 2;

                if (top < 0)
                {
                    top = 1;
                }
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }
                unsigned short R00 = pInputBuf[top * Width + lef];
                unsigned short R01 = pInputBuf[top * Width + rig];
                unsigned short R10 = pInputBuf[bot * Width + lef];
                unsigned short R11 = pInputBuf[bot * Width + rig];

                unsigned short D45 = abs(R01 - R10) + abs(2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + rig_G] - GChannel[(bot)* Width + lef]);
                unsigned short D135 = abs(R00 - R11) + abs(2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + lef] - GChannel[(bot)* Width + rig_G]);

                if (D45 > D135)
                {
                    RChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((R00 + R11) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + lef] - GChannel[(bot)* Width + rig_G]) / 4.0));
                }
                else if (D45 < D135)
                {
                    RChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((R01 + R10) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + rig_G] - GChannel[(bot)* Width + lef]) / 4.0));
                }
                else
                {
                    RChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((R01 + R10 + R00 + R11) / 4.0 + (4 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + rig_G] - GChannel[(bot)* Width + lef] - GChannel[(top_G)* Width + lef] - GChannel[(bot)* Width + rig_G]) / 8.0));

                }

            }
        }

    }
    else if (pattern == RGGB)
    {
        // G interpolation
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {
                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }

                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }

                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }

                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }

                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }

                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }

                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }

                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                // recover G in B
                unsigned short V = abs(pInputBuf[(i * 2) * Width + j * 2 + 1] - pInputBuf[(bot)* Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] - pInputBuf[top * Width + j * 2 + 1] - pInputBuf[bot_2 * Width + j * 2 + 1]);

                unsigned short H = abs(pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[(i * 2 + 1) * Width + rig]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] - pInputBuf[(i * 2 + 1) * Width + lef] - pInputBuf[(i * 2 + 1) * Width + rig_2]);

                if (V > H)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + rig]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2 + 1] + pInputBuf[(bot)* Width + j * 2 + 1]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + rig] + pInputBuf[(i * 2) * Width + j * 2 + 1] + pInputBuf[(bot)* Width + j * 2 + 1]) / 4.0));
                }

                // recover G in R
                V = abs(pInputBuf[(top)* Width + j * 2] - pInputBuf[(i * 2 + 1) * Width + j * 2]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[top_2 * Width + j * 2] - pInputBuf[bot * Width + j * 2]);

                H = abs(pInputBuf[(i * 2) * Width + lef] - pInputBuf[(i * 2) * Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[(i * 2) * Width + lef_2] - pInputBuf[(i * 2) * Width + rig]);

                if (V > H)
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + j * 2 + 1]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(top)* Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + j * 2]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + j * 2 + 1] + pInputBuf[(top)* Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + j * 2]) / 4.0));
                }

                GChannel[(i * 2) * Width + j * 2 + 1] = pInputBuf[(i * 2) * Width + j * 2 + 1];
                GChannel[(i * 2 + 1) * Width + j * 2] = pInputBuf[(i * 2 + 1) * Width + j * 2];
            }
        }

        // recover R in G
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {
                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }

                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }

                int lef = j * 2;

                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }

                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }

                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }

                RChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(i * 2) * Width + j * 2] - GChannel[(i * 2)* Width + rig_G]) / 4.0));
                RChannel[(i * 2) * Width + j * 2] = pInputBuf[(i * 2) * Width + j * 2];
                RChannel[(i * 2 + 1) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(bot)* Width + j * 2]) / 2.0 +
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2) * Width + j * 2] - GChannel[(bot_G)* Width + j * 2]) / 4.0));
            }
        }

        // recover B in G
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {
                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }

                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }

                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }

                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }

                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }

                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }

                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }

                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }

                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }

                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }

                BChannel[(i * 2 + 1) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2 + 1) * Width + lef_G] - GChannel[(i * 2 + 1) * Width + j * 2 + 1]) / 4.0));
                BChannel[(i * 2 + 1) * Width + j * 2 + 1] = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];
                BChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(top)* Width + j * 2 + 1] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));
            }
        }

        // recover B in R
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {
                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }

                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }

                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }

                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }

                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }

                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }

                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }

                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }

                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }

                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }

                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }

                unsigned short B00 = pInputBuf[top * Width + lef];
                unsigned short B01 = pInputBuf[top * Width + j * 2 + 1];
                unsigned short B10 = pInputBuf[(i * 2 + 1) * Width + lef];
                unsigned short B11 = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];

                unsigned short D45 = abs(B01 - B10) + abs(2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + lef_G]);
                unsigned short D135 = abs(B00 - B11) + abs(2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + lef_G] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]);

                if (D45 > D135)
                {
                    BChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((B00 + B11) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + lef_G] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));
                }
                else if (D45 < D135)
                {
                    BChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((B01 + B10) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + lef_G]) / 4.0));
                }
                else
                {
                    BChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((B00 + B11 + B01 + B10) / 4.0 + (4 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + lef_G] - GChannel[(i * 2 + 1)* Width + j * 2 + 1] -
                        GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + lef_G]) / 8.0));
                }
            }
        }

        // recover R in B
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {
                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }

                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }

                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }

                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }

                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }

                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }

                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }

                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }

                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }

                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }

                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }

                unsigned short R00 = pInputBuf[(i * 2) * Width + (j * 2)];
                unsigned short R01 = pInputBuf[(i * 2) * Width + rig];
                unsigned short R10 = pInputBuf[bot * Width + (j * 2)];
                unsigned short R11 = pInputBuf[bot * Width + rig];

                unsigned short D45 = abs(R01 - R10) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + (j * 2)]);
                unsigned short D135 = abs(R00 - R11) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + (j * 2)] - GChannel[(bot_G)* Width + rig_G]);

                if (D45 > D135)
                {
                    RChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((R00 + R11) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + (j * 2)] - GChannel[(bot_G)* Width + rig_G]) / 4.0));
                }
                else if (D45 < D135)
                {
                    RChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((R01 + R10) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + (j * 2)]) / 4.0));
                }
                else
                {
                    RChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((R01 + R10 + R00 + R11) / 4.0 + (4 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + (j * 2)] - GChannel[(bot_G)* Width + rig_G] -
                        GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + (j * 2)]) / 8.0));
                }
            }
        }

    }
    else if (pattern == BGGR)
    {
        //G interpolation

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }

                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                //recover G in B
                unsigned short V = abs(pInputBuf[(top)* Width + j * 2] - pInputBuf[(i * 2 + 1)* Width + j * 2]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[top_2 * Width + j * 2] - pInputBuf[bot * Width + j * 2]);

                unsigned short H = abs(pInputBuf[(i * 2) * Width + lef] - pInputBuf[(i * 2) * Width + (j * 2 + 1)]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[(i * 2) * Width + lef_2] - pInputBuf[(i * 2) * Width + rig]);

                if (V > H)
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + (j * 2 + 1)]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(top)* Width + j * 2] + pInputBuf[(i * 2 + 1)* Width + j * 2]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + (j * 2 + 1)] + pInputBuf[(top)* Width + j * 2] + pInputBuf[(i * 2 + 1)* Width + j * 2]) / 4.0));
                }

                //recover G in R
                V = abs(pInputBuf[(i * 2)* Width + j * 2 + 1] - pInputBuf[(bot)* Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] - pInputBuf[top * Width + j * 2 + 1] - pInputBuf[bot_2 * Width + j * 2 + 1]);

                H = abs(pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[(i * 2 + 1) * Width + rig]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2 + 1] - pInputBuf[(i * 2 + 1) * Width + lef] - pInputBuf[(i * 2 + 1) * Width + rig_2]);


                if (V > H)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + rig]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2)* Width + j * 2 + 1] + pInputBuf[(bot)* Width + j * 2 + 1]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + rig] + pInputBuf[(i * 2)* Width + j * 2 + 1] + pInputBuf[(bot)* Width + j * 2 + 1]) / 4.0));
                }

                GChannel[(i * 2) * Width + j * 2 + 1] = pInputBuf[(i * 2) * Width + j * 2 + 1];
                GChannel[(i * 2 + 1) * Width + j * 2] = pInputBuf[(i * 2 + 1) * Width + j * 2];


            }
        }

        //recover R in G

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2 - 1;
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;

                if (top < 0)
                {
                    top = 1;
                }
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }


                RChannel[(i * 2 + 1) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2 + 1) * Width + lef_G] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));

                RChannel[(i * 2 + 1) * Width + j * 2 + 1] = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];

                RChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(top)* Width + j * 2 + 1] + pInputBuf[(i * 2 + 1)* Width + j * 2 + 1]) / 2.0 +
                    (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));



            }
        }



        //recover B in G 
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }


                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }



                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }

                BChannel[(i * 2) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(i * 2) * Width + j * 2] - GChannel[(i * 2) * Width + rig_G]) / 4.0));


                BChannel[(i * 2) * Width + j * 2] = pInputBuf[(i * 2) * Width + j * 2];

                BChannel[(i * 2 + 1) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2)* Width + j * 2] + pInputBuf[(bot)* Width + j * 2]) / 2.0 + \
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + j * 2] - GChannel[(bot_G)* Width + j * 2]) / 4.0));
            }
        }


        //recover B in R
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }
                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }


                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }


                unsigned short B00 = pInputBuf[(i * 2) * Width + j * 2];
                unsigned short B01 = pInputBuf[(i * 2) * Width + rig];
                unsigned short B10 = pInputBuf[(bot)* Width + j * 2];
                unsigned short B11 = pInputBuf[(bot)* Width + rig];

                unsigned short D45 = abs(B01 - B10) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + j * 2]);
                unsigned short D135 = abs(B00 - B11) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + j * 2] - GChannel[(bot_G)* Width + rig_G]);


                if (D45 > D135)
                {
                    BChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((B00 + B11) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + j * 2] - GChannel[(bot_G)* Width + rig_G]) / 4.0));
                }
                else if (D45 < D135)
                {
                    BChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((B01 + B10) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + j * 2]) / 4.0));
                }
                else
                {
                    BChannel[(i * 2 + 1) * Width + j * 2 + 1] = CLIP_12bit(round((B00 + B11 + B01 + B10) / 4.0 + (4 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + j * 2] - GChannel[(bot_G)* Width + rig_G] -
                        GChannel[(i * 2)* Width + rig_G] - GChannel[(bot_G)* Width + j * 2]) / 8.0));
                }


            }
        }

        //recover R in B
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }
                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }


                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }
                unsigned short R00 = pInputBuf[(top)* Width + (lef)];
                unsigned short R01 = pInputBuf[(top)* Width + j * 2 + 1];
                unsigned short R10 = pInputBuf[(i * 2 + 1) * Width + (lef)];
                unsigned short R11 = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];

                unsigned short D45 = abs(R01 - R10) + abs(2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + (lef_G)]);
                unsigned short D135 = abs(R00 - R11) + abs(2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + (lef_G)] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]);

                if (D45 > D135)
                {
                    RChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((R00 + R11) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + (lef_G)] - GChannel[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));
                }
                else if (D45 < D135)
                {
                    RChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((R01 + R10) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + (lef_G)]) / 4.0));
                }
                else
                {
                    RChannel[(i * 2) * Width + j * 2] = CLIP_12bit(round((R01 + R10 + R00 + R11) / 4.0 + (4 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + (lef_G)] - GChannel[(i * 2 + 1)* Width + j * 2 + 1] -
                        GChannel[(top_G)* Width + j * 2 + 1] - GChannel[(i * 2 + 1)* Width + (lef_G)]) / 8.0));

                }

            }
        }


    }
    else if (pattern == GRBG)
    {
        //G interpolation

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }


                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                //recover G in B
                unsigned short V = abs(pInputBuf[(i * 2)* Width + j * 2] - pInputBuf[(bot)* Width + j * 2]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[top * Width + j * 2] - pInputBuf[bot_2 * Width + j * 2]);

                unsigned short H = abs(pInputBuf[(i * 2 + 1) * Width + lef] - pInputBuf[(i * 2 + 1) * Width + (j * 2 + 1)]) + \
                    abs(2 * pInputBuf[(i * 2 + 1) * Width + j * 2] - pInputBuf[(i * 2 + 1) * Width + lef_2] - pInputBuf[(i * 2 + 1) * Width + rig]);



                if (V > H)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + (j * 2 + 1)]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2)* Width + j * 2] + pInputBuf[(bot)* Width + j * 2]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + lef] + pInputBuf[(i * 2 + 1) * Width + (j * 2 + 1)] + pInputBuf[(i * 2)* Width + j * 2] + pInputBuf[(bot)* Width + j * 2]) / 4.0));
                }

                //recover G in R
                V = abs(pInputBuf[(top)* Width + j * 2 + 1] - pInputBuf[(i * 2 + 1)* Width + j * 2 + 1]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2 + 1] - pInputBuf[top_2 * Width + j * 2 + 1] - pInputBuf[bot * Width + j * 2 + 1]);

                H = abs(pInputBuf[(i * 2) * Width + j * 2] - pInputBuf[(i * 2) * Width + rig]) + \
                    abs(2 * pInputBuf[(i * 2) * Width + j * 2 + 1] - pInputBuf[(i * 2) * Width + lef] - pInputBuf[(i * 2) * Width + rig_2]);


                if (V > H)
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig]) / 2.0));
                }
                else if (H > V)
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(top)* Width + j * 2 + 1] + pInputBuf[(i * 2 + 1)* Width + j * 2 + 1]) / 2.0));
                }
                else
                {
                    GChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((pInputBuf[(i * 2) * Width + j * 2] + pInputBuf[(i * 2) * Width + rig] + pInputBuf[(top)* Width + j * 2 + 1] + pInputBuf[(i * 2 + 1)* Width + j * 2 + 1]) / 4.0));
                }

                GChannel[(i * 2) * Width + j * 2] = pInputBuf[(i * 2) * Width + j * 2];
                GChannel[(i * 2 + 1) * Width + j * 2 + 1] = pInputBuf[(i * 2 + 1) * Width + j * 2 + 1];


            }
        }

        //recover R in G

        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top = i * 2 - 1;
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;

                if (top < 0)
                {
                    top = 1;
                }
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }

                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }

                //recover R in G
                RChannel[(i * 2) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2) * Width + lef] + pInputBuf[(i * 2) * Width + j * 2 + 1]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(i * 2) * Width + lef_G] - GChannel[(i * 2)* Width + j * 2 + 1]) / 4.0));

                RChannel[(i * 2) * Width + j * 2 + 1] = pInputBuf[(i * 2) * Width + j * 2 + 1];

                RChannel[(i * 2 + 1) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2)* Width + j * 2 + 1] + pInputBuf[(bot)* Width + j * 2 + 1]) / 2.0 +
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2)* Width + j * 2 + 1] - GChannel[(bot_G)* Width + j * 2 + 1]) / 4.0));



            }
        }



        //recover B in G 
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }


                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }



                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }

                BChannel[(i * 2 + 1) * Width + j * 2 + 1] = (unsigned short)CLIP_12bit(round((pInputBuf[(i * 2 + 1) * Width + j * 2] + pInputBuf[(i * 2 + 1) * Width + rig]) / 2.0 + \
                    (2 * GChannel[(i * 2 + 1) * Width + j * 2 + 1] - GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2 + 1) * Width + rig_G]) / 4.0));


                BChannel[(i * 2 + 1) * Width + j * 2] = pInputBuf[(i * 2 + 1) * Width + j * 2];

                BChannel[(i * 2) * Width + j * 2] = (unsigned short)CLIP_12bit(round((pInputBuf[(top)* Width + j * 2] + pInputBuf[(i * 2 + 1)* Width + j * 2]) / 2.0 + \
                    (2 * GChannel[(i * 2) * Width + j * 2] - GChannel[(top_G)* Width + j * 2] - GChannel[(i * 2 + 1)* Width + j * 2]) / 4.0));
            }
        }


        //recover B in R
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }
                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }


                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }


                unsigned short B00 = pInputBuf[(top)* Width + j * 2];
                unsigned short B01 = pInputBuf[(top)* Width + rig];
                unsigned short B10 = pInputBuf[(i * 2 + 1)* Width + j * 2];
                unsigned short B11 = pInputBuf[(i * 2 + 1)* Width + rig];

                unsigned short D45 = abs(B01 - B10) + abs(2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + rig_G] - GChannel[(i * 2 + 1)* Width + j * 2]);
                unsigned short D135 = abs(B00 - B11) + abs(2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + j * 2] - GChannel[(i * 2 + 1)* Width + rig_G]);


                if (D45 > D135)
                {
                    BChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((B00 + B11) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + j * 2] - GChannel[(i * 2 + 1)* Width + rig_G]) / 4.0));
                }
                else if (D45 < D135)
                {
                    BChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((B01 + B10) / 2.0 + (2 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + rig_G] - GChannel[(i * 2 + 1)* Width + j * 2]) / 4.0));
                }
                else
                {
                    BChannel[(i * 2) * Width + j * 2 + 1] = CLIP_12bit(round((B00 + B11 + B01 + B10) / 4.0 + (4 * GChannel[(i * 2) * Width + j * 2 + 1] - GChannel[(top_G)* Width + j * 2] - GChannel[(i * 2 + 1)* Width + rig_G] -
                        GChannel[(top_G)* Width + rig_G] - GChannel[(i * 2 + 1)* Width + j * 2]) / 8.0));
                }


            }
        }

        //recover R in B
        for (int i = 0; i < Height / 2; i++)
        {
            for (int j = 0; j < Width / 2; j++)
            {

                int top_2 = i * 2 - 2;
                if (top_2 < 0)
                {
                    top_2 = i * 2;
                }
                int rig_2 = j * 2 + 3;
                if (rig_2 > (Width - 1))
                {
                    rig_2 = j * 2 + 1;
                }
                int bot_2 = i * 2 + 3;
                if (bot_2 > (Height - 1))
                {
                    bot_2 = i * 2 + 1;
                }
                int lef_2 = j * 2 - 2;
                if (lef_2 < 0)
                {
                    lef_2 = j * 2;
                }
                int top = i * 2 - 1;
                if (top < 0)
                {
                    top = 1;
                }
                int bot = i * 2 + 2;
                if (bot > (Height - 1))
                {
                    bot = i * 2;
                }
                int lef = j * 2 - 1;
                if (lef < 0)
                {
                    lef = j * 2 + 1;
                }
                int rig = j * 2 + 2;
                if (rig > (Width - 1))
                {
                    rig = j * 2;
                }


                int top_G = i * 2 - 1;
                if (top_G < 0)
                {
                    top_G = 0;
                }
                int bot_G = i * 2 + 2;
                if (bot_G > (Height - 1))
                {
                    bot_G = i * 2 + 1;
                }
                int lef_G = j * 2 - 1;
                if (lef_G < 0)
                {
                    lef_G = j * 2;
                }
                int rig_G = j * 2 + 2;
                if (rig_G > (Width - 1))
                {
                    rig_G = j * 2 + 1;
                }
                unsigned short R00 = pInputBuf[(i * 2)* Width + (lef)];
                unsigned short R01 = pInputBuf[(i * 2)* Width + j * 2 + 1];
                unsigned short R10 = pInputBuf[(bot)* Width + (lef)];
                unsigned short R11 = pInputBuf[(bot)* Width + j * 2 + 1];

                unsigned short D45 = abs(R01 - R10) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + j * 2 + 1] - GChannel[(bot_G)* Width + (lef_G)]);
                unsigned short D135 = abs(R00 - R11) + abs(2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + (lef_G)] - GChannel[(bot_G)* Width + j * 2 + 1]);

                if (D45 > D135)
                {
                    RChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((R00 + R11) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + (lef_G)] - GChannel[(bot_G)* Width + j * 2 + 1]) / 4.0));
                }
                else if (D45 < D135)
                {
                    RChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((R01 + R10) / 2.0 + (2 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + j * 2 + 1] - GChannel[(bot_G)* Width + (lef_G)]) / 4.0));
                }
                else
                {
                    RChannel[(i * 2 + 1) * Width + j * 2] = CLIP_12bit(round((R01 + R10 + R00 + R11) / 4.0 + (4 * GChannel[(i * 2 + 1) * Width + j * 2] - GChannel[(i * 2)* Width + (lef_G)] - GChannel[(bot_G)* Width + j * 2 + 1] -
                        GChannel[(i * 2)* Width + (lef_G)] - GChannel[(bot_G)* Width + j * 2 + 1]) / 8.0));

                }

            }
        }


    }


// 中值滤波
#if 0  // 中值滤波
    cv::Mat r = cv::Mat::zeros(Height, Width, CV_16UC1);
    cv::Mat g = cv::Mat::zeros(Height, Width, CV_16UC1);
    cv::Mat b = cv::Mat::zeros(Height, Width, CV_16UC1);
    for (int i = 0; i < Height; i++)
    {
        for (int j = 0; j < Width; j++)
        {
            r.at<unsigned short>(i, j) = CLIP(RChannel[i*Width + j], 0, 65535);
            g.at<unsigned short>(i, j) = CLIP(GChannel[i*Width + j], 0, 65535);
            b.at<unsigned short>(i, j) = CLIP(BChannel[i*Width + j], 0, 65535);
        }
    }
    cv::Mat r_medf = cv::Mat::zeros(Height, Width, CV_16UC1);
    cv::Mat g_medf = cv::Mat::zeros(Height, Width, CV_16UC1);
    cv::Mat b_medf = cv::Mat::zeros(Height, Width, CV_16UC1);
    cv::medianBlur(r, r_medf, 3);
    cv::medianBlur(g, g_medf, 3);
    cv::medianBlur(b, b_medf, 3);
    for (int i = 0; i < Height; i++)
    {
        for (int j = 0; j < Width; j++)
        {
            RChannel[i*Width + j] = r_medf.at<unsigned short>(i, j);
            BChannel[i*Width + j] = g_medf.at<unsigned short>(i, j);
            GChannel[i*Width + j] = b_medf.at<unsigned short>(i, j);
        }
    }
#endif


    memcpy(pOutputBuf, RChannel, ImgSize * sizeof(unsigned short));
    memcpy(pOutputBuf + ImgSize, GChannel, ImgSize * sizeof(unsigned short));
    memcpy(pOutputBuf + ImgSize * 2, BChannel, ImgSize * sizeof(unsigned short));


    free(RChannel);
    free(GChannel);
    free(BChannel);
    RChannel = NULL;
    GChannel = NULL;
    BChannel = NULL;

    return FUNCTION_OK;
}
