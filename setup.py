# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'esclient', 
    version = '0.0.2', 
    author = 'Mik Kocikowski', 
    author_email = 'mkocikowski@gmail.com', 
    packages = ['esclient', 'esclient.test'],
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'esclient = esclient.client:main', 
        ]
    }, 

)


