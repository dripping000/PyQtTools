#include "utils_opencv.h"

#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

#include <iostream>
#include <fstream>
#include <iomanip>


static int MatToByte(cv::Mat& matImage, unsigned char* pbyImage)
{
    int ret = 0;

    int nWidth = matImage.cols;
    int nHeight = matImage.rows;
    int nChannels = matImage.channels();

    int nBytes = nHeight * nWidth * nChannels;

    memcpy(pbyImage, matImage.data, nBytes);

    return ret;
}


static int ByteToMat(unsigned char* pbyImage, cv::Mat& matImage, int nWidth, int nHeight, int nChannels)
{
    int ret = 0;

    if (pbyImage == nullptr)
    {
        return -1;
    }

    int nBytes = nWidth * nHeight * nChannels;
    int nType = nChannels == 1 ? CV_8UC1 : CV_8UC3;
    matImage = cv::Mat::zeros(nHeight, nWidth, nType);
    memcpy(matImage.data, pbyImage, nBytes);

    return ret;
}


int OpenCVShow_unsigned_char(unsigned char *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_8UC1);

    for (int row = 0; row < height; row++)
    {
        unsigned char* byPixel_Mat = (unsigned char*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned char* byPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            byPixel_Mat[0] = byPixel_data[0];

            byPixel_Mat += 1;
            byPixel_data += 1;
        }
    }

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int OpenCVShow_unsigned_short(unsigned short *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_16UC3);

    for (int row = 0; row < height; row++)
    {
        unsigned short* wPixel_Mat = (unsigned short*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned short* wPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            wPixel_Mat[0] = 0;
            wPixel_Mat[1] = 0;
            wPixel_Mat[2] = wPixel_data[0];  // R通道显示实际亮度值

            wPixel_Mat += 3;
            wPixel_data += 1;
        }
    }

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int OpenCVShow_unsigned_short2unsigned_char(unsigned short *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_8UC1);

    for (int row = 0; row < height; row++)
    {
        unsigned char* byPixel_Mat = (unsigned char*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned short* wPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            unsigned char value = wPixel_data[0] / double(4095) * 255;
            byPixel_Mat[0] = value;

            byPixel_Mat += 1;
            wPixel_data += 1;
        }
    }

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int OpenCVShow_unsigned_short_equal_unsigned_char(unsigned short *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_8UC1);

    for (int row = 0; row < height; row++)
    {
        unsigned char* byPixel_Mat = (unsigned char*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned short* wPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            byPixel_Mat[0] = (unsigned char)(wPixel_data[0]);

            byPixel_Mat += 1;
            wPixel_data += 1;
        }
    }

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int OpenCVShow_double(double *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_64FC1);

    for (int row = 0; row < height; row++)
    {
        double* dPixel_Mat = (double*)(DebugMK_test.data + row * DebugMK_test.step);
        double* dPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            dPixel_Mat[0] = dPixel_data[0];

            dPixel_Mat += 1;
            dPixel_data += 1;
        }
    }

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int ReadMatToTxtFile_double(double *data, int width, int height, char *pchFilePath)
{
    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_64FC1);

    for (int row = 0; row < height; row++)
    {
        double* dPixel_Mat = (double*)(DebugMK_test.data + row * DebugMK_test.step);
        double* dPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            dPixel_Mat[0] = dPixel_data[0];

            dPixel_Mat += 1;
            dPixel_data += 1;
        }
    }


    cv::Rect rect = cv::Rect(0, 0, width, height);
    cv::Mat DebugMK_result = DebugMK_test(rect);

    std::ofstream outfile;
    outfile.open(std::string(pchFilePath), std::ios::out);
    if (!outfile.is_open())
    {
        std::cerr << "Open " << std::string(pchFilePath) << " failed!" << std::endl;
        return -1;
    }

    for (int i = 0; i < DebugMK_result.rows; i++)
    {
        for (int j = 0; j < DebugMK_result.cols; j++)
        {
            outfile << std::left << std::setw(15) << DebugMK_result.at<double>(i, j);
        }
        outfile << "\n";
    }

    return 0;
}


int ReadTxtFileToMat_unsigned_short(char *pchFilePath, int width, int height, unsigned short *data)
{
    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_16UC1);

    std::ifstream infile;
    infile.open(std::string(pchFilePath), std::ios::in);
    if (!infile.is_open())
    {
        std::cerr << "Open " << std::string(pchFilePath) << " failed!" << std::endl;
        return -1;
    }

    for (int i = 0; i < DebugMK_test.rows; i++)
    {
        for (int j = 0; j < DebugMK_test.cols; j++)
        {
            infile >> DebugMK_test.at<unsigned short>(i, j);
        }
    }

    infile.close();


    for (int row = 0; row < height; row++)
    {
        unsigned short* dPixel_Mat = (unsigned short*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned short* dPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            dPixel_data[0] = dPixel_Mat[0];

            dPixel_Mat += 1;
            dPixel_data += 1;
        }
    }

    OpenCVShow_unsigned_short(data, width, height, 0);  // [DebugMK]

    return 0;
}


int ReadTxtFileToMat_double(char *pchFilePath, int width, int height, double *data)
{
    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_64FC1);

    std::ifstream infile;
    infile.open(std::string(pchFilePath), std::ios::in);
    if (!infile.is_open())
    {
        std::cerr << "Open " << std::string(pchFilePath) << " failed!" << std::endl;
        return -1;
    }

    for (int i = 0; i < DebugMK_test.rows; i++)
    {
        for (int j = 0; j < DebugMK_test.cols; j++)
        {
            infile >> DebugMK_test.at<double>(i, j);
        }
    }

    infile.close();


    for (int row = 0; row < height; row++)
    {
        double* dPixel_Mat = (double*)(DebugMK_test.data + row * DebugMK_test.step);
        double* dPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            dPixel_data[0] = dPixel_Mat[0];

            dPixel_Mat += 1;
            dPixel_data += 1;
        }
    }

    OpenCVShow_double(data, width, height, 0);  // [DebugMK]

    return 0;
}


int OpenCVInfo_unsigned_short(unsigned short *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_32FC1);

    for (int row = 0; row < height; row++)
    {
        float* fPixel_Mat = (float*)(DebugMK_test.data + row * DebugMK_test.step);
        unsigned short* wPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            fPixel_Mat[0] = wPixel_data[0];

            fPixel_Mat += 1;
            wPixel_data += 1;
        }
    }


    // 最小值，最大值
    double min = 0.0, max = 0.0;
    double* pmin = &min;
    double* pmax = &max;
    int minId[2] = {}, maxId[2] = {};

    cv::minMaxIdx(DebugMK_test, pmin, pmax, minId, maxId);

    printf("[DebugMK] %s: min = %lf, (i, j) = (%d, %d)\n", __func__, min, minId[0], minId[1]);
    printf("[DebugMK] %s: max = %lf, (i, j) = (%d, %d)\n", __func__, max, maxId[0], maxId[1]);

    // 均值，标准差
    cv::Mat mat_mean, mat_stddev;
    cv::meanStdDev(DebugMK_test, mat_mean, mat_stddev);

    double mean, stddev;
    mean = mat_mean.at<double>(0, 0);
    stddev = mat_stddev.at<double>(0, 0);

    printf("[DebugMK] %s: mean = %lf\n", __func__, mean);
    printf("[DebugMK] %s: stddev = %lf\n", __func__, stddev);

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int OpenCVInfo_double(double *data, int width, int height, int flag)
{
    if (flag == 0)
    {
        return -1;
    }

    double t1 = cv::getTickCount();

    cv::Mat DebugMK_test = cv::Mat::zeros(height, width, CV_64FC1);

    for (int row = 0; row < height; row++)
    {
        double* dPixel_Mat = (double*)(DebugMK_test.data + row * DebugMK_test.step);
        double* dPixel_data = data + row * width;
        for (int col = 0; col < width; col++)
        {
            dPixel_Mat[0] = dPixel_data[0];

            dPixel_Mat += 1;
            dPixel_data += 1;
        }
    }


    // 最小值，最大值
    double min = 0.0, max = 0.0;
    double* pmin = &min;
    double* pmax = &max;
    int minId[2] = {}, maxId[2] = {};

    cv::minMaxIdx(DebugMK_test, pmin, pmax, minId, maxId);

    printf("[DebugMK] %s: min = %lf, (i, j) = (%d, %d)\n", __func__, min, minId[0], minId[1]);
    printf("[DebugMK] %s: max = %lf, (i, j) = (%d, %d)\n", __func__, max, maxId[0], maxId[1]);

    // 均值，标准差
    cv::Mat mat_mean, mat_stddev;
    cv::meanStdDev(DebugMK_test, mat_mean, mat_stddev);

    double mean, stddev;
    mean = mat_mean.at<double>(0, 0);
    stddev = mat_stddev.at<double>(0, 0);

    printf("[DebugMK] %s: mean = %lf\n", __func__, mean);
    printf("[DebugMK] %s: stddev = %lf\n", __func__, stddev);

    double t2 = cv::getTickCount();
    double t = ((t2 - t1) / cv::getTickFrequency()) * 1000;
    std::cout << "Execute time : " << t << " ms " << std::endl;

    return 0;
}


int outimg_u8(int height, int width, unsigned char* data, char* filepath)
{
    int ret = 0;

    cv::Mat img_out(height, width, CV_8UC3, cv::Scalar(0, 0, 0));

    int img_size = height * width;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            img_out.at<cv::Vec3b>(i, j)[2] = (unsigned char)((double)data[i*width + j + img_size * 0]);  // r
            img_out.at<cv::Vec3b>(i, j)[1] = (unsigned char)((double)data[i*width + j + img_size * 1]);  // g
            img_out.at<cv::Vec3b>(i, j)[0] = (unsigned char)((double)data[i*width + j + img_size * 2]);  // b
        }
    }

    cv::imwrite(filepath, img_out);

    return ret;
}


int outimg_u16(int width, int height, unsigned short* data, char* filepath)
{
    int ret = 0;

    cv::Mat img_out(height, width, CV_8UC3, cv::Scalar(0, 0, 0));

    int img_size = height * width;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            img_out.at<cv::Vec3b>(i, j)[2] = (unsigned char)((double)data[i*width + j + img_size * 0] / 4095.0 * 255);  // r
            img_out.at<cv::Vec3b>(i, j)[1] = (unsigned char)((double)data[i*width + j + img_size * 1] / 4095.0 * 255);  // g
            img_out.at<cv::Vec3b>(i, j)[0] = (unsigned char)((double)data[i*width + j + img_size * 2] / 4095.0 * 255);  // b
        }
    }

    cv::imwrite(filepath, img_out);

    return ret;
}
