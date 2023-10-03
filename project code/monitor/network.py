import numpy as np
from datetime import datetime
import socket
import time
from globalData import Data
from soilMonitorLog import SMLog

class Network(object):
    ImgName = ""
    raw_img_arr = 0

    def __init__(self):
        self.address = (("127.0.0.1", 8080))

    def set_address(self, _address):
        self.address = _address

    def create_connnect(self, _address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        print('connect start!')
        print(_address)
        s.connect(_address)
        print('connect success!')
        self.socketObj = s
        SMLog.debug("Connection created successfully!")

    def send_a_message(self):
        try:
            self.socketObj.send(b"ok")
            SMLog.debug("Sent successfully!")
        except Exception as e:
            SMLog.error("There's an anomaly. We're about to close the connection", e)
            self.close_connection()

    def receice_a_message(self):
        s = self.socketObj
        try:
            bin_stream = s.recv(4)
            stream_len = int.from_bytes(bin_stream, byteorder='big')
            SMLog.info("Bytes received: %s", stream_len)
            bin_stream = b''
            while len(bin_stream) != stream_len:
                bin_stream += s.recv(2048)
            w = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=0)[0]
            h = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=4)[0]
            img_arr = np.frombuffer(bin_stream, dtype=np.uint8, count=w*h*3, offset=8)
            img_arr.resize(w, h, 3)
            Data.raw_img_arr = img_arr
            SMLog.info("Receive picture size: %s",img_arr.shape)
            SMLog.info("Time of receiving pictures: %s", str(datetime.now()))
        except Exception:
            SMLog.error("An exception occurred and the connection will be closed：%s", Exception)
            self.close_connection()

    def close_connection(self):
        self.socketObj.close()

if __name__ == '__main__':
    net = Network()
    print("0")
    net.create_connnect(net.address)
    print("1")
    net.send_a_message()
    print("2")
    net.receice_a_message()
    print("3")
    time.sleep(2)
    net.send_a_message()
    print("4")
    net.receice_a_message()
    print("5")
    net.close_connection()
