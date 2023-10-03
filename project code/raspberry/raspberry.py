# -*- coding: utf-8 -*
'''
摄像头常开
'''
from socket import *
import time
import cv2
from cv2 import VideoCapture
import os
import struct
from threading import Thread

def take_photoes():
    while True:
        cap = VideoCapture(0)
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        c = cv2.waitKey(1)
        if c == ord('q'):
            break
        if c == ord('s'):
            path = os.path.join('foo.jpg')
            cv2.imwrite(path,frame)
        return frame

def take_viedo():

    global TakePicture,ImgData
    print("1")
    cap = VideoCapture(0)
    cap.set(3,1920)
    cap.set(4,1080)
    try:
        while (cap.isOpened()):
            ret_flag, ImgData = cap.read()
            cv2.imshow("Capture_Test", ImgData)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            if TakePicture == True:
                path = os.path.join('test.jpg')
                print("Pictures taken")
                TakePicture = False
    except Exception as e:
        cap.release()
        print("Camera shooting abnormality, rolled out, error cause：",e)


def pack_data(_arr):
    # return binary stream
    w = _arr.shape[0]
    h = _arr.shape[1]
    return struct.pack('I',w)+struct.pack('I',h)+_arr.tobytes()

def network():
    global TakePicture,ImgData
    myhost = ''
    myport = 8080
    sockobj = socket(AF_INET, SOCK_STREAM) # TCP
    sockobj.bind((myhost,myport))
    sockobj.listen(2)
    print ('Raspberry Pi up and running...')
    while True:
        print('Waiting for the host computer to connect...')
        connection, address = sockobj.accept()
        print ('Connecting to the host computer: ',address)
        while True:
            try:
                cmd = connection.recv(2)
                print("receive: ", cmd)
                if cmd == b'ok':
                    TakePicture = True
                    img = ImgData
                    # img = cv2.imread("test0.png")
                    print(img.shape)
                    packed_data = pack_data(img)
                    data_bytes = len(packed_data)
                    connection.send(data_bytes.to_bytes(4, 'big'))
                    connection.send(packed_data)
                    print("Number of bytes sent：", data_bytes)

                if cmd == b'':
                    connection.close()
                    break
            except Exception as e:
                connection.close()
                print("Anomaly in network reception, closed, reason for anomaly: ", e)
                break

if __name__ == '__main__':
    TakePicture = False
    ImgData = ''
    photoTask = Thread(target=take_viedo)
    networkTask = Thread(target=network)

    photoTask.start()
    networkTask.start()


