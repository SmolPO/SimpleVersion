# coding=utf-8

import socket

import Configurate as cnf

from MsgBox import *
from RecvHandler import Recv_Handler
from DataBase import Data_Base as DB
from GlobalsVariables import global_data as glb_d

class Connection_:

    def __init__(self, wnd):
        self.recv_handler = None
        self.sock = None
        self.is_connect = False
        self.wnd = wnd

    def connect(self):
        if self.is_connect:
            self.close_connect()
            ok_message_box("Reset connect")
            return

        print("connection start....")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self.sock.connect((cnf.server_address, cnf.PORT)) == -1:
                er_message_box("Not connect")
                return False
        except:
            er_message_box("Not connect")
            return False

        if not self.authentication(self.sock):
            er_message_box("It is bad server!...")
            return False
        self.is_connect = True
        self.recv_handler = Recv_Handler(self.sock, self.wnd)
        self.recv_handler.start()
        ok_message_box("You are wellcome!")
        return True

    def authentication(self, sock=None):

        try:
            if not sock.send(cnf.MY_TYPE):
                er_message_box("Пароль не отправлен")
                return False
            data = sock.recv(1)
            if not data:
                er_message_box("Ответ не получен")

            # записать свой ID в класс global_variables
            glb_d.set_self_id(data)

            return True
        except:
            return False

    def get_my_id(self, sock):
        #
        buffer = sock.recv(cnf.SIZE_ID)
        try:
            id_ = int(buffer)
            return id_
        except:
            return None

    def close_connect(self):
        if not self.sock:
            return
        self.sock.close()
        self.is_connect = False

