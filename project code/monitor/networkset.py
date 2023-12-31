from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,
        QPushButton, QVBoxLayout, QWidget)
from socket import *
from globalData import Data

class NetworkDialog(QDialog):
    def __init__(self, parent=None):
        super(NetworkDialog, self).__init__(parent)

        self.ip_label = QLabel("IP address:")  # IP address
        self.ip_lineEdit = QLineEdit()
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_lineEdit)

        self.port_label = QLabel("Port number:")  # port number
        self.port_lineEdit = QLineEdit()
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_lineEdit)

        self.YesButton = QPushButton("Confirm")
        self.NoButton = QPushButton("Cancel")
        YN_layout = QHBoxLayout()
        YN_layout.addWidget(self.YesButton)
        YN_layout.addWidget(self.NoButton)

        # Main layout
        mainLayout = QVBoxLayout()
        # mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(ip_layout)
        mainLayout.addLayout(port_layout)
        mainLayout.addLayout(YN_layout)

        # mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("network setting")
        self.resize(250,200)
        self.NoButton.clicked.connect(self.cancel)
        self.YesButton.clicked.connect(self.ok)

    def ok(self):
        ip = self.ip_lineEdit.text()
        port = self.port_lineEdit.text()
        if port != "" and ip != "":
            Data.address = (ip,int(port))
            print("Set up a new network connection：",Data.address)
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
    dialog = NetworkDialog()
    dialog.show()
    sys.exit(app.exec_())
