#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/29.

import cherrypy

from base.singleton import Singleton
from libs.pubHelper import pubHelper




@Singleton
class pubInit():
    def __init__(self):
        self.pub = pubHelper()
        self.pub.start()

    def handler(self,task_id):
        return self.pub.sig_recv(task_id)

@cherrypy.expose
class ThreadEnderApi():
    def GET(self,task_id):
        try:
            int(task_id)
        except:
            print("task_id must be a integer! not %s" % task_id)
            return

        rh = pubInit()
        rh.handler(task_id)
        return task_id





if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(ThreadEnderApi(), '/thread_ender', conf)