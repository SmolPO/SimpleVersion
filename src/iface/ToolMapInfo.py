# coding=utf-8
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from random import randint

from MsgBox import *
from MyQgisIface import Qgis_iface
from SendHandler import Send_Handler


class ToolMapInfo(QgsMapTool, QWidget):
    def __init__(self, canvas, *args):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.ind_luminaries, self.feature_dict, self.connection, self.lumlayer = args
        self.init_custom_menu()
        self.menu = QMenu()
        self.w = 100  # ширина области, в которой курсор определяет точки на слое
        self.luminary_as_feature = -1

    def init_custom_menu(self):
        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.create_context_menu)
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

    def create_context_menu(self, pos):
        """
        создание контекстного меню
        :param pos:
        :return:
        """

        luminary = self.is_near_luminaries(pos.x(), pos.y()) #list
        if not luminary:
            print ("Not lum")
        # отладка
        luminary = [1L]
        status = 6
        Qgis_iface().modify_status_luminary(status, 2L, self.lumlayer)
        self.canvas.refresh()
        self.luminary_as_feature = self.feature_dict[luminary[0]]
        luminary_as_point = Qgis_iface().get_coordinates_featuer(luminary[0], self.lumlayer) # получить координаты фонаря, что бы менюшка появилась как раз по центру; предполагается, что будет только один и скорее всего единственный

        self.menu.addAction(self.on_action_)
        self.menu.addAction(self.off_action_)
        self.menu.addAction(self.on_off_action_)
        self.menu.addAction(self.some_cmd_)
        self.menu.exec_(self.canvas.mapToGlobal(QPoint(*luminary_as_point)))

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
            print("on", self.luminary_as_feature)
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
            print("off", self.luminary_as_feature)
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
        return self.luminary_as_feature

    def get_area_near_cursor(self, x, y):
        w=self.w
        p1 = self.canvas.getCoordinateTransform().toMapCoordinates(x - w, y - w)
        p2 = self.canvas.getCoordinateTransform().toMapCoordinates(x + w, y + w)
        # p1 = QgsPoint(x - w, y - w)
        # p2 = QgsPoint(x + w, y + w)

        return QgsRectangle(p1, p2)

    def get_pos(self, obj):
        return obj.pos().x(), obj.pos().y()

    def get_cur_luminary(self, x, y):
        intersect = self.ind_luminaries.intersects(self.get_area_near_cursor(x, y))
        return intersect[0] if intersect else None

    # перемещение курсора
    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.is_near_luminaries(x, y):
            feature_id = self.get_cur_luminary(x, y)

    # нажатие клавиши
    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.create_context_menu(event.pos())

    def is_near_luminaries(self, x, y):
        intersect = self.ind_luminaries.intersects(self.get_area_near_cursor(x, y))
        return intersect

    def set_cur_luminary(self, feature_id):
        self.luminary_as_feature = feature_id