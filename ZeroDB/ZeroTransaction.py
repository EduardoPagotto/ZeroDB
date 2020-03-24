#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200324
@author: Eduardo Pagotto
 '''

import threading
import logging

from tinydb import TinyDB 

class AbortSignal(Exception):
    pass

def abort():
    raise AbortSignal

# def records(cls):
#     @wraps(cls)
#     def proxy(self, *args, **kwargs):
#         self.record.append(cls(*args, **kwargs))
#     return proxy

class ZeroTinyDB(object):
    def __init__(self, *args, **kwargs):
        self.db = TinyDB(*args, **kwargs)
        self.mutex_access = threading.Lock()
        self.log = logging.getLogger('ZeroDB')
        
    def table_access(self, *args, **kwargs):
        return self.mutex_access, self.db.table(*args, **kwargs)

class ProxyCall(object):
    def __init__(self, function, table, count):
        self.function = function
        self.table = table
        self.log = logging.getLogger('ZeroDB')
        self.count = count

    def __call__(self, *args, **kargs):
        self.log.debug('ProxyCall %d: func: %s, args: %s, kargs:%s', self.count, str(self.function), str(args), str(kargs))
        function = getattr(self.table, self.function)
        return function(*args, **kargs)

class ZeroTransaction(object):

    serial = 0
    mutex_serial = threading.Lock()

    def __init__(self, table_access):

        with ZeroTransaction.mutex_serial:

            self.count = ZeroTransaction.serial
            ZeroTransaction.serial += 1

            self.table = table_access[1]
            self.mutex_free = table_access[0]
            self.log = logging.getLogger('ZeroDB')
            self.log.debug('Transaction %d', self.count)

    def __enter__(self):
        self.log.debug('acquire %d', self.count)
        self.mutex_free.acquire()
        self.log.debug('acquired %d', self.count)
        return self

    def __exit__(self, type, value, traceback):
        #if not traceback: # FIXME: ver como se comporta no crash
        self.mutex_free.release()
        self.log.debug('release %d', self.count)
        return isinstance(value, AbortSignal)

    def __getattr__(self, name):

        if name == '__iter__':
            return None

        return ProxyCall(name, self.table, self.count)

