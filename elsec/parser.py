# -*- coding: utf-8 -*-

import readline
import logging
import traceback

import elsec.client
import elsec.help

logger = logging.getLogger(__name__)

completions = {
    'fields': [], 
    'hits': [], 
    'commands': ['search', 'count', 'view', 'exit', 'help', 'types', 'fields'], 
}

# http://www.doughellmann.com/PyMOTW/readline/
def complete(text, state):
    line = readline.get_line_buffer()

    # first token
    if text == line:
        matches = [c+" " for c in completions['commands'] if 
            c.startswith(text.lower())]
    
    else:
        command = line.split(" ")[0].lower()
        if command == 'view':
            matches = [h['_id'] for 
                h in completions['hits'] if 
                h['_id'].startswith(text)]
        elif command in ['count', 'search']: 
            matches = [f for 
                f in completions['fields'] if 
                f.startswith(text)]

    response = sorted(matches)[state]
    return response


def _output(request, response, separator=">"):
    elsec.client.output(request)
    elsec.client.output(">")
    elsec.client.output(response)
    

def parse(host, index, line):

    command = line.split(" ")[0].lower()
    params = line.split(" ")[1:]

    if command == 'search':
        curl, url, request, response = \
            elsec.actions.do_search(host, index, " ".join(params))
        if 'hits' in response:
            completions['hits'] = response['hits']['hits']
        _output(curl, response)

    elif command == 'count':
        curl, url, request, response = \
            elsec.actions.do_count(host, index, " ".join(params))
        _output(curl, response)

    elif command == 'view': 
        for p in params:
            docs = [(d['_index'], d['_type'], d['_id']) for 
                d in completions['hits'] if 
                d['_id'] == p]
            for d in docs:
                curl, url, request, response = \
                    elsec.actions.do_view(host, d[0], d[1], d[2])
                _output(curl, response)
    
    elif command == 'types':
        curl, url, request, response = elsec.actions.get_mappings(host, index)
        _output(curl, response)

    elif command == 'fields':
        elsec.client.output(sorted(completions['fields']))
    
    elif command == 'help':
        elsec.client.output(elsec.help.OVERVIEW)

    elif command == 'exit':
        raise EOFError()
        
    return

