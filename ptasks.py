# -*- coding: utf-8 -*-
"""
    SmartVision.ptasks
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-13 11:02
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import threading
import sys
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


def create_all_threads():
    t_t = create_task_getting_thd()
    t_u = create_url_getting_thd()
    t_i = create_img_getting_thds()
    t_r = create_img_recognition_thd()
    t_p = create_result_putback_thd()

    thds = [t_t,t_u] + t_i + [t_r,t_p]

    return thds
    

def run_all_threads(thds):
    for thd in thds:
        print(thd.getName() + " is running...")
        thd.start()

def daemon_all_threads(thds):
    while True:
        cmd = ""
        cmd = raw_input()
        if cmd == "quit":
            thds[0].join(1)
            break


def main():
    threads = create_all_threads()
    run_all_threads(threads)
    daemon_all_threads(threads)


    print("main ended...")

if __name__ == "__main__":
    main()
