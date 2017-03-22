# -*- coding: utf-8 -*-
"""
    SmartVision.mp_tasks
    ~~~~~~~~~~~~~~~~~~~~
    Created on 2017-03-22 09:08
    @author : huangguoxiong
    copyright: hikvision(c) 2017 company limited.
"""

import multiprocessing as mp
import time
import sys
import SmartVision.config.svs as svs
import SmartVision.task.analysis_task as a_task
import SmartVision.image.image_mgr as img_mgr
import SmartVision.ai.ssd as ssd
import SmartVision.result.analysis_result as a_result



# 1. 创建队列

task_queue = mp.Queue(maxsize=svs.queue_maxsize)               # 任务队列
url_queue = mp.Queue(maxsize=svs.queue_maxsize)                # 图片获取队列
img_queue = mp.Queue(maxsize=svs.queue_maxsize)                # 图片队列
result_queue = mp.Queue(maxsize=svs.queue_maxsize)             # 分析结果队列

# 2. 线程状态管理
process_stat_map = {}
PROCSSES_CREATE_FUNC_MAP = {}
# 3. 创建线程

def _create_thread(target=None,args=(),name=""):
    global thread_stat_map
    prcs = threading.Thread(target = target, args = args, name = name)
    prcs.setDaemon(True)
    return prcs

def _create_process(target=None,args=(),name=""):
    global process_stat_map
    prcs = mp.Process(target = target, args = args, name = name)
    prcs.daemon = True
    return prcs

def create_task_getting_prcs(name="task-get-process"):
    global task_queue
    prcs = _create_process(target = a_task.fetch_task, args = (task_queue,), name = name)
    return prcs


def create_url_getting_prcs(name="url-get-process"):
    global task_queue
    global img_fetching_queue
    prcs = _create_process(target = img_mgr.fetch_url, args = (task_queue,url_queue), name = name)
    return prcs

def create_img_getting_prcs(name="img-get-process", seq = 0):
    global task_queue
    global img_fetching_queue
    prcs = _create_process(target = img_mgr.fetch_img, args = (url_queue,img_queue),name = name + "-"+ str(seq))
    return prcs

def create_img_getting_prcss(name="img-get-process", para_num = 8):
    prcss = []
    for i in range(para_num):
        prcs = create_img_getting_prcs(name, i)
        prcss.append(prcs)

    return prcss


def create_img_recognition_prcs(name="img-recog-process"):
    global task_queue
    global img_fetching_queue
    prcs = _create_process(target = ssd.recognition_img, args = (img_queue,result_queue), name = name)
    return prcs

def create_result_putback_prcs(name="result-putback-process"):
    global task_queue
    global img_fetching_queue
    prcs = _create_process(target = a_result.response_result, args = (result_queue,), name = name)

    return prcs


def create_all_processes_map():
    PROCSSES_CREATE_FUNC_MAP["task-get-process"] = create_task_getting_prcs
    PROCSSES_CREATE_FUNC_MAP["url-get-process"] = create_url_getting_prcs
    PROCSSES_CREATE_FUNC_MAP["img-get-process"] = create_img_getting_prcs
    PROCSSES_CREATE_FUNC_MAP["img-recog-process"] = create_img_recognition_prcs
    PROCSSES_CREATE_FUNC_MAP["result-putback-process"] = create_result_putback_prcs

def create_all_processes():
    t_t = create_task_getting_prcs()
    t_u = create_url_getting_prcs()
    t_i = create_img_getting_prcss(para_num=svs.img_get_parallel_num)
    t_r = create_img_recognition_prcs()
    t_p = create_result_putback_prcs()

    prcss = [t_t,t_u] + t_i + [t_r,t_p]

    return prcss
    

def run_all_threads(prcss):
    for prcs in prcss:
        print(prcs.name + " is running...")
        prcs.start()

def show_processes(prcss):
    for t in prcss:
        print("...{} is alive? {}".format(t.name,t.is_alive()))

def show_queues(ques):
    names = ["tsk_queue","url_queue","img_queue","rst_queue"]
    for q,n in zip(ques,names):
        print("...size of {} we used is {}/{}".format(n,q.qsize(),svs.queue_maxsize))

def restart_process(prcss,name):
    for prcs in prcss:
        if prcs.name == name and not prcs.is_alive():
            func = PROCSSES_CREATE_FUNC_MAP[name]
            if "img-get-process" in name:
                num = name.split("-")[-1]
                if num.isdigit():
                    num = int(num)
                    prcs = func(num) 
                    print "%s is restartting..." %name
                    prcs.start()
            else:
                prcs = func()
                print "%s is restartting..." %name
                prcs.start()

def daemon_all_processes(prcss,ques):
    while True:
        cmd = ""
        cmd = raw_input()
        if cmd == "quit":
            break

        if cmd == "show process":
            show_processes(prcss)

        if cmd == "show queue":
            show_queues(ques)

        if "restart" in cmd :
            name = cmd.split(" ")[-1]
            restart_process(prcss, name)

        time.sleep(5)

def main():
    queues = [task_queue,url_queue,img_queue,result_queue]
    processes = create_all_processes()
    create_all_processes_map()
    run_all_threads(processes)
    daemon_all_processes(processes,queues)


    print("main ended...")
    sys.exit(0)

if __name__ == "__main__":
    main()
