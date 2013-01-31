# -*- coding: utf-8 -*-

# python setup.py -r http://testpypi.python.org/pypi register

from setuptools import setup

setup(
    name = 'elsec', 
    version = '0.0.2', 
    author = 'Mik Kocikowski', 
    author_email = 'mkocikowski@gmail.com', 
    url = 'https://github.com/mkocikowski/elsec', 
    description = 'Elasticsearch interactive command line client', 
    long_description=open('README.md').read(),
    packages = ['elsec', 'elsec.test'],
    entry_points = {
        'console_scripts': [
            'elsec = elsec.client:main', 
        ]
    }, 
    classifiers = [
        "Development Status :: 4 - Beta", 
        "Environment :: Console", 
        "Intended Audience :: Developers", 
        "Intended Audience :: End Users/Desktop", 
        "License :: OSI Approved :: MIT License", 
        "Natural Language :: English", 
        "Operating System :: POSIX",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",  
        "Topic :: Utilities",
    ], 
    license = 'MIT',
)


