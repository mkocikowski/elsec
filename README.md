Elasticsearch interactive client.
---------------------------------

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