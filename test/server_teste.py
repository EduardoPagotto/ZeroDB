#!/usr/bin/env python3
'''
Created on 20200603
Update on 20201207
@author: Eduardo Pagotto
'''

import logging

from Zero import GracefulKiller
from ZeroDB import ZdbServer

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    log = logging.getLogger('ServerTest')

    log.info('Iniciado')

    server = ZdbServer('uds://./data/uds_db_teste')
    server.loop_blocked(GracefulKiller())

    log.info('Finalizado')
