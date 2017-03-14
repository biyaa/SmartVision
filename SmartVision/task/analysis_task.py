# -*- coding: utf-8 -*-
"""
    task.analysis_task
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-14 14:47
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
from ..config.log import logger
def _fetch_task(q):
    while True:
        info = {}
        info['uuid'] = "aaaaa"
        info['picUrl'] = "http://1.1.1.1/xxx/xxx.jpg"
        info['areaCoords'] = 33
        logger.info("fetchhing task...")
        q.put(info)

def fetch_task(q):
    _fetch_task(q)
