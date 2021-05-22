import sys
import sqlite3
import os.path
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QColorDialog, QFileDialog, QInputDialog
from window import Ui_MainWindow
from shapes import BrushPoint, Line, Circle, Rect, Triangle, SqTriangle, ImportedImage


class Canvas(QWidget):  # виджет для рисования
    def __init__(self):
        super().__init__()
        self.objects = []   # список нарисованных фигур
        self.instrument = 'brush'   # текущий инструмент
        self.color = QColor(0, 0, 0)    # текущий цвет
        self.thickness = 8      # текущая толщина

    def paintEvent(self, event):    # отрисовка объектов из списка
        painter = QPainter()
        painter.begin(self)
        for obj in self.objects:
            if type(obj) is list:
                for i in obj:
                    i.draw(painter)
            else:
                obj.draw(painter)
        painter.end()

    def mousePressEvent(self, event):   # отслеживание кликов по мыши и добавление фигуры в список
        if self.instrument == 'brush':
            self.objects.append([])
            self.objects[-1].append(BrushPoint(event.x(), event.y(), self.thickness, self.color))
            self.update()
        elif self.instrument == 'line':
            self.objects.append(Line(event.x(), event.y(), event.x(), event.y(), self.thickness, self.color))
            self.update()
        elif self.instrument == 'circle':
            self.objects.append(Circle(event.x(), event.y(), event.x(), event.y(), self.thickness, self.color))
            self.update()
        elif self.instrument == 'rubber':
            self.objects.append([])
            self.objects[-1].append(BrushPoint(event.x(), event.y(), self.thickness, QColor(240, 240, 240)))
            self.update()
        elif self.instrument == 'rect':
            self.objects.append(Rect(event.x(), event.y(), 0, 0, self.thickness, self.color))
            self.update()
        elif self.instrument == 'square':
            self.objects.append(Rect(event.x(), event.y(), 0, 0, self.thickness, self.color))
            self.update()
        elif self.instrument == 'triangle':
            self.objects.append(Triangle(event.x(), event.y(), event.x(), event.y(), self.thickness, self.color))
            self.update()
        elif self.instrument == 'sqtriangle':
            self.objects.append(SqTriangle(event.x(), event.y(), event.x(), event.y(), self.thickness, self.color))
            self.update()

    def mouseMoveEvent(self, event):     # отслеживание движения мыши и изменение фигур (кроме BrushPoint)
        if self.instrument == 'brush':
            self.objects[-1].append(BrushPoint(event.x(), event.y(), self.thickness, self.color))
            self.update()
        elif self.instrument == 'line':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'circle':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'rubber':
            self.objects[-1].append(BrushPoint(event.x(), event.y(), self.thickness, QColor(240, 240, 240)))
            self.update()
        elif self.instrument == 'rect':
            self.objects[-1].ex = - self.objects[-1].sx + event.x()
            self.objects[-1].ey = - self.objects[-1].sy + event.y()
            self.update()
        elif self.instrument == 'square':
            self.objects[-1].ex = - self.objects[-1].sx + event.x()
            self.objects[-1].ey = - self.objects[-1].sx + event.x()
            self.update()
        elif self.instrument == 'triangle':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()
        elif self.instrument == 'sqtriangle':
            self.objects[-1].ex = event.x()
            self.objects[-1].ey = event.y()
            self.update()

    def setBrush(self):     # функции для изменения текущего инструмента
        self.instrument = 'brush'

    def setLine(self):
        self.instrument = 'line'

    def setCircle(self):
        self.instrument = 'circle'

    def setRubber(self):
        self.instrument = 'rubber'

    def setRect(self):
        self.instrument = 'rect'

    def setSquare(self):
        self.instrument = 'square'

    def setTriangle(self):
        self.instrument = 'triangle'

    def setSqTriangle(self):
        self.instrument = 'sqtriangle'

    def choose_color(self):     # выбор цвета
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def choose_thickness(self):     # выбор толщины
        thickness, ok_pressed = QInputDialog.getInt(
            self, "Введите толщину", "Толщина линии",
            self.thickness, 1, 100, 1)
        self.thickness = thickness


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.image_name = ''    # имя файла
        self.canceled_actions = []      # отмененные действия
        self.setCentralWidget(Canvas())     # устанавливаем виджет для рисования как центральный
        self.recent_files = []  # недавно редактированные файлы из БД
        # недавние файлы на панели меню
        self.recent_actions = [self.action, self.action_2, self.action_3, self.action_4, self.action_5]
        # инструменты рисования
        self.figures = [self.action_brush, self.action_line, self.action_circle, self.action_rect,
                        self.action_square, self.action_triangle, self.action_sq_triangle, self.action_rubber]
        # подключаем функции к кнопкам инструментов
        self.action_brush.triggered.connect(self.centralWidget().setBrush)
        self.action_line.triggered.connect(self.centralWidget().setLine)
        self.action_circle.triggered.connect(self.centralWidget().setCircle)
        self.action_rect.triggered.connect(self.centralWidget().setRect)
        self.action_square.triggered.connect(self.centralWidget().setSquare)
        self.action_triangle.triggered.connect(self.centralWidget().setTriangle)
        self.action_sq_triangle.triggered.connect(self.centralWidget().setSqTriangle)
        self.action_rubber.triggered.connect(self.centralWidget().setRubber)
        self.action_color.triggered.connect(self.centralWidget().choose_color)
        self.action_saveas.triggered.connect(self.save_as_canvas)
        self.action_save.triggered.connect(self.save_canvas)
        self.action_open.triggered.connect(self.open_image)
        self.action_new.triggered.connect(self.new_image)
        self.action_thickness.triggered.connect(self.centralWidget().choose_thickness)
        self.action_cancel.triggered.connect(self.cancel_action)
        self.action_repeat.triggered.connect(self.repeat_action)
        for i in self.recent_actions:
            i.triggered.connect(self.open_recent)
        self.update_recent()
        for i in self.figures:
            i.triggered.connect(self.is_active_action)
            i.setCheckable(True)
        self.action_brush.setChecked(True)

    def is_active_action(self):     # иконка выбранного инструмента становится активной, а другие - нет
        for i in self.figures:
            i.setChecked(False)
        self.sender().setChecked(True)

    def save_as_canvas(self):   # сохранить картику как
        self.image_name = QFileDialog.getSaveFileName(self, "Сохранить картинку как",
                                               "/home/jana/untitled.png",
                                               "Images (*.png *.xpm *.jpg)")[0]
        self.centralWidget().grab().save(self.image_name)
        self.db_names_append()
        self.update_recent()

    def save_canvas(self):      # сохранить картинку (если до этого не сохранялась - сохранить как)
        if self.image_name:
            self.centralWidget().grab().save(self.image_name)
        else:
            self.save_as_canvas()
        self.db_names_append()
        self.update_recent()

    def open_image(self):   # открыть картинку
        file_name = QFileDialog.getOpenFileName(self.centralWidget(), 'Выбрать картинку', '')[0]
        if file_name:
            self.centralWidget().objects.clear()
            self.canceled_actions.clear()
            self.image_name = file_name
        image = QPixmap(file_name)
        self.centralWidget().objects.append(ImportedImage(image))
        self.centralWidget().update()
        self.db_names_append()
        self.update_recent()

    def new_image(self):    # новая картинка
        self.centralWidget().objects.clear()
        self.canceled_actions.clear()
        self.image_name = ''
        self.centralWidget().update()

    def cancel_action(self):    # отменить действие
        try:
            last_action = self.centralWidget().objects.pop(-1)
            self.canceled_actions.append(last_action)
        except IndexError:
            pass
        self.centralWidget().update()

    def repeat_action(self):    # вернуть отмененное действие
        try:
            last_action = self.canceled_actions.pop(-1)
            self.centralWidget().objects.append(last_action)
        except IndexError:
            pass
        self.centralWidget().update()

    def db_names_append(self):  # добавляем в бд имя файла (сначала удаляем его чтобы избежать повторов)
        con = sqlite3.connect('ImageObjects.db')
        cur = con.cursor()
        cur.execute('DELETE FROM Objects WHERE title = ?', (self.image_name,))
        cur.execute('INSERT INTO Objects(title) VALUES(?)', (self.image_name,))
        con.commit()
        con.close()

    def db_recent_files(self):  # получаем из бд имена недавних файлов, проверяя, есть ли такой
        con = sqlite3.connect('ImageObjects.db')
        cur = con.cursor()
        result = cur.execute('SELECT * FROM Objects')
        self.recent_files.clear()
        for i in result:
            if os.path.isfile(i[1]):
                self.recent_files.append(i[1])
        self.recent_files.reverse()
        while len(self.recent_files) < 5:   # если файлов мало, добавляем прочерки
            self.recent_files.append('-')
        con.close()

    def update_recent(self):    # обновляем список имен файлов
        self.db_recent_files()
        for i in range(len(self.recent_actions)):
            self.recent_actions[i].setText(self.recent_files[i])

    def open_recent(self):  # открыть недавний файл
        self.image_name = self.sender().text()
        if self.image_name != '-':
            self.centralWidget().objects.clear()
            self.canceled_actions.clear()
        image = QPixmap(self.image_name)
        self.centralWidget().objects.append(ImportedImage(image))
        self.centralWidget().update()
        self.db_names_append()
        self.update_recent()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
