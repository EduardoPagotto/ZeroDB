'''
Created on 20200323
Update on 20200324
@author: Eduardo Pagotto
'''

import setuptools

PACKAGE = "ZeroDB"
VERSION = __import__(PACKAGE).__version__

classifiers = """\
Development Status :: 1 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU v3.0
Programming Language :: Python
Programming Language :: Python :: 3.7
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""

setuptools.setup(
    name=PACKAGE,
    version=VERSION,
    packages=setuptools.find_packages(),
    classifiers=filter(None, classifiers.split('\n')),
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="Atomic transactions for TinyDB",
    license="GNUv3.0",
    url="https://github.com/EduardoPagotto/ZeroDB.git",
    install_requires=['Zero',
                      'tinydb',
                      'bson']
)