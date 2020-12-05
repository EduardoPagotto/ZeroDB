#!/usr/bin/env python3
'''
Created on 20200603
Update on 20201204
@author: Eduardo Pagotto
'''

import sys
import logging
from datetime import datetime
from bson.objectid import ObjectId

from tinydb import Query, where
from tinydb.operations import increment

from ZeroDB import ZeroDBClient, ZeroDbLock

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    log = logging.getLogger('ClientTest')
    log.info('Iniciado')

    zdb = None
    sdb = None

    try:
        zdb = ZeroDBClient('uds://./data/uds_db_teste')
        sdb = zdb.open('db_teste1')

    except Exception as exp:
        log.error('Falha critica conexao: %s', str(exp))
        sys.exit()

    id_teste = str(ObjectId())

    try:
        with ZeroDbLock(sdb, 'tabela01') as ztr:
            #time.sleep(self.espara)

            # inserção dado
            val01 = ztr.insert({'id_data': str(ObjectId()),
                                'idade':10,
                                'status':0,
                                'nome':'Eduardo Pagotto',
                                'sexo':True,
                                'last':datetime.timestamp(datetime.now())})

            val02 = ztr.insert({'id_data': str(ObjectId()),
                                'status':0,
                                'idade':51,
                                'nome':'Eduardo Pagotto',
                                'sexo':True,
                                'last':datetime.timestamp(datetime.now())})

            val03 = ztr.insert({'id_data': str(ObjectId()),
                                'status':0,
                                'idade':55,
                                'nome':'Eduardo Pagotto',
                                'sexo':True,
                                'last':datetime.timestamp(datetime.now())})

            val04 = ztr.insert({'id_data': str(ObjectId()),
                                'status':0,
                                'nome':'Eduardo Pagotto',
                                'sexo':False,
                                'idade':30,
                                'last':datetime.timestamp(datetime.now())})

            # query com where
            result2 = ztr.search(where('sexo') == False)
            log.debug(str(result2))

            for item in result2:
                ztr.update(increment('status'), where('id_data')==item['id_data'])

            # query
            dados = Query()

            result = ztr.search((dados.idade > 50) & (dados.sexo == True))
            log.debug(str(result))

            ultimo = None
            for item in result:
                # update
                novo = {'last': datetime.timestamp(datetime.now()), 'status':3}
                ztr.update(novo, where('id_data') == item['id_data'])
                ultimo = item

            ztr.remove(dados.id_data == ultimo['id_data'])

            lista_existe = ztr.search(where('id_data') == ultimo['id_data'])

            # Mostra tudo
            result = ztr.all()
            log.debug(str(result))

    except Exception as exp:
        log.error('erro %s: %s', id_teste, str(exp))

    log.debug('End: %s', id_teste)
