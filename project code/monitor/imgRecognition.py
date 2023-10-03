# -*- coding: utf-8 -*-

from preprocess import PreprocessImg
from soilDetectorGauss import GaussDetector
from hdbscanClusterImg import Dbscan_cluster
from classification import Classification
from modelPredict import HumidityPredict
import time
from datetime import datetime
import os
from globalData import Data
from soilMonitorLog import SMLog
from copy import deepcopy
import cv2
import numpy as np
from matplotlib import pyplot as plt
#############################################################################
## Image recognition algorithms, including: image denoising, soil image segmentation,  clustering
## Input: numpy array of cv2 images.
## Output: the classification number of the image (int)
#############################################################################

class RecognitionAlgorithm(object):

    def __init__(self,_bgr_arr,saveProImg = False):
        self.__start_time = time.time()
        self.bgr_arr = _bgr_arr
        self.saveProImg = saveProImg
        # Set up various image save paths
        name_img_use_time = self.time_name()  # 180524_172850
        Data.img_name = name_img_use_time+".jpg"
        self.raw_img_path = Data.raw_img_folder+name_img_use_time+".jpg"
        self.filtered_img_path = Data.filtered_img_folder+name_img_use_time+".jpg"
        self.segmented_img_path = Data.segmented_img_folder+name_img_use_time+".jpg"
        self.clustered_img_path = Data.clustered_img_folder+name_img_use_time+".jpg"
        self.rectangle_img_path = Data.clustered_img_folder + name_img_use_time + "_sub.jpg"

    def implement(self):
        #
        bgr_arr = deepcopy(self.bgr_arr)
        cv2.imwrite(self.raw_img_path, bgr_arr)
        SMLog.info("Save original picture")





        self.bgr_arr = cv2.cvtColor(self.bgr_arr,cv2.COLOR_BGR2GRAY)
        bgr_arr = deepcopy(self.bgr_arr)[510:710, 985:1185]  # Intercept centers 200*200 area clustering
        print("dbscan_start")

        #  Show split image
        Data.segmented_img_arr = bgr_arr
        bgr_arr = np.array(bgr_arr)

        cv2.imwrite(self.segmented_img_path, bgr_arr)

        # clustering
        db = Dbscan_cluster(bgr_arr)

        soil_mean = db.hdbscan_cluster(bgr_arr)
        Data.clustered_img_arr = db.gbr_arr
        Data.soil_mean = soil_mean[0]
        print(Data.soil_mean)
        hum_predictor = HumidityPredict(Data.model_path)
        predict_y = hum_predictor.regression_predict(soil_mean[0])
        Data.predict_result = np.around(predict_y[0],decimals=2)
        SMLog.info("Water content prediction results：%s", predict_y)
        return Data.soil_mean

    def time_name(self):
        img_time_name = datetime.now().date().strftime("%y%m%d") + datetime.now().time().strftime("_%H%M%S")
        return img_time_name

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.__start_time,2)

if __name__ == '__main__':
    import cv2
    img_path = "C:/Users/ExCitrus/Desktop/rice940_1/07/1.jpg"
    reg = RecognitionAlgorithm(cv2.imread(img_path))
    print(reg.implement())
