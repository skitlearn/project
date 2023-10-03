# -*- coding: utf-8 -*-


#  Turn on multithreading to receive network data and call the algorithm


from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
import time
from globalData import Data
from network import Network
from imgRecognition import RecognitionAlgorithm
from soilMonitorLog import SMLog
import numpy as np

class ReceiceImg(Thread,QObject):
    isHandled = True  # Whether incoming images have been processed
    receivedSignal = pyqtSignal()   # Customized signals
    def __init__(self):
        Thread.__init__(self)  # Call the parent class constructor and get an error for not calling it.
        QObject.__init__(self)

        if Data.isOnline == True:   # Online Detection
            # Connecting to the network
            address = Data.address
            self.net = Network()
            print('network enter')
            self.net.create_connnect(address)
            print('create_connnect enter')
            SMLog.info("Create and connect networks!")
            SMLog.info("Connect IP,Port：%s", address)

    def run(self):
        # 接收图片
        if Data.isOnline == True:
            while True:
                try:
                    if ReceiceImg.isHandled==True:
                        self.net.send_a_message()
                        self.net.receice_a_message()
                        Data.raw_img_arr = np.array(Data.raw_img_arr)
                        Data.raw_img_arr.flags.writeable = True
                        # ReceiceImg.isReceived = True
                        self.recognition_algorithm() # Calling algorithms in multiple threads
                        # time.sleep(4)
                        ReceiceImg.isHandled = False
                        self.receivedSignal.emit()
                        # self.conn
                except Exception as e:
                    SMLog.error("Online detection of multithreading error, error causes:%s", e)
                    break

        else:  # 离线检测
            while True:
                # print(ReceiceImg.isHandled)
                try:
                    if ReceiceImg.isHandled==True:
                        self.recognition_algorithm()  # Calling algorithms in multiple threads
                        ReceiceImg.isHandled = False
                        self.receivedSignal.emit()
                except Exception as e:
                    SMLog.error("Offline detection of multithreading error, error causes:%s", e)

    def recognition_algorithm(self):

        reg = RecognitionAlgorithm(Data.raw_img_arr)
        reg.implement()
        Data.algorithm_used_time = reg.used_time
        SMLog.info("Total time of image algorithm(s)：%s", reg.used_time)  # image algorithm total elapsed time
