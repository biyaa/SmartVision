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

fileConfig('SmartVision/config/logger.conf')
logger=logging.getLogger('consoleLogger')
log = logger
#logger.info('test1')
#logger.error('error')
