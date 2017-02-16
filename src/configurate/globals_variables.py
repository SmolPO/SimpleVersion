# coding=utf-8
class Global_variables:

    def __init__(self):
        self._self_id_ = 1
        self._PORT_ = 27000
        self._server_ip_ = 'localhost'
        self._MAX_CONNECT_ = 10
        self._BUFFER_SIZE_ = 30
        self._my_type_ = 'Cl'
        self._luminaries_name_ = 'lum_point'

    def set_self_id(self, val):
        self._self_id_ = val

    def set_server_ip(self, val):
        self._server_ip_ = val

    def set_port(self, val):
        self._PORT_ = val

    def set_my_type(self, val):
        self._my_type_ = val

    def set_luminaries_name(self, val):
        self._luminaries_name_ = val

    def get_luminaries_name(self):
        return self._luminaries_name_

    def get_self_id(self):
        return self._self_id_

    def get_server_ip(self):
        return self._server_ip_

    def get_port(self):
        return self._PORT_

    def get_my_type(self):
        return self._my_type_

global_data = Global_variables()