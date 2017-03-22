# -*- coding: utf-8 -*-
"""
    config.svs_config
    ~~~~~~~~~~~~~~~~~
    Created on 2017-03-21 14:36
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import ConfigParser
import codecs
cp = ConfigParser.SafeConfigParser()
servers = '10.100.60.68:9092'
api_version = (0,9)
task_topic = 'CITY-MANAGEMENT-INTELLIGENT-ANALYZE'
result_topic = 'CITY-MANAGEMENT-INTELLIGENT-ANALYZE-RESULT'
ssd_root ='caffe-ssd'
compute_mode = 'GPU'
queue_maxsize = 32
img_get_parallel_num = 8
ai_parallel_num = 8

with codecs.open('SmartVision/config/svs.conf', 'r', encoding='utf-8') as f:
    cp.readfp(f)

    if cp.has_option('kafka', 'servers'):
        servers_s = cp.get('kafka','servers')
        servers = servers_s.split(",")

    if cp.has_option('kafka', 'task_topic'):
        task_topic = cp.get('kafka','task_topic')

    if cp.has_option('kafka', 'result_topic'):
        result_topic = cp.get('kafka','result_topic')

    if cp.has_option('kafka', 'api_version'):
        s_api = cp.get('kafka','api_version')
        api_version = tuple([int(x) for x in s_api.split(",")])

    if cp.has_option('svs', 'queue_maxsize'):
        queue_maxsize = cp.getint('svs','queue_maxsize')

    if cp.has_option('svs', 'img_get_parallel_num'):
        img_get_parallel_num = cp.getint('svs','img_get_parallel_num')


    if cp.has_option('svs', 'ai_parallel_num'):
        ai_parallel_num = cp.getint('svs','ai_parallel_num')

    if cp.has_option('svs', 'compute_mode'):
        compute_mode = cp.get('svs','compute_mode')

    if cp.has_option('svs', 'ssd_root'):
        ssd_root = cp.get('svs','ssd_root')

