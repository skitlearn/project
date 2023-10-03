# -*- coding: UTF-8
'''
# Filtered preprocessed images
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

class PreprocessImg(object):
    #  Filtering images
    def __init__(self, _bgr_arr):
        self.__start_time = time.time()
        self.bgr_arr = _bgr_arr
        self.filtered_arr = None

    def averageFilter(self):
        # Mean filtering
        img = self.bgr_arr
        self.filtered_arr = cv2.blur(img, (3, 3))

    def medianFilter(self):
        # Median filtering
        img = self.bgr_arr
        self.filtered_arr = cv2.medianBlur(img, 3)

    def gaussianFilter(self):
        # Gaussian filtering
        img = self.bgr_arr
        self.filtered_arr = cv2.GaussianBlur(img, (3, 3), 0)

    def save_filtered_img(self,_path):
        # Save the filtered image
        cv2.imwrite(_path, self.filtered_arr)

    def get_filtered_arr(self):
        return self.filtered_arr

    @property
    def used_time(self):
        # Calculation time consuming
        return round(time.time()-self.__start_time,2)

if __name__ == '__main__':
    img_path = "data/180529_202903_180524_172941.jpg"
    img_array = cv2.imread(img_path)
    pre = PreprocessImg(img_array)
    print("time of use: ", pre.used_time)





