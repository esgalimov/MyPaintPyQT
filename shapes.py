from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QPoint


class BrushPoint:   # классы фигур
    def __init__(self, x, y, thickness=4, color=QColor(0, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness

    def draw(self, painter):
        painter.setBrush(QBrush(self.color))
        painter.setPen(self.color)
        painter.drawEllipse(self.x - (self.thickness // 2), self.y - (self.thickness // 2), self.thickness, self.thickness)


class Shape:
    def __init__(self, sx, sy, ex, ey, thickness, color=QColor(0, 0, 0)):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.color = color
        self.thickness = thickness


class Circle(Shape):
    def draw(self, painter):
        painter.setBrush(QBrush(self.color, 0))
        painter.setPen(QPen(self.color, self.thickness))
        radius = int(((self.sx - self.ex) ** 2 + (self.sy - self.ey) ** 2) ** 0.5)
        painter.drawEllipse(self.sx - radius, self.sy - radius, 2 * radius, 2 * radius)


class Line(Shape):
    def draw(self, painter):
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)


class Rect(Shape):
    def draw(self, painter):
        painter.setBrush(QBrush(self.color, 0))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawRect(self.sx, self.sy, self.ex, self.ey)


class Triangle(Shape):
    def draw(self, painter):
        painter.setBrush(QBrush(self.color, 0))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawPolygon(QPoint((self.sx + self.ex) // 2, self.sy),
                            QPoint(self.sx, self.ey),
                            QPoint(self.ex, self.ey))


class SqTriangle(Shape):
    def draw(self, painter):
        painter.setBrush(QBrush(self.color, 0))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawPolygon(QPoint(self.sx, self.sy),
                            QPoint(self.sx, self.ey),
                            QPoint(self.ex, self.ey))


class ImportedImage:    # класс для импорта изображения
    def __init__(self, image):
        self.image = image

    def draw(self, painter):
        painter.drawPixmap(0, 0, self.image)
