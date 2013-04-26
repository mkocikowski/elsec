# -*- coding: utf-8 -*-

import elsec.parser

OVERVIEW = """
Relax, you can't break anything with this tool!

Press TAB twice to see available commands. Press TAB while entering a 'search'
or 'count' command to complete a field name. Press TAB when entering a 'view'
or 'open' command to complete document id. 

'search' and 'count' commands take a Lucene query as their parameters. 'view'
and 'open' commands take document id/s as its input. Read up on Lucene query
syntax: http://lucene.apache.org/core/3_6_2/queryparsersyntax.html

Elasticsearch extends the Lucene query syntax with _exists_ and _missing_
elements, worth the read, see the very bottom of this page:
http://www.elasticsearch.org/guide/reference/query-dsl/query-string-query.html

Don't worry, you won't break anything by using this tool! See full
documentation, use examples, and a tutorial at: 
https://github.com/mkocikowski/elsec/
"""

COMMANDS = """
Commands
--------

'search': when followed by a Lucene query string, will execute that query
(end the line with a semicolon). When followed by a request in JSON
format (you can copy and paste these, see the tutorial), will execute
that request. Just 'search', followed by nothing, will re-run the most
recent request. 

'count': same as search (but count ;-)

'flat': re-run the most recent request, but outputting in single line
(useful for copying requests / responses for applications which expect
single lines on stdin).

'edit': edit the most recent request with vim, execute when done editing.
 
"""