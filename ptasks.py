# -*- coding: utf-8 -*-
"""
    SmartVision.ptasks
    ~~~~~~~~~~~~~~~~~~
    Created on 2017-03-13 11:02
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""
import threading
import time
import sys
from Queue import Queue
import SmartVision.config.svs as svs
import SmartVision.task.analysis_task as a_task
import SmartVision.image.image_mgr as img_mgr
import SmartVision.ai.ssd as ssd
import SmartVision.result.analysis_result as a_result



# 1. 创建队列

task_queue = Queue(maxsize=svs.queue_maxsize)               # 任务队列
url_queue = Queue(maxsize=svs.queue_maxsize)                # 图片获取队列
img_queue = Queue(maxsize=svs.queue_maxsize)                # 图片队列
result_queue = Queue(maxsize=svs.queue_maxsize)             # 分析结果队列

# 2. 线程状态管理
thread_stat_map = {}
# 3. 创建线程

def _create_thread(target=None,args=(),name=""):
    global thread_stat_map
    thd = threading.Thread(target = target, args = args, name = name)
    thd.setDaemon(True)
    return thd

def create_task_getting_thd(name="task-get-thread"):
    global task_queue
    thd = _create_thread(target = a_task.fetch_task, args = (task_queue,), name = name)
    return thd


def create_url_getting_thd(name="url-get-thread"):
    global task_queue
    global img_fetching_queue
    thd = _create_thread(target = img_mgr.fetch_url, args = (task_queue,url_queue), name = name)
    return thd

def create_img_getting_thds(name="img-get-thread", thd_num = 8):
    global task_queue
    global img_fetching_queue
    thds = []
    for i in range(thd_num):
        thd = _create_thread(target = img_mgr.fetch_img, args = (url_queue,img_queue),name = name + "-"+ str(i) )
        thds.append(thd)

    return thds


def create_img_recognition_thd(name="img-recog-thread"):
    global task_queue
    global img_fetching_queue
    thd = _create_thread(target = ssd.recognition_img, args = (img_queue,result_queue), name = name)
    return thd

def create_result_putback_thd(name="result-putback-thread"):
    global task_queue
    global img_fetching_queue
    thd = _create_thread(target = a_result.response_result, args = (result_queue,), name = name)

    return thd


def create_all_threads():
    t_t = create_task_getting_thd()
    t_u = create_url_getting_thd()
    t_i = create_img_getting_thds(thd_num=svs.img_get_thd_num)
    t_r = create_img_recognition_thd()
    t_p = create_result_putback_thd()

    thds = [t_t,t_u] + t_i + [t_r,t_p]

    return thds
    

def run_all_threads(thds):
    for thd in thds:
        print(thd.getName() + " is running...")
        thd.start()

def show_threads(thds):
    for t in thds:
        print("...{} is alive? {}".format(t.getName(),t.isAlive()))

def show_queues(ques):
    names = ["tsk_queue","url_queue","img_queue","rst_queue"]
    for q,n in zip(ques,names):
        print("...size of {} we used is {}/{}".format(n,q.qsize(),svs.queue_maxsize))

def daemon_all_threads(thds,ques):
    while True:
        cmd = ""
        cmd = raw_input()
        if cmd == "quit":
            break

        if cmd == "show thread":
            show_threads(thds)

        if cmd == "show queue":
            show_queues(ques)

        time.sleep(5)

def main():
    queues = [task_queue,url_queue,img_queue,result_queue]
    threads = create_all_threads()
    run_all_threads(threads)
    daemon_all_threads(threads,queues)


    print("main ended...")
    sys.exit(0)

if __name__ == "__main__":
    main()
