# coding:utf-8
# !/usr/bin/env python
# Created by Charles on 2019/3/29.
import concurrent
import queue
import random
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from copy import copy

from Exception.msg import ReceiverEndMsgException
from base.pools import  threadSubmit
from base.queues import  threadLinkQueue
from base.stageRange import STI, stop_thread
from libs.endLib import TASK_ENDER
from libs.subHelper import subHelper

FINISHED = 'FINISHED'

class pushStage(threading.Thread):
    def __init__(self,stage,wait_queue,thread_wait,submit_queue,task_id):
        super(pushStage,self).__init__()
        self.stage = stage
        self.wait_queue = wait_queue
        self.thread_wait = thread_wait
        self.submit_queue = submit_queue
        self.task_id = task_id

    def run(self):
        print("start push stage %s" % taskPapa.get_name_from_func(self.stage))
        if taskPapa.get_name_from_func(self.stage) == "do_nothing":
            return

        def is_current_fn_on():
            return self.wait_queue.get()

        res = self.thread_wait.submit(is_current_fn_on)

        class is_current_fn_should_commit(threading.Thread):
            def __init__(se, self):
                super(is_current_fn_should_commit, se).__init__()
                while True:
                    if res.result():
                        self.stage_submitor(self.stage)
                        break
                    time.sleep(0.5)

        xx = is_current_fn_should_commit(self)
        xx.setDaemon(True)
        xx.start()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("")


    def stage_submitor(self, stage):
        func = taskPapa.get_name_from_func(stage)
        print("start submit task %s " % func)
        stir = STI(func, stage, self.task_id,self.wait_queue)
        self.submit_queue.put(stir)
        print("now thread pool thread num is %s" % self.submit_queue.qsize())
        with stageWaiter():
            pass



class taskPapa():

    def __init__(self):
        self.task_id = 0
        self.submit_queue = threadLinkQueue().submit_queue
        self.wait_queue = queue.Queue() # 模拟任务调度，每次编排一个stage
        self.wait_queue.put(True)  # 初始化调度
        self.fix_stage_ls = list()
        self.thread_wait = ThreadPoolExecutor()


    def fix_stages(self) -> list:
        raise Exception("must be implement~!")

    @staticmethod
    def get_name_from_func(func):
        return func.__name__

    def do_nothing(self):
        return 0

    def gen_task_id(self):
        self.task_id = random.randint(1,1000086)
        print("a new task create , end html is http://127.0.0.1:8080/thread_ender/?task_id=%s   "%self.task_id)

    def stage_compose(self):
        self.gen_task_id()
        print("a new task , task id is %s"%self.task_id)
        self.fix_stage_ls = copy(self.fix_stages())
        if self.do_nothing not in self.fix_stage_ls:
            self.fix_stage_ls.append(self.do_nothing)

        for stage in self.fix_stage_ls:
            with pushStage(stage,self.wait_queue,self.thread_wait,self.submit_queue,self.task_id):
                print("")



class stageWaiter(threading.Thread):
    def __init__(self):
        super(stageWaiter, self).__init__()
        self.gtir = threadLinkQueue().submit_queue.get()
        self.thread_submit = threadSubmit().thread_submit
        print("id of thread submit",id(self.thread_submit))

    def __enter__(self):
        self.setDaemon(True)
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self):
        func = self.gtir.get_thread_infos
        exe = self.thread_submit.submit(func)
        rs_queue = queue.Queue()
        with stageEnder(self.gtir, exe, rs_queue):
            try:
                flag = 0   # timeout
                timeo = random.randint(1,2)
                exe.exception(timeout=timeo)

                if not rs_queue.get(block=False):
                    print("step %s end queue get" % self.gtir.fn)
                    print("step %s set flag to 1" % self.gtir.fn)
                    flag = 1  #  killed
                    raise exe._exception
                print("fn %s exe done is " % self.gtir.fn, exe.done())
            except queue.Empty:
                pass

            except ReceiverEndMsgException:
                print(("got end msg for  task %s , task will term self thread %s , name is %s "
                       % (self.gtir.fn, self.gtir.b, self.gtir.a)))
                try:
                    # TASK_ENDER().task_ender(task_id=self.gtir.task_id)
                    stop_thread(self.gtir.b)
                except SystemExit:
                    print("SystemExit error")

            except concurrent.futures._base.TimeoutError as e:
                print("flag is %s" % flag)
                if flag == 0:
                    print("task %s timeout , task will term self thread %s , name is %s " % (
                        self.gtir.fn, self.gtir.b, self.gtir.a))
                elif flag == 1:
                    print("task %s end from queue , task will term self thread %s , name is %s " % (
                        self.gtir.fn, self.gtir.b, self.gtir.a))
                TASK_ENDER().task_ender(task_id=self.gtir.task_id)
                stop_thread(self.gtir.b)
            finally:
                print("getting resulting ")
                self.gtir.wait.put(True)


class stageEnder(threading.Thread):
    def __init__(self, gtir, exe, rs_queue,rdsu=None):
        super(stageEnder, self).__init__()
        self.gtir = gtir
        self.rs_queue = rs_queue
        self.exe = exe
        self.rdsu = rdsu

    def __enter__(self):
        self.setDaemon(True)
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self):

        print("start task init %s"%self.gtir.task_id)
        task_end_sig = subHelper().task_init(self.gtir.task_id)
        if task_end_sig:
            with self.exe._condition:
                print("waiter is ", self.exe._condition._waiters)
                self.exe._condition.notify_all()
                if self.exe._state != FINISHED:
                    self.exe.set_exception(ReceiverEndMsgException)
                    self.rs_queue.put(False)
                else:
                    self.rs_queue.put(True)
