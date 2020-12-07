#!/usr/bin/env python3
'''
Created on 20201207
Update on 20201207
@author: Eduardo Pagotto
 '''

from typing import Optional, List
import threading
import logging

from Zero import ServiceBus
from Zero.ProxyObject import ProxyObject


__all__ = ('ZdbClient', 'ZdbClientSession', 'ZdbLock')

class AbortSignal(Exception):
    pass

def abort():
    raise AbortSignal

class ZdbClientSession(object):
    def __init__(self, database_name : str, connection_str : str) -> None:

        self.database_name : str = database_name
        self.table_name : str = 'Default'

        self.bus = ServiceBus(s_address=connection_str, retry=5, max_threads=5)
        self.rpc : ProxyObject = self.bus.getObject()
        self.id = self.rpc.open(database_name)

        self.critical : threading.Lock = threading.Lock()
        self.log = logging.getLogger('ZeroDB.ZdbClientSession')

    def __del__(self):
        del self.rpc

    def table(self, name : Optional[str] = None) -> None:
        if name is None:
            self.table_name = 'Default'

        self.rpc.table(self.id, name)

    def lock(self):
        self.critical.acquire()
        self.rpc.enter_trans(self.id)

    def unlock(self):
        self.critical.release()
        self.rpc.exit_trans(self.id)

##-----

class ZdbClient(object):
    """[Classe de Conexao ao Servidor remoto]
    Arguments:
        ServiceBus {[type]} -- [description]
    """
    def __init__(self, connection_str : str) -> None:

        self.log = logging.getLogger('ZeroDB.Client')
        self.connection_str : str = connection_str
        self.sessions : List[ZdbClientSession] = []

    def __del__(self):

        for sessao in reversed(self.sessions):
            self.sessions.remove(sessao)
            del sessao

    def open(self, database_name : str) -> ZdbClientSession:

        session : ZdbClientSession = ZdbClientSession(database_name, self.connection_str)
        self.sessions.append(session)
        return session

    def close(self, session : ZdbClientSession) -> None:

        self.sessions.remove(session)
        del session

#---

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

#---

class ZdbLock(object):

    serial = 0
    mutex_serial = threading.Lock()

    def __init__(self, session : ZdbClientSession, table_name: str):

        with ZdbLock.mutex_serial:

            self.count = ZdbLock.serial
            ZdbLock.serial += 1

            self.session : ZdbClientSession = session
            self.table_name : str = table_name
            self.log = logging.getLogger('ZeroDB')
            self.log.debug('Transaction %d', self.count)

    def __enter__(self):
        self.log.debug('acquire %d', self.count)
        self.session.lock()
        self.session.table(self.table_name)
        self.log.debug('acquired %d', self.count)
        return self

    def __exit__(self, type, value, traceback):

        #if not traceback: # FIXME: ver como se comporta no crash
        self.session.unlock()
        self.log.debug('release %d', self.count)
        return isinstance(value, AbortSignal)

    def __getattr__(self, funcion_name : str):

        if funcion_name == '__iter__':
            return None

        return ProxyCall(funcion_name, self.session, self.table_name, self.count)