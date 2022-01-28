from tools.rawimageeditor.ImageInfo import ImageInfo
from tools.rawimageeditor.RawImageEditorParams import RawImageEditorParams

import numpy as np
import ctypes

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
