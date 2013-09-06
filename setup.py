# -*- coding: utf-8 -*-

# python setup.py -r http://testpypi.python.org/pypi register
# python setup.py sdist upload -r http://pypi.python.org/pypi

from setuptools import setup

ld = """
The goal of the project is to provide an easy to use, interactive
command line (terminal) client to Elasticsearch, with behavior similar
to 'mysql' or 'psql' clients. The tool is to give a safe (read-only) way
to explore data in ES indices, addressing use cases common among
non-technical, non-administrator users. Anyone capable of using the
mysql client to dig around a mysql database should be able to use the
'elsec' to look at data in an ES index. 
"""

setup(
    name = 'elsec', 
    version = '1.0.2', 
    author = 'Mik Kocikowski', 
    author_email = 'mkocikowski@gmail.com', 
    url = 'https://github.com/mkocikowski/elsec', 
    description = 'Elasticsearch interactive command line client', 
    long_description=ld,
    packages = ['elsec', 'elsec.test'], 
    package_data={'': ['README.md',],},
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
    test_suite = "elsec.test.units.suite", 
)
