#!/usr/bin/env python3
'''
Created on 20200603
Update on 20200603
@author: Eduardo Pagotto
'''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import logging

from Zero import GracefulKiller
from ZeroDB import ZeroDBServer

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(threadName)-16s %(funcName)-20s %(message)s',
        datefmt='%H:%M:%S',
    )

    log = logging.getLogger('ServerTest')

    log.info('Iniciado')

    server = ZeroDBServer('uds://uds_db_teste')
    server.loop_blocked(GracefulKiller())

    log.info('Finalizado')
