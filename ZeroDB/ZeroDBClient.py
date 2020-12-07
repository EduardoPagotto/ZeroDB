#!/usr/bin/env python3
'''
Created on 20200602
Update on 20201207
@author: Eduardo Pagotto
 '''

from Zero.ProxyObject import ProxyObject
from typing import List, Optional
import logging

from ZeroDB.ZdbClientSession import ZdbClientSession

class ZeroDBClient(object):
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



