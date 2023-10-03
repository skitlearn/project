#coding:utf-8
import json
import imgRecognition as ir
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from copy import deepcopy
import time
import sys
from PIL import Image
import joblib

filelist1 = "C:/Users/MMS/Desktop/soil_multi3/x82/"
filelist2 = "C:/Users/MMS/Desktop/soil_multi3/xs101/"
filelist3 = "C:/Users/MMS/Desktop/soil_multi3/red/"
filelist4 = "C:/Users/MMS/Desktop/soil_multi3/yellow/"

reg = joblib.load('./model/xs101_final.model')
xx = []

for j in range(1, 37):              # listdir的参数是文件夹的路径
    img1 = cv2.imread(filelist4+str(j)+'.jpg',0)   # 读取图片，第二个参数表示以灰度图像读入
    # img1 = deepcopy(img)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # cv2.namedWindow(str(j)+'.jpg', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow(str(j)+'.jpg', img1[550:650,870:970])
    img1 = np.array(img1)
    gray = img1
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=60, minRadius=150)
    for circle in circles[0]:
        # 圆的基本信息
        # print(circle[2])
        # 坐标行列－圆心坐标
        x = int(circle[0])
        y = int(circle[1])
        if x < 500 and x > 1400:
            continue
        if y < 450 and y > 1000:
            continue
        r = int(circle[2])
        gray = gray[y - r:y + r, x - r:x + r]
        break
    gray = ir.RecognitionAlgorithm(gray)
    cls = gray.implement()
    # cls = reg.predict(cls)
    xx.append(cls)
    j = j + 1

print("len:"+str(len(xx)))
for j in range(len(xx)):
    print(xx[j])
# # print(len(cla_data))
# # for j in range(31):
# #     print(cla_data[j])
# ax = plt.subplot(111)
# ax.plot(x, cla_data1, color='g')
# ax.plot(x, cla_data2, color='b')
# # sum = sum / i
# # print("final cal:"+str(sum))
#
# ax.set_ylabel('Y')
# ax.set_xlabel('X')
#
# plt.show()
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
