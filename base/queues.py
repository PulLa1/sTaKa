#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.

from queue import Queue

from base.singleton import Singleton

MAX_QUEUE_SIZE = 10

@Singleton
class threadLinkQueue():
    def __init__(self):
        self.submit_queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self.wait_queue = Queue(maxsize=MAX_QUEUE_SIZE)
        self.task_wait_queue = Queue(maxsize=MAX_QUEUE_SIZE)

