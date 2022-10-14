from typing import Tuple
from PyQt5 import QtGui, QtCore, QtWidgets, Qt
from mapStorage import MapStorage


class Painter(QtWidgets.QGraphicsView):
    """ Render tiles, other objects using QT API"""

    def __init__(self):
        self.map = MapStorage()
        super(Painter, self).__init__()
        
    def fill_background(self, painter: QtGui.QColor, color: str, width: float,
                        height: float):
        painter.resetTransform()
        painter.fillRect(0, 0, width, height,
                         QtGui.QColor(color))

    def draw_rect(self, start_pos: Tuple[float, float],
                  scale: float,
                  painter: QtGui.QPainter,
                  grid_width: float,
                  grid_height: float,
                  color: str = "green"):
        painter.resetTransform()
        painter.setPen(QtGui.QColor(color))
        painter.drawRect(
            QtCore.QRectF(start_pos[0] - 1,
                          start_pos[1] - 1,
                          grid_width * scale + 1,
                          grid_height * scale + 1
                          ))

    @staticmethod
    def draw_border(pixmap: QtGui.QPixmap, point: tuple, widget):
        painter = QtGui.QPainter(widget)
        #pixmap = QtGui.QPixmap("myPic.png")
        painter.drawPixmap(widget.rect(), pixmap)
        pen = QtGui.QPen(QtGui.QColor('green'), 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, widget.rect().width() - 10, 10)


''' painter = QtGui.QPainter(pixmap)
pen = QtGui.QPen()
pen.setWidth(5)
pen.setColor(QtGui.QColor('green'))
painter.setPen(pen)
painter.drawPoint(point[0], point[1])
painter.end()
'''