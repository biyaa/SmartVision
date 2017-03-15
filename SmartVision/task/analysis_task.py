# -*- coding: utf-8 -*-
"""
    task.analysis_task
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-14 14:47
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import json
from kafka import KafkaConsumer
from ..config.log import logger
from ..common import error as error
from ..common import fields as F

def _fetch_task(q):
    consumer = KafkaConsumer(bootstrap_servers='10.100.60.68:9092')
    consumer.subscribe(['city-management-intelligent-analyze'])
    for msg in consumer:
        value = msg.value
        infos = json.loads(value)
        for info in infos:
            info[F.ERRORCODE] = 0
            if not _verify_ele(info):
                info[F.ERRORCODE] = error.ERROR_FORMAT
                
            logger.info(info)
            q.put(info)

#    while True:
#        info = {}
#        info['uuid'] = "aaaaa"
#        info['picUrl'] = "http://www.baidu.com"
#        info['areaCoords'] = 33
#        logger.info("fetchhing task...")
#        q.put(info)

def _verify_ele(info):
    result = True
    if not info.has_key(F.UUID):
        result = False

    if not info.has_key(F.PICURL):
        result = False

    if not info.has_key(F.INTELLIGENTRESULTTYPE):
        result = False

    logger.debug("check task format: " + str(result))
    return result

def fetch_task(q):
    _fetch_task(q)
