#!/usr/bin/env python3
'''
Created on 20200602
Update on 20200602
@author: Eduardo Pagotto
 '''

import logging

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