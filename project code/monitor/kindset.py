# -*- coding: utf-8 -*-
#############################################################################
#
#############################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,
        QPushButton, QVBoxLayout, QWidget)
from socket import *
from globalData import Data

class kindDialog(QDialog):
    def __init__(self, parent=None):
        super(kindDialog, self).__init__(parent)

        self.name_label = QLabel("Geotechnical type:")
        self.name_lineEdit = QLineEdit()
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_lineEdit)

        self.YesButton = QPushButton("recognize")
        self.NoButton = QPushButton("cancel")
        YN_layout = QHBoxLayout()
        YN_layout.addWidget(self.YesButton)
        YN_layout.addWidget(self.NoButton)

        # 主布局
        mainLayout = QVBoxLayout()
        # mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(name_layout)
        mainLayout.addLayout(YN_layout)

        # mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("model settings")
        self.resize(250,200)
        self.NoButton.clicked.connect(self.cancel)
        self.YesButton.clicked.connect(self.ok)

    def ok(self):
        soil_name = self.name_lineEdit.text()
        if soil_name != "":
            Data.model_path = "./model/" + soil_name + "_final.model"
            print("Setting up a new network connection：",Data.model_path)
        self.close()
        # return self.address

    def cancel(self):
        self.close()

    def get_name(self):
        return self.soil_name


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    dialog = NetworkDialog()
    dialog.show()
    sys.exit(app.exec_())
