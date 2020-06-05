#!/usr/bin/env python3
'''
Created on 20200323
Update on 20200603
@author: Eduardo Pagotto
 '''

import time

class ClasseTeste(object):
    def __init__(self):
        print('ClasseTeste constructor')

    def __del__(self):
        print('ClasseTeste destructor')

    def exec1(self):
        print('ClasseTeste exec1!!')

class ZeroLock(object):
    def __init__(self):
        print('INIT!!')
        self.valor1 = ClasseTeste()

    def __enter__(self):
        print('ENTER!!')
        return self.valor1 #ClasseTeste()

    def __exit__(self, exc_type, exc_value, traceback):
        print('EXIT!!')
        self.valor1 = None
        del self.valor1
        return isinstance(exc_value, TypeError)



if __name__ == "__main__":

    print('inicio')
    with ZeroLock() as tt:
        tt.exec1()

        #raise Exception('erro mane')

        print('dentro')

        tt = None

    print('fim')
    time.sleep(5)
    print('fim')
    print('fim')

