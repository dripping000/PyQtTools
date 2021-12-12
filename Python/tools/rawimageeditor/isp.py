from tools.rawimageeditor.ImageInfo import ImageInfo
from tools.rawimageeditor.RawImageEditorParams import RawImageEditorParams

import numpy as np
import ctypes

import tools.rawimageeditor.isp_utils.isp_dpc as isp_dpc

from common import *


def get_src_raw_data(raw: ImageInfo, params: RawImageEditorParams):
    filename = params.rawformat.filename
    width = params.rawformat.width
    height = params.rawformat.height
    bit_depth = params.rawformat.bit_depth

    ret_img = ImageInfo()
    if (filename != "" and width != 0 and height != 0 and bit_depth != 0):
        ret_img.set_color_space("raw")
        ret_img.set_raw_pattern(params.rawformat.pattern)
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
    ret_img.data = data
    return ret_img


""" IspGain """
def IspGain(raw: ImageInfo, params: RawImageEditorParams):
    digital_gain = params.digital_gain_params.digital_gain

    data = raw.get_data().copy()

    data = data * digital_gain
    data = np.clip(data, 0, raw.max_data)

    ret_img = ImageInfo()
    ret_img.data = data
    return ret_img


""" IspDPC """
def IspDPC(raw: ImageInfo, params: RawImageEditorParams):
    dpc_threshold_ratio = params.dpc_params.dpc_threshold_ratio
    dpc_method = params.dpc_params.dpc_method

    data = raw.get_data().copy()

    data = isp_dpc.DPC(data, dpc_threshold_ratio, dpc_method)

    ret_img = ImageInfo()
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
    ret_img.data = data_out
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
    ret_img.data = data_out
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
