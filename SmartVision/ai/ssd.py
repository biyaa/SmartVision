# -*- coding: utf-8 -*-
"""
    ai.ssd
    ~~~~~~
    Created on 2017-03-14 19:01
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import time
from ..config.log import logger
from ..config import svs
from ..common import fields as F
from ..common import error as error
from .caffe_ssd import Ai_ssd
def _is_analysizable(rec):
    result = False
    if rec[F.ERRORCODE] == 0:
        result = True
    return result

def _get_batch_imgs(records):
    imgs = []
    for rec in records:
        img = rec[F.IMG]
        imgs.append(img)
    return imgs

def _get_next_batch(img_q, result_q, num):
    records = []
    for i in range(num):
        if img_q.qsize() >0:
            rec = img_q.get()
            if _is_analysizable(rec):
                records.append(rec)
            else:
                result_q.put(rec)
        else:
            time.sleep(0.5)  # interval 500 millisecs to submit to analyzie
            break
    return records

def _clear_img(rec):
    del rec[F.IMG]
    return rec

def _tag_time(rec):
    rec[F.FINISHEDTIME] = int(time.time() * 1000)
    return rec

def _put_result(records, result_q):
    for rec in records:
#        rec[F.INTELLIGENTRESULTTYPE] = [1]
        rec = _tag_time(rec)
        rec = _clear_img(rec)
        result_q.put(rec)

def _recognition_img(img_q,result_q):
    ai = Ai_ssd()
    ai.init_model(caffe_root=svs.ssd_root)
    while True:
        records = _get_next_batch(img_q,result_q,8)
        imgs = []
        if len(records)>0:
            logger.info("analyizing number of images:{}".format(len(records)))
            imgs = _get_batch_imgs(records)
            ai.pred_picture(records)
            _put_result(records,result_q)

def recognition_img(img_q,result_q):
    _recognition_img(img_q,result_q)
