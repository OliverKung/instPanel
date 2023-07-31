# pyBode GUI with Kivy
import numpy as np
import pyqtgraph as pg
import sys,threading
import os,time,multiprocessing,subprocess,re
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QMessageBox,QSystemTrayIcon,QMenu,QLCDNumber
from PyQt5.QtCore import QUrl,pyqtSlot,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
import PyQt5.QtCore as QtCore
from PyQt5.QtGui import QIcon
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import DMM_Panel_GUI
import UniversalDMM
from qt_material import apply_stylesheet

class mainCode(QMainWindow,DMM_Panel_GUI.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        DMM_Panel_GUI.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.STOPButton.setEnabled(False)
        self.set_graph_ui()
        self.bind_singnal_and_slot()
        self.refresh_model()
        self.time_array=np.zeros(0,dtype=float)
        self.value_array = np.zeros(0,dtype=float)
    
    def bind_singnal_and_slot(self):
        self.Model_Refresh.clicked.connect(self.refresh_model)
        return
    
    def updateLCD(self):
        with open(".\\tmp\\currentvalue.csv","r") as f:
            self.DisplayLabel.setText(f.readline().replace("\r","").replace("\n",""))
            f.close()
    
    def refresh_model(self):
        folder_path=".\\model\\"
        for file in os.listdir(folder_path):
            if(file.endswith(".ini")):
                self.DMM_Model.addItem(file.split(".ini")[0])
    
    @pyqtSlot()
    def on_ConnectButton_clicked(self):
        self.dmm = UniversalDMM.DMM(self.IP_ADDR.text(),self.DMM_Model.currentText())
    
    def set_graph_ui(self):
        pg.setConfigOptions(antialias = True)
        win = pg.GraphicsLayoutWidget()
        self.WaveFormLayout.addWidget(win)
        self.waveform = win.addPlot()

    @pyqtSlot()
    def on_DCV_Button_clicked(self):
        self.on_STOPButton_clicked()
        if(self.dmm is not None):
            self.dmm.set_DCV()
        self.on_StartButton_clicked()
    
    @pyqtSlot()
    def on_ACV_Button_clicked(self):
        self.on_STOPButton_clicked()
        if(self.dmm is not None):
            self.dmm.set_ACV()
        self.on_StartButton_clicked()

    @pyqtSlot()
    def on_StartButton_clicked(self):
        self.thread = threading.Thread(target=self.start_jobs)
        self.thread.start()
        self.STOPButton.setEnabled(True)
        self.StartButton.setEnabled(False)
        self.time_array=np.zeros(0,dtype=float)
        self.value_array = np.zeros(0,dtype=float)

    def start_jobs(self):
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(func=self.readValue,trigger="interval",seconds = 1,id = "readvaluejob")
        self.scheduler.start()

    def readValue(self):
        value = self.dmm.read()
        self.DisplayLabel.setText(str(value))
        self.value_array=np.append(self.value_array,value)
        self.time_array=np.append(self.time_array,len(self.time_array))
        self.waveform.plot(self.time_array,self.value_array)

    
    @pyqtSlot()
    def on_STOPButton_clicked(self):
        self.scheduler.shutdown()
        self.StartButton.setEnabled(True)
        self.STOPButton.setEnabled(False)

if __name__=="__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app,theme="dark_amber.xml")
    mainc=mainCode()
    mainc.show()
    sys.exit(app.exec_())