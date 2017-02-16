# coding=utf-8

from threading import Thread

import Configurate as cnf
from DataBase import Data_Base as DB
import Commands as CMD
import _test_
from message_box import *
class Recv_Handler(Thread):
    """

    """
    is_conn = True # есть ли связь с клиентом
    sock       = None
    connection = None

    def __init__(self, socket, connection=None):

        Thread.__init__(self)
        print("recv handler init begin")
        self.sock    = socket
        self.connection = connection
        self.packet = cnf.init_ntuple_data_message()
        print("recv handler init ok")
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

            self.add_to_packet_from_main_header(current_message)

            while current_message.size_next > 0:
                current_message = cnf.from_bytes_get_data_message(bytes(self.sock.recv(size_next_mess)))
                if not current_message or self.check_mess(current_message):
                    DB().mess_to_log("dont have data or is not good...\n -->> ", current_message)
                    self.close_session()
                    return
                else:
                    pack.append(current_message.data)

            # прием закончен, добавить в CacheClient
            print("принято!!!")
            self._add_datas_in_packet(pack)
            self.analise_packet(self.packet)

            pass
        pass #ошибка: разрыв соединения

    def analise_packet(self, packet):
        print(packet)
        if packet == cnf.init_ntuple_data_message():
            er_message_box("empty packet...")
            return False
        if packet.cmd == CMD.OFF_LIGHT:
            er_message_box("OFF LIGHT")
        elif packet.cmd == CMD.ON_LIGHT:
            er_message_box("ON LIGHT")
        elif packet.cmd:
            er_message_box("SOME CMD")
        return True

    # преорабразование сообщения
    def parse_message(self, mess):
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

    def parse_data(self, mess):
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
    def add_to_packet_from_main_header(self, main_hdr):

        self.packet = self.packet._replace(
            id=main_hdr.id,
            cmd=main_hdr.cmd,
            sender=main_hdr.sender,
            recv=main_hdr.recv,
            size_next=main_hdr.size_next,
            data=main_hdr.data
        )

    def _add_datas_in_packet(self, data):

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

    # проверка сообщения
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

        _test_.is_connect = False




