from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class WeightBob(QGraphicsItem):
    def __init__(self,posx=0, posy=0, size=30, scene = None, base=False,color=Qt.green,):
        super().__init__()

        self.center_x = posx
        self.center_y = posy

        self.size = size

        self.color = color

        # base/main pivot of pendulum
        self.base = base



        if base:
            rect = scene.sceneRect()
            self.center_x = rect.right()/2
            self.center_y = rect.bottom()/2

        self.top_x = self.center_x - self.size/2
        self.top_y = self.center_y - self.size/2

        self.initUI()


    def boundingRect(self):
        return QRectF(
            self.top_x,
            self.top_y,
            self.size,
            self.size
        ).normalized()


    def initUI(self):
        if not self.base:
            self.setFlag(QGraphicsItem.ItemIsSelectable)
            self.setFlag(QGraphicsItem.ItemIsMovable)


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)

        path_content.addEllipse(self.top_x, self.top_y, self.size,self.size)

        if self.isSelected():
            painter.setPen(Qt.yellow)

        else:
            painter.setPen(Qt.NoPen)

        if self.base:
            painter.setBrush(Qt.red)
        else:
            painter.setBrush(self.color)

        painter.drawPath(path_content.simplified())



    def center(self):
        return [int(self.center_x),int(self.center_y)]





























