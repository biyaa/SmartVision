# -*- coding: utf-8 -*-
"""
    image.image_mgr
    ~~~~~~~~~~~~~~~
    Created on 2017-03-14 15:13
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

from ..config.log import logger
def _fetch_url(task_q,url_fetch_q):
    while True:
        info = task_q.get()
        logger.info("info->picUrl:{}".format(info['picUrl']))
        url_fetch_q.put(info)

def _fetch_img(url_fetch_q,img_q):
    while True:
        info = url_fetch_q.get()
        info['img'] = "person picture"
        logger.info("info->img:{}".format(info['img']))
        logger.info(img_q.qsize())
        img_q.put(info)

def fetch_url(task_q,url_fetch_q):
    _fetch_url(task_q,url_fetch_q)

def fetch_img(url_fetch_q,img_q):
    _fetch_img(url_fetch_q,img_q)
