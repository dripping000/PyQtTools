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


class DigitalGainParams():
    def __init__(self):
        self.digital_gain = 1.0

        self.name = 'digital gain'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.digital_gain.setValue(self.digital_gain)


    def get(self, ui:Ui_ImageEditor):
        self.set_digital_gain(ui.digital_gain.value())
        return self.need_flush


    def set_digital_gain(self, digital_gain):
        if(digital_gain != self.digital_gain):
            self.digital_gain = digital_gain
            self.need_flush = True


class DPCParams():
    def __init__(self):
        self.dpc_threshold_ratio = 1
        self.dpc_method = 'mean'

        self.name = 'bad pixel correction'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.dpc_threshold_ratio.setValue(self.dpc_threshold_ratio)
        ui.dpc_method.setCurrentText(self.dpc_method)


    def get(self, ui:Ui_ImageEditor):
        self.set_dpc_threshold_ratio(ui.dpc_threshold_ratio.value())
        self.set_dpc_method(ui.dpc_method.currentText())
        return self.need_flush


    def set_dpc_threshold_ratio(self, dpc_threshold_ratio):
        if(dpc_threshold_ratio != self.dpc_threshold_ratio):
            self.dpc_threshold_ratio = dpc_threshold_ratio
            self.need_flush = True


    def set_dpc_method(self, dpc_method):
        if(dpc_method != self.dpc_method):
            self.dpc_method = dpc_method
            self.need_flush = True


class DemosaicParams():
    def __init__(self):
        self.demosaic_method = 'blinnear'

        self.name = 'demosaic'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.demosaic_method.setCurrentText(self.demosaic_method)


    def get(self, ui:Ui_ImageEditor):
        self.set_demosaic_method(ui.demosaic_method.currentText())
        return self.need_flush


    def set_demosaic_method(self, demosaic_method):
        if(demosaic_method != self.demosaic_method):
            self.demosaic_method = demosaic_method
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


class CCMParams():
    def __init__(self):
        self.ccm_matrix = [[1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]]

        self.name = 'CCM'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.ccm_rr.setValue(self.ccm_matrix[0][0])
        ui.ccm_rg.setValue(self.ccm_matrix[0][1])
        ui.ccm_rb.setValue(self.ccm_matrix[0][2])
        ui.ccm_gr.setValue(self.ccm_matrix[1][0])
        ui.ccm_gg.setValue(self.ccm_matrix[1][1])
        ui.ccm_gb.setValue(self.ccm_matrix[1][2])
        ui.ccm_br.setValue(self.ccm_matrix[2][0])
        ui.ccm_bg.setValue(self.ccm_matrix[2][1])
        ui.ccm_bb.setValue(self.ccm_matrix[2][2])


    def get(self, ui:Ui_ImageEditor):
        self.set_ccm_matrix([[ui.ccm_rr.value(), ui.ccm_rg.value(), ui.ccm_rb.value()],
                             [ui.ccm_gr.value(), ui.ccm_gg.value(), ui.ccm_gb.value()],
                             [ui.ccm_br.value(), ui.ccm_bg.value(), ui.ccm_bb.value()]])
        return self.need_flush


    def set_ccm_matrix(self, ccm_matrix):
        if(ccm_matrix != self.ccm_matrix):
            self.ccm_matrix = ccm_matrix
            self.need_flush = True


class GammaParams():
    def __init__(self):
        self.gamma_ratio = 2.2

        self.name = 'gamma'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.gamma_ratio.setValue(self.gamma_ratio)


    def get(self, ui:Ui_ImageEditor):
        self.set_gamma_ratio(ui.gamma_ratio.value())
        return self.need_flush


    def set_gamma_ratio(self, gamma_ratio):
        if(gamma_ratio != self.gamma_ratio):
            self.gamma_ratio = gamma_ratio
            self.need_flush = True


class LTMParams():
    def __init__(self):
        self.dark_boost = 100
        self.bright_suppress = 100

        self.name = 'LTM'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.dark_boost.setValue(self.dark_boost)
        ui.bright_suppress.setValue(self.bright_suppress)


    def get(self, ui:Ui_ImageEditor):
        self.set_dark_boost(ui.dark_boost.value())
        self.set_bright_suppress(ui.bright_suppress.value())
        return self.need_flush


    def set_dark_boost(self, dark_boost):
        if(dark_boost != self.dark_boost):
            self.dark_boost = dark_boost
            self.need_flush = True


    def set_bright_suppress(self, bright_suppress):
        if(bright_suppress != self.bright_suppress):
            self.bright_suppress = bright_suppress
            self.need_flush = True


class CSCParams():
    def __init__(self):
        self.color_space = 'BT709'

        self.brightness = 50
        self.contrast = 50
        self.hue = 50
        self.saturation = 50

        self.name = 'CSC'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        index = ui.color_space.findText(self.color_space)
        ui.color_space.setCurrentIndex(index)

        ui.luma.setValue(self.brightness)
        ui.contrast.setValue(self.contrast)
        ui.hue.setValue(self.hue)
        ui.saturation.setValue(self.saturation)


    def get(self, ui:Ui_ImageEditor):
        self.set_color_space(ui.color_space.currentText())

        self.set_brightness(ui.luma.value())
        self.set_contrast(ui.contrast.value())
        self.set_hue(ui.hue.value())
        self.set_saturation(ui.saturation.value())
        return self.need_flush


    def set_color_space(self, color_space):
        if(color_space != self.color_space):
            self.color_space = color_space
            self.need_flush = True


    def set_brightness(self, brightness):
        if(brightness != self.brightness):
            self.brightness = brightness
            self.need_flush = True

    def set_contrast(self, contrast):
        if(contrast != self.contrast):
            self.contrast = contrast
            self.need_flush = True

    def set_hue(self, hue):
        if(hue != self.hue):
            self.hue = hue
            self.need_flush = True

    def set_saturation(self, saturation):
        if(saturation != self.saturation):
            self.saturation = saturation
            self.need_flush = True


class DenoiseParams():
    def __init__(self):
        self.noise_threshold = [50, 50, 50]     # [0, 100]
        self.denoise_strength = [50, 50, 50]    # [0, 100]
        self.noise_weight = [50, 50, 50]        # [0, 100]

        self.color_denoise_strength = 50        # [0, 100]

        self.name = 'yuv denoise'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.noise_threshold_l.setValue(self.noise_threshold[0])
        ui.noise_threshold_m.setValue(self.noise_threshold[1])
        ui.noise_threshold_h.setValue(self.noise_threshold[2])
        ui.denoise_strength_l.setValue(self.denoise_strength[0])
        ui.denoise_strength_m.setValue(self.denoise_strength[1])
        ui.denoise_strength_h.setValue(self.denoise_strength[2])
        ui.noise_weight_l.setValue(self.noise_weight[0])
        ui.noise_weight_m.setValue(self.noise_weight[1])
        ui.noise_weight_h.setValue(self.noise_weight[2])
        ui.color_denoise_strength.setValue(self.color_denoise_strength)


    def get(self, ui:Ui_ImageEditor):
        self.set_noise_threshold([ui.noise_threshold_l.value(), ui.noise_threshold_m.value(), ui.noise_threshold_h.value()])
        self.set_denoise_strength([ui.denoise_strength_l.value(), ui.denoise_strength_m.value(), ui.denoise_strength_h.value()])
        self.set_noise_weight([ui.noise_weight_l.value(), ui.noise_weight_m.value(), ui.noise_weight_h.value()])
        self.set_color_denoise_strength(ui.color_denoise_strength.value())
        return self.need_flush


    def set_noise_threshold(self, noise_threshold):
        if(noise_threshold != self.noise_threshold):
            self.noise_threshold = noise_threshold
            self.need_flush = True


    def set_denoise_strength(self, denoise_strength):
        if(denoise_strength != self.denoise_strength):
            self.denoise_strength = denoise_strength
            self.need_flush = True


    def set_noise_weight(self, noise_weight):
        if(noise_weight != self.noise_weight):
            self.noise_weight = noise_weight
            self.need_flush = True


    def set_color_denoise_strength(self, color_denoise_strength):
        if(color_denoise_strength != self.color_denoise_strength):
            self.color_denoise_strength = color_denoise_strength
            self.need_flush = True


class SharpenParams():
    def __init__(self):
        self.medianblur_strength = 0    # [0, 100]
        self.sharpen_strength = 5       # [0, 5]
        self.clip_range = 64            # [0, 128]
        self.denoise_threshold = 50     # [0, 250]

        self.name = 'yuv sharpen'
        self.need_flush = False


    def set(self, ui:Ui_ImageEditor):
        ui.medianblur_strength.setValue(self.medianblur_strength)
        ui.sharpen_strength.setValue(self.sharpen_strength)
        ui.clip_range.setValue(self.clip_range)
        ui.denoise_threshold.setValue(self.denoise_threshold)


    def get(self, ui:Ui_ImageEditor):
        self.set_medianblur_strength(ui.medianblur_strength.value())
        self.set_sharpen_strength(ui.sharpen_strength.value())
        self.set_clip_range(ui.clip_range.value())
        self.set_denoise_threshold(ui.denoise_threshold.value())
        return self.need_flush


    def set_medianblur_strength(self, medianblur_strength):
        if(medianblur_strength != self.medianblur_strength):
            self.medianblur_strength = medianblur_strength
            self.need_flush = True


    def set_sharpen_strength(self, sharpen_strength):
        if(sharpen_strength != self.sharpen_strength):
            self.sharpen_strength = sharpen_strength
            self.need_flush = True


    def set_clip_range(self, clip_range):
        if(clip_range != self.clip_range):
            self.clip_range = clip_range
            self.need_flush = True


    def set_denoise_threshold(self, denoise_threshold):
        if(denoise_threshold != self.denoise_threshold):
            self.denoise_threshold = denoise_threshold
            self.need_flush = True


class RawImageEditorParams():
    def __init__(self):
        self.need_flush = False
        self.need_flush_isp = []

        self.ui_params = [
            FormatParams(),
            BLCParams(),
            DigitalGainParams(),
            DPCParams(),
            AWBParams(),
            DemosaicParams(),
            CCMParams(),
            GammaParams(),
            LTMParams(),
            CSCParams(),
            DenoiseParams(),
            SharpenParams(),
        ]

        [
            self.rawformat,
            self.blc,
            self.digital_gain_params,
            self.dpc_params,
            self.awb,
            self.demosaic_params,
            self.ccm_params,
            self.gamma_params,
            self.ltm_params,
            self.csc_params,
            self.denoise_params,
            self.sharpen_params,
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
