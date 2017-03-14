# -*- coding: utf-8 -*-
"""
    config.log
    ~~~~~~~~~~
    Created on 2017-03-14 17:18
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import logging
from logging.config import fileConfig

fileConfig('SmartVision/config/logger_config.ini')
logger=logging.getLogger('infoLogger')
logger.info('test1')
logger_error=logging.getLogger('errorhandler')
logger_error.error('test5')
