# -*- coding: utf-8 -*-
import time
time1 = time.time()
from pylab import mpl
from sklearn import linear_model
from sklearn import tree
# from sklearn.externals import joblib
import joblib
from soilMonitorLog import SMLog
from globalData import Data

class HumidityPredict(object):
    def __init__(self,_model_path):
        self.__start_time = time.time()
        try:
            self.reg = joblib.load(_model_path)
        except Exception as e:
            self.reg = None
            SMLog.error("predictive model loading error: %s", e)

    def regression_predict(self,_X):
        self.predict_y = self.reg.predict(_X)
        return self.predict_y
    @property
    def used_time(self):
        # Calculation time consuming
        return round(time.time()-self.__start_time,2)

if __name__ == '__main__':
    MODEL_PATH = "./model/xs101_shaoliang_grand_final.model"
    hp = HumidityPredict(MODEL_PATH)
    num = hp.regression_predict(80)
    print(num)
    print(hp.used_time)
