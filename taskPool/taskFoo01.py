#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.
import time
from concurrent.futures.thread import ThreadPoolExecutor

from base.queues import threadLinkQueue
from taskPool.taskPa import taskPapa


class Foo(taskPapa):

    def fix_stages(self):
        stages = []
        stages.append(self.do_foo),
        stages.append(self.do_bar)
        return stages

    def do_foo(self):
        for i in range(20):
            time.sleep(2)
            print("%s sleep * %s"%(self.task_id,i))
        print("this is foo \n")

    def do_bar(self):
        print("this is bar\n")


if __name__ == '__main__':
    time1 = time.time()
    thread_test = ThreadPoolExecutor(thread_name_prefix="thread_test")

    for i in range(10):
        fO = Foo()
        fO.stage_compose()
    while threadLinkQueue().task_wait_queue.empty():
        threadLinkQueue().task_wait_queue.get().join()

    print("total cost ",time.time() - time1)
