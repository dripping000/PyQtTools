#ifndef _UTILS_OPENCV_H_
#define _UTILS_OPENCV_H_


/* OpenCVShow */
int OpenCVShow_unsigned_char(unsigned char *data, int width, int height, int flag);

int OpenCVShow_unsigned_short(unsigned short *data, int width, int height, int flag);
int OpenCVShow_unsigned_short2unsigned_char(unsigned short *data, int width, int height, int flag);
int OpenCVShow_unsigned_short_equal_unsigned_char(unsigned short *data, int width, int height, int flag);

int OpenCVShow_double(double *data, int width, int height, int flag);


/* Mat Txt */
int ReadMatToTxtFile_double(double *data, int width, int height, char *pchFilePath);

int ReadTxtFileToMat_unsigned_short(char *pchFilePath, int width, int height, unsigned short *data);
int ReadTxtFileToMat_double(char *pchFilePath, int width, int height, double *data);


/* OpenCVInfo */
int OpenCVInfo_unsigned_short(unsigned short *data, int width, int height, int flag);
int OpenCVInfo_double(double *data, int width, int height, int flag);


/* imwrite */
int outimg_u8(int height, int width, unsigned char* data, char* filepath);
int outimg_u16(int width, int height, unsigned short* data, char* filepath);


#endif
