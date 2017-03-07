# coding=utf-8
from qgis._core import QgsVectorDataProvider, QgsFeature

from Configurate import STATUS_LUMINARY, COLOR_STATUS

class Qgis_iface:
    def modify_all_attributes(self, layer, feature_id, attrs):
        """
        изменяет значение поля атрибута
        :param layer: слой
        :param id_: id объекта
        :param field: номер поля (0 - 4)
        :param val: значение
        :return: bool
        """

        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.ChangeAttributeValue:
            res = layer.dataProvider().changeAttributes({feature_id : attrs})
            return res

    def modify_point_on_cursor(self, layer, features_id):
        """
         изменение размера объекта под курсором
        :param layer: слой
        :param features_id:
        :return:
        """
        #

        pass

    def add_point(self, layer, location_point, attributes):
        """
        добавление точки по координатам
        :param layer:
        :param point:
        :param attributes:
        :return:
        """
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.AddFeatures:
            feature = QgsFeature(layer.pendingFields())
            feature.setAttributes(attributes)  # feat.setAttribute('name', name) or feat.setAttribute(4, name)
            feature.setGeometry(QgsGeometry.fromPoint(location_point))
            res = layer.dataProvider().addFeatures([feature])
            print ("add point")
            return res
        pass

    def delete_feature_from_id(self, layer, features_id):
        """
        удаляеет точку по id
        :param layer:
        :param id:
        :return:
        """
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.DeleteFeatures:
            res = layer.dataProvider().deleteFeatures(features_id)
            return res
        pass

    def modify_location(self, layer, features_id, new_point):
        """
        изменить координаты существующей точки
        :param layer:
        :param fid:
        :param new_point:
        :return:
        """
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.ChangeGeometries:
            geom = QgsGeometry.fromPoint(new_point)
            layer.dataProvider().changeGeometryValues({features_id: geom})
        pass

    def modify_color_point(self, layer, feature_id, new_color):
        """
        установить новый цвет точки
        :param layer:
        :param id:
        :param new_color:
        :return:
        """

        pass

    def modify_status_luminary(self, layer, feature_id, new_status):
        caps = layer.dataProvider().capabilities()
        iter = layer.getFeatures()
        field_status = 3 # номер поля статус в таблице атрибутов
        attrs = None # если цикл ниже не найдет объект, то это вызовет ошибку в коде
        for feat in iter:                       # TODO получить объект по id
            if feat.id() == feature_id:
                attrs = feat.attributes()

        if caps & QgsVectorDataProvider.ChangeAttributeValue:
            attrs[field_status] = new_status;
            res = layer.dataProvider().changeAttributes({feature_id: attrs})
            return res

    def modify_attr_point(self, layer, features_id, new_attrs):
        """
        изменяет атрибут элемента
        :param fid:
        :param new_attrs:
        :return:
        """
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.ChangeAttributeValues:
            layer.dataProvider().changeAttributeValues({features_id: new_attrs})

    def set_on_light(self, layer, features_id):
        self.modify_status_luminary(layer, features_id, STATUS_LUMINARY['on'])
        self.modify_color_point(layer, features_id, COLOR_STATUS['on']) # TODO зашить цвета
        pass

    def set_off_light(self, layer, features_id):
        self.modify_status_luminary(layer, features_id, STATUS_LUMINARY['off'])
        self.modify_color_point(layer, features_id, COLOR_STATUS['off'])
        pass
    def set_disconnect_light(self, layer, feature_id):

        pass
        # radius_point = 10
        # color_green = (0, 255, 0)
        # color_black = (0, 0, 0)
        # self.point = self.toMapCoordinates(pos)
        # print (self.point.x(), self.point.y())
        # m = QgsVertexMarker(self.canvas)
        # m.setCenter(self.point)
        # m.setColor(QColor(*color_green))
        # m.setIconSize(radius_point)
        # # TODO сделать маркер нужного вида
        # m.setIconType(QgsVertexMarker.ICON_CIRCLE)  # or ICON_CROSS, ICON_X
        # m.setPenWidth(radius_point)
        # l = dir(m)
        # for i in l:
        #     print (i)
        # print ("end")
        # m.shape()
        # m.setBoundingRegionGranularity(2)
        #  m.setColor(QColor(*color_black))
        # m.setPenWidth(2)