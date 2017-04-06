# -*- coding: utf-8 -*-
"""
    result.analysis_result
    ~~~~~~~~~~~~~~~~~~~~~~
    Created on 2017-03-14 19:23
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

import json
import time
#import pdb
from kafka import KafkaProducer
from kafka.errors import KafkaError
from ..config.log import logger
from ..config import svs
from ..common import fields as F
from ..common import convention as C
from ..common import error as error
from ..common import exit as exit_mgr

exit_flag = False
def _get_next_batch(result_q, num=8):
    global exit_flag
    records = []
    for i in range(num):
        if result_q.qsize() >0:
            rec = result_q.get()
            exit_flag = exit_mgr.is_sms_exit(rec[F.PICURL]) or exit_flag
            if exit_flag:
                continue
            records.append(rec)
        else:
            time.sleep(0.1)  # interval 100 millisecs to submit to analyzie
            break
    return records

def _response_result(result_q,event):
    logger.debug("kafka:{},topic:{},api_version{}".format(svs.servers, svs.result_topic, svs.api_version))
    logger.debug("result-putback-process is running...")
    producer = KafkaProducer(bootstrap_servers=svs.servers, api_version=svs.api_version,retries=3,client_id=svs.client_id)
    global exit_flag
    while not (exit_flag and result_q.qsize()<1):
        records = _get_next_batch(result_q)
        #logger.info("size of thread {}".format(len(records)))
        for rec in records:
            logger.info("task->result:{}".format(rec[F.INTELLIGENTRESULTTYPE]))
            for t in rec[F.INTELLIGENTRESULTTYPE]:
                if C.OCCUPY_FOOTWAY_BY_CATERING == t:
                    logger.debug("{} OCCUPIED_FOOTWAY_BY_CATERING".format(rec[F.UUID]))
                else:
                    logger.debug("{} HASN'T OCCUPIED_FOOTWAY_BY_CATERING".format(rec[F.UUID]))


            logger.debug("Through SmartVision AI, it preds the result(s) as blow:\n{}".format(rec))
        if len(records)>0:
            msg = json.dumps(records)
            logger.debug(msg)
            producer.send(svs.result_topic, msg)

            producer.flush()
    logger.debug("result-putback-process is stopping...")

def response_result(result_q,event):
    #pdb.set_trace()
    _response_result(result_q,event)
