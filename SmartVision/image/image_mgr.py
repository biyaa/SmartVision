# -*- coding: utf-8 -*-
"""
    image.image_mgr
    ~~~~~~~~~~~~~~~
    Created on 2017-03-14 15:13
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

import time
import random
from ..config.log import logger
from ..config import svs as svs
from ..common import fields as F
from ..common import error as error
from ..common import global_env as ge

import image_pulling as im_p

def _fetch_url(task_q,url_fetch_q):
    logger.debug("fetch url process running...")
    while not (ge.EXIT_FLAG and task_q.qsize>0):
        if task_q.qsize > 1:
            rec = task_q.get()
            if rec[F.ERRORCODE] == 0:
                logger.debug("fetched task->picUrl: {}".format(rec[F.PICURL]))
            url_fetch_q.put(rec)
        else:
            time.sleep(0.5)

def _rand_sleep():
    rand_num = random.randint(1, 500) * 0.001
    time.sleep(rand_num)

def _fetch_img(url_fetch_q,img_q,retries=3):
    logger.debug("fetch img process running...")
    while not (ge.EXIT_FLAG and url_fetch_q.qsize>0):
        logger.debug("fetchhing img...")
        if url_fetch_q.qsize > 1:
            rec = url_fetch_q.get()
            rec[F.IMG] = ""
            retried = 0
            normal = True
            
            if rec[F.ERRORCODE] == 0:
                while retried < retries:
                    try:
                        content = im_p.pull_image(rec[F.PICURL])
                        if content > 100 :
                            rec[F.IMG] = content
                            rec[F.ERRORCODE] = 0
                            normal = True
                            break
                        else:
                            rec[F.ERRORCODE] = error.ERROR_FORMAT_CONTENT
                            normal = False
                            raise Exception("Image content too small")
                    except Exception,e:
                        rec[F.ERRORCODE] = error.ERROR_GETTING_IMG
                        normal = False
                        retried = retried + 1
                        logger.error("Img get error:{}".format(repr(e)))
                        _rand_sleep()
                logger.info("url:{}, img size:{}".format(rec[F.PICURL],len(rec[F.IMG])))

            img_q.put(rec)
        else:
            time.sleep(0.5)

def fetch_url(task_q,url_fetch_q):
    _fetch_url(task_q,url_fetch_q)

def fetch_img(url_fetch_q,img_q):
    _fetch_img(url_fetch_q,img_q, retries = svs.img_get_retry)
