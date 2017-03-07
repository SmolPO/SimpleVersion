# coding=utf-8
from code import interact

from SendHandler import Send_Handler
from MsgBox import *
from qgis.gui import *

from qgis.core import *

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
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
from MyQgisIface import Qgis_iface

class ToolMapInfo(QgsMapTool, QWidget):
    def __init__(self, canvas, *args):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.ind_luminaries, self.feature_dict, self.connection, self.lumlayer = args
        self.init_custom_menu()
        self.menu = QMenu()
        self.w = 10  # ширина области, в которой курсор определяет точки на слое
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
        if not self.is_near_luminaries(pos.x(), pos.y()):
            print ("Not lum")
            return
        self.set_cur_luminary()

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
        if not self.connection.is_connect:
            er_message_box("Is not connect")
            return

        lum = self.get_tmp_luminary()
        if lum == -1:
            er_message_box("No lum!((")
            return

        if Send_Handler().on_light_cmd(lum, self.connection.sock):
            print("on", self.tmp_luminary)
            return
        print ("cmd ON_LIGHT is not send!")

    def off_action(self):
        if not self.connection.is_connect:
            er_message_box("Is not connect")
            return

        lum = self.get_tmp_luminary()
        if lum == -1:
            er_message_box("No lum!((")
            return

        if Send_Handler().off_light_cmd(lum, self.connection.sock):
            print("off", self.tmp_luminary)
            return
        print ("cmd OFF_LIGHT is not send!")

    def on_off_action(self):
        if not self.connection.is_connect:
            er_message_box("Is not connect")
            return

        self.on_action()
        self.off_action()

    def some_cmd(self):
        if not self.connection.is_connect:
            er_message_box("Is not connect")
            return

        id_ = self.get_tmp_luminary()
        er_message_box("luminaries id is: ")
        cmd, ok = QInputDialog.getText(self, 'Input cmd for ', 'Entry command:')
        if not ok or not cmd.isdigit():
            er_message_box("Cansel or uncorrect data")
            return

        data, ok = QInputDialog.getText(self, 'Input data for', 'Entry data:')
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

    def get_cur_luminary(self, x, y):
        intersect = self.ind_luminaries.intersects(self.get_area(x, y))
        return intersect[0] if intersect else None

    # перемещение курсора
    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.is_near_luminaries(x, y):
            feature_id = self.get_cur_luminary(x, y)
            Qgis_iface().modify_point_on_cursor(feature_id)

    # нажатие клавиши
    def canvasReleaseEvent(self, event):
        # Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        # обработка клика
        # вывести контекстное меню
        Qgis_iface().modify_point_on_cursor(x, y)
        self.init_context_menu(event.pos())

    def is_near_luminaries(self, x, y):
        intersect = self.ind_luminaries.intersects(self.get_area(x, y))
        return True if intersect else False

    def set_cur_luminary(self, feature_id):
        self.tmp_luminary = feature_id