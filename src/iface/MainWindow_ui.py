# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Jun 20 19:30:00 2011
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(893, 764)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.ForceTabbedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout_6.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.dockListWidget = QtGui.QDockWidget(MainWindow)
        self.dockListWidget.setMinimumSize(QtCore.QSize(218, 440))
        self.dockListWidget.setSizeIncrement(QtCore.QSize(20, 20))
        self.dockListWidget.setFloating(False)
        self.dockListWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockListWidget.setObjectName("dockListWidget")
        self.dockWidgetListContent = QtGui.QWidget()
        self.dockWidgetListContent.setObjectName("dockWidgetListContent")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetListContent)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetListContent)
        self.treeWidget.setMinimumSize(QtCore.QSize(200, 400))
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setDefaultSectionSize(100)

        self.verticalLayout.addWidget(self.treeWidget)
        self.dockListWidget.setWidget(self.dockWidgetListContent)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockListWidget)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetWarningContent = QtGui.QWidget()
        self.dockWidgetWarningContent.setObjectName("dockWidgetWarningContent")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetWarningContent)
        self.verticalLayout_4.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetWarningContent)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabErrors = QtGui.QWidget()
        self.tabErrors.setObjectName("tabErrors")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabErrors)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.listErrors = QtGui.QTableView(self.tabErrors)
        self.listErrors.setGridStyle(QtCore.Qt.DotLine)
        self.listErrors.setObjectName("listErrors")
        self.verticalLayout_3.addWidget(self.listErrors)

        self.tabWidget.addTab(self.tabErrors, "")
        self.tabWarning = QtGui.QWidget()
        self.tabWarning.setObjectName("tabWarning")

        self.horizontalLayout = QtGui.QHBoxLayout(self.tabWarning)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.listWarning = QtGui.QTableView(self.tabWarning)
        self.listWarning.setObjectName("listWarning")
        self.horizontalLayout.addWidget(self.listWarning)

        self.tabWidget.addTab(self.tabWarning, "")
        self.tabMessage = QtGui.QWidget()
        self.tabMessage.setObjectName("tabMessage")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tabMessage)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.listMessage = QtGui.QTableView(self.tabMessage)
        self.listMessage.setObjectName("listMessage")

        self.horizontalLayout_2.addWidget(self.listMessage)
        self.tabWidget.addTab(self.tabMessage, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.dockWidget.setWidget(self.dockWidgetWarningContent)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 21))
        self.menubar.setObjectName("menubar")
        self.menuMap = QtGui.QMenu(self.menubar)
        self.menuMap.setObjectName("menuMap")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        self.mpActionZoomIn.setCheckable(True)

        iconZoomIn = QtGui.QIcon()
        iconZoomIn.addPixmap(QtGui.QPixmap(":/images/mActionZoomIn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconZoomOut = QtGui.QIcon()
        iconZoomOut.addPixmap(QtGui.QPixmap(":/images/mActionZoomOut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconAcPan = QtGui.QIcon()
        iconAcPan.addPixmap(QtGui.QPixmap(":/images/mActionPan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconZoomFull = QtGui.QIcon()
        iconZoomFull.addPixmap(QtGui.QPixmap("../images/ZoomFull.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconInd = QtGui.QIcon()
        iconInd.addPixmap(QtGui.QPixmap("../images/mActionIdentify.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconCon = QtGui.QIcon()
        iconCon.addPixmap(QtGui.QPixmap("../images/connect.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconConOk = QtGui.QIcon()
        iconConOk.addPixmap(QtGui.QPixmap("../images/connect_ok.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconMsg = QtGui.QIcon()
        iconMsg.addPixmap(QtGui.QPixmap("../images/some_msg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconProj = QtGui.QIcon()
        iconProj.addPixmap(QtGui.QPixmap("../images/newProject.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        iconNewVector = QtGui.QIcon()
        iconNewVector.addPixmap(QtGui.QPixmap("../images/NewVectorLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.mpActionZoomIn.setIcon(iconZoomIn)
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")
        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        self.mpActionZoomOut.setCheckable(True)

        self.mpActionZoomOut.setIcon(iconZoomOut)
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")
        self.mpActionPan = QtGui.QAction(MainWindow)
        self.mpActionPan.setCheckable(True)

        self.mpActionPan.setIcon(iconAcPan)
        self.mpActionPan.setObjectName("mpActionPan")
        self.mpActionZoomFullExtent = QtGui.QAction(MainWindow)

        self.mpActionZoomFullExtent.setIcon(iconZoomFull)
        self.mpActionZoomFullExtent.setObjectName("mpActionZoomFullExtent")

        self.mpActionIndetity = QtGui.QAction(MainWindow)
        self.mpActionIndetity.setIcon(iconInd)
        self.mpActionIndetity.setObjectName("mpActionIndtity")

        self.mpLoadLayer = QtGui.QAction(MainWindow)
        self.mpLoadLayer.setIcon(iconNewVector)
        self.mpLoadLayer.setObjectName("mpLoadLayer")

        self.mpLoadProject = QtGui.QAction(MainWindow)
        self.mpLoadProject.setIcon(iconProj)
        self.mpLoadProject.setObjectName("mpLoadProject")

        self.connection_to_server_ = QtGui.QAction(MainWindow)
        self.connection_to_server_.setIcon(iconCon)
        self.connection_to_server_.setObjectName("connectionToServer")

        self.mpSend_cmd = QtGui.QAction(MainWindow)
        self.mpSend_cmd.setIcon(iconMsg)
        self.mpSend_cmd.setObjectName("mpSend_cmd")

        # Меню
        self.menuMap.addAction(self.mpActionPan)
        self.menuMap.addAction(self.mpActionZoomIn)
        self.menuMap.addAction(self.mpActionZoomOut)
        self.menuMap.addAction(self.mpActionZoomFullExtent)
        self.menubar.addAction(self.menuMap.menuAction())
        self.menuMap.addAction(self.mpActionIndetity)
        self.menuMap.addAction(self.mpLoadLayer)
        self.menuMap.addAction(self.mpLoadProject)

        self.toolBar.addAction(self.mpActionPan)
        self.toolBar.addAction(self.mpActionZoomIn)
        self.toolBar.addAction(self.mpActionZoomOut)
        self.toolBar.addAction(self.mpActionZoomFullExtent)
        self.toolBar.addAction(self.mpActionIndetity)

        self.toolBar.addAction(self.connection_to_server_)
        self.toolBar.addAction(self.mpSend_cmd)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "РАССВЕТ", None, QtGui.QApplication.UnicodeUTF8))
        self.dockListWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Список узлов", None, QtGui.QApplication.UnicodeUTF8))

        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "пункты", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "МГЛ", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "СД", None, QtGui.QApplication.UnicodeUTF8))

        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Журнал", None, QtGui.QApplication.UnicodeUTF8))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabErrors), QtGui.QApplication.translate("MainWindow", "Аварии", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWarning), QtGui.QApplication.translate("MainWindow", "События", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMessage), QtGui.QApplication.translate("MainWindow", "Сообщения", None, QtGui.QApplication.UnicodeUTF8))

        self.menuMap.setTitle(QtGui.QApplication.translate("MainWindow", "Карта", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Увеличение", None, QtGui.QApplication.UnicodeUTF8))

        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Уменьшение", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Перемещение", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomFullExtent.setText(QtGui.QApplication.translate("MainWindow", "Вся карта", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionIndetity.setText(QtGui.QApplication.translate("MainWindow", "точка", None, QtGui.QApplication.UnicodeUTF8))
        self.mpLoadLayer.setText(QtGui.QApplication.translate("MainWindow", "загрузить слой", None, QtGui.QApplication.UnicodeUTF8))
        self.mpLoadProject.setText(QtGui.QApplication.translate("MainWindow", "открыть проект", None, QtGui.QApplication.UnicodeUTF8))

import ResourcesRc
