'''
Created on 20200323
Update on 20200323
@author: Eduardo Pagotto
'''

import setuptools

PACKAGE = "ZeroDB"
VERSION = __import__(PACKAGE).__version__

setuptools.setup(
    include_package_data=True, # para adicionar o manifest
    name="ZeroDB",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="TinyDB remote call in jsonRPC",
    long_description="TinyDB remote call in jsonRPC",
    url="https://github.com/EduardoPagotto/ZeroDB.git",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['Zero',
                      'tinydb',
                      'bson']
)