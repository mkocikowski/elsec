# -*- coding: utf-8 -*-

"""Interactive command line application for querying Elasticsearch. 

Modules:
- client.py: main() is the entry point for the application, main input loop
- parser.py: provides tab completion, execute() parses and executes commands
- actions.py: calls to Elasticsearch, used by parser.py
- http.py: wrappers around httplib, used by actions.py for http calls
- help.py: help strings
- exceptions.py: exceptions
- templates.py: JSON templates for Elasticsearch requests

Tests:
All tests are in the 'test' package. The test runner is in 'units.py'. For
tests to run there needs to be an Elasticsearch server running on localhost. 

"""


__version__ = "1.0.3"
