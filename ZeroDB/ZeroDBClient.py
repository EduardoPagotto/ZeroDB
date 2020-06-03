#!/usr/bin/env python3
'''
Created on 20200602
Update on 20200603
@author: Eduardo Pagotto
 '''

#pylint: disable=C0301, C0116, W0703, C0103, C0115

import threading
import logging

from Zero import ServiceBus

class ZeroDBClient(ServiceBus):
    """[Classe de Conexao ao Servidor remoto]
    Arguments:
        ServiceBus {[type]} -- [description]
    """
    def __init__(self, connection_str, file_data):
        """[summary]
        Arguments:
            connection_str {[type]} -- [String de conexao]
            file_data {[type]} -- [Arquivo de db]
        """
        super().__init__(connection_str)
        self.log = logging.getLogger('ZeroDB.Client')
        self.peer = self.getObject()
        self.peer.connect(file_data, sort_keys=True, indent=4, separators=(',', ': '))
        self.mutex_access = threading.Lock()

    def table_access(self, *args, **kwargs):
        """[Acesso a trava e conexao remota]
        Returns:
            [Tupla(mutex, proxy)] -- [Tupla com trava e metodos remotos]
        """
        return self.mutex_access, self.peer #self.db.table(*args, **kwargs)
