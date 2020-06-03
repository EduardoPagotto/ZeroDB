#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200603
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import logging
from tinydb import TinyDB

from Zero import ServiceObject #, ExceptionZeroRPC

class MapDataDB(object):
    def __init__(self, *args, **kargs):
        self.db = TinyDB(*args, **kargs)
        self.tables = []

    def setTable(self, table_name):
        self.tables.append(table_name)


class ZeroDBServer(ServiceObject):
    def __init__(self, str_connection):
        super().__init__(str_connection, self)  # tcp://127.0.0.1:5151 #uds://./uds_db_teste
        self.log = logging.getLogger('ZeroDB.Server')
        self.log.info('Servidor ativo: %s', str_connection)
        self.mapa = []

    def connect(self, *args, **kargs):
        item = MapDataDB(*args, **kargs)
        self.mapa.append(item)

    # #@ServiceObject.rpc_call(rpc.GET_DICIONARIO_INTERFACE, input=('d',), output=('d'))
    # def get_dict(self, dicionario):
    #     dicionario['novo'] = 'ola'
    #     return dicionario
