#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/30.
import logging
import queue
from queue import Queue
from threading import Thread
import zmq
from base.const import MSG_ENG, SHUT_DOWN
from logUtils.log import Log


class pubHelper(Thread):
    def __init__(self):
        super(pubHelper, self).__init__()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5557")
        self.queue = Queue()
        self.log = Log().get_log()


    def sig_recv(self,task_id):
        try:
            self.socket.get_hwm()
        except zmq.error.ZMQError:
            print("ZMQ maybe shutdown")
            return -1
        self.queue.put(task_id)
        return 0


    def run(self):
        while True:
            try:
                task_id = self.queue.get(block=True,timeout=10)
                task_id = int(task_id)
                self.socket.send("%a %a".encode("utf-8") % (task_id, MSG_ENG))
            except queue.Empty :
                continue
            except ValueError:
                if task_id == SHUT_DOWN:
                    print("end pub-sub system!")
                    self.socket.close()
                    self.context.term()
                    break
                self.log.info("Error msg --- task_id is  %s"%task_id)

            except Exception as e:
                print(e.args)
                print("Unknow Error!")



if __name__ == '__main__':
    ph = pubHelper()
    ph.start()
    while True:
        task_id = input("id\n")
        rest = ph.sig_recv(task_id)
        if rest == -1:
            print("error accur, exit system")
            exit(rest)

