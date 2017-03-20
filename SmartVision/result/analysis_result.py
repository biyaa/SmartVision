# -*- coding: utf-8 -*-
"""
    result.analysis_result
    ~~~~~~~~~~~~~~~~~~~~~~
    Created on 2017-03-14 19:23
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

from ..config.log import logger
from ..common import fields as F
from ..common import error as error

def _response_result(result_q):
    while True:
        info = result_q.get()
        logger.info("info->result:{}".format(info[F.INTELLIGENTRESULTTYPE]))
        logger.debug("result info:{}".format(info))

def response_result(result_q):
    _response_result(result_q)
