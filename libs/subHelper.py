#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/30.

import zmq

from logUtils.log import Log


class subHelper():
    def __init__(self,debug=False):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        print("Collecting msg from server...")
        self.socket.connect("tcp://127.0.0.1:5557")
        self.log = Log().get_log()
        self.debug = debug


    def task_init(self,task_id):
        while True:
            msg = self.socket.recv_string()
            if self.debug:
                self.log.info("recv a message %s",msg)
            recv_task_id,cmd = msg.split()
            if int(recv_task_id) == task_id:
                self.log.info("recv end signal from pub system !")
                self.log.info("end task id is %s",task_id)
                return 1


    def task_exit(self):
        self.socket.close()



if __name__ == '__main__':
    ff = subHelper(debug=True)
    ff.task_init(12)