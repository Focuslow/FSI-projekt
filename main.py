from time import sleep
from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import math
from graphic_dot import WeightBob
from pendulum_calc import accel0, accel1, angles


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # layouts and graphics
        self.showFullScreen()
        self.HBox = QtWidgets.QHBoxLayout()
        self.setLayout(self.HBox)
        self.setStyleSheet("background-color: black;")
        self.createGraphicView()
        self.HBox.addWidget(self.graphicview)
        self.VBox = QtWidgets.QVBoxLayout()
        self.HBox.addLayout(self.VBox)

        # timer
        self.timer = self.startTimer(0.01)
        self.paused = 1

        # control panel
        self.createControls()

        # init painter
        self.init_paint()
        self.calc_init()

    def createControls(self):
        self.RunBtns()

        self.weightSliders()

        self.frictionCheck()

        # animate
        self.move_change = False
        self.animate = False

        self.connCntrls()

    def RunBtns(self):
        # start
        self.start = QtWidgets.QPushButton(self)
        self.start.setText("Start")
        self.start.show()
        self.VBox.addWidget(self.start)
        self.start.setStyleSheet("background-color: white;")

        self.reset = QtWidgets.QPushButton(self)
        self.reset.setText("Reset")
        self.reset.show()
        self.reset.setStyleSheet("background-color: white;")
        self.VBox.addWidget(self.reset)

    def weightSliders(self):
        # weight
        self.mainControlBox = QtWidgets.QVBoxLayout(self)
        self.VBox.addLayout(self.mainControlBox)
        self.mainControlBox.setSpacing(20)

        self.weighCntrl = QtWidgets.QLabel(self)
        self.weighCntrl.setText("Weight control")
        self.weighCntrl.setAlignment(QtCore.Qt.AlignCenter)
        self.weighCntrl.setFixedWidth(100)
        self.weighCntrl.setFixedHeight(20)
        self.weighCntrl.show()
        self.mainControlBox.addWidget(self.weighCntrl)
        self.weighCntrl.setStyleSheet(
            "background-color: white; border: 2px solid gray; font:bold 11px; border-radius: 5px; }")

        self.WeightBox1 = QtWidgets.QVBoxLayout(self)
        self.mainControlBox.addLayout(self.WeightBox1)
        self.WeightBox1.setSpacing(5)

        self.label0 = QtWidgets.QLabel(self)
        self.label0.setText("Weight no.1")
        self.label0.setAlignment(QtCore.Qt.AlignCenter)
        self.label0.setFixedWidth(100)
        self.label0.setFixedHeight(20)
        self.label0.show()
        self.WeightBox1.addWidget(self.label0)
        self.label0.setStyleSheet("background-color: white; border: 2px solid gray; border-radius: 5px; }")

        self.slider0 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider0.setFixedWidth(100)
        self.slider0.show()
        self.slider0.setValue(60)
        self.slider0.setMinimum(40)
        self.slider0.setMaximum(80)
        self.slider0.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.WeightBox1.addWidget(self.slider0)

        self.WeightBox2 = QtWidgets.QVBoxLayout(self)
        self.mainControlBox.addLayout(self.WeightBox2)
        self.WeightBox2.setSpacing(5)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Weight no.2")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setFixedWidth(100)
        self.label1.setFixedHeight(20)
        self.label1.show()
        self.WeightBox2.addWidget(self.label1)
        self.label1.setStyleSheet("background-color: white; border: 2px solid gray; border-radius: 5px; }")

        self.slider1 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider1.setFixedWidth(100)
        self.slider1.show()
        self.slider1.setValue(60)
        self.slider1.setMinimum(40)
        self.slider1.setMaximum(80)
        self.slider1.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.WeightBox2.addWidget(self.slider1)

        self.slider0Hold = self.slider0.value()
        self.slider1Hold = self.slider1.value()

    def frictionCheck(self):
        # friction
        self.FricBox = QtWidgets.QVBoxLayout(self)
        self.VBox.addLayout(self.FricBox)
        self.FricBox.setSpacing(5)

        self.fricLab = QtWidgets.QLabel(self)
        self.fricLab.setText("Drag coefficient")
        self.fricLab.setAlignment(QtCore.Qt.AlignCenter)
        self.fricLab.setFixedWidth(100)
        self.fricLab.setFixedHeight(20)
        self.fricLab.show()
        self.FricBox.addWidget(self.fricLab)
        self.fricLab.setStyleSheet(
            "background-color: white; border: 2px solid gray; font:bold 11px; border-radius: 5px; }")

        self.fricSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.fricSlider.setFixedWidth(100)
        self.fricSlider.show()
        self.fricSlider.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.FricBox.addWidget(self.fricSlider)
        self.fricSliderHold = self.fricSlider.value()
        self.fricSlider.setMinimum(1)
        self.fricSlider.setMaximum(100)

    def connCntrls(self):
        self.start.clicked.connect(self.animate_switch)
        self.reset.clicked.connect(self.resetRun)
        self.slider0.valueChanged.connect(self.weightChange)
        self.slider1.valueChanged.connect(self.weightChange)
        self.fricSlider.valueChanged.connect(self.fricChange)

    def createGraphicView(self):
        self.scene = QtWidgets.QGraphicsScene(self)

        screen_resolution = app.desktop().screenGeometry()
        self.width, self.height = screen_resolution.width(), screen_resolution.height()

        self.scene.setSceneRect(0, 0, int(4 * self.width / 5), self.height)

        self.graphicview = QtWidgets.QGraphicsView(self.scene, self)
        self.graphicview.showFullScreen()
        self.graphicview.setGeometry(0, 0, int(4 * self.width / 5), self.height)
        self.graphicview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.dot_size0 = 40
        self.dot_size1 = 40

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            if event.key() == QtCore.Qt.Key_Escape:
                sys.exit(0)
            elif event.key() == QtCore.Qt.Key_Space:
                if self.paused == 0:
                    self.killTimer(self.timer)
                    self.paused = 1
                    if self.animate:
                        self.start.setText("Unpause")
                        self.grDot0.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                        self.grDot1.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)


                    else:
                        self.start.setText("Start")

                else:
                    try:
                        self.grDot0.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                        self.grDot1.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                    except:
                        pass
                    self.killTimer(self.timer)
                    self.timer = self.startTimer(30)
                    self.animate_switch()

    def calc_init(self):
        self.mass0 = 40
        self.mass1 = 40
        self.angle0 = +math.pi / 2
        self.angle1 = +math.pi / 2
        self.length0 = 200
        self.length1 = 200

        self.start0 = [200, 0]
        self.start1 = [200, 0]

        self.angle_velocity0 = 0
        self.angle_velocity1 = 0
        self.angle_acceleration0 = 0
        self.angle_acceleration1 = 0

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

        self.g = 3
        self.friction = 0

    def init_paint(self):
        self.greenBrush = QtGui.QBrush(QtCore.Qt.green)
        self.pen = QtGui.QPen(QtCore.Qt.white, 4)
        self.smallPen = QtGui.QPen(QtCore.Qt.white, 1)
        self.smallPenGreen = QtGui.QPen(QtCore.Qt.green, 1)
        self.smallPenBlue = QtGui.QPen(QtCore.Qt.blue, 1)

        self.main = WeightBob(0, 0, 36, self.scene, base=True, )
        self.mid_x = self.main.center()[0]
        self.mid_y = self.main.center()[1]

        self.start_dot0 = [self.main.center()[0] + 200, self.main.center()[1]]
        self.grDot0 = WeightBob(0, 0, self.dot_size0, color=QtCore.Qt.green)
        self.grDot0.setPos(self.start_dot0[0], self.start_dot0[1])
        self.start_dot1 = [self.grDot0.scenePos().x() + 200, self.grDot0.scenePos().y()]
        self.grDot1 = WeightBob(0, 0, self.dot_size1, color=QtCore.Qt.blue)
        self.grDot1.setPos(self.start_dot1[0], self.start_dot1[1])

        self.oldPos0 = self.grDot0.scenePos()
        self.oldPos1 = self.grDot1.scenePos()
        self.oldtest0 = self.grDot0.scenePos()
        self.oldtest1 = self.grDot1.scenePos()

        self.line0 = self.scene.addLine(self.mid_x, self.mid_y, self.grDot0.center()[0], self.grDot0.center()[1],
                                        self.pen)
        self.line1 = self.scene.addLine(self.grDot0.center()[0], self.grDot0.center()[1], self.grDot1.center()[0],
                                        self.grDot1.center()[1],
                                        self.pen)

        self.scene.addItem(self.grDot0)
        self.scene.addItem(self.grDot1)
        self.scene.addItem(self.main)
        self.paint()

    def paint(self):
        pos0 = self.grDot0.scenePos()
        self.line0.setLine(self.mid_x, self.mid_y, self.grDot0.center()[0] + pos0.x(),
                           self.grDot0.center()[1] + pos0.y())
        pos1 = self.grDot1.scenePos()
        self.line1.setLine(self.grDot0.center()[0] + pos0.x(), self.grDot0.center()[1] + pos0.y(),
                           self.grDot1.center()[0] + pos1.x(), self.grDot1.center()[1] + pos1.y())

    def timerEvent(self, event: QtCore.QTimerEvent):
        if self.paused == 0:
            self.slider0.setStyleSheet(
                "QSlider::handle:horizontal {background-color: gray; border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
            self.slider1.setStyleSheet(
                "QSlider::handle:horizontal {background-color: gray; border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
            self.fricSlider.setStyleSheet(
                "QSlider::handle:horizontal {background-color: gray; border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
            self.get_coords()
            self.oldPos0 = self.grDot0.scenePos()
            self.oldPos1 = self.grDot1.scenePos()
            self.grDot0.moveBy(self.move0x, self.move0y)
            self.grDot1.moveBy(self.move1x, self.move1y)
            self.oldtest0 = self.grDot0.scenePos()
            self.oldtest1 = self.grDot1.scenePos()

        self.paint()
        sleep(0.013)

    def get_coords(self):

        old_x0 = self.x0
        old_y0 = self.y0
        old_x1 = self.x1
        old_y1 = self.y1

        self.angle_acceleration0 = accel0(self.angle0, self.angle1, self.mass0, self.mass1,
                                          self.length0, self.length1, self.g,
                                          self.angle_velocity0, self.angle_velocity1)

        self.angle_acceleration1 = accel1(self.angle0, self.angle1, self.mass0, self.mass1,
                                          self.length0, self.length1, self.g,
                                          self.angle_velocity0, self.angle_velocity1)

        self.x0 = float(self.length0 * math.sin(self.angle0) - self.start0[0])
        self.y0 = float(self.length0 * math.cos(self.angle0) - self.start0[1])

        self.move0x = self.x0 - old_x0
        self.move0y = self.y0 - old_y0

        self.scene.addLine(self.grDot0.scenePos().x(), self.grDot0.scenePos().y(),
                           self.oldPos0.x(), self.oldPos0.y(), self.smallPenGreen)

        self.x1 = float(self.x0 + self.length1 * math.sin(self.angle1) - self.start1[0])
        self.y1 = float(self.y0 + self.length1 * math.cos(self.angle1) - self.start1[1])

        self.move1x = self.x1 - old_x1
        self.move1y = self.y1 - old_y1

        self.scene.addLine(self.grDot1.scenePos().x(), self.grDot1.scenePos().y(),
                           self.oldPos1.x(), self.oldPos1.y(), self.smallPenBlue)


        fric = self.fricSlider.value() * 0.0001


        self.angle_velocity0 += self.angle_acceleration0 - fric * self.angle_velocity0
        self.angle_velocity1 += self.angle_acceleration1 - fric * self.angle_velocity1
        self.angle0 += self.angle_velocity0
        self.angle1 += self.angle_velocity1

    def animate_switch(self):
        if self.animate:
            if self.paused == 0:
                self.paused = 1
                self.start.setText("Unpause")
                self.grDot0.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
                self.grDot1.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            else:
                self.paused = 0
                self.start.setText("Pause")
                self.grDot0.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
                self.grDot1.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        else:
            if self.grDot0.scenePos().x() != self.oldtest0.x() or self.grDot0.scenePos().y() != self.oldtest0.y():
                self.move_change = True

            if self.grDot1.scenePos().x() != self.oldtest1.x() or self.grDot1.scenePos().y() != self.oldtest1.y():
                self.move_change = True

            self.animate = True
            self.paused = 0
            self.start.setText("Pause")
            #
            if self.move_change:
                pos_0 = (self.grDot0.scenePos().x() - self.mid_x - self.start0[0],
                         self.grDot0.scenePos().y() - self.mid_y - self.start0[1])
                pos_1 = (self.grDot1.scenePos().x() - self.start1[0] - self.mid_x - self.start0[0],
                         self.grDot1.scenePos().y() - self.start1[1] - self.mid_y - self.start0[1])

                self.start0[0] += pos_0[0]
                self.start0[1] += pos_0[1]

                self.start1[0] += pos_1[0] - pos_0[0]
                self.start1[1] += pos_1[1] - pos_0[1]

                self.oldPos0 = self.grDot0.scenePos()
                self.oldPos1 = self.grDot1.scenePos()

                self.angle0, self.angle1, self.length0, self.length1 = angles(pos_0[0], pos_0[1], self.length0,
                                                                              pos_1[0],
                                                                              pos_1[1], self.length1)

                self.angle_velocity0 = 0
                self.angle_velocity1 = 0
                self.angle_acceleration0 = 0
                self.angle_acceleration1 = 0

        self.paint()

    def resetRun(self):
        self.scene.clear()
        self.init_paint()
        self.calc_init()
        self.paint()
        self.animate = False
        self.paused = 1
        self.start.setText("Start")
        self.fricSlider.setValue(0)
        self.slider0.setValue(50)
        self.slider1.setValue(50)
        self.slider0.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.slider1.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")
        self.fricSlider.setStyleSheet(
            "QSlider::handle:horizontal {background-color: rgb(79,174,231); border: 1px; height: 40px; width: 40px; margin: 0 0;}\n")

    def weightChange(self):
        if self.paused == 1 and not self.animate:
            self.slider0Hold = self.slider0.value()
            self.slider1Hold = self.slider1.value()
            self.dot_size0 = self.slider0.value()-10
            self.dot_size1 = self.slider1.value()-10
            self.mass0 = self.dot_size0-20
            self.mass1 = self.dot_size1-20
            self.scene.clear()
            self.init_paint()
            self.animate = False
            self.paused = 1
            self.start.setText("Start")
        else:
            self.slider0.setSliderPosition(self.slider0Hold)
            self.slider1.setSliderPosition(self.slider1Hold)

    def fricChange(self):
        if self.paused and not self.animate:
            self.fricSliderHold = self.fricSlider.value()
        else:
            self.fricSlider.setSliderPosition(self.fricSliderHold)

if __name__ == "__main__":
    ##gui
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()