# -*- coding: utf-8 -*-
"""
    image.image_pulling
    ~~~~~~~~~~~~~~~~~~~
    Created on 2017-03-15 10:05
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
from ..config.log import logger
import urllib2
def pull_image(url):
    request = urllib2.Request(url)
    #request.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        pass
    else:
        content = ""
    return content
