# -*- coding: utf-8 -*-
"""
    ai.caffe_init
    ~~~~~~~~~~~~~
    Created on 2017-03-17 11:26
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

import sys
import os
import time
import numpy as np
import glob as glob
from google.protobuf import text_format
class Ai_ssd(object):
    def __init__(self,caffe_root='/mnt/nndisk/tim/SmartVision/caffe-ssd'):
        web_path = os.getcwd()
        self.caffe_root = caffe_root
        # Make sure that caffe is on the python path:
        os.chdir(caffe_root)
        sys.path.insert(0, caffe_root + '/python')                                                 #####################
        import caffe
        self.caffe = caffe
        self.caffe.set_mode_gpu()

        ####################################################
        from caffe.proto import caffe_pb2
        self.caffe_pb2 = caffe_pb2
        # load PASCAL VOC labels
        labelmap_file = 'data/coco/labelmap_coco.prototxt'
        file = open(labelmap_file, 'r')
        self.labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), self.labelmap)



        ####################################################

        model_def = 'models/VGGNet/coco/SSD_512x512/deploy.prototxt'                                  #####################
        model_weights = 'models/VGGNet/coco/SSD_512x512/VGG_coco_SSD_512x512_iter_360000.caffemodel'  #####################

        net = caffe.Net(model_def,      # defines the structure of the model
                        model_weights,  # contains the trained weights
                        caffe.TEST)     # use test mode (e.g., don't perform dropout)

        os.chdir(web_path)
