# coding=utf-8
"""
формировка пакета согласно размеру данных. разбить на сообщения согласно максимальному размера пакета
"""
from itertools import count

import Config as cnf
from Commands import *
from GlobalsVariables import global_data as glb_d
from MsgBox import *


class Send_Handler:
    cur_id = count()

    def send_message(self, cmd, receiver, data, sock):

        packet_messages = self.create_packet(cmd, receiver, data)

        tmp = sock.send(packet_messages)
        print(packet_messages, tmp)
        if not tmp:
            print("dont sending message....")
            return False
        print("message is sending...", cmd, receiver)
        return True

    def create_packet(self, cmd, receiver, data):
        """
        сформировать пакет для отправки. Массив, готовый к отправке
        :param cmd:
        :param sender:
        :param data:
        :return:
        """
        id = next(self.cur_id)
        packet = []

        size_next_msg = 0
        mess = cnf.ntuple_data_message(id, cmd, glb_d.get_self_id(), receiver, size_next_msg, data)
        return cnf.to_bytes_from_data_message(mess)

    def send_file(self):
        # TODO пересылка файлов
        pass
        return

    def on_light_cmd(self, lum, sock):
        print (lum)
        if not Send_Handler().send_message(cmd=ON_LIGHT, receiver=lum, data=0, sock=sock):
            er_message_box("Cansel or uncorrect data")
            return False
        return True

    def off_light_cmd(self, lum, sock):
        print (lum)
        if not Send_Handler().send_message(cmd=OFF_LIGHT, receiver=lum, data=0, sock=sock):
            er_message_box("Cansel or uncorrect data")
            return False
        return True

    def send_some_cmd(self, conn):
        if not conn.is_connect:
            er_message_box("Not connect")
            return

        ok = QInputDialog.getText('Input cmd', 'Entry command:')
        # if not ok or not cmd.isdigit():
        #     er_message_box("Cansel or uncorrect data")
        #     return
        #
        # sender, ok = QInputDialog.getText('Input id luminaries', 'Entry id:')
        # if not ok or not cmd.isdigit():
        #     er_message_box("Cansel or uncorrect data")
        #     return
        #
        # data, ok = QInputDialog.getText(self, 'Input data', 'Entry data:')
        # if not ok or not cmd.isdigit():
        #     er_message_box("Cansel or uncorrect data")
        #     return
        #
        # if not Send_Handler().send_message(cmd=cmd, receiver=sender, data=data, sock=self.sock):
        #     er_message_box("Cansel or uncorrect data")
        #     return

        return