# coding=utf-8
from qgis._core import QgsVectorDataProvider, QgsFeature

from Config import STATUS_LUMINARY, COLOR_STATUS

class Qgis_iface:
    def modify_all_attributes(self, feature_id, attrs, layer):
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


    def modify_from_query(self, val, field, layer):
        """
        изменение атрибутов по запросу
        :param layer:
        :param field:
        :param val:
        :return:
        """
        exp = QgsExpression("num_line ILIKE \'%1\'")
        request = QgsFeatureRequest(exp)
        attrs = [99, 99, 99, 99, "D99"]
        # TODO как по запросу изменить только некоторые поля!!!
        request.setSubsetOfAttributes(attrs)

    def add_point(self, attributes, location_point, layer):
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

    def delete_feature_from_id(self, features_id, layer):
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

    def modify_location(self, new_point, features_id, layer):
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

    def get_coordinates_featuer(self, features_id, layer):
        """
        получить координаты точки
        :param features_id:
        :param layer:
        :return: (x, y)
        """
        iter = layer.getFeatures()
        for feature in iter:
            if feature.id() == features_id:
                geom = feature.geometry().asPoint()
                return (geom.x(), geom.y())

    def get_attrs_feature(self, feature_id, layer):
        iter = layer.getFeatures()
        for feat in iter:
            if feat.id() == feature_id:
                attrs = feat.attributes()
                return attrs

    def modify_status_luminary(self, new_status, feature_id, layer):
        layer.beginEditCommand("Feature triangulation")
        layer.startEditing()
        caps = layer.dataProvider().capabilities()
        iter = layer.getFeatures()
        field_status = 3 # номер поля статус в таблице атрибутов
        attrs = [] # если цикл ниже не найдет объект, то это вызовет ошибку в коде
        attrs_as_dict = {}
        # TODO сдеалть обращение через список feat_dictinory

        for feat in iter:
            if feat.id() == feature_id:
                attrs = feat.attributes()
                attrs_as_dict = dict(id=attrs[0], line=attrs[1], status=new_status, name=attrs[3])
                break

        if caps & QgsVectorDataProvider.ChangeAttributeValues:
            tmp = layer.dataProvider()
            res = tmp.changeAttributeValues({feature_id: attrs_as_dict})
            layer.updateExtents()
            self.get_attrs_feature(feature_id, layer)
            pass

        layer.commitChanges()
        layer.endEditCommand("end")

    def modify_attr_point(self, new_attrs, features_id, layer):
        """
        изменяет атрибут элемента
        :param fid:
        :param new_attrs:
        :return:
        """
        caps = layer.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.ChangeAttributeValues:
            layer.dataProvider().changeAttributeValues({features_id: new_attrs})

    def set_on_light(self, features_id, layer):
        self.modify_status_luminary(STATUS_LUMINARY['on'], features_id, layer)
        pass

    def set_off_light(self, features_id, layer):
        self.modify_status_luminary(STATUS_LUMINARY['off'], features_id, layer)
        pass

    def set_disconnect_light(self, features_id, layer):
        self.modify_status_luminary(STATUS_LUMINARY['disconnet'], features_id, layer)
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