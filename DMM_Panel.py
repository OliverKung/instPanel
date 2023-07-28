# pyBode GUI with Kivy
import numpy as np
import pyqtgraph as pg
import sys
import os,time,multiprocessing,subprocess,re
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QMessageBox,QSystemTrayIcon,QMenu
from PyQt5.QtCore import QUrl,pyqtSlot,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QIcon
import DMM_Panel_GUI
import ctypes

class mainCode(QMainWindow,DMM_Panel_GUI.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        DMM_Panel_GUI.Ui_MainWindow.__init__(self)
        self.setupUi(self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(icon)
    mainc=mainCode()
    mainc.show()
    sys.exit(app.exec_())