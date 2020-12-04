#!/usr/bin/env python3
'''
Created on 20200602
Update on 20201204
@author: Eduardo Pagotto
 '''

from Zero.ProxyObject import ProxyObject
from typing import List, Optional
import threading
import logging

from Zero import ServiceBus

class SessionDB(object):
    def __init__(self, database_name : str, connection_str : str) -> None:

        self.database_name : str = database_name
        self.table_name : str = 'Default'

        self.bus = ServiceBus(s_address=connection_str, retry=5, max_threads=5)
        self.rpc : ProxyObject = self.bus.getObject()
        self.id = self.rpc.open(database_name)

        self.critical : threading.Lock = threading.Lock()

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



class ZeroDBClient(object):
    """[Classe de Conexao ao Servidor remoto]
    Arguments:
        ServiceBus {[type]} -- [description]
    """
    def __init__(self, connection_str : str) -> None:

        self.log = logging.getLogger('ZeroDB.Client')
        self.connection_str : str = connection_str
        self.sessions : List[SessionDB] = []

    def __del__(self):

        for sessao in reversed(self.sessions):
            self.sessions.remove(sessao)
            del sessao

    def open(self, database_name : str) -> SessionDB:

        session : SessionDB = SessionDB(database_name, self.connection_str)
        self.sessions.append(session)
        return session

    def close(self, session : SessionDB) -> None:

        self.sessions.remove(session)
        del session



