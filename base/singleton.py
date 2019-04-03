#coding:utf-8
#!/usr/bin/env python
#Created by Charles on 2019/3/30.

def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton