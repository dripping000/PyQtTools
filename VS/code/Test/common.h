#ifndef _COMMON_H_
#define _COMMON_H_


#include <iostream>


#if 1
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT __declspec(dllimport)
#endif


#define FUNCTION_OK         0
#define FUNCTION_ERROR      -1


#define MIN(a, b)               ((a) > (b) ? (b) : (a))
#define MAX(a, b)               ((a) < (b) ? (b) : (a))

#define CLIP_8bit(x)            ((x) >  255 ?  255 : ((x) <   0 ?   0 : (x)))
#define CLIP_12bit(x)           ((x) > 4095 ? 4095 : ((x) <   0 ?   0 : (x)))
#define CLIP(x, min, max)       ((x) >  max ?  max : ((x) < min ? min : (x)))


#define DEBUGMK
#ifdef DEBUGMK
#define printf_DEBUGMK(format,...) printf("[DebugMK] Function:%s, File:%s, Line:%05d: "format"", __func__, __FILE__, __LINE__, ##__VA_ARGS__)
#else
#define printf_DEBUGMK(format,...)
#endif


#endif
