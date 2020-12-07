#!/usr/bin/env python3
'''
Created on 20190822
Update on 20201207
@author: Eduardo Pagotto
'''

import logging
import threading
from typing import List
from tinydb import TinyDB

from bson.objectid import ObjectId

from Zero import ServiceObject

__all__ = ('ZdbServer', 'ZdbServerSession')

class ZdbServerSession(object):
    def __init__(self, database_name : str) -> None:

        self.database_name = database_name
        self.db = TinyDB('./data/{0}.json'.format(database_name), sort_keys=True, indent=4, separators=(',', ': '))
        self.id = str(ObjectId())

        self.table_name = 'Default'
        self.table = self.db.table(self.table_name)
        self.critical = threading.Lock()

        self.critical_write = threading.Lock()

    def setTable(self, table_name : str) -> None:
        if self.table_name != table_name:
            self.table = self.db.table(table_name)
            self.table_name = table_name

    def lock(self):
        self.critical.acquire()

    def unlock(self):
        self.critical.release()

#---

class ProxyDB(object):
    def __init__(self, function_name : str, sessions : ZdbServerSession):
        self.function_name = function_name
        self.sessions = sessions
        self.log = logging.getLogger('ZeroDB.Server')
        self.log.debug('Name: %s', function_name)

    def __call__(self, *args, **kargs):
        # Como em  ProxyCall
        self.log.debug('Recebido: %s; %s', str(args), str(kargs))

        session = None
        for st in self.sessions:
            if st.id == kargs['__session_id']:
                session = st

        if session is None:
            raise Exception("Id invalido: %s", id)

        del kargs['__session_id']
        del kargs['__table_name']

        function = getattr(session.table, self.function_name)
        return function(*args, **kargs)

#---

class ZdbServer(ServiceObject):
    def __init__(self, str_connection : str) -> None:
        super().__init__(str_connection, self)  # tcp://127.0.0.1:5151 #uds://./uds_db_teste

        self.log = logging.getLogger('ZeroDB.Server')
        self.log.info('Servidor ativo: %s', str_connection)

        self.sessions : List[ZdbServerSession] = []

    def open(self, database_name : str) -> str:

        session = None
        for st in self.sessions:
            if st.database_name == database_name:
                self.log.info('refercenc server session: %s', st.id)
                session = st

        if session is None:
            session = ZdbServerSession(database_name)
            self.log.info('new server session: %s', session.id)
            self.sessions.append(session)

        return session.id

    def __find_session(self, id : str) -> ZdbServerSession:
        for session in self.sessions:
            if session.id == id:
                return session

        raise Exception('session id not fond: %s', id)

    def enter_trans(self, id : str):
        session = self.__find_session(id)
        session.lock()

    def exit_trans(self, id : str):
        session = self.__find_session(id)
        session.unlock()

    def table(self, id : str, name : str) -> None:
        session = self.__find_session(id)
        session.setTable(name)

    # def insert(self, id : str, document : Dict):
    #     session = self.__find_session(id)
    #     with session.critical_write:
    #         session.table.insert(document)

    # def select_table(self, id : str, table_name : str):
    #     session = self.__find_session(id)
    #     session.lock()
    #     session.setTable(table_name)

    # def un_select_table(self, id : str):
    #     session = self.__find_session(id)
    #     session.unlock()

    def __getattr__(self, function_name):
        if function_name == '__iter__':
            return None

        return ProxyDB(function_name, self.sessions)