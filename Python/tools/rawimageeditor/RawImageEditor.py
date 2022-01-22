from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QGraphicsView

from tools.rawimageeditor.ui.rawimageeditor_window import Ui_ImageEditor
from tools.rawimageeditor.RawImageEditorParams import RawImageEditorParams

import os

from components.window import SubWindow
from components.customwidget import ImageView

from tools.rawimageeditor.ImageInfo import ImageInfo
from tools.rawimageeditor.isppipeline import ISPPipeline


class RawImageEditor(SubWindow):

    def __init__(self, name='RawImageEditor', parent=None):
        super().__init__(name, parent, Ui_ImageEditor(), qProgressBar=True)

        self.scene = QGraphicsScene()
        self.imageview = ImageView(self.scene, parent)
        self.ui.graphicsView.addWidget(self.imageview)

        # 成员变量
        self.RawImageEditor_params = self.load_params(RawImageEditorParams())

        self.c_IspPipeline = ISPPipeline(self.RawImageEditor_params, qProgressBar=self.qProgressBar)

        self.c_ImageInfo = ImageInfo()
        self.c_display_image = None

        self.__x = None
        self.__y = None
        self.__point_value = None
        self.__scale_ratio = 100

        self.__select_from_raw_rect = []
        self.__awb_select_white_area_flag = False

        # 界面控制
        self.ui.open_image.clicked.connect(self.open_image)
        self.ui.pipeline_ok.clicked.connect(self.update_pipeline)
        self.ui.select_from_raw.clicked.connect(self.select_from_raw)
        # 信号与槽
        self.imageview.signalDragEvent.connect(self.update_filename)
        self.imageview.signalmouseMoveEvent.connect(self.display_point_value)
        self.imageview.signalWheelEvent.connect(self.display_scale_ratio)

        self.imageview.rubberBandChanged.connect(self.update_select_from_raw)

        self.c_IspPipeline.c_ISPProc.doneCB.connect(self.update_display_image)
        self.c_IspPipeline.c_ISPProc.processRateCB.connect(self.update_process_bar)
        self.c_IspPipeline.c_ISPProc.costTimeCB.connect(self.update_time_bar)

        self.RawImageEditor_Init()


    def RawImageEditor_Init(self):
        self.RawImageEditor_params.set_img_params_ui(self.ui)
        self.update_pipeline()


    def update_pipeline(self):
        """
        func: 运行ISP pipeline
        """
        self.RawImageEditor_params.get_img_params_ui(self.ui)

        self.c_IspPipeline.clear_pipeline()

        for i in range(self.ui.pipeline.count()):
            if (self.ui.pipeline.item(i).checkState() == Qt.Checked):
                self.c_IspPipeline.add_pipeline_node(self.ui.pipeline.item(i).data(0))

        self.c_IspPipeline.run_pipeline()


    def update_filename(self, file_name):
        if file_name != "":
            self.ui.filename.setText(file_name)

            self.update_pipeline()


    def open_image(self):
        if self.RawImageEditor_params.rawformat.filename != "":
            file_path = os.path.dirname(self.RawImageEditor_params.rawformat.filename)
        else:
            file_path = "./"

        image_path = QFileDialog.getOpenFileName(
            None,               # 指定父组件
            "Open RAW",         # 标题
            file_path,          # 对话框显示时默认打开的目录
            "raw (*.raw)"       # 文件扩展名过滤器
        )

        self.update_filename(image_path[0])


    def display_image(self, image):
        self.scene.clear()

        self.c_ImageInfo = image
        self.c_display_image = self.c_ImageInfo.get_display_data()

        if(self.c_display_image is not None):
            display_image_ = QImage(
                self.c_display_image,
                self.c_display_image.shape[1],
                self.c_display_image.shape[0],
                QImage.Format_BGR888
            )

            self.scene.addPixmap(QPixmap(display_image_))
            self.ui.photo_title.setTitle(self.c_ImageInfo.get_filename())


    def update_display_image(self):
        self.c_ImageInfo = self.c_IspPipeline.get_IspPipeline_list(-1)
        self.display_image(self.c_ImageInfo)


    # 更新进度条和时间
    def update_process_bar(self, value):
        """
        func: ISP 处理进度回调
        """
        self.qProgressBar.setValue(value)


    def update_time_bar(self, value):
        """
        func: ISP 处理时间回调
        """
        self.qLable_time.setText(value)


    # 更新图像信息
    def display_image_info(self):
        """
        func: 显示像素点的值以及缩放比例
        """
        if(self.__point_value.size == 1):
            self.qLabel_info.setText(
                "x:{},y:{} : {}: 亮度:{} 缩放比例:{}%".format(self.__x, self.__y, self.c_ImageInfo.get_data_point_raw_pattern(self.__y, self.__x).upper(), self.__point_value, self.__scale_ratio))

        elif(self.__point_value.size == 3):  # [DebugMK]
            if(self.c_ImageInfo.get_color_space() == 'RGB'):
                self.qLabel_info.setText(
                    "x:{},y:{} : R:{} G:{} B:{} 缩放比例:{}%".format(self.__x, self.__y, self.__point_value[2], self.__point_value[1], self.__point_value[0], self.__scale_ratio))
            else:
                self.qLabel_info.setText(
                    "x:{},y:{} : Y:{} Cr:{} Cb:{} 缩放比例:{}%".format(self.__x, self.__y, self.__point_value[0], self.__point_value[1], self.__point_value[2], self.__scale_ratio))


    def display_point_value(self, point):
        if(self.c_ImageInfo.get_data() is not None):
            self.__x = int(point.x())
            self.__y = int(point.y())

            point_value = self.c_ImageInfo.get_data_point(self.__x, self.__y)
            if (point_value is not None):
                self.__point_value = point_value
                self.display_image_info()


    def display_scale_ratio(self, scale_ratio):
        if(self.c_ImageInfo.get_data() is not None):
            self.__scale_ratio = int(scale_ratio * 100)
            self.display_image_info()


    def select_from_raw(self):
        self.imageview.setDragMode(QGraphicsView.RubberBandDrag)
        self.__awb_select_white_area_flag = True


    def update_select_from_raw(self, viewportRect, fromScenePoint, toScenePoint):
        # print(fromScenePoint.x(), " ", fromScenePoint.y(), " ", toScenePoint.x(), " ", toScenePoint.y())

        if((toScenePoint.x() == 0) and (toScenePoint.y() == 0)
            and (self.__select_from_raw_rect[2] > self.__select_from_raw_rect[0]) and (self.__select_from_raw_rect[3] > self.__select_from_raw_rect[1])):
            if (self.__awb_select_white_area_flag == True):
                self.imageview.setDragMode(QGraphicsView.ScrollHandDrag)
                self.__awb_select_white_area_flag = False

                print(self.__select_from_raw_rect[0], " ", self.__select_from_raw_rect[1], " ", self.__select_from_raw_rect[2], " ", self.__select_from_raw_rect[3])

                awb_gain = self.c_ImageInfo.get_raw_awb_gain(self.__select_from_raw_rect)
                if(awb_gain is not None):
                    self.RawImageEditor_params.awb.set_awb_gain(awb_gain)
                    self.RawImageEditor_params.awb.set(self.ui)  # DebugMK
        else:
            self.__select_from_raw_rect = [int(fromScenePoint.x()), int(fromScenePoint.y()),
                                            int(toScenePoint.x()), int(toScenePoint.y())]
