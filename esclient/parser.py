# -*- coding: utf-8 -*-

import readline
import logging
import traceback

import esclient.client
import esclient.help

logger = logging.getLogger(__name__)

completions = {
    'fields': [], 
    'hits': [], 
    'commands': ['search', 'count', 'view', 'exit', 'help'], 
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
    esclient.client.output(request)
    esclient.client.output(">")
    esclient.client.output(response)
    

def parse(host, index, line):

    command = line.split(" ")[0].lower()
    params = line.split(" ")[1:]

    if command == 'search':
        curl, url, request, response = \
            esclient.actions.do_search(host, index, " ".join(params))
        if 'hits' in response:
            completions['hits'] = response['hits']['hits']
        _output(curl, response)

    elif command == 'count':
        curl, url, request, response = \
            esclient.actions.do_count(host, index, " ".join(params))
        _output(curl, response)

    elif command == 'view': 
        for p in params:
            docs = [(d['_type'], d['_id']) for 
                d in completions['hits'] if 
                d['_id'] == p]
            for d in docs:
                curl, url, request, response = \
                    esclient.actions.do_view(host, index, d[0], d[1])
                _output(curl, response)
    
    elif command == 'help':
        esclient.client.output(esclient.help.OVERVIEW)

    elif command == 'exit':
        raise EOFError()
        
    return

