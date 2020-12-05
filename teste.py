#!/usr/bin/env python3
'''
Created on 20200703
Update on 20201204
@author: Eduardo Pagotto
'''

from ZeroDB.queries import Query

if __name__ == '__main__':

    print('teste inicio')

    query = Query()

    # val = query.id == 10
    # QueryImpl('==', ('id',), 10)

    val = (query.id == 10) & (query.name != 'Joao')
    # QueryImpl('and', frozenset({('==', ('id',), 10), ('!=', ('name',), 'Joao')}))

    # val = (query.id == 10) & (query.name != 'Joao') & (query.sexo == False)
    # QueryImpl('and', frozenset({('==', ('sexo',), False), ('and', frozenset({('==', ('id',), 10), ('!=', ('name',), 'Joao')}))}))

    #val = ((query.id == 10) & (query.name != 'Joao')) | (query.sexo == False)
    # QueryImpl('or', frozenset({('==', ('sexo',), False), ('and', frozenset({('==', ('id',), 10), ('!=', ('name',), 'Joao')}))}))

    #val = ((query.summary.id.val == 10) & (query.summary.id.data != '2009')) | (query.sexo == False)
    #val = (query.id == 10) & (query.name != 'joao')



    print(val)
