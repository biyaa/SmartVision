# -*- coding: utf-8 -*-
"""
    SmartVision.ptasks
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-13 11:02
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import threading
from Queue import Queue
import SmartVision.task.analysis_task as a_task
import SmartVision.image.image_mgr as img_mgr
import SmartVision.ai.ssd as ssd
import SmartVision.result.analysis_result as a_result




# 1. 创建队列

task_queue = Queue(maxsize=32)               # 任务队列
url_queue = Queue(maxsize=32)                # 图片获取队列
img_queue = Queue(maxsize=32)                # 图片队列
result_queue = Queue(maxsize=32)             # 分析结果队列



# 2. 创建线程

def create_task_getting_thd(name="task-get-thread"):
    global task_queue
    thd = threading.Thread(target = a_task.fetch_task, args = (task_queue,), name = name)
    return thd


def create_url_getting_thd(name="url-get-thread"):
    global task_queue
    global img_fetching_queue
    thd = threading.Thread(target = img_mgr.fetch_url, args = (task_queue,url_queue), name = name)

    return thd

def create_img_getting_thds(name="img-get-thread", thd_num = 8):
    global task_queue
    global img_fetching_queue
    thds = []
    for i in range(thd_num):
        thd = threading.Thread(target = img_mgr.fetch_img, args = (url_queue,img_queue),name = name + "-"+ str(i) )
        thds.append(thd)

    return thds


def create_img_recognition_thd(name="img-recog-thread"):
    global task_queue
    global img_fetching_queue
    thd = threading.Thread(target = ssd.recognition_img, args = (img_queue,result_queue), name = name)

    return thd

def create_result_putback_thd(name="result-putback-thread"):
    global task_queue
    global img_fetching_queue
    thd = threading.Thread(target = a_result.response_result, args = (result_queue,), name = name)

    return thd


def main():
    t1 = create_task_getting_thd()
    t1.start()

    t2 = create_url_getting_thd()
    t2.start()
    
    t3 = create_img_getting_thds()
    for t in t3:
        t.start()

    t4 = create_img_recognition_thd()
    t4.start()

    t5 = create_result_putback_thd()
    t5.start()

    print("main ended.")

if __name__ == "__main__":
    main()
