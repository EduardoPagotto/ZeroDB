#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200324
@author: Eduardo Pagotto
 '''

import logging

from datetime import datetime
from bson.objectid import ObjectId

from tinydb import Query, where 
from tinydb.operations import increment

from ZeroDB.ZeroTransaction import ZeroTransaction, ZeroTinyDB

def main():

    # criação
    zdb = ZeroTinyDB('./data/db_teste1.json', sort_keys=True, indent=4, separators=(',', ': '))

    zdb.log.info('Iniciado')
    
    table_access = zdb.table_access('tabela01')
    
    try:

        with ZeroTransaction(table_access) as ztr:

            # inserção dado
            ztr.insert({'id_data': str(ObjectId()),
                        'idade':10,
                        'status':0,
                        'nome':'Eduardo Pagotto',
                        'sexo':True,
                        'last':datetime.timestamp(datetime.now())})

            ztr.insert({'id_data': str(ObjectId()),
                        'status':0,
                        'idade':51,
                        'nome':'Eduardo Pagotto',
                        'sexo':True,
                        'last':datetime.timestamp(datetime.now())})

            ztr.insert({'id_data': str(ObjectId()),
                        'status':0,
                        'idade':55,
                        'nome':'Eduardo Pagotto',
                        'sexo':True,
                        'last':datetime.timestamp(datetime.now())})              

            ztr.insert({'id_data': str(ObjectId()),
                        'status':0,
                        'nome':'Eduardo Pagotto',
                        'sexo':False,
                        'idade':30,
                        'last':datetime.timestamp(datetime.now())})

            # query com where
            result2 = ztr.search(where('sexo') == False)
            zdb.log.debug(str(result2))

            for item in result2:
                ztr.update(increment('status'), where('id_data')==item['id_data'])

            # query
            dados = Query() 

            result = ztr.search((dados.idade > 50) & (dados.sexo == True))
            zdb.log.debug(str(result))

            ultimo = None
            for item in result:
                # update
                novo = {'last': datetime.timestamp(datetime.now()), 'status':3}
                ztr.update(novo, where('id_data')==item['id_data'])
                ultimo = item

            ztr.remove(dados.id_data == ultimo['id_data'])

            lista_existe = ztr.search(where('id_data') == ultimo['id_data'])

            # Mostra tudo
            result = ztr.all()
            zdb.log.debug(str(result))

    except Exception as exp:
        zdb.log.error('erro: %s', str(exp))

    zdb.log.info('fim')

if __name__ == "__main__":
    
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    main()
