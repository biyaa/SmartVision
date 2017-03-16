# -*- coding: utf-8 -*-
"""
    image.image_mgr
    ~~~~~~~~~~~~~~~
    Created on 2017-03-14 15:13
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

from ..config.log import logger
from ..common import fields as F
from ..common import error as error

import image_pulling as im_p

def _fetch_url(task_q,url_fetch_q):
    while True:
        info = task_q.get()
        if info[F.ERRORCODE] == 0:
            logger.debug("fetch info->picUrl: {}".format(info[F.PICURL]))
        url_fetch_q.put(info)

def _fetch_img(url_fetch_q,img_q):
    while True:
        info = url_fetch_q.get()
        info[F.IMG] = ""
        if info[F.ERRORCODE] == 0:
            content = im_p.pull_image(info[F.PICURL])
            if content > 100 :
                info[F.IMG] = content
            else:
                info[F.ERRORCODE] = error.ERROR_FORMAT_CONTENT

        logger.info("url:{}, img size:{}".format(info[F.PICURL],len(info[F.IMG])))
        img_q.put(info)

def fetch_url(task_q,url_fetch_q):
    _fetch_url(task_q,url_fetch_q)

def fetch_img(url_fetch_q,img_q):
    _fetch_img(url_fetch_q,img_q)
