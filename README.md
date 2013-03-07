Elasticsearch interactive client
--------------------------------
The goal of the project is to provide an easy to use, interactive
command line (terminal) client to Elasticsearch, with behavior similar
to 'mysql' or 'psql' clients. The tool is to give a safe (read-only) way
to explore data in ES indices, addressing use cases common among
non-technical, non-administrator users. Anyone capable of using the
mysql client to dig around a mysql database should be able to use the
'elsec' to look at data in an ES index. 

The basic use case is to execute 'search' or 'count' requests based on Lucene
query strings entered on the command line. Tab completion of field names is
available, based on index mappings. 

All requests are echoed as curl calls, and so can easily be copied and
executed outside the client (for debugging? sharing?) Any valid Elasticsearch
search or count request can also be pasted into the client and executed (this
is how you do complex queries).

This tool is not intended to be an admin interface, or a complex query
builder. It is to be quick to learn and safe and easy to use, more of a spoon
than a swiss army knife.

Installation
------------
For the current 'stable' release:
    
    pip install elsec

For the 'dev' release: 

    pip install https://github.com/mkocikowski/elsec/archive/dev.zip

Tutorial
--------
See the [project wiki](https://github.com/mkocikowski/elsec/wiki) 
(which should be a copy of the TUTORIAL.md file)

License
-------

The project uses [the MIT license](http://opensource.org/licenses/MIT):

    Copyright (c) 2013 Mikolaj Kocikowski
    
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
    
