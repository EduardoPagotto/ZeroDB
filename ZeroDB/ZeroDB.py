#!/usr/bin/env python3
'''
Created on 20200602
Update on 20200602
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