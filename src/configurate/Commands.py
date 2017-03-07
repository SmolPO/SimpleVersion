# coding=utf-8

ON_LIGHT = 1
OFF_LIGHT = 2
DISCONNECT = 3

class Commands:
    """
    команды
    0   - 99  - клиент
        0  - 30  - база данных
        31 - 50  - управление светом
        51 - 101 - прочие
    101 - 199 - сервер
    201 - 299 - ПП
    301 - 399 - СВ

    """

    class SrvCmd:
        DISCONN_SV  = 101
        NEW_PP      = 102
        CMD_FROM_PP = 103
        CMD_FROM_SV = 104
        NEW_MAP     = 105
        TAKE_DB     = 106
        NOT_ANSWER  = 107

    class ClnCmd:
     # data
        GET_DB      = 1
        GET_MAP     = 2
    # controlLight
        ON_LIGHT    = 11
        OF_LIGTH    = 12
        WINK        = 13
    # with analis
        SET_NEW_MAP = 21

    class PPCmd:
        CONNECT_SV  = 201
        DIS_CONN_SV = 202
        PROBLEM_SV  = 203

    class SVCmd:
        ON_LIGHT    = 301
        OF_LIGTH    = 302
        PROBLEM     = 303

def get_text_message_from_cmd(cmd):
    """
    получить текствое сообщение ипо номеру команды
    :param cmd:
    :return:
    """
    if cmd == ON_LIGHT:
        return u"включени"
    elif cmd == OFF_LIGHT:
        return u"выключени"
    elif cmd == DISCONNECT:
        return u"разрыв соединения"