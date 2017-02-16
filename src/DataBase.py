# coding=utf-8
from threading import Thread

class Data_Base:
    """
    интерфейс БД на серваке
    """
    ER_MESSADE_ISNOT_SEND = "Сообщение не отправлено"
    def __init__(self):
        pass

    def mess_to_log(self, mess, *args):
        print(mess)
        pass

if __name__ == '__main__':
    Data_Base().mess_to_log("Тест", (7, 3, 4))