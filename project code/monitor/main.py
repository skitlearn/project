# -*- coding: utf-8 -*-
#  main
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from soilMonitorLog import SMLog

if __name__ == '__main__':
    import sys
    SMLog.info("上位机启动\n")
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
