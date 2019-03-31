#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.

import requests

from base.singleton import Singleton

ender_url = "http://127.0.0.1:8080/thread_ender/?task_id=%s"

@Singleton
class TASK_ENDER():

    def task_ender(self,step_id=None,task_id=None):
        requests.get(ender_url%task_id)
