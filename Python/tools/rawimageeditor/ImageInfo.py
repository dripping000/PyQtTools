import numpy as np
import cv2


class ImageInfo():
    def __init__(self):
        self.rgb_pattern = {
            'r':2,
            'g':1,
            'b':0
        }


        self.color_space = "raw"  # "raw" "RGB" "YCrCb"

        self.raw_pattern = "gbrg"
        self.bit_depth_src = 12
        self.bit_depth_dst = 12  # raw图数据位深小于12bit归一化到12bit
        self.max_data = (1 << self.bit_depth_dst) - 1

        self.filename = ""
        self.data_type = np.float32
        self.data = None
        self.display_data = None


    def load_data(self, filename, width, height, bit_depth):
        """
        function: 加载图像
        input: 图像宽高和位深
        brief: 由于RAW图不同的bit深度，同样的ISP流程会导致出来的亮度不一样
        所以在RawImageInfor将原始raw图统一对齐为14bit
        """
        if(height > 0 and width > 0):
            self.data = np.fromfile(filename, dtype="uint16").reshape((height, width))

        if (self.data is not None):
            self.filename = filename.split('/')[-1]
            self.data = self.data.astype(self.data_type)
            self.bit_depth_src = bit_depth

            if(np.issubdtype(self.data_type, np.integer)):  # https://blog.csdn.net/archimekai/article/details/107188494
                if (self.bit_depth_src < 12):
                    self.data = np.left_shift(self.data, self.bit_depth_dst - self.bit_depth_src)
                self.max_data = (1 << self.bit_depth_dst) - 1
            else:
                self.max_data = (1 << self.bit_depth_src) - 1


    def load_data_with_params(self, params):
        """
        function: 加载图像
        input: RawImageEditorParams
        brief: 由于RAW图不同的bit深度，同样的ISP流程会导致出来的亮度不一样
        所以在RawImageInfor将原始raw图统一对齐为14bit
        """
        self.load_data(params.rawformat.filename, params.rawformat.width, params.rawformat.height, params.rawformat.bit_depth)


    def save_display_data(self, filename):
        # cv2.imwrite(filename, self.display_data)
        cv2.imencode('.jpg', self.display_data)[1].tofile(filename)


    def get_data_point_raw_pattern(self, y, x):
        return self.raw_pattern[(y % 2) * 2 + x % 2]


    def get_data_point(self, x, y):
        """
        获取图像中一个点的亮度值，注意颜色顺序是BGR
        如果是raw图，获取的就是当前颜色的亮度
        如果是RGB，获取的就是BGR
        如果是YUV，获取的就是YCRCB
        """
        if(x > 0 and x < self.get_width() and y > 0 and y < self.get_height()):
            if(np.issubdtype(self.data_type, np.integer)):
                right_shift_num = self.bit_depth_dst - self.bit_depth_src
                return np.right_shift(self.data[y, x], right_shift_num)
            else:
                return np.int32(self.data[y, x])
        else:
            return None


    def get_data(self):
        return self.data


    def get_display_data(self):
        """
        function: convert to QImage
        brief: 把图像转换为用于显示的正常图像
        """
        if(self.data is not None):
            if (self.color_space == "raw"):
                self.display_data = self.convert_bayer2rgbuint8()
            elif (self.color_space == "RGB"):
                self.display_data = self.convert_rgb2rgbuint8()
            elif (self.color_space == "YCrCb"):
                self.display_data = self.convert_YCrCb2rgbuint8()
            return self.display_data
        else:
            return None


    def get_size(self):
        return self.data.shape


    def get_width(self):
        return self.data.shape[1]


    def get_height(self):
        return self.data.shape[0]


    def get_depth(self):
        if np.ndim(self.data) > 2:
            return self.data.shape[2]
        else:
            return 0


    def set_color_space(self, color_space):
        self.color_space = color_space

    def get_color_space(self):
        return self.color_space


    def set_raw_pattern(self, bayer_pattern):
        self.raw_pattern = bayer_pattern

    def get_raw_pattern(self):
        return self.raw_pattern


    def set_bit_depth_src(self, bit_depth):
        self.bit_depth_src = bit_depth

    def get_bit_depth_src(self):
        return self.bit_depth_src


    def set_bit_depth_dst(self, bit_depth):
        self.bit_depth_dst = bit_depth
        self.max_data = (1 << self.bit_depth_dst) - 1

    def get_bit_depth_dst(self):
        return self.bit_depth_dst


    def set_filename(self, name):
        self.filename = name

    def get_filename(self):
        return self.filename



    def bayer_channel_separation(self):
        if (self.raw_pattern == "rggb"):
            R = self.data[::2, ::2]
            Gr = self.data[::2, 1::2]
            Gb = self.data[1::2, ::2]
            B = self.data[1::2, 1::2]
        elif (self.raw_pattern == "grbg"):
            Gr = self.data[::2, ::2]
            R = self.data[::2, 1::2]
            B = self.data[1::2, ::2]
            Gb = self.data[1::2, 1::2]
        elif (self.raw_pattern == "gbrg"):
            Gb = self.data[::2, ::2]
            B = self.data[::2, 1::2]
            R = self.data[1::2, ::2]
            Gr = self.data[1::2, 1::2]
        elif (self.raw_pattern == "bggr"):
            B = self.data[::2, ::2]
            Gb = self.data[::2, 1::2]
            Gr = self.data[1::2, ::2]
            R = self.data[1::2, 1::2]
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return

        return R, Gr, Gb, B


    def bayer_channel_merge(self, pattern):
        R, Gr, Gb, B = self.bayer_channel_separation()

        data = np.zeros_like(self.data)
        if (pattern == "rggb"):
            data[::2, ::2] = R
            data[::2, 1::2] = Gr
            data[1::2, ::2] = Gb
            data[1::2, 1::2] = B
        elif (pattern == "grbg"):
            data[::2, ::2] = Gr
            data[::2, 1::2] = R
            data[1::2, ::2] = B
            data[1::2, 1::2] = Gb
        elif (pattern == "gbrg"):
            data[::2, ::2] = Gb
            data[::2, 1::2] = B
            data[1::2, ::2] = R
            data[1::2, 1::2] = Gr
        elif (pattern == "bggr"):
            data[::2, ::2] = B
            data[::2, 1::2] = Gb
            data[1::2, ::2] = Gr
            data[1::2, 1::2] = R
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return

        return data


    def convert_bayer2rgbuint8(self):
        data = np.zeros((self.get_height(), self.get_width(), 3), dtype="uint8")

        if (self.raw_pattern == "rggb" or self.raw_pattern == "grbg" or self.raw_pattern == "gbrg" or self.raw_pattern == "bggr"):
            if(np.issubdtype(self.data_type, np.integer)):
                right_shift_num = self.get_bit_depth_dst() - 8

                for channel, (y, x) in zip(self.raw_pattern, [(0, 0), (0, 1), (1, 0), (1, 1)]):
                    data[y::2, x::2, self.rgb_pattern[channel]] = np.right_shift(self.data[y::2, x::2], right_shift_num)
            else:
                ratio = 256/(self.max_data + 1)

                for channel, (y, x) in zip(self.raw_pattern, [(0, 0), (0, 1), (1, 0), (1, 1)]):
                    data[y::2, x::2, self.rgb_pattern[channel]] = np.uint8(self.data[y::2, x::2] * ratio)
            return data
        else:
            print("pattern must be one of these: rggb, grbg, gbrg, bggr")
            return None


    def convert_rgb2rgbuint8(self):
        data = np.zeros((self.get_height(), self.get_width(), 3), dtype="uint8")

        if(np.issubdtype(self.data_type, np.integer)):
            right_shift_num = self.get_bit_depth_dst() - 8

            data[:, :, 0] = np.right_shift(self.data[:, :, 0], right_shift_num)
            data[:, :, 1] = np.right_shift(self.data[:, :, 1], right_shift_num)
            data[:, :, 2] = np.right_shift(self.data[:, :, 2], right_shift_num)
        else:
            ratio = 256/(self.max_data + 1)

            data = np.uint8(ratio * self.data)
        return data


    def convert_rgb2gray(self):
        data = np.zeros((self.get_height(), self.get_width()), dtype=self.data_type)

        data = 0.299 * self.data[:, :, 0] + 0.587 * self.data[:, :, 1] + 0.114 * self.data[:, :, 2]

        return data


    def convert_YCrCb2rgbuint8(self):
        ratio = 256/(self.max_data + 1)

        data = cv2.cvtColor(self.data, cv2.COLOR_YCrCb2BGR)
        data = np.clip(data, 0, self.max_data)

        data = np.uint8(ratio * data)
        return data
