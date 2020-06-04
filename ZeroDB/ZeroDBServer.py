#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200603
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import re
import logging
import threading
from tinydb import TinyDB

from Zero import ServiceObject #, ExceptionZeroRPC

class ProxyDB(object):
    def __init__(self, name, mapa):
        self.name = name
        self.mapa = mapa
        self.log = logging.getLogger('ZeroDB.Server')
        self.log.debug('Name: %s', name)

    def __call__(self, *args, **kargs):
        # Como em  ProxyCall
        self.log.debug('Recebido: %s; %s', str(args), str(kargs))

        dataDB = self.mapa[kargs['__db_name']]
        del kargs['__db_name']
        del kargs['__table_name']

        function = getattr(dataDB.table, self.name)
        return function(*args, **kargs)

class MapDataDB(object):
    def __init__(self, *args, **kargs):
        self.db = TinyDB(*args, **kargs)
        self.keydb = re.sub(r'\W+', '', args[0])
        self.table_name = 'Default'
        self.table = self.db.table(self.table_name)
        self.mutex_acess = threading.Lock()

    def setTable(self, table_name):
        if self.table_name != table_name:
            self.table = self.db.table(table_name)
            self.table_name = table_name

class ZeroDBServer(ServiceObject):
    def __init__(self, str_connection):
        super().__init__(str_connection, self)  # tcp://127.0.0.1:5151 #uds://./uds_db_teste
        self.log = logging.getLogger('ZeroDB.Server')
        self.log.info('Servidor ativo: %s', str_connection)
        self.mapa = {}

    def connect(self, *args, **kargs):

        key_db = re.sub(r'\W+', '', args[0])
        key_find = None
        for k, v in self.mapa.items():
            if k == key_db:
                key_find = k

        if key_find is None:
            self.mapa[key_db] = MapDataDB(*args, **kargs)

        return key_db

    def select_table(self, db_name, table_name):
        for k, v in self.mapa.items():
            if k == db_name:
                v.mutex_acess.acquire()
                v.setTable(table_name)
                return

        msg = 'Nao existe Instancia do DB: {0}'.format(db_name)
        self.log.error(msg)
        raise Exception(msg)

    def un_select_table(self, db_name):
        for k, v in self.mapa.items():
            if k == db_name:
                v.mutex_acess.release()
                return

    def __getattr__(self, name):
        if name == '__iter__':
            return None

        return ProxyDB(name, self.mapa)
