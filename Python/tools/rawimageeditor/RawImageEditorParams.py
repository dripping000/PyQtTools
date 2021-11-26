from tools.rawimageeditor.ui.rawimageeditor_window import Ui_ImageEditor


class FormatParams():
    def __init__(self):
        """
        RAW图片格式相关参数
        """
        self.width = 4096
        self.height = 2176
        self.bit_depth = 12

        self.raw_format = "PACKED"
        self.pattern = "GBRG"

        self.filename = 'Z:/Qt/ImageTools/Resource/D50_HisiRAW_4096x2176_12bits_GBRG_Linear_20191018143802.raw'

        self.name = 'original raw'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.width.setValue(self.width)
        ui.height.setValue(self.height)
        ui.bit.setValue(self.bit_depth)

        index = ui.raw_format.findText(self.raw_format)
        ui.raw_format.setCurrentIndex(index)
        index = ui.pattern.findText(self.pattern.upper())
        ui.pattern.setCurrentIndex(index)

        ui.filename.setText(self.filename)


    def get(self, ui:Ui_ImageEditor):
        self.set_width(ui.width.value())
        self.set_height(ui.height.value())
        self.set_bit_depth(ui.bit.value())

        self.set_raw_format(ui.raw_format.currentText())
        self.set_pattern(ui.pattern.currentText().lower())

        self.set_filename(ui.filename.text())

        return self.need_flush


    def set_width(self, value):
        if(self.width != value):
            self.width = value
            self.need_flush = True

    def set_height(self, value):
        if(self.height != value):
            self.height = value
            self.need_flush = True

    def set_bit_depth(self, value):
        if(self.bit_depth != value):
            self.bit_depth = value
            self.need_flush = True

    def set_raw_format(self, value):
        if(self.raw_format != value):
            self.raw_format = value
            self.need_flush = True

    def set_pattern(self, value):
        if(self.pattern != value):
            self.pattern = value
            self.need_flush = True

    def set_filename(self, value):
        if(self.filename != value):
            self.filename = value
            self.need_flush = True


class BLCParams():
    def __init__(self):
        self.black_level = [256, 256, 256, 256]

        self.name = 'BLC'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.blc_r.setValue(self.black_level[0])
        ui.blc_gr.setValue(self.black_level[1])
        ui.blc_gb.setValue(self.black_level[2])
        ui.blc_b.setValue(self.black_level[3])


    def get(self, ui:Ui_ImageEditor):
        self.set_black_level([ui.blc_r.value(), ui.blc_gr.value(), ui.blc_gb.value(), ui.blc_b.value()])
        return self.need_flush


    def set_black_level(self, black_level):
        if(black_level != self.black_level):
            self.black_level = black_level
            self.need_flush = True


class AWBParams():
    def __init__(self):
        self.awb_gain = [1.0, 1.0, 1.0]

        self.name = 'AWB'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.awb_r.setValue(self.awb_gain[0])
        ui.awb_g.setValue(self.awb_gain[1])
        ui.awb_b.setValue(self.awb_gain[2])


    def get(self, ui:Ui_ImageEditor):
        self.set_awb_gain([ui.awb_r.value(), ui.awb_g.value(), ui.awb_b.value()])
        return self.need_flush


    def set_awb_gain(self, awb_gain):
        if(awb_gain != self.awb_gain):
            self.awb_gain = awb_gain
            self.need_flush = True


class RawImageEditorParams():
    def __init__(self):
        self.need_flush = False
        self.need_flush_isp = []

        self.ui_params = [
            FormatParams(),
            BLCParams(),
            AWBParams(),
        ]

        [
            self.rawformat,
            self.blc,
            self.awb,
        ] = self.ui_params


    def set_img_params_ui(self, ui:Ui_ImageEditor):
        """
        设置界面参数
        """
        for param in self.ui_params:
            param.set(ui)


    def get_img_params_ui(self, ui:Ui_ImageEditor):
        """
        获取界面参数
        """
        self.need_flush_isp = []

        for ui_param in self.ui_params:
            if ui_param.get(ui) == True:
                self.need_flush_isp.append(ui_param.name)
                ui_param.need_flush = False

        if(len(self.need_flush_isp) > 0):
            self.need_flush = True
