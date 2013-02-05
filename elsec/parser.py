# -*- coding: utf-8 -*-

"""Responsible for tab completion, parsing and execution of commands. 

Functions:
- complete(): called by readline for tab completion
- handle(): called by client.input_loop to handle commands

"""


import readline
import logging
import traceback

import elsec.client
import elsec.help

logger = logging.getLogger(__name__)

completions = {
    'fields': [], 
    'hits': [], 
    'commands': ['search', 'count', 'view', 'open', 'exit', 'help', 'version'], 
}


# http://www.doughellmann.com/PyMOTW/readline/
#
def complete(text, state):
    """Tab complete for readline."""

    line = readline.get_line_buffer()
    
    # there is a difference in the way line buffer is handled by GNU readline
    # and by libedit, which is what runs by default on OSX. With GNU readline
    # the line buffer is empty after each command; with libedit, old buffer
    # remains, and gets overwritten from the beginning on (if the previous
    # line was 'foobaz', and someone types 'xxx' on new line, then the line
    # buffer is 'xxxbaz'). This is why the content of the line buffer needs to
    # be trimmed, if completion decisions are to be made based on the buffer
    # content. 
    #
    line = line[:readline.get_endidx()]

    # first token
    if text == line:
        matches = [c+" " for c in completions['commands'] if 
            c.startswith(text.lower())]
    
    else:
        command = line.split(" ")[0].lower()
        if command in ['view', 'open']:
            matches = [h['_id'] for 
                h in completions['hits'] if 
                h['_id'].startswith(text)]
        elif command in ['count', 'search']: 
            matches = [f for 
                f in completions['fields'] if 
                f.startswith(text)]

    response = sorted(matches)[state]
    return response


def handle(host, index, output_f, line): 
    """Parse command line, execute command, output results. 
    
    Input:
    - host, index: str
    - output_f: callable with signature f(data), see client.output()
    - line: str, input to be parsed
    
    Returns:
    nothing, command execution and result output handled here. If you want to
    see what gets output (for testing) provide your own output_f.

    """

    for _func, _args in _parse(line):
        for request, response in _func(host, index, *_args): 
            _output(output_f, request, response)
            # add document ids to autocomplete
            if 'hits' in response:
                completions['hits'] = response['hits']['hits']

    return 


def _parse(line):
    """Parse input line, yield callable with parameters.
    
    A single command (collapsing multiline commands into single line has
    already been done in client.input_loop()) may result in one or more
    function calls (such as when 'view' has multiple documents). This function
    will yield tuples with appropriate functions to be called and with their
    parameters.

    Input: 
    - line: str
    
    Yields:
    tuple(function, params). The function should accept the *params, and in
    turn yield (request, response). 
    
    """
    
    command = line.split(" ")[0].lower()
    params = line.split(" ")[1:]

    if command == 'search':
        _func = elsec.actions.do_search
        _args = [" ".join(params),]
        yield (_func, _args)
    
    elif command == 'count':
        _func = elsec.actions.do_count
        _args = [" ".join(params),]
        yield (_func, _args)
                
    elif command == 'view': 
        for p in params:
            _func = elsec.actions.do_view
            _args = [p,]
            yield (_func, _args)

    elif command == 'open': 
        for p in params:
            _func = elsec.actions.do_open
            _args = [p,]
            yield (_func, _args)
    
    elif command == 'help':
        def _help(*args, **kwargs):
            yield (None, elsec.help.OVERVIEW)
        yield (_help, [])
    
    elif command == 'version':
        def _version(*args, **kwargs):
            yield(None, elsec.__version__)
        yield (_version, [])
        
    elif command == 'exit':
        def _exit(*args, **kwargs):
            raise EOFError
        yield (_exit, [])
        

def _output(output_f, request, response, separator=">"):

    if request: 
        output_f(request)
        output_f(">")

    output_f(response)

    return

