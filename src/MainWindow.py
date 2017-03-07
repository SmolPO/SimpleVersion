# coding=utf-8
from qgis.gui import *
from qgis.core import * #QgsApplication
from PyQt4 import QtCore

import sys
from itertools import count
import Config
from Config import ntuple_attrs
from Connection_ import Connection_
from Commands import *
from GlobalsVariables import global_data as glb_d

from MainWindow_ui import Ui_MainWindow
from MsgBox import *
from SendHandler import Send_Handler
from ToolMapInfo import ToolMapInfo

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        settings = QSettings("MPEI", "LightControlClient")
        #        self.restoreGeometry(settings.value("geometry").toByteArray())
        #       self.restoreState(settings.value("windowState").toByteArray())
        Config.address_db = "empty"
        print (Config.address_db)

        self.init_canvas()
        self.iface = QgisInterface
        #self.layer_load()
        self.project = QgsProject.instance()
        self.project_load()

         # индексировнаие слоя luminaries
        self.init_index_luminaries()
        # приязать карту на формочку
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        self.connection = Connection_(self)

        self.init_tools()
        self.init_components()
        self.init_luminaries()
        self.canvas.show()
        self.canvas.refresh()
        self.pan()

      # ---- Соединение и общение с сервером ----
    def connect_(self):
       self.connection.connect()

    def send_cmd(self):
        Send_Handler().send_some_cmd(self.connection)

    ### ---- сообщение об ошибки соединения с сервером ----

    def treeItemDoubleClicked(self, item, column):
        """
        переход к фонарю на карте при нажатие на иконку справа на панеле
        :param item: сам элемент
        :param column: номер колонки, по которой нажали
        :return:
        """
        if item.childCount() > 0: return
        name_luminaries = item.data(0, 0) # получить текст из первого поля в строке в дереве фонарей
        feat = self.find_luminary_from_name(name_luminaries)
        rect = QgsRectangle()
        rect.scale(self.canvas.scale(), feat.geometry().asPoint())
        self.canvas.setExtent(rect)
        self.canvas.refresh()

    # ---- инструменты карты ----
    def zoom_in(self):
        self.canvas.setMapTool(self.tool_zoom_in)

    def zoom_out(self):
        self.canvas.setMapTool(self.tool_zoom_out)

    def pan(self):
        self.canvas.setMapTool(self.tool_pan)

    def zoom_full(self):
        self.canvas.zoomToFullExtent()

    def point(self):
        self.canvas.setMapTool(self.tool_map_info)

    # --- инициализация элементов --- #
    def init_index_luminaries(self):
        self.ind_luminaries = QgsSpatialIndex()
        self.add_layer_to_index(self.lumlayer)

    def init_canvas(self):
        self.canvas = QgsMapCanvas()
        # Çàäàåì öâåò ôîíà êàðòû
        self.canvas.setCanvasColor(QColor(255, 255, 255))
        self.canvas.enableAntiAliasing(True)

    def init_tools(self):
        self.tool_pan = QgsMapToolPan(self.canvas)
        self.tool_pan.setAction(self.mpActionPan)
        self.tool_zoom_in = QgsMapToolZoom(self.canvas, False)
        self.tool_zoom_in.setAction(self.mpActionZoomIn)
        self.tool_zoom_out = QgsMapToolZoom(self.canvas, True)
        self.tool_zoom_out.setAction(self.mpActionZoomOut)
        self.tool_map_info = ToolMapInfo(self.canvas, self.ind_luminaries, self.feature_dict, self.connection, self.lumlayer)
        self.tool_map_info.setAction(self.mpActionIndetity)

        self.connect(self.mpActionZoomIn, SIGNAL("triggered()"), self.zoom_in)
        self.connect(self.mpActionZoomOut, SIGNAL("triggered()"), self.zoom_out)
        self.connect(self.mpActionPan, SIGNAL("triggered()"), self.pan)
        self.connect(self.mpActionZoomFullExtent, SIGNAL("triggered()"), self.zoom_full)
        self.connect(self.mpActionIndetity, SIGNAL("triggered()"), self.point)
        self.connect(self.mpLoadLayer, SIGNAL("triggered()"), self.layer_load)
        self.connect(self.mpLoadProject, SIGNAL("triggered()"), self.project_load)
        self.connect(self.mpActionIndetity, SIGNAL("triggered()"), self.point)

        self.connect(self.connection_to_server_, SIGNAL("triggered()"), self.connect_)
        self.connect(self.mpSend_cmd, SIGNAL("triggered()"), self.send_cmd)
        # дерево элементов
        self.connect(self.treeWidget, SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.treeItemDoubleClicked)

    def init_components(self):
        self.icon_on = QIcon(":/images/bulb_on.png")  # включенный фонарь
        self.icon_off = QIcon(":/images/bulb_off.png")  # выкюченный фонарь

        self.topA = QTreeWidgetItem(["LINE_A", "", ""], 0)
        self.topB = QTreeWidgetItem(["LINE_B", "", ""], 0)
        self.topC = QTreeWidgetItem(["LINE_C", "", ""], 0)
        self.topD = QTreeWidgetItem(["LINE_D", "", ""], 0)

        self.treeWidget.addTopLevelItem(self.topA)
        self.treeWidget.addTopLevelItem(self.topB)
        self.treeWidget.addTopLevelItem(self.topC)
        self.treeWidget.addTopLevelItem(self.topD)
        self.treeWidget.sortItems(0, Qt.AscendingOrder)

        self.model = QStandardItemModel(3, 4)
        self.model.setHeaderData(0, Qt.Horizontal, u"Время")
        self.model.setHeaderData(1, Qt.Horizontal, u"Линия")
        self.model.setHeaderData(2, Qt.Horizontal, u"Светильник")
        self.model.setHeaderData(3, Qt.Horizontal, u"Тип аварии")

        self.model.setData(self.model.index(0, 0), u"19.06.2011 23:00:45", Qt.DisplayRole);
        self.model.setData(self.model.index(0, 1), u"LINE_A", Qt.DisplayRole);
        self.model.setData(self.model.index(0, 2), u"A06", Qt.DisplayRole);
        self.model.setData(self.model.index(0, 3), u"Неверный режим МГЛ", Qt.DisplayRole);

        self.model.setData(self.model.index(1, 0), u"20.06.2011 01:15:23", Qt.DisplayRole);
        self.model.setData(self.model.index(1, 1), u"LINE_A", Qt.DisplayRole);
        self.model.setData(self.model.index(1, 2), u"A15", Qt.DisplayRole);
        self.model.setData(self.model.index(1, 3), u"Отказ МГЛ", Qt.DisplayRole);

        self.model.setData(self.model.index(2, 0), u"20.06.2011 03:25:38", Qt.DisplayRole);
        self.model.setData(self.model.index(2, 1), u"LINE_A", Qt.DisplayRole);
        self.model.setData(self.model.index(2, 2), u"A16", Qt.DisplayRole);
        self.model.setData(self.model.index(2, 3), u"Потеря связи", Qt.DisplayRole);

        self.progressBar = QProgressBar()
        self.progressBar.setValue(-1)
        self.progressBar.setMaximumWidth(286)
        self.progressBar.setMaximumHeight(15)
        self.statusBar.addPermanentWidget(self.progressBar, 1)

        self.msg_model = QStandardItemModel(3, 2)
        self.msg_model.cur_msg = count()

        self.msg_model.setHeaderData(0, Qt.Horizontal, u"Фонарь")
        self.msg_model.setHeaderData(1, Qt.Horizontal, u"Сообщение")
        number_row = self.msg_model.cur_msg.next()
        self.msg_model.setData(self.msg_model.index(number_row, 0), u"A1", Qt.DisplayRole);
        self.msg_model.setData(self.msg_model.index(number_row, 1), u"включение", Qt.DisplayRole);

        self.listErrors.setModel(self.model)
        self.listMessage.setModel(self.msg_model)

        # инициализация и загрузка

    def project_load(self):
        self.lumlayer = QgsVectorLayer()
        # открывает проектный файл и перебирает слои!!!
        projectPath = QFileDialog.getOpenFileName(self, u"Открыть файл", "/home/kis/LC/SimpleVersion/SimpleClient/map",
                                                  u"QgsProject (*.qgs);;Все файлы(*.*)")
        self.project.read(QtCore.QFileInfo(projectPath))
        point_layer, line_layer, polygom_layer = [], [], []
        POINT_TYPE, LINE_TYPE, POLYGON_TYPE = 0, 1, 2
        for k, v in QgsMapLayerRegistry.instance().mapLayers().iteritems():

            if v.name() == glb_d.get_luminaries_name():
                self.lumlayer = v
            if v.geometryType() == POINT_TYPE:
                point_layer.append(QgsMapCanvasLayer(v))
            elif v.geometryType() == LINE_TYPE:
                line_layer.append(QgsMapCanvasLayer(v))
            elif v.geometryType() == POLYGON_TYPE:
                polygom_layer.append(QgsMapCanvasLayer(v))
            self.canvas.setExtent(v.extent())

        point_layer.append(QgsMapCanvasLayer(self.lumlayer))
        self.layers = point_layer + line_layer + polygom_layer
      #  self.canvas.setExtent(self.lumlayer.extent())
        self.canvas.setLayerSet(self.layers)
        self.zoom_full()

    def layer_load(self):
        """
        :return:
        """
        project_path = QFileDialog.getOpenFileName(self, u"Открыть файл", "/home/kis/LC/SimpleVersion/SimpleClient/map",
                                                   u"QgsProject (*.shp);;Все файлы(*.*)")
        self.lumlayer = QgsVectorLayer()
        self.lumlayer = QgsVectorLayer(project_path, 'luminaries', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(self.lumlayer)
        self.canvas.setExtent(self.lumlayer.extent())
        self.canvas.setLayerSet([QgsMapCanvasLayer(self.lumlayer)])
        self.zoom_full()

    def add_layer_to_index(self, layer=None):  # ругается на layer=self.luminary
        if not layer:
            layer = self.lumlayer

        self.feature_dict = {f.id(): f for f in layer.getFeatures()}

        self.ind_luminaries = QgsSpatialIndex()
        for f in self.feature_dict.values():
            self.ind_luminaries.insertFeature(f)

    def init_luminaries(self):
        # добавление списка узлов
        # TODO заменить attrs на numtaples
        iter = self.lumlayer.getFeatures()
        not_working = 1
        broke = 2
        on_light = 3
        off_light = 4
        line_A = 1
        line_B = 2
        line_C = 3
        for feat in iter:
            attrs = ntuple_attrs(*feat.attributes())
            lum = QTreeWidgetItem(["%s" % (attrs.name), "", ""])
            lum.setData(0, Qt.UserRole, feat.id())
            if attrs.status == on_light:
                lum.setIcon(1, self.icon_on)
                lum.setIcon(2, self.icon_on)
            elif attrs.status == off_light:
                lum.setIcon(1, self.icon_off)
                lum.setIcon(2, self.icon_on)
            elif attrs.status == broke:
                lum.setIcon(1, self.icon_off)
                pink = QColor("pink")
                lum.setBackgroundColor(1, pink)
                lum.setIcon(2, self.icon_on)
            elif attrs.status == not_working:
                lum.setIcon(1, self.icon_off)
                lum.setIcon(2, self.icon_off)
                pink = QColor("pink")
                lum.setBackgroundColor(0, pink)
                lum.setBackgroundColor(1, pink)
                lum.setBackgroundColor(2, pink)

            if attrs.line == line_A:
                self.topA.addChild(lum)
            elif attrs.line == line_B:
                self.topB.addChild(lum)
            elif attrs.line == line_C:
                self.topC.addChild(lum)
            else:
                self.topD.addChild(lum)


    def add_message_to_message_list(self, message):
        """
        из пакета получает отправителя, затем по нему отпределяет имя фонаря
        по команде выбирает текст сообщения, выводит его
        :param message:
        :return:
        """
        sender = message.sender
        feature, attrs = self.find_luminary_from_id(sender)
        number_row = self.msg_model.cur_msg.next()
        cmd = message.cmd
        text_message_to_model = get_text_message_from_cmd(cmd)
        self.msg_model.setData(self.msg_model.index(number_row, 0), attrs.name, Qt.DisplayRole);
        self.msg_model.setData(self.msg_model.index(number_row, 1), text_message_to_model, Qt.DisplayRole);

    # поиск фонарей по атрибутам
    def find_luminaries_from_status(self, status):
        features = []
        iter = self.lumlayer.getFeatures()
        for feat in iter:
            attrs = ntuple_attrs(*feat.attributes())
            if attrs.status == status:
                features.append([feat, attrs])
        return features

    def find_luminary_from_id(self, feature_id):
        """
        возвращает feature
        :param feature_id:
        :return:
        """
        iter = self.lumlayer.getFeatures()
        for feat in iter:
            attrs = ntuple_attrs(*feat.attributes())
            if attrs.id == feature_id:
                return feat, attrs

    def find_luminary_from_name(self, name):
        iter = self.lumlayer.getFeatures()
        for feat in iter:
            attrs = ntuple_attrs(*feat.attributes())
            if attrs.name == name:
                return feat, attrs

    def find_lumonaries_from_line(self, line):
        features = []
        iter = self.lumlayer.getFeatures()
        for feat in iter:
            attrs = ntuple_attrs(*feat.attributes())
            if attrs.id == line:
                features.append([feat, attrs])
        return features

    def closeEvent(self, event):
        settings = QSettings("MPEI", "LightControlClient")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        QMainWindow.closeEvent(self, event)


def main(app):

    QgsApplication.setPrefixPath("/usr", True)
    QgsApplication.initQgis()

    wnd = MainWindow()
    wnd.show()

    retval = app.exec_()

    QgsApplication.exitQgis()
    sys.exit(retval)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle("Cleanlooks")
    main(app)


# def main():
#     app_ = Application()
#     app_.start()
#     print("Application start....")
#     app_.join()
#     print("Exit")


if __name__ == '__main__':
    main()


        # def add_poligon_or_line(self):
#     r = QgsRubberBand(self.canvas, False)  # False = not a polygon
#     points = [QgsPoint(0, 0), QgsPoint(50, 50), QgsPoint(60, -60)]
#     r.setToGeometry(QgsGeometry.fromPolyline(points), None)
#     r.setColor(QColor(0, 0, 255))
#     r.setWidth(3)
#
#     rv = QgsRubberBand(self.canvas, True)  # True = a polygon
#     points = [[QgsPoint(0, 0), QgsPoint(-10, -10), QgsPoint(20, 20)]]
#
#     rv.setToGeometry(QgsGeometry.fromPolygon(points), None)
#     rv.setColor(QColor(0, 0, 255))
#     rv.setWidth(3)


    ### нарисовать что либо  в этой точке
    # self.point = self.toMapCoordinates(e.pos())
    # print (self.point.x(), self.point.y())
    # m = QgsVertexMarker(self.canvas)
    # m.setCenter(self.point)
    # m.setColor(QColor(0, 255, 0))
    # m.setIconSize(5)
    # m.setIconType(QgsVertexMarker.ICON_BOX)  # or ICON_CROSS, ICON_X
    # m.setPenWidth(3)

# retreive every feature with its geometry and attributes

        # iface = iface.activeLayer()  # your layer
        # fid = 10  # your feature id
        #
        # f = iface.getFeatures(QgsFeatureRequest(fid)).next()
        # r = QgsRubberBand(iface.mapCanvas())
        # r.setColor(Qt.red)
        # r.setToGeometry(f.geometry(), l)
        # r.show()

        # while provider:
        #     attrs = feat.attributeMap()
        #     lum = QTreeWidgetItem(["%s" % (attrs[1].toString()), "", ""])
        #     lum.setData(0, Qt.UserRole, QVariant(feat.id()))
        #     if attrs[4] == 4:
        #         lum.setIcon(1, self.icon_on)
        #         lum.setIcon(2, self.icon_on)
        #     elif attrs[4] == 3:
        #         lum.setIcon(1, self.icon_off)
        #         lum.setIcon(2, self.icon_on)
        #     elif attrs[4] == 1:
        #         lum.setIcon(1, self.icon_off)
        #         pink = QColor("pink")
        #         lum.setBackgroundColor(1, pink)
        #         lum.setIcon(2, self.icon_on)
        #     elif attrs[4] == 0:
        #         lum.setIcon(1, self.icon_off)
        #         lum.setIcon(2, self.icon_off)
        #         pink = QColor("pink")
        #         lum.setBackgroundColor(0, pink)
        #         lum.setBackgroundColor(1, pink)
        #         lum.setBackgroundColor(2, pink)
        #     if attrs[2] == 1:
        #         topA.addChild(lum)
        #     elif attrs[2] == 2:
        #         topB.addChild(lum)
        #     elif attrs[2] == 3:
        #         topC.addChild(lum)

#  provider = self.lumlayer.dataProvider()
#   feat = QgsFeature()
# if provider.featureAtId(item.data(0, Qt.UserRole).toInt()[0], feat):
