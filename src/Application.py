# coding=utf-8


import sys
from threading import Thread

from PyQt4.Qt import *

import MainWindow

class Application(Thread):
    """
    читает конфиг
    запускает
    """
    Connect = None
    Wnd = None
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = QApplication(sys.argv)
        app.setStyle("Cleanlooks")

        QgsApplication.setPrefixPath("/usr", True)
        QgsApplication.initQgis()

        self.inerface = MainWindow()
        self.inerface.show()

        retval = app.exec_()

        QgsApplication.exitQgis()
        sys.exit(retval)

        print("Client starting...")
        self.inerface.join()
        print("Application end...")


