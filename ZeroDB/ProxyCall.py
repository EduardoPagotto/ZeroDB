#!/usr/bin/env python3
'''
Created on 20200602
Update on 20201204
@author: Eduardo Pagotto
 '''

from ZeroDB.ZeroDBClient import ZdbClientSession
import logging

class ProxyCall(object):
    def __init__(self, function : str, session : ZdbClientSession, table_name : str, count : int):
        self.function = function
        self.session = session
        self.table_name = table_name
        self.count = count
        self.log = logging.getLogger('ZeroDB')

    def __call__(self, *args, **kargs):
        self.log.debug('ProxyCall %d: func: %s, args: %s, kargs:%s', self.count, str(self.function), str(args), str(kargs))
        function = getattr(self.session.rpc, self.function)
        return function(*args, **dict(kargs, __table_name=self.table_name, __session_id=self.session.id))