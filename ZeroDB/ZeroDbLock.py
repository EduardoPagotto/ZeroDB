#!/usr/bin/env python3
'''
Created on 20200323
Update on 20201204
@author: Eduardo Pagotto
 '''

import threading
import logging

from ZeroDB.utils import AbortSignal
from ZeroDB.ProxyCall import ProxyCall
from ZeroDB.ZeroDBClient import SessionDB

class ZeroDbLock(object):

    serial = 0
    mutex_serial = threading.Lock()

    def __init__(self, session : SessionDB, table_name: str):

        with ZeroDbLock.mutex_serial:

            self.count = ZeroDbLock.serial
            ZeroDbLock.serial += 1

            self.session : SessionDB = session
            self.table_name : str = table_name
            self.log = logging.getLogger('ZeroDB')
            self.log.debug('Transaction %d', self.count)

    def __enter__(self):
        self.log.debug('acquire %d', self.count)
        self.session.lock()
        self.session.table(self.table_name)
        self.log.debug('acquired %d', self.count)
        return self

    def __exit__(self, type, value, traceback):

        #if not traceback: # FIXME: ver como se comporta no crash
        self.session.unlock()
        self.log.debug('release %d', self.count)
        return isinstance(value, AbortSignal)

    def __getattr__(self, funcion_name : str):

        if funcion_name == '__iter__':
            return None

        return ProxyCall(funcion_name, self.session, self.table_name, self.count)
