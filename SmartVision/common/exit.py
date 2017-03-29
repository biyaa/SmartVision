# -*- coding: utf-8 -*-
"""
    common.exit
    ~~~~~~~~~~~~~~~~
    Created on 2017-03-29 16:35
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import fields as F

SPACIAL_EXIT_FLAG="====EXIT SMARTIVISION AI====="
def is_sms_exit(spcial_url):
    global SPACIAL_FLAG
    return spcial_url == SPACIAL_EXIT_FLAG


def gen_exit_obj():
    global SPACIAL_FLAG
    quit_obj ={}
    quit_obj[F.PICURL] = SPACIAL_EXIT_FLAG
    return quit_obj
