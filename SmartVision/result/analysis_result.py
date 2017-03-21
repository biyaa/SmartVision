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
from ..common import fields as F
from ..common import error as error

def _get_next_batch(result_q, num=8):
    records = []
    for i in range(num):
        if result_q.qsize() >0:
            rec = result_q.get()
            records.append(rec)
        else:
            time.sleep(0.1)  # interval 100 millisecs to submit to analyzie
            break
    return records

def _response_result(result_q):
    producer = KafkaProducer(bootstrap_servers=['10.100.60.68:9092'], api_version=(0,9),retries=3)
    while True:
        records = _get_next_batch(result_q)
        #logger.info("size of thread {}".format(len(records)))
        for rec in records:
            logger.info("info->result:{}".format(rec[F.INTELLIGENTRESULTTYPE]))
            logger.debug("result info:{}".format(rec))
        if len(records):
            msg = json.dumps(records)
            producer.send('CITY-MANAGEMENT-INTELLIGENT-ANALYZE-RESULT', msg)

            producer.flush()

def response_result(result_q):
    #pdb.set_trace()
    _response_result(result_q)
