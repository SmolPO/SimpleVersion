# coding=utf-8


from threading import Thread
from qgis.core import *
from qgis.gui import *

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

import mainWindow

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

        self.inerface = mainWindow.MainWindow()
        self.inerface.show()

        retval = app.exec_()

        QgsApplication.exitQgis()
        sys.exit(retval)

        print("Client starting...")
        self.inerface.join()
        print("Application end...")




