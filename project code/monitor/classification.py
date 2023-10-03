import sys
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
from preprocess import PreprocessImg
# from sklearn.externals import joblib
import joblib
import collections

# Classification, receive cv2 imgarray, classify the data

class Classification(object):
    def __init__(self,_X_data):
        self.__start_time = time.time()
        self.X = _X_data
        self.model = joblib.load("model/train_model.m")  # load model

    def predict(self):
        # Output: Predicted category (int)
        output_matrix = self.model.predict(self.X)
        count_dict = dict(collections.Counter(output_matrix))
        print("预测细节：", count_dict)
        sorted_count_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_count_dict[0][0]

    @property
    def used_time(self):
        # Calculated time consuming
        return round(time.time() - self.__start_time,2)

if __name__ == '__main__':
    '''test'''
    img_path = "data/test.jpg"
    clf = Classification(img_path)
    print("test result: ", clf.predict())
