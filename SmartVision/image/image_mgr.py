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
        rec = task_q.get()
        if rec[F.ERRORCODE] == 0:
            logger.debug("fetched info->picUrl: {}".format(rec[F.PICURL]))
        url_fetch_q.put(rec)

def _fetch_img(url_fetch_q,img_q):
    while True:
        rec = url_fetch_q.get()
        rec[F.IMG] = ""
        if rec[F.ERRORCODE] == 0:
            content = im_p.pull_image(rec[F.PICURL])
            if content > 100 :
                rec[F.IMG] = content
            else:
                rec[F.ERRORCODE] = error.ERROR_FORMAT_CONTENT

        logger.info("url:{}, img size:{}".format(rec[F.PICURL],len(rec[F.IMG])))
        img_q.put(rec)

def fetch_url(task_q,url_fetch_q):
    _fetch_url(task_q,url_fetch_q)

def fetch_img(url_fetch_q,img_q):
    _fetch_img(url_fetch_q,img_q)
