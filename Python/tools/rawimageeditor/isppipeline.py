from PyQt5.QtCore import pyqtSignal, QThread

import time
from imp import reload
from threading import Lock

from tools.rawimageeditor.RawImageInfo import RawImageInfo
import tools.rawimageeditor.ispfunction as ispfunction


class IspPipeline():

    def __init__(self, parmas, qProgressBar=None):
        # 成员变量
        self.IspPipeline_params = parmas
        self.IspPipeline_qProgressBar = qProgressBar

        self.pipeline = []
        self.old_pipeline = []

        # IspPipeline_list存储了IspPipeline中途所有的图像，IspPipeline_list长度比IspPipeline长1
        self.IspPipeline_list = [RawImageInfo()]
        self.IspPipeline_list_mutex = Lock()
        self.c_ISPProc = ISPProc(self.IspPipeline_params, self.IspPipeline_list, self.IspPipeline_list_mutex)


    def reload_pipeline(self):
        """
        func: 热更新 重载ISP算法模块
        """
        reload(ispfunction.isp)
        reload(ispfunction)

        self.IspPipeline_params.need_flush = True
        if (self.IspPipeline_qProgressBar is not None):
            self.IspPipeline_qProgressBar.setValue(0)


    def reset_pipeline(self):
        """
        func: 重新开始一个pipeline，把以前的图像清除
        """
        if(len(self.IspPipeline_list) > 1):
            self.IspPipeline_list_mutex.acquire()
            self.IspPipeline_list = [RawImageInfo()]
            self.IspPipeline_list_mutex.release()

            self.old_pipeline = []
            self.pipeline = []
            return True
        return False


    def set_pipeline(self, pipeline):
        self.old_pipeline = self.pipeline
        self.pipeline = pipeline


    def clear_pipeline(self):
        self.set_pipeline([])


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


    def check_pipeline(self):
        """
        func: 检查pipeline，如果有不同的，修改img_list
        ret: 如果pipeline不需要修改，就返回None，如果需要修改，就返回需要修改的pipeline
        """
        self.remove_RawImageInfo(0)
        return self.pipeline

        index_compare_pipeline = self.compare_pipeline()  # pipeline是否发生变化

        if(self.params.need_flush == True):  # 界面参数发生变化
            self.params.need_flush = False

            if(len(self.params.need_flush_isp) > 0):
                index = self.get_pipeline_node_index(self.params.need_flush_isp[0])
                if(index != -1):  # 有效ISP模块
                    if(index_compare_pipeline != -1):
                        min_index = min(index_compare_pipeline, index)
                        self.remove_RawImageInfo(min_index)
                        return self.pipeline[min_index:]
                    else:
                        return self.pipeline[index:]

                else:  # 无效ISP模块
                    return None

            else:
                self.remove_RawImageInfo(0)
                return self.pipeline

        else:  # 界面参数未发生变化
            if(index_compare_pipeline != -1):
                self.remove_RawImageInfo(index_compare_pipeline)
                return self.pipeline[index_compare_pipeline:]
            return None


    def run_pipeline(self):
        """
        func: 运行pipeline，process_bar是用于显示进度的process bar, callback是运行完的回调函数
        """
        pipeline = self.check_pipeline()
        print(pipeline)

        self.c_ISPProc.set_pipeline(pipeline)
        # self.ispProcthread.start()  # [DebugMK]
        self.c_ISPProc.run_DebugMK()


    def remove_RawImageInfo(self, index):
        """
        func: 去除>=index之后的node，由于image的长度比pipeline多1，因此需要将index+1
        """
        index = index + 1

        self.IspPipeline_list_mutex.acquire()
        while index < len(self.IspPipeline_list):
            self.IspPipeline_list.pop()
        self.IspPipeline_list_mutex.release()


    def get_RawImageInfo(self, index):
        """
        func: 获取pipeline中的一幅图像
        如果输入-1，则返回最后一幅图像
        """
        RawImageInfo_ = None

        self.IspPipeline_list_mutex.acquire()

        if (index >= 0 and index < len(self.IspPipeline_list)):
            RawImageInfo_ = self.IspPipeline_list[index]
        elif (index < 0 and len(self.pipeline) + 1 + index < len(self.IspPipeline_list)):
            RawImageInfo_ = self.IspPipeline_list[len(self.pipeline) + 1 + index]

        self.IspPipeline_list_mutex.release()

        if(RawImageInfo_ is not None):
            return RawImageInfo_
        else:
            return RawImageInfo()


class ISPProc(QThread):

    doneCB = pyqtSignal()
    processRateCB = pyqtSignal(int)
    costTimeCB = pyqtSignal(str)
    errorCB = pyqtSignal(str)


    def __init__(self, params, RawImageInfo_list, RawImageInfo_list_mutex:Lock, parent=None):
        super(ISPProc, self).__init__(parent)

        self.params = params
        self.RawImageInfo_list = RawImageInfo_list
        self.RawImageInfo_list_mutex = RawImageInfo_list_mutex

        self.pipeline = None


    def set_pipeline(self, pipeline):
        self.pipeline = pipeline


    def run_node(self, node, data):
        # 这里进行检查之后，后续就不需要检查了
        if(data is not None and self.params is not None):
            return ispfunction.pipeline_dict[node](data, self.params)


    def run_DebugMK(self):
        self.processRateCB.emit(0)

        if (self.pipeline is not None):
            i = 1
            length = len(self.pipeline)

            start_time = time.time()

            for node in self.pipeline:
                data = self.RawImageInfo_list[-1]
                try:
                    RawImageInfo_ = self.run_node(node, data)
                except Exception as e:
                    self.errorCB.emit("ISP算法[{}]运行错误:\r\n{}".format(node, e))
                    return

                if(RawImageInfo_ is not None):
                    self.RawImageInfo_list_mutex.acquire()
                    self.RawImageInfo_list.append(RawImageInfo_)
                    self.RawImageInfo_list_mutex.release()
                else:
                    break

                self.processRateCB.emit(i / length * 100)
                i += 1

            stop_time = time.time()
            self.costTimeCB.emit('总耗时:{:.3f}s'.format(stop_time-start_time))

            self.doneCB.emit()
        else:
            self.processRateCB.emit(100)
