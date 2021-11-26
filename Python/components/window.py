from PyQt5.QtWidgets import QMainWindow, QMessageBox, QProgressBar, QLabel

import os
import pickle

from components.ui.mainwindow import Ui_MainWindow


CACHE_FILEPATH = "./config/"


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def delete_folder(folder_path):
    """
    功能：删除文件夹下所有文件，不包括子文件夹
    """
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


def load_pickle(data, file_path):  # pickle.load失败返回原数据
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fp:
            data = pickle.load(fp)

    return data


def write_pickle(data, file_path):
    with open(file_path, 'wb') as fp:
        pickle.dump(data, fp)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 成员变量
        self.sub_windows = []

        self.clear_cache_flag = False
        self.file_name = CACHE_FILEPATH + "QtToolsSubWindows.tmp"
        self.subwindows_cache = []

        # Init
        self.subwindows_cache = load_pickle(self.subwindows_cache, self.file_name)


    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                    "QtTools",
                                    "是否退出程序？",
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.clear_cache_flag == False:
                create_folder(CACHE_FILEPATH)

                self.subwindows_cache = []
                while len(self.sub_windows) > 0:
                    if (self.sub_windows[0].name is not None):
                        self.subwindows_cache.append(self.sub_windows[0].name)
                        self.sub_windows[0].close()

                write_pickle(self.subwindows_cache, self.file_name)
            else:
                delete_folder(CACHE_FILEPATH)

            event.accept()
        else:
            event.ignore()


class SubWindow(QMainWindow):

    def __init__(self, name, parent, ui_view, qProgressBar=False):
        super().__init__(parent)

        self.ui = ui_view
        self.ui.setupUi(self)

        # 成员变量
        self.name = name
        self.parent = parent

        self.params = None
        self.file_name = CACHE_FILEPATH + name + ".tmp"

        # Init
        if (True == qProgressBar):
            self.qProgressBar = QProgressBar()
            self.qLabel_info = QLabel()
            self.qLable_time = QLabel()

            self.ui.statusBar.addPermanentWidget(self.qLabel_info, stretch=7)
            self.ui.statusBar.addPermanentWidget(self.qLable_time, stretch=1)
            self.ui.statusBar.addPermanentWidget(self.qProgressBar, stretch=2)

            self.qProgressBar.setRange(0, 100)
            self.qProgressBar.setValue(0)


    def load_params(self, init_params):
        self.params = load_pickle(self.params, self.file_name)

        if self.params == None:
            self.params = init_params

        return self.params


    def closeEvent(self, event):
        create_folder(CACHE_FILEPATH)

        write_pickle(self.params, self.file_name)

        # [DebugMK]
        # try:
        #     self.parent.sub_windows.remove(self)
        # except Exception:
        #     print("{}工具不支持记忆存储".format(self.name))  # [DebugMK]

        # self.name = None  # [DebugMK]

        self.parent.sub_windows.remove(self)

        event.accept()
