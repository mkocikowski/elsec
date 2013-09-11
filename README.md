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

Requirements
------------
Python 2.7; tested on OSX and on Linux (2.6), no plans to support Windows. On
OSX, I highly recommend you install 'readline' (like you would for ipython),
with 'easy_install readline'. Using the OSX standard 'libedit' will cause the
command history to be intermittently lost between sessions. 

Installation
------------
For the current 'stable' release:
    
    pip install elsec

For the 'dev' release: 

    pip install https://github.com/mkocikowski/elsec/archive/dev.zip

If you don't want to use pip (which is a nice python package manager /
installer), you can download the source, cd to the directory which contains
the 'setup.py' file, and run 'python setup.py install'. But I recommend using
'pip'.

Tutorial
--------
See the 'TUTORIAL.md' file in the main project directory. 

Bugs / suggestions
------------------
Please submit bugs and suggestions to [issues](https://github.com/mkocikowski/elsec/issues) project page.

Changes
-------
- 1.0.3 (2013-09-11) Issue #9, improved command line args sanitation.
- 1.0.2 (2013-09-05) Issue #8, -h/--host and -p/--port args, better help.
- 1.0.1 (2013-04-26) Public release. 
- 0.9.6 (2013-03-27) Issue #6 (bug, 'view' setting request to 'none')
- 0.9.5 (2013-03-22) Issue #3 (proper tab completion for multi fields)
- 0.9.4 (2013-03-19) Issues #1 ('flat' command) and #2 (request timeouts, Sushant Shankar) addressed
- 0.9.3 (2013-03-12) 'Vim edit' (Alexander Scammon) tested and documented, request history saved on exit and restored on startup, more tests, better documentation
- 0.9.2 (2013-03-10) Basic vim edit capability, allowing users to edit requests without leaving the client
- 0.9.1 (2013-03-06) Base functionality

Contribute
----------
The project is on github - of course I'd like people to get involved.
This said, I'd like to keep the tool simple, focused in its purpose, and
general in its application. Keep it simple, up to date, try to perfect
it. 

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
    
