# -*- coding: utf-8 -*-
'''
use dbscan algorithm to segment img of soil;
'''
import cv2
from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import hdbscan
from copy import deepcopy
import os
import collections
from globalData import Data
from matplotlib import pyplot as plt

import time
time1 = time.time()

class Dbscan_cluster(object):
    def __init__(self,_img_bgr_arr):
        self.gbr_arr = _img_bgr_arr             # Input image path
        self.img_shape = self.gbr_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.labels = []
        self.soil_label = -1  #

        self.n_clusters_ = 0

    def hdbscan_cluster(self,_arr,_EPS = 4):
        # input: lab or rgb cluster; the EPS
        # output: the mean of cluster

        mean = []
        amount_clusting = []
        soil_mean_of_cluster = []
        clustered_data = []


        X = deepcopy(_arr).reshape(-1,1)

        gbr_arr_flatten = self.gbr_arr.reshape(-1, 1)

        print(X)
        # Set parameter values EPS and MINPTS for clustering
        EPS = _EPS
        MINPTS = self.img_width*self.img_length/10  #  MinPts radius is set to w*h # /10
        db = hdbscan.HDBSCAN(min_cluster_size=2100, min_samples=60).fit(X)

        self.labels = db.labels_
        prob = db.probabilities_

        for i in range(len(self.labels)):
            if prob[i] < 0.5:
                self.labels[i] = -1
            if self.labels[i] == -1:
                gbr_arr_flatten[i] = [255]
            if self.labels[i] != -1:
                clustered_data.append(gbr_arr_flatten[i][0])

        if len(clustered_data) == 0:
            gbr_arr_flatten = X
            soil_mean_of_cluster = [np.mean(gbr_arr_flatten[:, 0])]
        else:
            soil_mean_of_cluster = [np.mean(clustered_data)]
        clustered_arr_1d = gbr_arr_flatten.reshape(self.gbr_arr.shape)
        self.gbr_arr = clustered_arr_1d
        _arr = clustered_arr_1d


        return soil_mean_of_cluster

    def save_segmented_imgs(self,_save_path):
        gbr_arr_flatten = self.gbr_arr.reshape(-1, 1)  # gray
        gbr_arr_flatten[self.labels != self.soil_label] = [255]
        clustered_arr_1d = gbr_arr_flatten.reshape(self.gbr_arr.shape)
        cv2.imwrite(_save_path, clustered_arr_1d)

if __name__ == '__main__':
    import sys
    img_path = "data/dbscan_test_1.png"
    img_arr = cv2.imread(img_path)
    db = Dbscan_cluster(img_arr)
    db.dbscan_cluster(db.lab_arr)


