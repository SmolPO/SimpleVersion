from MyQgisIface import Qgis_iface
class handlers_commands():
    def __init__(self, layer, wnd):
        self.layer = layer
        self.wnd = wnd


    def on_light(self, features_id):
        Qgis_iface().set_on_light(features_id)
        pass

    def off_light(self, features_id):
        Qgis_iface().set_off_light(features_id)
        pass