#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.
import ctypes
import inspect
import threading


class STI:
    def __init__(self, fn, func,task_id,wait):
        self.fn = fn
        self.a = None
        self.b = None
        self.func = func
        self.task_id = task_id
        self.wait = wait

    def get_thread_infos(self):
        print("curret stage thread name is %s , thread id is %s" % (
            threading.currentThread().getName(), threading.currentThread().ident))
        self.a = threading.currentThread().getName()
        self.b = threading.currentThread().ident
        return self.func()


def thread_pool_init():
    print("start a new thread in the pool, id is %s, name is %s \n" % (
        threading.currentThread().ident, threading.currentThread().getName()))



def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread, SystemExit)
