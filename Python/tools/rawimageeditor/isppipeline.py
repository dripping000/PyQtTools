from PyQt5.QtCore import pyqtSignal, QThread

import time
from imp import reload
from threading import Lock

from tools.rawimageeditor.ImageInfo import ImageInfo
import tools.rawimageeditor.ispfunction as ispfunction


class ISPPipeline():

    def __init__(self, parmas, qProgressBar=None):
        # 成员变量
        self.ISPPipeline_params = parmas
        self.ISPPipeline_qProgressBar = qProgressBar

        self.pipeline = []
        self.old_pipeline = []

        # IspPipeline_list存储了IspPipeline中途所有的图像，IspPipeline_list长度比IspPipeline长1
        self.ISPPipeline_list = [ImageInfo()]
        self.ISPPipeline_list_mutex = Lock()
        self.c_ISPProc = ISPProc(self.ISPPipeline_params, self.ISPPipeline_list, self.ISPPipeline_list_mutex)


    def add_pipeline_node(self, node):
        """
        func: 为pipeline添加一个节点
        输入是pipeline_dict的字符串
        """
        if(node.lower() in ispfunction.pipeline_dict):
            self.pipeline.append(node.lower())


    def get_pipeline_node_index(self, node):
        """
        func: 返回该node在pipeline的index, 如果不存在，就返回-1
        """
        if(node.lower() in self.pipeline and node.lower() in ispfunction.pipeline_dict):
            return self.pipeline.index(node.lower())
        else:
            return -1


    def set_pipeline(self, pipeline):
        self.old_pipeline = self.pipeline
        self.pipeline = pipeline


    def clear_pipeline(self):
        self.set_pipeline([])


    def compare_pipeline(self):
        """
        func: 对比新老pipeline的区别
        如果不同的话，会返回一个index，表示从第index个值开始不一样的，注意这个index可能不存在于老的pipeline中
        如果相同的话，或者新isp是老isp子集，会返回-1
        """
        for i, node in enumerate(self.pipeline):
            if(i > len(self.old_pipeline) - 1 or node != self.old_pipeline[i]):
                return i

        return -1


    def remove_IspPipeline_list(self, index):
        """
        func: 去除>=index之后的node，由于image的长度比pipeline多1，因此需要将index+1
        """
        index = index + 1

        self.ISPPipeline_list_mutex.acquire()
        while index < len(self.ISPPipeline_list):
            self.ISPPipeline_list.pop()
        self.ISPPipeline_list_mutex.release()


    def get_IspPipeline_list(self, index):
        """
        func: 获取pipeline中的一幅图像
        如果输入-1，则返回最后一幅图像
        """
        RawImageInfo_ = None

        self.ISPPipeline_list_mutex.acquire()

        if (index >= 0 and index < len(self.ISPPipeline_list)):
            RawImageInfo_ = self.ISPPipeline_list[index]
        elif (index < 0 and len(self.pipeline) + 1 + index < len(self.ISPPipeline_list)):
            RawImageInfo_ = self.ISPPipeline_list[len(self.pipeline) + 1 + index]

        self.ISPPipeline_list_mutex.release()

        if(RawImageInfo_ is not None):
            return RawImageInfo_
        else:
            return ImageInfo()


    def reload_pipeline(self):
        """
        func: 热更新 重载ISP算法模块
        """
        reload(ispfunction.isp)
        reload(ispfunction)

        self.ISPPipeline_params.need_flush = True
        if (self.ISPPipeline_qProgressBar is not None):
            self.ISPPipeline_qProgressBar.setValue(0)


    def reset_pipeline(self):
        """
        func: 重新开始一个pipeline，把以前的图像清除
        """
        if(len(self.ISPPipeline_list) > 1):
            self.ISPPipeline_list_mutex.acquire()
            self.remove_IspPipeline_list(-1)  # 清空IspPipeline_list
            self.ISPPipeline_list = [ImageInfo()]
            self.ISPPipeline_list_mutex.release()

            self.clear_pipeline()
            return True
        return False


    def check_pipeline(self):
        """
        func: 检查pipeline，如果有不同的，修改img_list
        ret: 如果pipeline不需要修改，就返回None，如果需要修改，就返回需要修改的pipeline
        """
        # [DebugMK]
        # self.remove_IspPipeline_list(0)
        # return self.pipeline

        index_min = -1
        index_compare_pipeline = -1
        index_need_flush = -1

        index_compare_pipeline = self.compare_pipeline()

        if(self.ISPPipeline_params.need_flush == True):
            self.ISPPipeline_params.need_flush = False

            if(len(self.ISPPipeline_params.need_flush_isp) > 0):
                index_need_flush = self.get_pipeline_node_index(self.ISPPipeline_params.need_flush_isp[0])

        if index_compare_pipeline == -1:                                    # pipeline未发生变化
            if index_need_flush == -1:                                      # pipeline未发生变化，界面参数未发生变化
                return None
            else:                                                           # pipeline未发生变化，界面参数发生变化
                index_min = index_need_flush
        else:                                                               # pipeline发生变化
            if index_need_flush == -1:
                index_min = index_compare_pipeline                          # pipeline发生变化，界面参数未发生变化
            else:
                index_min = min(index_compare_pipeline, index_need_flush)   # pipeline发生变化，界面参数发生变化

        self.remove_IspPipeline_list(index_min)
        return self.pipeline[index_min:]


    def run_pipeline(self):
        """
        func: 运行pipeline，process_bar是用于显示进度的process bar, callback是运行完的回调函数
        """
        pipeline = self.check_pipeline()
        print(pipeline)

        self.c_ISPProc.set_proc_pipeline(pipeline)
        # self.c_ISPProc.start()  # [DebugMK]
        self.c_ISPProc.run_DebugMK()


class ISPProc(QThread):

    doneCB = pyqtSignal()
    processRateCB = pyqtSignal(int)
    costTimeCB = pyqtSignal(str)
    errorCB = pyqtSignal(str)


    def __init__(self, params, list, list_mutex:Lock):
        super().__init__()

        self.__params = params
        self.__list = list
        self.__list_mutex = list_mutex

        self.__pipeline = None


    def set_proc_pipeline(self, pipeline):
        self.__pipeline = pipeline


    def run_node(self, node, data):
        if(data is not None and self.__params is not None):
            return ispfunction.pipeline_dict[node](data, self.__params)


    def run_DebugMK(self):
        self.processRateCB.emit(0)

        if (self.__pipeline is not None):
            i = 1
            length = len(self.__pipeline)

            start_time = time.time()

            for node in self.__pipeline:
                data = self.__list[-1]
                try:
                    RawImageInfo_ = self.run_node(node, data)
                except Exception as e:
                    self.errorCB.emit("ISP算法[{}]运行错误:\r\n{}".format(node, e))
                    return

                if(RawImageInfo_ is not None):
                    self.__list_mutex.acquire()
                    self.__list.append(RawImageInfo_)
                    self.__list_mutex.release()
                else:
                    break

                self.processRateCB.emit(i / length * 100)
                i += 1

            stop_time = time.time()
            self.costTimeCB.emit('总耗时:{:.3f}s'.format(stop_time-start_time))

            self.doneCB.emit()
        else:
            self.processRateCB.emit(100)
