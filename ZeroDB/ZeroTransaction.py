#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200603
@author: Eduardo Pagotto
 '''

import threading
import logging

from ZeroDB.Utils import AbortSignal
from ZeroDB.ProxyCall import ProxyCall

class ZeroTransaction(object):

    serial = 0
    mutex_serial = threading.Lock()

    def __init__(self, client, table_name):

        with ZeroTransaction.mutex_serial:

            self.count = ZeroTransaction.serial
            ZeroTransaction.serial += 1

            self.client = client
            self.table_name = table_name
            self.log = logging.getLogger('ZeroDB')
            self.log.debug('Transaction %d', self.count)

    def __enter__(self):
        self.log.debug('acquire %d', self.count)
        self.client.mutex_access.acquire()
        self.client.peer.select_table(self.client.db_name, self.table_name)
        self.log.debug('acquired %d', self.count)
        return self

    def __exit__(self, type, value, traceback):
        #if not traceback: # FIXME: ver como se comporta no crash
        self.client.mutex_access.release()
        self.client.peer.un_select_table(self.client.db_name)
        self.log.debug('release %d', self.count)
        return isinstance(value, AbortSignal)

    def __getattr__(self, name):

        if name == '__iter__':
            return None

        return ProxyCall(name, self.client, self.table_name, self.count)
