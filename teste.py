#!/usr/bin/env python3
'''
Created on 20200703
Update on 20200703
@author: Eduardo Pagotto
'''

import re
from typing import Mapping, Tuple, Callable, Any, Union, List

def is_sequence(obj):
    return hasattr(obj, '__iter__')

class FrozenDict(dict):
    """
    An immutable dictoinary.
    This is used to generate stable hashes for queries that contain dicts.
    Usually, Python dicts are not hashable because they are mutable. This
    class removes the mutability and implements the ``__hash__`` method.
    """

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def _immutable(self, *args, **kws):
        raise TypeError('object is immutable')

    # Disable write access to the dict
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    setdefault = _immutable
    popitem = _immutable

    def update(self, e=None, **f):
        raise TypeError('object is immutable')

    def pop(self, k, d=None):
        raise TypeError('object is immutable')

#pylint: disable=C0301, C0116, W0703, C0103, C0115
def freeze(obj):
    """
    Freeze an object by making it immutable and thus hashable.
    """
    if isinstance(obj, dict):
        # Transform dicts into ``FrozenDict``s
        return FrozenDict((k, freeze(v)) for k, v in obj.items())
    elif isinstance(obj, list):
        # Transform lists into tuples
        return tuple(freeze(el) for el in obj)
    elif isinstance(obj, set):
        # Transform sets into ``frozenset``s
        return frozenset(obj)
    else:
        # Don't handle all other objects
        return obj


class QueryInstanceTest:
    def __init__(self, test, hashval):
        self._test = test
        self._hash = hashval

    def __call__(self, value):
        return self._test(value)

    def __hash__(self):
        return hash(self._hash)

    def __repr__(self):
        return 'QueryImpl{}'.format(self._hash)

    def __eq__(self, other):
        if isinstance(other, QueryInstanceTest):
            return self._hash == other._hash

        return False

    def __and__(self, other):
        return QueryInstanceTest(lambda value: self(value) and other(value), ('and', frozenset([self._hash, other._hash])))

    def __or__(self, other: 'QueryInstanceTest') -> 'QueryInstanceTest':
        return QueryInstanceTest(lambda value: self(value) or other(value), ('or', frozenset([self._hash, other._hash])))

    def __invert__(self) -> 'QueryInstance':
        return QueryInstanceTest(lambda value: not self(value), ('not', self._hash) )


class QueryTest(QueryInstanceTest):
    def __init__(self):
        self._path = ()

        def notest(_):
            raise RuntimeError('Empty query was evaluated')

        super().__init__(test=notest, hashval=(None,))

    def __repr__(self):
        return '{}()'.format(type(self).__name__)

    def __hash__(self):
        return super().__hash__()

    def __getattr__(self, item):
        query = type(self)()

        # Now we add the accessed item to the query path ...
        query._path = self._path + (item,)

        # ... and update the query hash
        query._hash = ('path', query._path)

        return query

    def __getitem__(self, item):
        # A different syntax for ``__getattr__``
        return getattr(self, item)

    def _generate_test(self, test, hashval):
        """
        Generate a query based on a test function that first resolves the query
        path.
        :param test: The test the query executes.
        :param hashval: The hash of the query.
        :return: A :class:`~tinydb.queries.QueryInstance` object
        """
        if not self._path:
            raise ValueError('Query has no path')

        def runner(value):
            try:
                # Resolve the path
                for part in self._path:
                    value = value[part]
            except (KeyError, TypeError):
                return False
            else:
                # Perform the specified test
                return test(value)

        return QueryInstanceTest(lambda value: runner(value), hashval)


    def __eq__(self, rhs):
        return self._generate_test(lambda value: value == rhs, ('==', self._path, freeze(rhs)))

    def __ne__(self, rhs):
        return self._generate_test(lambda value: value != rhs, ('!=', self._path, freeze(rhs)))

    def __lt__(self, rhs):
        return self._generate_test(lambda value: value < rhs, ('<', self._path, rhs))

    def __le__(self, rhs):
        return self._generate_test(lambda value: value <= rhs, ('<=', self._path, rhs))

    def __gt__(self, rhs):
        return self._generate_test(lambda value: value > rhs, ('>', self._path, rhs))

    def __ge__(self, rhs):
        return self._generate_test(lambda value: value >= rhs, ('>=', self._path, rhs))

    def exists(self):
        return self._generate_test(lambda _: True, ('exists', self._path))

    def matches(self, regex, flags=0):
        def test(value):
            if not isinstance(value, str):
                return False

            return re.match(regex, value, flags) is not None

        return self._generate_test(test, ('matches', self._path, regex))

    def search(self, regex, flags=0):
        def test(value):
            if not isinstance(value, str):
                return False

            return re.search(regex, value, flags) is not None

    def test(self, func, *args):
        return self._generate_test(lambda value: func(value, *args), ('test', self._path, func, args))

    def any(self, cond):
        if callable(cond):
            def test(value):
                return is_sequence(value) and any(cond(e) for e in value)
        else:
            def test(value):
                return is_sequence(value) and any(e in cond for e in value)

        return self._generate_test(lambda value: test(value), ('any', self._path, freeze(cond)))

    def all(self, cond):
        if callable(cond):
            def test(value):
                return is_sequence(value) and all(cond(e) for e in value)
        else:
            def test(value):
                return is_sequence(value) and all(e in value for e in cond)
        return self._generate_test(lambda value: test(value), ('all', self._path, freeze(cond)))

    def one_of(self, items):
        return self._generate_test(lambda value: value in items, ('one_of', self._path, freeze(items)))

    def noop(self):
        return QueryInstanceTest(lambda value: True, ())

def where(key):
    return QueryTest()[key]

if __name__ == '__main__':

    query = QueryTest()

    summary = {'id': 10}

    val = query.summary > 10
    #val = ((query.summary.id.val == 10) & (query.summary.id.data != '2009')) | (query.sexo == False)

    print(val)
