import tools.rawimageeditor.isp as isp


pipeline_dict = {
    "original raw"  :                     isp.get_src_raw_data,
    "blc"           :                     isp.IspBLC,
    "demosaic"      :                     isp.demosaic,
    "awb"           :                     isp.IspAWB,
}