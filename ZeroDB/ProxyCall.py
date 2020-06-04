#!/usr/bin/env python3
'''
Created on 20200602
Update on 20200603
@author: Eduardo Pagotto
 '''

import logging

class ProxyCall(object):
    def __init__(self, function, client, table_name, count):
        self.function = function
        self.client = client
        self.table_name = table_name
        self.count = count
        self.log = logging.getLogger('ZeroDB')

    def __call__(self, *args, **kargs):
        self.log.debug('ProxyCall %d: func: %s, args: %s, kargs:%s', self.count, str(self.function), str(args), str(kargs))
        function = getattr(self.client.peer, self.function)
        return function(*args, **dict(kargs, __table_name=self.table_name, __db_name=self.client.db_name))