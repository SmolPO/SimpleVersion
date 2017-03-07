# coding=utf-8

from threading import Thread

import Commands as CMD
import Config as cnf
from DataBase import Data_Base as DB
from Handlers import handlers_commands
from MsgBox import *
class Recv_Handler(Thread):
    """

    """
    is_conn = True # есть ли связь с клиентом
    sock       = None
    connection = None

    def __init__(self, socket, wnd):
        Thread.__init__(self)
        self.sock    = socket
       # self.connection = connection
        self.wnd = wnd
        self.packet = cnf.init_ntuple_data_message()
        self.handler_command = handlers_commands(wnd.luminary, wnd)
        pass

    def run(self):
        print("recv handler start...")
        while self.is_conn:
            # CLIENT___________________________________________________
            # инициализируем и чистим значения при последующих циклах
            pack            = []  # сборка цепочки сообщений
            size_next_mess  = 0
            current_message = cnf.init_ntuple_data_message()
            msg = None
            try:
                msg = self.sock.recv(cnf.SIZE_HEADER)
            except:
                er_message_box("reset connect")
                DB().mess_to_log("reset connect...")
                self.close_session()
                return
            print("new message...  ", msg)
            if not msg:
               self.close_session()
               return
            current_message = cnf.from_bytes_get_data_message(bytes(msg))
            if not current_message:
                self.close_session()
                return
            self._add_to_packet_from_main_header_(current_message)
            while current_message.size_next > 0:
                current_message = cnf.from_bytes_get_data_message(bytes(self.sock.recv(size_next_mess)))
                if not current_message or self.check_mess(current_message):
                    DB().mess_to_log("dont have data or is not good...\n -->> ", current_message)
                    self.close_session()
                    return
                else:
                    pack.append(current_message.data)

            print("принято!!!")
            self._add_datas_in_packet_(pack)
            self._analise_packet_(self.packet)

            pass
        pass #ошибка: разрыв соединения

    def _analise_packet_(self, packet):
        print(packet)
        self.wnd.add_message_to_message_list(packet)
        if packet == cnf.init_ntuple_data_message():
            print("empty packet...")
            return False

        feature_id = self._get_luminaries_feat_from_id_(packet)
        if packet.cmd == CMD.OFF_LIGHT:
            self.handler_command.off_light(feature_id)
            print("OFF LIGHT")
        elif packet.cmd == CMD.ON_LIGHT:
            self.handler_command.on_light(feature_id)
            print("ON LIGHT")
        elif packet.cmd:
            print("SOME CMD")
        return True

    def _get_luminaries_feat_from_id_(self, id):
        iter = self.wnd.lumlayer.getFeatures()
        for feat in iter:
            attrs = cnf.ntuple_attrs(*feat.attributes())
            if attrs.id == id:
                return feat
        return None

    def _get_sender_as_feature_id_(self, packet):
        """
        возвращает id отправителя.
        :param packet:
        :return:
        """
        return packet.sender

    # преорабразование сообщения
    def _parse_message_(self, mess):
        """
        аналог функции from_bytes_to_data_mesage(), только разбивает байты
        не используется
        :param mess: bytes
        :return: ntuple_data_message, size_next_mess
        """
        id_ = int(mess[cnf.id_slice])
        cmd = int(mess[cnf.cmd_slice])
        sender = int(mess[cnf.sender_slice])
        receiver = int(mess[cnf.receiver_slice])
        data = int(mess[cnf.data_slice])
        size_next_mess = int(mess[cnf.size_next_mess_slice])

        return cnf.ntuple_data_message(id_, cmd, sender, receiver, data, size_next_mess), size_next_mess

    def _parse_data_(self, mess):
        """
        парсит последующие после ЗС сообщения
        не используется
        :param mess:
        :return: data, size
        """
        data = bytes(mess[cnf.data_slice])
        size_next = int(mess[cnf.size_next_mess_slice])

        return data, size_next

    # добавление в переменные класса
    def _add_to_packet_from_main_header_(self, main_hdr):

        self.packet = self.packet._replace(
            id=main_hdr.id,
            cmd=main_hdr.cmd,
            sender=main_hdr.sender,
            recv=main_hdr.recv,
            size_next=main_hdr.size_next,
            data=main_hdr.data
        )

    def _add_datas_in_packet_(self, data):

        if not data:
            data_to_str = ''
        else:
            data_to_str = ''.join(data)  # преобразование списка в строку
        self.packet = self.packet._replace(data=(str(self.packet.data) + data_to_str))

        self.packet = cnf.ntuple_data_message(
            self.packet.id,
            self.packet.cmd,
            self.packet.sender,
            self.packet.recv,
            self.packet.size_next,
            str(self.packet.data) + data_to_str,
        )

    # проверка сообщения, что сообщения относятся к одной цепочке собщений
    def check_mess(self, mess):
        """
        проверяет, что поля cmd и sender соответствуют данным из текущего пакета
        :param mess:
        :return:
        """
        if mess[0] != self.packet.id:
            DB().mess_to_log("dont match id")
            return False

        if mess[1] != self.packet.cmd:
            DB().mess_to_log("dont match cmd")
            return False

        if mess[2] != self.packet.sender:
            DB().mess_to_log("dont match sender")
            return False
        if mess[3] != self.packet.recv:
            DB().mess_to_log("dont match receiver")
            return False

        return True

    def close_session(self):
        Recv_Handler.is_conn = False
        er_message_box("reset connect... (((")
        DB().mess_to_log("reset connect...")
        self.sock.close()




