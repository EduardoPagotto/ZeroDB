#!/usr/bin/env python3
'''
Created on 20200603
Update on 20200627
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import sys
import logging
from datetime import datetime
from bson.objectid import ObjectId

from ZeroDB import ZeroDBClient, ZeroDbLock

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    log = logging.getLogger('ClientTest')
    log.info('Iniciado')

    try:
        zdb = ZeroDBClient('uds://./data/uds_db_teste', './data/db_teste1.json')
    except Exception as exp:
        log.error('Falha critica conexao: %s', str(exp))
        sys.exit()

    id_teste = str(ObjectId())

    try:
        with ZeroDbLock(zdb, 'tabela01') as ztr:
            #time.sleep(self.espara)

            ztr.insert({'id_data':  str(ObjectId()),
                        'idade':10,
                        'status':0,
                        'nome':'Eduardo Pagotto',
                        'sexo':True,
                        'last':datetime.timestamp(datetime.now())})

    except Exception as exp:
        log.error('erro %s: %s', id_teste, str(exp))

    log.debug('End: %s', id_teste)
