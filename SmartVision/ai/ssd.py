# -*- coding: utf-8 -*-
"""
    ai.ssd
    ~~~~~~
    Created on 2017-03-14 19:01
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

from ..config.log import logger

def _recognition_img(img_q,result_q):
    while True:
        info = img_q.get()
        info['result'] = "餐饮占道"
        logger.info("info->picUrl:{}".format(info['picUrl']))
        result_q.put(info)

def recognition_img(img_q,result_q):
    _recognition_img(img_q,result_q)
