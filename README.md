## Elasticsearch interactive client

NOT YET READY FOR PUBLIC CONSUMPTION, PORTING FROM BUSINESS-INTERNAL
IMPLEMENTATION, WILL ANNOUNCE HERE WHEN 'READY', WHICH SHOULD BE SOON (BY THE
END OF FEBRUARY 2013?).

The goal of the project is to provide an easy to use, interactive text-based
(terminal) client to Elasticsearch, with behavior similar to 'mysql' or 'psql'
clients. The tool is to give a safe (read-only) way to explore data in ES
indices, addressing use cases common among non-technical, non-administrator
users. Anyone capable of using the mysql client to dig around a mysql database
should be able to use the esclient to look at data in an ES index.

Capabilities:

* execute 'search' and 'count' commands with Lucene query strings
* use mapping data for field name TAB auto complete / mapping exploration
* input and output data in JSON, copy/modify/paste & curl friendly

Thinking:

* simple (tool for exploring indices and for exploring data in them)
* safe (read only, no 'admin' tools)
* familiar (similar in use to 'mysql' and 'psql')

All commands are echoed as JSON curl calls, which can be copied, modified, and
pasted back in, or run outside of the client. This allows users to
incrementally build complex requests (not limited to Lucene query strings),
with the benefit of feedback from the interactive environment. In my
experience, this gives determined users enough to construct search and count
requests to address all the use cases they can dream up. 

## License

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
    
