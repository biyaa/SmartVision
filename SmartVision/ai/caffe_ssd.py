# -*- coding: utf-8 -*-
"""
    ai.caffe_ssd
    ~~~~~~~~~~~~
    Created on 2017-03-17 16:31
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""


import sys
import os
import time
import numpy as np
import glob as glob
import skimage
from PIL import Image
from StringIO import StringIO
from google.protobuf import text_format
from ..config.log import logger
from ..config import svs
from ..common import fields as F
from ..common import convention as C
from ..common import error as error


class Ai_ssd(object):
    def __init__(self):
        self.is_init = False

    def _split_result(self,detections,img_seq):

        begin = img_seq * 200
        end = (img_seq + 1) * 200
        #print(begin,end)
        
        # Parse the outputs.
        det_label = detections[0,0,:,1]
        det_conf = detections[0,0,:,2]
        det_xmin = detections[0,0,:,3]
        det_ymin = detections[0,0,:,4]
        det_xmax = detections[0,0,:,5]
        det_ymax = detections[0,0,:,6]
        
        # Get detections with confidence higher than 0.1.
        top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.1]                                  #####################
        #print (top_indices)
        top_indices_i = [i for i in top_indices if i>=begin and i<end]
        
        #print (top_indices_i)
        top_conf = det_conf[top_indices_i]
        top_label_indices = det_label[top_indices_i].tolist()
        top_labels = self.get_labelname(self.labelmap, top_label_indices)
        top_xmin = det_xmin[top_indices_i]
        top_ymin = det_ymin[top_indices_i]
        top_xmax = det_xmax[top_indices_i]
        top_ymax = det_ymax[top_indices_i]
        ####################################################
        '''
        umbrella chair
        table
        chair >= 6
        '''
        #limistprint = {"umbrella":0.1,"chair":0.1,"dining table":0.1}
        limistprint = {"umbrella":0,"chair":0,"dining table":0}
        logger.debug(top_labels[:len(top_indices_i)])
        for i in range(len(top_indices_i)): #top_conf.shape[0]):
            label_name = top_labels[i]
            if label_name in limistprint:
                limistprint[label_name]=limistprint[label_name]+1

        if limistprint["dining table"] > 0 or limistprint["chair"] >=5 or (limistprint["chair"] > 0 and limistprint["umbrella"]):
            return True
        else:
            return False

    def init_model(self,caffe_root='/mnt/nndisk/tim/SmartVision/caffe-ssd'):
        web_path = os.getcwd()
        self.caffe_root =  os.path.join(web_path, caffe_root)
        # Make sure that caffe is on the python path:
        os.chdir(self.caffe_root)
        sys.path.insert(0, self.caffe_root + '/python')                                                 #####################
        import caffe
        self.caffe = caffe
        if svs.compute_mode == "GPU":
            self.caffe.set_device(0)
            self.caffe.set_mode_gpu()
        else:
            self.caffe.set_mode_cpu()

        ####################################################
        from caffe.proto import caffe_pb2
        self.caffe_pb2 = caffe_pb2
        # load PASCAL VOC labels
        labelmap_file = 'data/coco/labelmap_coco.prototxt'
        file = open(labelmap_file, 'r')
        self.labelmap = caffe_pb2.LabelMap()
        text_format.Merge(str(file.read()), self.labelmap)


        self.capability = [C.OCCUPY_FOOTWAY_BY_CATERING]

        ####################################################

        model_def = 'models/VGGNet/coco/SSD_512x512/deploy.prototxt'                                  #####################
        model_weights = 'models/VGGNet/coco/SSD_512x512/VGG_coco_SSD_512x512_iter_360000.caffemodel'  #####################

        self.net = caffe.Net(model_def,      # defines the structure of the model
                        model_weights,  # contains the trained weights
                        caffe.TEST)     # use test mode (e.g., don't perform dropout)
        # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
        self.transformer = self.caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))
        self.transformer.set_mean('data', np.array([104,117,123])) # mean pixel
        self.transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

        self.image_resize = 512   

        os.chdir(web_path)
        print("model initialization done!")


    def get_labelname(self,labelmap, labels):
        num_labels = len(labelmap.item)
        labelnames = []
        if type(labels) is not list:
            labels = [labels]
        for label in labels:
            found = False
            for i in range(0, num_labels):
                if label == labelmap.item[i].label:
                    found = True
                    labelnames.append(labelmap.item[i].display_name)
                    break
            assert found == True
        return labelnames

    def is_capability(self,rec):
        return set(self.capability).issubset(rec[F.INTELLIGENTTYPES])

    def filled_by_capaility(self,records):
        r_map = {} 
        r_imgs = []
        i = 0
        for rec in records:
            if self.is_capability(rec):
                r_imgs.append(rec[F.IMG])
                r_map[i] = rec
                i = i + 1


        return (r_imgs,r_map)

    #   convert content to array
    def preprocess_img(self,img):
        """
        Load an image converting from grayscale or alpha as needed.
        Parameters
        ----------
        img : string
        Returns
        -------
        image : an image with type np.float32 in range [0, 1]
            of size (H x W x 3) in RGB or
            of size (H x W x 1) in grayscale.
        """
        img = np.array(Image.open(StringIO(img)))
        img = skimage.img_as_float(img).astype(np.float32)
        logger.debug("decode jpg content:{}".format(img[:3,1,1]))

        if img.ndim == 2:
            img = img[:, :, np.newaxis]
            if color:
                img = np.tile(img, (1, 1, 3))
        elif img.shape[2] == 4:
            img = img[:, :, :3]
        return img

    #   convert content to array
    def convert_to_img(self,imgs_content):
        images = []
        for img_c in imgs_content:
            image = self.preprocess_img(img_c)
            images.append(image)
        
        return images


    #  ananlyize img through by nn
    def pred_picture(self, records, ai_types =[1] ):

        start_time = time.time()
        imgs_content,imgs_map = self.filled_by_capaility(records)
        img_num = len(imgs_content)
        logger.debug("pred img num:{}".format(img_num))
        # 如果符合条件的图片就分析
        #if img_num > 0: 
        imgs = self.convert_to_img(imgs_content)
        ####################################################
        #image = from  memory
        ####################################################
        self.net.blobs['data'].reshape(img_num,3,self.image_resize,self.image_resize)

        for i in range(len(imgs)):
            transformed_image = self.transformer.preprocess('data', imgs[i])
            self.net.blobs['data'].data[i,...] = transformed_image
        
            # Forward pass.
            detections = self.net.forward()['detection_out']

            rec_result = []

            for i in range(img_num):
                r = self._split_result(detections,i)
                rec_result.append(r)

            
            for i in range(img_num):
                rec = imgs_map[i]
                if rec_result[i] :
                    rec[F.INTELLIGENTRESULTTYPE] = rec[F.INTELLIGENTRESULTTYPE] + ai_types  #暂时没有分析多个能力
                else:
                    if len(rec[F.INTELLIGENTRESULTTYPE]) == 0 :
                        rec[F.INTELLIGENTRESULTTYPE] = [C.RESULT_NO] 

            logger.info("Deep looking takes {} secs.".format(time.time()-start_time))

