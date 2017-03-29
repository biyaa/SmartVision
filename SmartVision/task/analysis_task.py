# -*- coding: utf-8 -*-
"""
    task.analysis_task
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-14 14:47
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import json
#import pdb
from kafka import KafkaConsumer
from ..config.log import logger
from ..config import svs
from ..common import error as error
from ..common import fields as F

def _fetch_msg(consumer,q,event):
    logger.info("task-get-process is running...")
    consumer.subscribe(svs.task_topic)
    for msg in consumer:
        value = msg.value
        try:
            records = json.loads(value)
            for rec in records:
                rec[F.ERRORCODE] = 0
                if not _verify_ele(rec):
                    rec[F.ERRORCODE] = error.ERROR_FORMAT_CONTENT
                    
                logger.info(rec)
                q.put(rec)


        except Exception, e:
            logger.error("Task Centent:{}".format(value))
            logger.error("Task Error Type:{}".format(repr(e)))
        finally:
            if event.is_set():
                break

    logger.info("task-get-process is stopping...")

def _fetch_task(q,event):

    logger.debug("kafka:{},topic:{},api_version{}".format(svs.servers, svs.task_topic, svs.api_version))
    consumer = KafkaConsumer(bootstrap_servers=svs.servers, api_version=svs.api_version,client_id=svs.client_id,group_id=svs.group_id)
    try:
        _fetch_msg(consumer,q,event)
    except KeyboardInterrupt:
        logger.error("consumer is stopped.")
        raise


def _verify_ele(rec):
    result = True
    if not rec.has_key(F.UUID):
        result = False

    if not rec.has_key(F.PICURL):
        result = False

    if not rec.has_key(F.INTELLIGENTTYPES):
        result = False

    rec[F.INTELLIGENTRESULTTYPE] = [] 
    logger.debug("Check task format: " + str(result))
    return result

def fetch_task(q,event):
    _fetch_task(q,event)
