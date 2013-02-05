# -*- coding: utf-8 -*-

import elsec.parser

OVERVIEW = """
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
https://github.com/mkocikowski/elsec/wiki
"""