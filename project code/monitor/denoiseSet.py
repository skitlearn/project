# -*- coding: utf-8 -*-
#############################################################################
#
#############################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,
        QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QKeySequence,QFont,QPixmap,QImage,QRgba64
from globalData import Data

class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super(DenoiseDialog, self).__init__(parent)

        filter_layout = QVBoxLayout()
        self.button1 = QPushButton("Lower unit camera setup")
        self.button1.setFont(QFont("Roman times", 20))
        self.button2 = QPushButton("Lower computer ip address setting")
        self.button2.setFont(QFont("Roman times", 20))
        self.button3 = QPushButton("Denoising algorithm selection")
        self.button3.setFont(QFont("Roman times", 20))
        filter_layout.addWidget(self.button1)
        filter_layout.addWidget(self.button2)
        filter_layout.addWidget(self.button3)
        filter_layout.setAlignment(Qt.AlignCenter)
        filter_layout.setSpacing(40)
        YN_layout = QHBoxLayout()

        # 主布局
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(filter_layout)
        mainLayout.setSpacing(20)
        self.setLayout(mainLayout)
        self.setWindowTitle("parameterization")
        self.resize(300,300)


    def ok(self):
        self.close()
        # return self.address

    def cancel(self):
        self.close()

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    dialog = DenoiseDialog()
    dialog.show()
    sys.exit(app.exec_())
