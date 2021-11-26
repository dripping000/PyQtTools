from PyQt5.QtWidgets import QMessageBox, QGraphicsView, QAbstractScrollArea
from PyQt5.QtCore import pyqtSignal, QPointF, Qt


def info(string: str, parent=None):
    if string != None:
        QMessageBox.information(
            parent,                 # 指定的父窗口控件
            "info", string,         # 对话框标题，对话框文本
            QMessageBox.Yes,        # 多个标准按钮
            QMessageBox.Yes         # 默认选中的标准按钮，默认是第一个标准按钮
        )
    return


def critical(string: str, parent=None):
    if(string is not None):
        QMessageBox.critical(
            parent,
            'warning', string,
            QMessageBox.Yes,
            QMessageBox.Yes
        )
    return


class ImageView(QGraphicsView):
    signalmouseMoveEvent = pyqtSignal(QPointF)
    signalWheelEvent = pyqtSignal(float)
    signalDragEvent = pyqtSignal(str)
    MousePosition = None


    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setupUi_()

        self.scale_ratio = 1.0


    def setupUi_(self):
        self.setMouseTracking(True)     # 支持鼠标跟踪

        self.setAcceptDrops(True)       # 支持鼠标拖动图片
        '''
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#DragMode-enum
        NoDrag                       什么都没发生; 鼠标事件被忽略。
        ScrollHandDrag               光标变成指针，拖动鼠标将滚动滚动条。 该模式可以在交互式和非交互式模式下工作。
        RubberBandDrag               拖动鼠标将设置橡皮筋几何形状，并选择橡皮筋所覆盖的所有项目。 对于非交互式视图，此模式被禁用。
        '''
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        '''
        #参考 https://doc.qt.io/qt-5/qabstractscrollarea.html#SizeAdjustPolicy-enum
        AdjustIgnored                       滚动区域将像以前一样运行 - 并且不做任何调整。
        AdjustToContents                    滚动区域将始终调整到视口
        AdjustToContentsOnFirstShow         滚动区域将在第一次显示时调整到其视口。
        '''
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        '''
        #参考 https://doc.qt.io/qt-5/qgraphicsview.html#transformationAnchor-prop
        AnchorViewCenter                    确保视图中心的场景点在转换过程中保持不变（例如，旋转时，场景看起来会围绕视图中心旋转）
        '''
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)  # [DebugMK]

        '''
        #当视图被调整大小时，视图如何定位场景。使用这个属性来决定当视口控件的大小改变时，如何在视口中定位场景。 缺省行为NoAnchor在调整大小的过程中不改变场景的位置; 视图的左上角将显示为在调整大小时被锚定。请注意，只有场景的一部分可见（即有滚动条时），此属性的效果才明显。 否则，如果整个场景适合视图，QGraphicsScene使用视图对齐将视景中的场景定位。
        #参考 http://doc.qt.io/qt-5/qgraphicsview.html#ViewportAnchor-enum
        NoAnchor                     视图保持场景的位置不变
        AnchorViewCenter             视图中心被用作锚点。
        AnchorUnderMouse             鼠标当前位置被用作锚点
        '''
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)


    def mouseMoveEvent(self, event):
        self.MousePosition = self.mapToScene(event.pos())
        self.signalmouseMoveEvent.emit(self.MousePosition)
        return super().mouseMoveEvent(event)


    def wheelEvent(self, event):
        self.centerOn(self.MousePosition)  # 鼠标滚轮放大缩小以当前坐标为中心

        angle = event.angleDelta().y()
        if (angle > 0):
            self.scale(1.2, 1.2)
            self.scale_ratio *= 1.2
        else:
            self.scale(0.8, 0.8)
            self.scale_ratio *= 0.8

        self.signalWheelEvent.emit(self.scale_ratio)
        return super().wheelEvent(event)


    def dragEnterEvent(self, event):
        event.accept()


    def dragMoveEvent(self, event):
        event.accept()


    def dropEvent(self, event):
        if event.mimeData().hasText():
            try:
                self.signalDragEvent.emit(event.mimeData().text()[8:])
            except Exception as e:
                print(e)
