#!/usr/bin/env python3
'''
Created on 20190822
Update on 20200602
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import logging

from Zero import ServiceObject
from Zero import ExceptionZeroRPC

class ServerRPC(ServiceObject):
    def __init__(self):
        self.log = logging.getLogger('ServerZeroDB')
        super().__init__('uds://uds_db_teste', self)  # tcp://127.0.0.1:5151 #uds://./uds_db_teste
        #self.files = []
        #self.tables_name = []

    def connect(self, file, table_name):
        pass

    # #@ServiceObject.rpc_call(rpc.GET_DICIONARIO_INTERFACE, input=('d',), output=('d'))
    # def get_dict(self, dicionario):
    #     dicionario['novo'] = 'ola'
    #     return dicionario

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    server = ServerRPC()
    server.loop_blocked()
