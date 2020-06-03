#!/usr/bin/env python3
'''
Created on 20200324
Update on 20200603
@author: Eduardo Pagotto
 '''

import time
import logging
import threading

from datetime import datetime
#from bson.objectid import ObjectId

from ZeroDB import ZeroTransaction, ZeroDBClient #, ZeroTinyDB

class Thread_Test(object):
    def __init__(self, table_access, id, delay, espera):
        self.table_access = table_access
        self.id = id
        self.log = logging.getLogger('Test')
        self.delay = delay
        self.espara = espera

    def get_name(self):
        return 'th_{0}'.format(self.id)

    def __call__(self, *args, **kargs):

        self.log.debug('Begin: %d', self.id)

        #time.sleep(self.delay)

        try:
            with ZeroTransaction(self.table_access) as ztr:
                #time.sleep(self.espara)

                self.log.debug('Executa %d', self.id)

                ztr.insert({'id_data': self.id,#str(ObjectId()),
                            'idade':10,
                            'status':0,
                            'nome':'Eduardo Pagotto',
                            'sexo':True,
                            'last':datetime.timestamp(datetime.now())})

        except Exception as exp:
            self.log.error('erro %d: %s',self.id, str(exp))

        time.sleep(10)

        self.log.debug('End: %d', self.id)

def main():

    zdb = ZeroDBClient('uds://uds_db_teste', './data/db_teste1.json')
    zdb.log.info('Iniciado')

    table_access = zdb.table_access('tabela01')

    lista_classes = []
    lista_threads = []

    for indice in range(1):
        lista_classes.append(Thread_Test(table_access, indice, 1, 5))

    for item in lista_classes:
        lista_threads.append(threading.Thread(target=item, name= item.get_name()))

    for item in lista_threads:
        item.start()

    while len(lista_threads) !=0:
        for item in lista_threads:
            item.join()
            lista_threads.remove(item)
            break
        time.sleep(1)

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    main()
