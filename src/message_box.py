# coding=utf-8
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def er_message_box(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText(text)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Cancel)
    msg.buttonClicked.connect(er_msgbtn)

    retval = msg.exec_()

    # --- обработчик кнопки в сообщение об ошибки -----

def ok_message_box(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText(text)
    msg.setWindowTitle("Message box")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.buttonClicked.connect(ok_msgbtn)

    retval = msg.exec_()
    #print ("value of pressed message box button:", retval)

def er_msgbtn(i):
    pass

def ok_msgbtn(i):
    pass
