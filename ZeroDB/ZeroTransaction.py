#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200602
@author: Eduardo Pagotto
 '''

import threading
import logging

from ZeroDB.ZeroDB import ZeroTinyDB, AbortSignal
from ZeroDB.ProxyCall import ProxyCall

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

