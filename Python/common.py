import sys


# DEBUGMK(sys._getframe().f_code.co_name, __file__, str(sys._getframe().f_lineno), "interface_interpolation_ret={}".format(ret))
def DEBUGMK(function, file, line, info):
    print("[DebugMK] Function:" + function + ", File:" + file + ", Line:" + line + " " + info)
