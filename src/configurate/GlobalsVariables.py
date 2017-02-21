# coding=utf-8
class Global_variables:

    def __init__(self):
        self.__self_id__ = 1
        self.__PORT__ = 27000
        self.__server_ip__ = 'localhost'
        self.__MAX_CONNECT__ = 10
        self.__BUFFER_SIZE__ = 30
        self.__my_type__ = 'Cl'
        self.__luminaries_name__ = 'lum_point'

    def set_self_id(self, val):
        self.__self_id__ = val

    def set_server_ip(self, val):
        self.__server_ip__ = val

    def set_port(self, val):
        self.__PORT__ = val

    def set_my_type(self, val):
        self.__my_type__ = val

    def set_luminaries_name(self, val):
        self.__luminaries_name__ = val

    def get_luminaries_name(self):
        return self.__luminaries_name__

    def get_self_id(self):
        return self.__self_id__

    def get_server_ip(self):
        return self.__server_ip__

    def get_port(self):
        return self.__PORT__

    def get_my_type(self):
        return self.__my_type__

global_data = Global_variables()