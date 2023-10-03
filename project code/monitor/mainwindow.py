#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
## 主窗口
##
#############################################################################

from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream,QThread
from PyQt5.QtGui import QKeySequence,QFont,QPixmap,QImage,QRgba64
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,QLabel,QPushButton,QWidget,QSpacerItem,
                             QMessageBox, QTextEdit, QGraphicsView, QTextBrowser, QGraphicsScene,QHBoxLayout,QVBoxLayout)
from PyQt5 import QtWidgets
from datetime import datetime
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')                                    #后端

from networkset import NetworkDialog
from kindset import kindDialog
from denoiseSet import DenoiseDialog
from imgRecognition import RecognitionAlgorithm
from globalData import Data
from multiThread import ReceiceImg
from soilMonitorLog import SMLog

# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.recentFileActs = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.createActions()
        self.createMenus()
        self.statusBar()


        self.img_label = QLabel("Raw geotechnical images received")
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setFont(QFont("Times new roman", 14)) #, QFont.Bold
        self.raw_img_view = QGraphicsView()

        self.pro_img_label = QLabel("Geotechnical image after image segmentation")
        self.pro_img_label.setAlignment(Qt.AlignCenter)
        self.pro_img_label.setFont(QFont("Times new roman", 14)) #, QFont.Bold
        self.segmented_img_view = QGraphicsView()

        self.chooseImgButton = QPushButton("Offline Detection")
        self.chooseImgButton.setFont(QFont("Times new roman", 14))  # , QFont.Bold
        self.onlineButton = QPushButton("Online Detection")
        self.onlineButton.setFont(QFont("Times new roman", 14))  # , QFont.Bold

        self.grayHistogram_label = QLabel("Geotechnical image after clustering")
        self.grayHistogram_label.setAlignment(Qt.AlignCenter)
        self.grayHistogram_label.setFont(QFont("Times new roman", 14))  #, QFont.Bold
        self.clustered_img_view = QGraphicsView()

        self.text_label = QLabel("Geotechnical moisture test results")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFont(QFont("Times new roman", 14))
        self.result_text = QTextBrowser()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Times new roman", 16))#, QFont.Bold
        self.hide_button = QPushButton(" ")
        self.hide_button.setFont(QFont("Times new roman", 14))  # , QFont.Bold
        leftDown_layout = QHBoxLayout()
        leftDown_layout.addWidget(self.chooseImgButton)
        leftDown_layout.addWidget(self.onlineButton)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.img_label)
        left_layout.addWidget(self.raw_img_view)
        left_layout.addWidget(self.pro_img_label)
        left_layout.addWidget(self.segmented_img_view)
        left_layout.addLayout(leftDown_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.grayHistogram_label)
        right_layout.addWidget(self.clustered_img_view)
        right_layout.addWidget(self.text_label)
        right_layout.addWidget(self.result_text)
        right_layout.addWidget(self.hide_button)
        mainlayout = QHBoxLayout()
        mainlayout.addLayout(left_layout)
        mainlayout.addLayout(right_layout)
        self.widget.setLayout(mainlayout)
        #
        self.setWindowTitle("Geotechnical Moisture Online Detection System Upper Unit")
        self.setGeometry(250,100,1080,820)

        self.chooseImgButton.clicked.connect(self.clicked_local_button)
        self.onlineButton.clicked.connect(self.clicked_online_button)

        self.networkset = None
        self.kindset = None
        self.ReceiceImgThread = None


    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def save(self):
        pass

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        information = "form  ：    humidity\n" + "form0： 0%-2.5%\n" + "form1： 2.5%-7.5%\n" + "form2： 7.5%-12.5%\n" \
                      + "form3： 12.5%-17.5%\n" + "form4： 17.5%-22.5%\n" + "form5： 22.5%及以上\n"
        # QMessageBox.setFont(QFont("Times new roman", 10))
        QMessageBox.about(self, "soil monitor","Geotechnical Moisture Online Detection System Upper Unit \n"+information)

    def cameraSetDialog(self):
        pass

    def networkDialog(self):
        self.networkset = NetworkDialog()
        self.networkset.show()

    def kindselect(self):
        self.kindset = kindDialog()
        self.kindset.show()

    def denoiseDialog(self):
        self.denoiseSet = DenoiseDialog()
        self.denoiseSet.show()

    def online_show_analysis_calculate_image(self):
        self.showImageArray(Data.raw_img_arr,self.raw_img_view)
        self.showImageArray(Data.segmented_img_arr, self.segmented_img_view)
        self.showImageArray(Data.clustered_img_arr, self.clustered_img_view)
        self.show_result()
        # QApplication.processEvents()
        ReceiceImg.isHandled = True

    def local_show_analysis_calculate_image(self):
        self.showImageArray(Data.segmented_img_arr, self.segmented_img_view)
        self.showImageArray(Data.clustered_img_arr, self.clustered_img_view)
        self.show_result()

    def clicked_local_button(self):
        Data.isOnline = False
        if self.chooseImg():
            self.showImageArray(Data.raw_img_arr, self.raw_img_view)
            # if type(img_arr) == "":
            # self.local_show_analysis_calculate_image()
            if self.ReceiceImgThread == None:
                self.ReceiceImgThread = ReceiceImg()
                self.ReceiceImgThread.receivedSignal.connect(self.local_show_analysis_calculate_image)
                self.ReceiceImgThread.start()
            else:
                ReceiceImg.isHandled = True

    def clicked_online_button(self):
        Data.isOnline = True
        if self.ReceiceImgThread == None:
            self.ReceiceImgThread = ReceiceImg()
            self.ReceiceImgThread.receivedSignal.connect(self.online_show_analysis_calculate_image)
            self.ReceiceImgThread.start()

    def chooseImg(self):
        """
        选取本地图片并返回路径
        """
        img_path = ''
        imageFile, _ = QFileDialog.getOpenFileName(self,
                "Choose an image file to open", img_path, "Images (*.*)")
        if imageFile != '':
            img_path = imageFile
            SMLog.debug("img path: %s",img_path)
            # Data.raw_img_path = img_path
            Data.raw_img_arr = cv2.imread(img_path)

            Data.raw_img_arr = np.array(Data.raw_img_arr)
            # print(Data.raw_img_arr.shape)
            print(Data.raw_img_arr.ndim)
            return True
        else: return False

    def showImageFile(self, imageFile, _QGraphicsView_obj):
        # 显示图片
        # input: image path, QGraphicsView object
        pixmap = QPixmap(imageFile)
        scene = QGraphicsScene()
        pixmap = pixmap.scaled(_QGraphicsView_obj.size(),Qt.KeepAspectRatio)
        scene.clear()
        scene.addPixmap(pixmap)
        _QGraphicsView_obj.setScene(scene)

    def showImageArray(self, _bgrimg, _QGraphicsView_obj):
        # input: image path, QGraphicsView object
        if type(_bgrimg) == type(None):
            # 当输入数组为 None 时
            return
        rgbimg = cv2.cvtColor(_bgrimg, cv2.COLOR_BGR2RGB)
        # print(rgbimg.shape())
        qimg = QImage(rgbimg.data,rgbimg.shape[1],rgbimg.shape[0],QImage.Format_RGB888)
        pixmap = QPixmap(qimg)
        scene = QGraphicsScene()
        pixmap = pixmap.scaled(_QGraphicsView_obj.size(),Qt.KeepAspectRatio)
        scene.clear()
        scene.addPixmap(pixmap)
        _QGraphicsView_obj.setScene(scene) # 显示图像


    def show_result(self):
        str_date = datetime.now().date().isoformat()
        str_time = datetime.now().time().strftime("%H:%M:%S")
        result_str = "date: " + str_date + '\n' + "time: " + str_time \
                     + "\nimage: " + str(Data.img_name) \
                     + "\nclustering center: \n" + "    " + str(Data.soil_mean) \
                     + "\nThe moisture content was tested to be: " + str(Data.predict_result) + "%" \
                     + "\nAlgorithm time(s): " + str(Data.algorithm_used_time)
        self.result_text.setText(result_str)
        # self.result_text.show()

    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application",
                               triggered=QApplication.instance().closeAllWindows)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

        # self.cameraSet = QAction("Camera settings", self,
        #                          statusTip="Camera settings",
        #                          triggered=self.cameraSetDialog)

        self.cameraSet = QAction("Lower unit camera setup", self,
                                 statusTip="Setting the camera parameters",
                                 triggered=self.cameraSetDialog)

        # self.networkSet = QAction("IP settings", self,
        #                          statusTip="IP settings",
        #                          triggered=self.networkDialog)

        self.networkSet = QAction("Lower computer ip address setting", self,
                                  statusTip="Setting up a network connection",
                                  triggered=self.networkDialog)

        self.kindSet = QAction("Soil type setting", self,
                                 statusTip="Soil type setting",
                                 triggered=self.kindselect)

        # self.denoiseSet = QAction("Help", self,
        #                          statusTip="Help",
        #                          triggered=self.denoiseDialog)

        self.denoiseSet = QAction("Denoising algorithm selection", self,
                                 statusTip="Denoising algorithm selection",
                                 triggered=self.denoiseDialog)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.separatorAct = self.fileMenu.addSeparator()
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()
        self.setting = self.menuBar().addMenu("&Settings")
        self.setting.addAction(self.cameraSet)
        self.setting.addAction(self.networkSet)
        self.setting.addAction(self.kindSet)
        self.setting.addAction(self.denoiseSet)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def loadFile(self, fileName):
        pass

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
