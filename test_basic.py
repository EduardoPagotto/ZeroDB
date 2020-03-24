#!/usr/bin/env python3
'''
Created on 20200324
Update on 20200324
@author: Eduardo Pagotto
 '''

from datetime import datetime
from bson.objectid import ObjectId

from tinydb import TinyDB, Query, where 
from tinydb.operations import increment

def main():

    # criação
    db = TinyDB('./data/db_teste0.json', sort_keys=True, indent=4, separators=(',', ': '))

    tabela = db.table('tabela01')

    # inserção dado
    tabela.insert({'id_data': str(ObjectId()),
               'idade':10,
               'status':0,
               'nome':'Eduardo Pagotto',
               'sexo':True,
               'last':datetime.timestamp(datetime.now())})

    tabela.insert({'id_data': str(ObjectId()),
               'status':0,
               'idade':51,
               'nome':'Eduardo Pagotto',
               'sexo':True,
               'last':datetime.timestamp(datetime.now())})

    tabela.insert({'id_data': str(ObjectId()),
               'status':0,
               'idade':55,
               'nome':'Eduardo Pagotto',
               'sexo':True,
               'last':datetime.timestamp(datetime.now())})              

    tabela.insert({'id_data': str(ObjectId()),
               'status':0,
               'nome':'Eduardo Pagotto',
               'sexo':False,
               'idade':30,
               'last':datetime.timestamp(datetime.now())})

    # query com where
    result2 = tabela.search(where('sexo') == False)
    print(str(result2))
    for item in result2:
        tabela.update(increment('status'), where('id_data')==item['id_data'])

    # query
    dados = Query() 

    result = tabela.search((dados.idade > 50) & (dados.sexo == True))
    print(str(result))

    ultimo = None
    for item in result:
        # update
        novo = {'last': datetime.timestamp(datetime.now()), 'status':3}
        tabela.update(novo, where('id_data')==item['id_data'])
        ultimo = item

    tabela.remove(dados.id_data == ultimo['id_data'])

    lista_existe = tabela.search(where('id_data') == ultimo['id_data'])

    # Mostra tudo
    result = tabela.all()
    print(str(result))