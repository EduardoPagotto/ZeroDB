#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200323
@author: Eduardo Pagotto
 '''

import threading

from tinydb import TinyDB #, Query, where 
#from tinydb.operations import increment

class AbortSignal(Exception):
    pass

def abort():
    raise AbortSignal

def records(cls):
    @wraps(cls)
    def proxy(self, *args, **kwargs):
        self.record.append(cls(*args, **kwargs))
    return proxy


class ZeroTinyDB(object):
    def __init__(self, *args, **kwargs):
        self.db = TinyDB(*args, **kwargs)
        
    def table(self, *args, **kwargs):
        self.db.table(*args, **kwargs)

class ProxyCall(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kargs):
        print('ProxyCall {0} {1} {2}'.format(self.function, str(args), str(kargs)))

        self.function(*args, **kargs)


        return True

class ZeroTransaction(object):
    def __init__(self, table):
        self.table = table
        self.mutex_free = threading.Lock()

    def __enter__(self):
        self.mutex_free.acquire()
        return self

    def __exit__(self, type, value, traceback):
        #if not traceback: # FIXME: ver como se comporta no crash
        self.mutex_free.release()
        return isinstance(value, AbortSignal)

    def __getattr__(self, name):
        return ProxyCall(name)

