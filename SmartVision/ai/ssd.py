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
from ..common import fields as F
from ..common import error as error
def _is_analysizable(info):
    result = False
    if info[F.ERRORCODE] == 0:
        result = True
    return result

def _get_next_batch(img_q, result_q, num):
    infos = []
    for i in range(num):
        if img_q.qsize() >0:
            info = img_q.get()
            if _is_analysizable(info):
                infos.append(info)
            else:
                result_q.put(info)
        else:
            break
    return infos

def _put_result(infos, result_q):
    for info in infos:
        info[F.INTELLIGENTRESULTTYPE] = [1]
        result_q.put(info)

def _recognition_img(img_q,result_q):
    while True:
        infos = _get_next_batch(img_q,result_q,8)
        if len(infos)>0:
            logger.info("analyizing number of images:{}".format(len(infos)))
            time.sleep(1)
            _put_result(infos,result_q)

def recognition_img(img_q,result_q):
    _recognition_img(img_q,result_q)
