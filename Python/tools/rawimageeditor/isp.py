from tools.rawimageeditor.ImageInfo import ImageInfo
from tools.rawimageeditor.RawImageEditorParams import RawImageEditorParams

import numpy as np
import math
import ctypes

import pywt

from tools.rawimageeditor.isp_utils import isp_dpc
from tools.rawimageeditor.isp_utils import isp_demosaic

from common import *

# [DebugMK]
from tools.rawimageeditor.isp_utils import plained_raw
import cv2


def DebugMK(file_name, image_name, data):
    plained_raw.write_plained_file(file_name, data)  # [DebugMK]

    # data_show = data.copy()
    # data_show = data_show[..., [2,1,0]]
    # cv2.imwrite(image_name, data_show.astype(np.uint8))  # [DebugMK]


def get_src_raw_data(raw: ImageInfo, params: RawImageEditorParams):
    filename = params.rawformat.filename
    width = params.rawformat.width
    height = params.rawformat.height
    bit_depth = params.rawformat.bit_depth

    ret_img = ImageInfo()
    if (filename != "" and width != 0 and height != 0 and bit_depth != 0):
        ret_img.set_color_space("raw")
        ret_img.set_raw_pattern(params.rawformat.pattern)
        ret_img.set_bit_depth_src(params.rawformat.bit_depth)
        ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
        ret_img.load_data(filename, width, height, bit_depth)
        return ret_img
    else:
        print("图片格式不正确")
        return None


""" BLC """
class EMBayerPatternType(ctypes.c_int):
    RGGB = 0
    GBRG = 1
    GRBG = 2
    BGGR = 3


class TBLCParam(ctypes.Structure):
    _fields_ = [
        ("Width", ctypes.c_int),
        ("Height", ctypes.c_int),

        ("Pattern", ctypes.c_int),

        ("R_blc", ctypes.c_ushort),
        ("Gr_blc", ctypes.c_ushort),
        ("Gb_blc", ctypes.c_ushort),
        ("B_blc", ctypes.c_ushort),

        ("Domain", ctypes.c_ushort),
    ]


def IspBLC(raw: ImageInfo, params: RawImageEditorParams):
    black_level = params.blc.black_level

    pattern_value = get_pattern_value(raw.get_raw_pattern())
    bit_depth_src = raw.get_bit_depth_src()

    width = raw.get_width()
    height = raw.get_height()
    data = raw.get_data().copy()

    data = np.asarray(data, dtype=np.uint16)
    data_p = data.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

    dll = ctypes.cdll.LoadLibrary("./Test.dll")

    dll.interface_BLC.argtypes = (TBLCParam, ctypes.POINTER(ctypes.c_uint16))
    dll.interface_BLC.restype = ctypes.c_int
    tBLCParam = TBLCParam(
        width,
        height,
        pattern_value,
        black_level[0], black_level[1], black_level[2], black_level[3],
        2**bit_depth_src-1
        )
    ret = dll.interface_BLC(tBLCParam, data_p)
    DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "interface_BLC_ret={}".format(ret))

    ret_img = ImageInfo()
    ret_img.set_color_space("raw")
    ret_img.set_raw_pattern(params.rawformat.pattern)
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data
    return ret_img


""" IspGain """
def IspGain(raw: ImageInfo, params: RawImageEditorParams):
    digital_gain = params.digital_gain_params.digital_gain

    data = raw.get_data().copy()

    data = data * digital_gain
    data = np.clip(data, 0, raw.max_data)

    ret_img = ImageInfo()
    ret_img.set_color_space("raw")
    ret_img.set_raw_pattern(params.rawformat.pattern)
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data
    return ret_img


""" IspDPC """
def IspDPC(raw: ImageInfo, params: RawImageEditorParams):
    dpc_threshold_ratio = params.dpc_params.dpc_threshold_ratio
    dpc_method = params.dpc_params.dpc_method

    data = raw.get_data().copy()

    data = isp_dpc.DPC(data, dpc_threshold_ratio, dpc_method)

    ret_img = ImageInfo()
    ret_img.set_color_space("raw")
    ret_img.set_raw_pattern(params.rawformat.pattern)
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data
    return ret_img


""" demosaic """
class TInterpolationParam(ctypes.Structure):
    _fields_ = [
        ("Width", ctypes.c_int),
        ("Height", ctypes.c_int),

        ("Pattern", ctypes.c_int),

        ("Domain", ctypes.c_ushort),
    ]


def demosaic(raw: ImageInfo, params: RawImageEditorParams):
    pattern_value = get_pattern_value(raw.get_raw_pattern())
    bit_depth_src = raw.get_bit_depth_src()

    width = raw.get_width()
    height = raw.get_height()
    data_in = raw.get_data().copy()

    data_in = np.asarray(data_in, dtype=np.uint16)
    data_in_p = data_in.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

    shape = (height, width, 3)
    data_out = np.zeros(shape, dtype=np.uint16)
    data_out_p = data_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

    dll = ctypes.cdll.LoadLibrary("./Test.dll")

    dll.interface_interpolation.argtypes = (TInterpolationParam, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16))
    dll.interface_interpolation.restype = ctypes.c_int
    tInterpolationParam = TInterpolationParam(
        width,
        height,
        pattern_value,
        2**bit_depth_src-1
        )
    ret = dll.interface_interpolation(tInterpolationParam, data_in_p, data_out_p)
    DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "interface_interpolation_ret={}".format(ret))

    ret_img = ImageInfo()
    ret_img.set_color_space("RGB")
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data_out
    return ret_img


def demosaic_Python(raw: ImageInfo, params: RawImageEditorParams):
    demosaic_method = params.demosaic_params.demosaic_method

    pattern = raw.get_raw_pattern().upper()
    maxvalue = raw.get_max_data()

    width = raw.get_width()
    height = raw.get_height()
    data_in = raw.get_data().copy()

    if demosaic_method == 'blinnear':
        data_in = isp_demosaic.blinnear(data_in, pattern)
    elif demosaic_method == 'AHD':
        data_in = isp_demosaic.AHD(data_in, pattern, delta=2, gamma=1, maxvalue=maxvalue)

    data_in = data_in[..., ::-1]  # RGB--->BGR

    ret_img = ImageInfo()
    ret_img.set_color_space("RGB")
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data_in
    return ret_img


""" AWB """
class TAWBParam(ctypes.Structure):
    _fields_ = [
        ("Width", ctypes.c_int),
        ("Height", ctypes.c_int),

        ("RGain", ctypes.c_double),
        ("BGain", ctypes.c_double),

        ("Domain", ctypes.c_ushort),
    ]


def IspAWB(raw: ImageInfo, params: RawImageEditorParams):
    awb_gain = params.awb.awb_gain
    bit_depth_src = raw.get_bit_depth_src()

    width = raw.get_width()
    height = raw.get_height()
    data_in = raw.get_data().copy()

    data_in = np.asarray(data_in, dtype=np.uint16)
    data_in_p = data_in.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

    shape = (height, width, 3)
    data_out = np.zeros(shape, dtype=np.uint16)
    data_out_p = data_out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

    dll = ctypes.cdll.LoadLibrary("./Test.dll")

    dll.interface_AWB.argtypes = (TAWBParam, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16))
    dll.interface_AWB.restype = ctypes.c_int
    tAWBParam = TAWBParam(
        width,
        height,
        awb_gain[1]/awb_gain[0],
        awb_gain[1]/awb_gain[2],
        2**bit_depth_src-1
        )
    ret = dll.interface_AWB(tAWBParam, data_in_p, data_out_p)
    DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "interface_AWB_ret={}".format(ret))

    ret_img = ImageInfo()
    ret_img.set_color_space("RGB")
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data_out
    return ret_img


""" CCM """
def IspCCM_Python(raw: ImageInfo, params: RawImageEditorParams):
    ccm_matrix = params.ccm_params.ccm_matrix

    width = raw.get_width()
    height = raw.get_height()

    data = raw.get_data().copy()

    shape = (height, width, 3)
    data_out = np.zeros(shape, dtype=np.uint16)

    data = data[..., ::-1]  # BGR--->RGB
    data_out[:, :, 0] = data[:, :, 0] * ccm_matrix[0][0] + data[:, :, 1] * ccm_matrix[0][1] + data[:, :, 2] * ccm_matrix[0][2]
    data_out[:, :, 1] = data[:, :, 0] * ccm_matrix[1][0] + data[:, :, 1] * ccm_matrix[1][1] + data[:, :, 2] * ccm_matrix[1][2]
    data_out[:, :, 2] = data[:, :, 0] * ccm_matrix[2][0] + data[:, :, 1] * ccm_matrix[2][1] + data[:, :, 2] * ccm_matrix[2][2]
    data_out = data_out[..., ::-1]  # RGB--->BGR

    ret_img = ImageInfo()
    ret_img.set_color_space("RGB")
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data_out
    return ret_img


""" gamma """
def IspGamma_Python(raw: ImageInfo, params: RawImageEditorParams):
    gamma_ratio = params.gamma_params.gamma_ratio

    data = raw.get_data().copy()

    data = ((data/raw.max_data) ** (1.0/gamma_ratio)) * raw.max_data
    data = np.clip(data, 0, raw.max_data)

    ret_img = ImageInfo()
    ret_img.set_color_space("RGB")
    ret_img.set_bit_depth_src(params.rawformat.bit_depth)
    ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
    ret_img.data = data
    return ret_img


""" LTM """
def IspLTM_Python(raw: ImageInfo, params: RawImageEditorParams):
    dark_boost = params.ltm_params.dark_boost / 100
    bright_suppress = params.ltm_params.bright_suppress / 100

    maxvalue = raw.max_data

    data = raw.get_data().copy()
    data = data[..., ::-1]  # BGR--->RGB

    if (raw.get_color_space() == "RGB"):
        gray_image = 0.299 * data[:, :, 0] + 0.587 * data[:, :, 1] + 0.114 * data[:, :, 2]

        # 双边滤波的保边特性，这样可以减少处理后的halo瑕疵
        mask = cv2.GaussianBlur(gray_image, (5,5), 1.5)

        # 归一化
        mask = mask / maxvalue

        # 亮区和暗区用不同的LUT曲线
        mask = np.where(mask < 0.5, 1 - dark_boost * (mask - 0.5) * (mask - 0.5), 1 + bright_suppress * (mask - 0.5) * (mask - 0.5))
        alpha = np.empty(data.shape, dtype=np.float32)
        alpha[:, :, 0] = mask
        alpha[:, :, 1] = mask
        alpha[:, :, 2] = mask

        # 在原来的基础上叠加一个乘方，相当于对每个区域的gamma值进行修改
        data = maxvalue * np.power(data/maxvalue, alpha)
        data = np.clip(data, 0, maxvalue)
        data = data[..., ::-1]  # RGB--->BGR

        ret_img = ImageInfo()
        ret_img.set_color_space("RGB")
        ret_img.set_bit_depth_src(params.rawformat.bit_depth)
        ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
        ret_img.data = data
        return ret_img
    else:
        DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "LTM need RGB data!")
        return None


""" CSC """
def IspCSC_Python(raw: ImageInfo, params: RawImageEditorParams):
    """
    function: CSC色彩空间转换，从BGR色彩空间转换成YUV，并可以调节亮度、对比度、色调、饱和度

    原理：
    模拟海思的算法
    对比度调整：
        contrast * (rgb - 128) + 128，先减去128，然后乘以相应的倍数，最后在加上128
    亮度调整：
        整张图像同时加减一个值
    色调调整：
        cb = cb * cos(m) + cr * sin(m);
        cr = cr * cos(m) - cb * sin(m); 其中m从-180度到180度变化
    饱和度调整：
        UV同时乘以一个值
    总公式：
        saturation * hue * csc * (contrast * (RGB - 128) + 128 + luma)

    注意:
    1. YUV没有负值，Y,Cr,Cb最高位为符号位，U = Cr + 128;V = Cb +128
    2. 在8bit位深前提下，TV标准的yuv范围是16-235，PC标准的yuv范围是0-255，而RGB全是0-255
    3. Cb为蓝色色度分量，对应U；Cr为红色色度分量，对应V

    参考:
    http://avisynth.nl/index.php/Color_conversions
    ITU-R BT.709-6标准：https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-C.pdf
    """

    # 各个标准的YUV转换矩阵值kr,kb,kg
    kr_kb_dict = {
        "BT601": [0.299, 0.114],
        "BT709": [0.2126, 0.0722],
        "BT2020": [0.2627, 0.0593]
    }

    kr = kr_kb_dict[params.csc_params.color_space][0]
    kb = kr_kb_dict[params.csc_params.color_space][1]
    kg = 1 - (kr + kb)

    brightness = (params.csc_params.brightness - 50) / 50 * 32
    contrast = params.csc_params.contrast / 50
    hue = (params.csc_params.hue - 50 ) / 50
    saturation = params.csc_params.saturation / 50

    maxvalue = raw.max_data
    ratio = (maxvalue + 1) / 256

    data = raw.get_data().copy()

    # RGB转YCRCB/YVU矩阵
    csc = np.array([
        [kr, kg, kb],
        [0.5, -0.5 * kg/(1-kr), -0.5 * kb/(1-kr)],
        [-0.5 * kr/(1-kb), -0.5 * kg/(1-kb), 0.5],
    ])

    if (raw.get_color_space() == "RGB"):
        blackin = -128 * ratio
        blackout = (brightness + 128) * ratio

        # DebugMK
        # if(params.csc.limitrange == 2):
        #     csc_ratio = np.array([219/255, 224/255, 224/255]).reshape((3,1))
        # else:
        #     csc_ratio = 1
        csc_ratio = 1

        # 色调和饱和度调整矩阵
        adjust_matrix = np.array([
            [1., 0., 0.],
            [0., saturation * math.cos(hue * math.pi), -saturation * math.sin(hue * math.pi)],
            [0., saturation * math.sin(hue * math.pi), saturation * math.cos(hue * math.pi)]
        ])

        data = data + blackin
        B, G, R = cv2.split(data)

        matrix = np.dot(adjust_matrix, csc * csc_ratio * contrast)

        # 由于加减RGB=128时，CrCb的值都为0，可以进行化简
        Y  = matrix[0][0] * R + matrix[0][1] * G + matrix[0][2] * B + blackout
        Cr = matrix[1][0] * R + matrix[1][1] * G + matrix[1][2] * B
        Cb = matrix[2][0] * R + matrix[2][1] * G + matrix[2][2] * B
        data = cv2.merge([Y,Cr,Cb])
        # clip
        data[:, :, 0] = np.clip(data[:,:,0], 0, maxvalue)
        data[:, :, 1:] = np.clip(data[:,:,1:], -maxvalue/2, maxvalue/2)
        data = data.astype(np.float32)

        ret_img = ImageInfo()
        ret_img.set_color_space("YCrCb")
        ret_img.set_bit_depth_src(params.rawformat.bit_depth)
        ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
        ret_img.data = data
        return ret_img
    else:
        DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "CSC need RGB data!")
        return None


""" YUV Denoise """
def denoise_one_level(src, strength, noise_threshold, noise_weight):
    """
    func: 对每层小波变换的图像进行双边滤波降噪和软阈值处理
    原理图：
        - 降噪：https://image.qinxing.xyz/20210428232539.png
        - 软阈值处理：https://image.qinxing.xyz/20210428232408.png
    详细原理：
    1. 每层小波变换后的图像先经过一个双边低通滤波滤波器，得到Xb, 与原图X相减，得到噪声信息X-Xb
    3. 对噪声信息进行软阈值处理Xn: 先对Xn乘以一个降噪权重[0,1], 值越大降噪越强，然后限制阈值
    4. 原图X与噪声信号Xn相减，得到每层的输出
    """
    Xb = cv2.bilateralFilter(src, 5, strength, strength)
    noise = src - Xb
    Xn = np.clip(noise * noise_weight, -noise_threshold, noise_threshold)
    return (src - Xn)


def IspDenoise_Python(raw: ImageInfo, params: RawImageEditorParams):
    """
    func: 小波降噪
    我理解的高通滤波器原理：
        1. 先进行3层小波变换，分别是低频、中频、高频
        2. 每层都经过一个双边低通滤波滤波器，得到Xb，与原图X相减，得到噪声信息X-Xb
        3. 对噪声信息进行软阈值处理Xn：先对Xn乘以一个降噪权重，然后限制阈值
        4. 原图X与噪声信号Xn相减，得到每层的输出
        5. 进行小波逆变换，还原图像
        其中的234步骤，封装到了denoise_one_level函数中
    参数：
    @noise_threshold：降噪阈值，值越大，噪声范围越大
    @denoise_strength：降噪强度，值越大，双边滤波的强度越强
    @noise_weight：降噪权重，值越大，降噪越强，值为0的时候，就不进行降噪
    @color_denoise_strength：色度降噪强度，值越大，色度降噪越强
    """
    noise_threshold = params.denoise_params.noise_threshold
    denoise_strength = params.denoise_params.denoise_strength
    noise_weight = params.denoise_params.noise_weight
    color_denoise_strength = params.denoise_params.color_denoise_strength

    data = raw.get_data().copy()

    w = 'sym4'  # 定义小波基的类型
    l = 2       # 简化变换层次为2

    if (raw.get_color_space() == "YCrCb"):
        # 亮度降噪
        # 对图像进行小波分解
        Y = data[:, :, 0]
        coeffs = pywt.wavedec2(data=Y, wavelet=w, level=l)

        # 将中高频图像保存到list中
        list_coeffs = [[0] * 3 for i in range(l)]
        # 将中高频的图像进行降噪
        for r1 in range(len(list_coeffs)):
            for r2 in range(len(list_coeffs[r1])):
                list_coeffs[r1][r2] = denoise_one_level(
                    coeffs[r1+1][r2], denoise_strength[r1+1], noise_threshold[r1+1], noise_weight[0]/100)

        rec_coeffs = []
        # 对低频图像进行降噪
        rec_coeffs.append(denoise_one_level(
            coeffs[0], denoise_strength[0], noise_threshold[0], noise_weight[0]/100))

        # 转换成tuple
        for j in range(len(list_coeffs)):
            rec_coeffs_ = tuple(list_coeffs[j])
            rec_coeffs.append(rec_coeffs_)

        # 小波逆变换
        data[:, :, 0] = pywt.waverec2(rec_coeffs, w)

        # 色度降噪
        data[:, :, 1] = cv2.bilateralFilter(data[:, :, 1], 7, color_denoise_strength, color_denoise_strength)
        data[:, :, 2] = cv2.bilateralFilter(data[:, :, 2], 7, color_denoise_strength, color_denoise_strength)

        ret_img = ImageInfo()
        ret_img.set_color_space("YCrCb")
        ret_img.set_bit_depth_src(params.rawformat.bit_depth)
        ret_img.set_bit_depth_dst(params.rawformat.bit_depth)
        ret_img.data = data
        return ret_img
    else:
        DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "YUV Denoise need YCrCb data!")
        return None


""" private """
def get_pattern_value(pattern):
    if pattern == "rggb":
        pattern_value = EMBayerPatternType.RGGB
    elif pattern == "gbrg":
        pattern_value = EMBayerPatternType.GBRG
    elif pattern == "grbg":
        pattern_value = EMBayerPatternType.GRBG
    elif pattern == "bggr":
        pattern_value = EMBayerPatternType.BGGR
    else:
        pattern_value = EMBayerPatternType.RGGB
        DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "default pattern")

    return pattern_value
