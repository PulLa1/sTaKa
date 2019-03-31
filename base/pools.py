#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.


from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

from base.queues import MAX_QUEUE_SIZE
from base.singleton import Singleton
from base.stageRange import thread_pool_init


THREAD_WAIT = ThreadPoolExecutor(thread_name_prefix="thread_wait", max_workers=MAX_QUEUE_SIZE, initializer=thread_pool_init)
THREAD_SHOULD_SUBMIT = ThreadPoolExecutor(thread_name_prefix="thread_submit", max_workers=MAX_QUEUE_SIZE, initializer=thread_pool_init)


@Singleton
class threadSubmit():
    def __init__(self):
        self.thread_submit = THREAD_SHOULD_SUBMIT

