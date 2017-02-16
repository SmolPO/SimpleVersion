# coding=utf-8
"""
   что делает
   1) отправить сообщение
   2) получить и отобразить в консольке

"""
from threading import Thread

from DataBase import Data_Base as DB
from SendHandler import Send_Handler
from connection import Connection
from RecvHandler import Recv_Handler

is_connect = True

class TestClient(Thread):


    recv_handler = None
    sock = None
    connection = None

    def __init__(self):
        Thread.__init__(self)
        self.connection = Connection()
        self.sock = self.connection.connect()
        if not self.sock:
            print("Dont have connect to server....")
            return

        self.recv_handler = Recv_Handler(self.connection.sock)
        self.recv_handler.start()

        global is_connect
        is_connect = True

    def run(self):
        self.recv_handler.start()
        #while True:

            #while is_connect:
                # chose = input("Установить соединение с сервером? Д/н\nДля закрытия введите К\n")
                # if chose == "Д":
                #     # соединение с сервером
                #     self.connection = Connection()
                #     self.sock = self.connection.connect()
                #     if not self.sock:
                #         DB().mess_to_log("Не удалось подключится к серверу....")
                #         continue
                #
                #     self.recv_handler = Recv_Handler(self.connection.sock)
                #     self.recv_handler.start()
                #
                #     self.is_conn = True
                #     break
                #
                # if chose == 'К':
                #     DB().mess_to_log("До свидания!")
                #     return
                # else:
                #     continue

        # while is_connect:
        #     cmd = input("Введите команду:\n")
        #     receiver = input("Введите получателя\n")
        #     print("Вы хотете отправить пакет:\n ", cmd, receiver, sep=' ; ')
        #     answer = input("Д/н\n")
        #     if answer == "Д":
        #         # отправить пакет.
        #         if not Send_Handler().send_message(cmd=cmd, receiver=receiver, sock=self.sock):
        #             print("Сообщение не отправлено")
        #             self.close_session()
        #             return
        #         DB().mess_to_log("Сообщение отправлено", cmd, receiver)
        #     else:
        #         return

    def close_session(self):
        print("разрыв соединения")
        is_connect = False
        self.recv_handler.close_session()