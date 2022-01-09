from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import sys

from components.window import MainWindow
from components.customwidget import info

from tools.rawimageeditor.RawImageEditor import RawImageEditor

from test import *  # [DebugMK]


class ImageTools(MainWindow):

    subwindow_function = {
        "RawImageEditor": RawImageEditor,
    }

    def __init__(self):
        super().__init__()

        self.subwindows_ui = self.ui.mdiArea
        self.subwindows_ui.setStyleSheet("QTabBar::tab { height: 30px;}")  # 设置TabWidget高度固定

        # 界面控制
        self.ui.qAction_clear_cache.triggered.connect(self.clear_cache)

        self.ui.qAction_RawImageEditor.triggered.connect(self.add_subwindow_RawImageEditor)

        self.ui.qAction_DebugMK.triggered.connect(self.test)  # [DebugMK]

        self.ImageTools_Init()


    def ImageTools_Init(self):
        self.load_subwindows_cache()


    def add_subwindow(self, sub_window_name):
        sub_window = self.subwindow_function[sub_window_name](parent=self)
        self.subwindows_ui.addSubWindow(sub_window)
        self.sub_windows.append(sub_window)
        sub_window.show()


    def load_subwindows_cache(self):
        for name in self.subwindows_cache:
            self.add_subwindow(name)


    def clear_cache(self):
        self.clear_cache_flag = True
        info("缓存删除成功！\r\n请重启软件", self)


    def add_subwindow_RawImageEditor(self):
        self.add_subwindow("RawImageEditor")


    def test(self):  # [DebugMK]
        print("test_begin")
        # test_copy_dll()
        # test_python_call_c()

        test_gamma()
        print("test_end")


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 高清屏幕自适应

    apps = QApplication(sys.argv)
    appswindow = ImageTools()
    appswindow.show()

    sys.exit(apps.exec_())
