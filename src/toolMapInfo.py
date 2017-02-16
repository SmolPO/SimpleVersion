# coding=utf-8
import sys
import time
from qgis.core import *
from qgis.gui import *

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from SendHandler import Send_Handler
from message_box import *

# class InfoMapTool(QgsMapToolPan):
#     _mDragging = False
#
#     def __init__(self, canvas):
#         QgsMapToolPan.__init__(self, canvas)
#
#     def canvasMoveEvent(self, event):
#         if self._mDragging and (event.buttons() & Qt.LeftButton) == Qt.LeftButton:
#             self.canvas().panAction(event)
#
#     def canvasPressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             print("PRESS Event!")
#             self._mDragging = True
#
#     def canvasIndetity(self, event):
#         if event.button() == Qt.LeftButton:
#             print("MapInfoIndetity")
#
#     def canvasReleaseEvent(self, event):
#         if self._mDragging and event.button() == Qt.LeftButton:
#             self.canvas().panActionEnd(event.pos())
#             self._mDragging = False
#         else:
#             pass

class ToolMapInfo(QgsMapTool, QWidget):
    def __init__(self, canvas, *args):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.ind_luminaries, self.feature_dict = args
        self.init_custom_menu()
        self.menu = QMenu()
        self.w = 20  # ширина области, в которой курсор определяет точки на слое
        self.tmp_luminary = -1

    def init_custom_menu(self):
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.init_context_menu)
        #
        self.on_action_ = QAction(('on'), self)
        self.off_action_ = QAction(('off'), self)
        self.on_off_action_ = QAction(('on/off'), self)
        self.some_cmd_ = QAction(('some cmd'), self)
        #
        self.on_action_.triggered.connect(self.on_action)
        self.off_action_.triggered.connect(self.off_action)
        self.on_off_action_.triggered.connect(self.on_off_action)
        self.some_cmd_.triggered.connect(self.some_cmd)

    def init_context_menu(self, pos):
        """
        создание контекстного меню
        :param pos:
        :return:
        """
        intersect = self.ind_luminaries.intersects(self.get_area(pos.x(), pos.y()))
        if not intersect:
            print ("not point")
            return
        # запоминаем выбранный фонарь
        self.tmp_luminary = intersect

        self.menu.addAction(self.on_action_)
        self.menu.addAction(self.off_action_)
        self.menu.addAction(self.on_off_action_)
        self.menu.addAction(self.some_cmd_)
        self.menu.exec_(self.canvas.mapToGlobal(pos))


    # обработчики контекстного меню
    def on_action(self):
        """
        включить свет. Сначала тестим этот пункт, остальное добавим потом
        :return:
        """
        lum = self.get_tmp_luminary()
        if not lum:
            er_message_box("No lum!((")
            return

        print("on", self.tmp_luminary)

    def off_action(self):
        print('off')

    def on_off_action(self):
        print('on/off')

    def some_cmd(self):
        id_ = self.get_tmp_luminary()
        er_message_box("luminaries id is: " + id_[0])
        cmd, ok = QInputDialog.getText(self, 'Input cmd for ' + id_[0], 'Entry command:')
        if not ok or not cmd.isdigit():
            er_message_box("Cansel or uncorrect data")
            return

        data, ok = QInputDialog.getText(self, 'Input data for' + id_[0], 'Entry data:')
        if not ok or not cmd.isdigit():
            er_message_box("Cansel or uncorrect data")
            return

        if not Send_Handler().send_message(cmd=cmd, receiver=id_[0], data=data, sock=self.sock):
            er_message_box("Cansel or uncorrect data")
            return

    def get_tmp_luminary(self):
        return self.tmp_luminary

    def get_area(self, x, y):
        w=self.w
        p1 = self.canvas.getCoordinateTransform().toMapCoordinates(x - w, y - w)
        p2 = self.canvas.getCoordinateTransform().toMapCoordinates(x + w, y + w)
        return QgsRectangle(p1, p2)

    def get_pos(self, obj):
        return obj.pos().x(), obj.pos().y()

    # перемещение курсора
    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        # lum = self.get_luninaries_id()
        # if not lum:
        #     er_message_box("No lum!((")
        #     return
        #     # TODO!!! увеличить размер точки, над которой расположен курсор

    # нажатие клавиши
    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        # обработка клика
        # вывести контекстное меню
        self.init_context_menu(event.pos())