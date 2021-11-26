import os
import sys
import shutil
import numpy as np
import ctypes

import cv2


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

    dll.test_OpenVino.argtypes = ()
    dll.test_OpenVino.restype = ctypes.c_int
    ret = dll.test_OpenVino()
    print(ret)


def test_copy_dll():
    try:
        if os.path.exists("./Test.dll"):
            os.remove("./Test.dll")

        shutil.copyfile("../VS/bin/Test.dll", "./Test.dll")
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


def test_read_gamma():
    '''
    with open("./Resource/Gamma/gamma_fae_mk.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            if i != 0:
                line = line.strip('\n')
                print(line)

    with open("./Resource/Gamma/gamma_hisi_int.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            line = line.split(',')
            print(line)
    '''

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
