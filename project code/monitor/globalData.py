# -*- coding: utf-8 -*-

class Data(object):

    address = ("192.168.5.3",8080) # socket address
    algorithm_used_time = 0  # the used time of algorithm
    isOnline = False
    img_name = None
    #  Visualization of arrays
    raw_img_arr = None  # raw image array
    filtered_img_arr = None  # processed image array
    segmented_img_arr = None # segmented image array
    clustered_img_arr = None  # gray histogram image array

    #  The folder where the images are stored
    raw_img_folder = "data/raw/"
    filtered_img_folder = "data/filtered/"
    segmented_img_folder = "data/segmented/"
    clustered_img_folder = "data/clustered/"

    # the predict about
    model_path = "./model/x82_final.model"
    predicted_classification = -1

    # Intermediate as well as final results
    soil_mean = None
    predict_result = None


