import os
import sys
import shutil
import numpy as np
import ctypes
import matplotlib.pyplot as plt

import cv2


def test_copy_dll():
    try:
        if os.path.exists("./Test.dll"):
            os.remove("./Test.dll")

        shutil.copyfile("../VS/bin/Test.dll", "./Test.dll")
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


class TStruct(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte)),
    ]


def test_python_call_c():
    image = cv2.imread("./Resource/example.jpg")
    h, w, c = image.shape

    image_data = np.asarray(image, dtype=np.uint8)
    image_data_p = image_data.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))

    dll = ctypes.cdll.LoadLibrary("../VS/bin/Test.dll")

    dll.test.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte))
    dll.test.restype = ctypes.c_int
    ret = dll.test(w, h, image_data_p)
    print(ret)

    dll.test_struct.argtypes = (ctypes.POINTER(TStruct),)
    dll.test_struct.restype = ctypes.c_int
    tStruct = TStruct(w, h, image_data_p)
    ret = dll.test_struct(ctypes.POINTER(TStruct)(tStruct))
    print(ret)


'''
gamma
'''
def test_gamma_hisi2sigmastar():
    input_x = 1024
    input_y = 4096

    output_x = 256
    output_y = 1024

    output_value_list = []

    with open("./Resource/Gamma/gamma_hisi_int.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.split(',')

            for j, value in enumerate(line):
                print(j, value)
                if (j % 4) == 0:
                    output_value = int(float(value) / input_y * output_y)
                    output_value_list.append(output_value)

    with open("./Resource/Gamma/gamma_hisi_int2sigmastar.txt","w") as f:
        f.write("pixel red:1~256 green:257~512 blue:513~768\n")

        for i in range(256):
            f.write(str(output_value_list[i])+"\n")

        for i in range(256):
            f.write(str(output_value_list[i])+"\n")

        for i in range(256):
            f.write(str(output_value_list[i])+"\n")


def test_hisi_gamma_degamma():
    hisi_gamma_x = 1024-1
    hisi_gamma_y = 4096-1

    hisi_degamma_x = 256-1
    hisi_degamma_y = 1.0

    gamma_hisi_x1023_y4095 = []
    degamma_x255_y1 = []

    with open("./Resource/Gamma/gamma_hisi_int.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.split(',')

            gamma_hisi_x1023_y4095 = [float(x) for x in line]
            # for j, value in enumerate(line):
            #     print(j, value)

            # x = np.arange(0, 1024+1, 1)  # np.arange(start, end+step, step)  [start, end] end/step+1
            # plt.plot(x, gamma_hisi_x1023_y4095)
            # plt.show()

        for i in range(hisi_degamma_x+1):  # for i in range(0, hisi_degamma_x+1, 1):

            for j, value in enumerate(gamma_hisi_x1023_y4095):
                if (value / hisi_gamma_y * hisi_degamma_x) >= i:
                    degamma_x255_y1.append(j/hisi_gamma_x)
                    break

        # x = np.arange(0, hisi_degamma_x+1, 1)
        # plt.plot(x, degamma_x255_y1)
        # plt.show()


def test_gamma():
    '''
    with open("./Resource/Gamma/gamma_sigmastar.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            if i != 0:
                line = line.strip('\n')
                print(line)

    # hisi
    with open("./Resource/Gamma/gamma_hisi_float.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.split(',')

            for j, value in enumerate(line):
                print(j, value)

            line = [float(x) for x in line]

            x = np.arange(0, 1+1/1024, 1/1024)
            plt.plot(x, line)
            plt.show()
    '''

    test_hisi_gamma_degamma()


'''
get_file_list
'''
def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        # dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=False)
        dir_list = sorted(dir_list, key=lambda x: int(x[:-4]), reverse=False)  # [DebugMK]
        # print(dir_list)
        return dir_list


def test_get_file_list():
    dir_path = "C:/Users/mengkun/Desktop/抓取的图/"
    dir_list = get_file_list(dir_path)


'''
YUV2Video
'''
def NV212RGB(yuv_path, width, height):
    with open(yuv_path, 'rb') as f:
        yuvdata = np.fromfile(f, dtype=np.uint8)
    # yuvdata = yuvdata[4 * 4 :]

    cv_format = cv2.COLOR_YUV2BGR_NV12
    bgr_img = cv2.cvtColor(yuvdata.reshape((height*3//2, width)), cv_format)

    return bgr_img


def test_YUV2Video():
    dir_path = "C:/Users/mengkun/Desktop/抓取的图/"
    dir_list = get_file_list(dir_path)

    width = 4096
    height = 2176

    fps = 25
    video = cv2.VideoWriter(dir_path+'isp_yuv.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width,height))  # [DebugMK]

    for file_name in dir_list:
        file_path = dir_path + file_name
        print(file_path)

        image = NV212RGB(file_path, width, height)

        image_save_path = file_path.replace(".yuv",".bmp")
        cv2.imencode('.bmp', image[:,:4096,:])[1].tofile(image_save_path)

        video.write(image)
