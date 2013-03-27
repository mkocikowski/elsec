# -*- coding: utf-8 -*-

"""Responsible for tab completion, parsing and execution of commands. 

Functions:
- complete(): called by readline for tab completion
- handle(): called by client.input_loop to handle commands

"""


import json
import readline
import logging
import os.path

import elsec.actions
import elsec.help


logger = logging.getLogger(__name__)

completions = {
    'fields': [], 
    'hits': [], 
    'commands': ['search', 'count', 'view', 'open', 'exit', 'help', 'version', 'edit', 'flat'], 
}

REQUEST_HISTORY_PATHNAME = os.path.join(os.path.expanduser("~"), ".elsec_request")
request = None


def save_request_history():
    try: 
        with open(REQUEST_HISTORY_PATHNAME, "w") as f:
            f.write(json.dumps(request._asdict()))
        logger.debug("Stored request history to: %s" % (REQUEST_HISTORY_PATHNAME, ))
    except (IOError, AttributeError) as exc:
        logger.debug(str(exc), exc_info=True)
    return

def read_request_history(): 
    try: 
        with open(REQUEST_HISTORY_PATHNAME, "rU") as f:
            r = f.read()
        r = json.loads(r)
        global request
        request = elsec.actions.RequestT(r['url'], r['method'], r['request'], r['curl'])
        logger.debug("Read request history from: %s" % (REQUEST_HISTORY_PATHNAME, ))
    except (IOError, AttributeError, ValueError) as exc:
        logger.debug(str(exc), exc_info=True)
    return


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
        for req, res in _func(host, index, *_args):
            try: 
                _output(output_f, req, res)
                # add document ids to autocomplete
                if res and 'hits' in res.data:
                    completions['hits'] = res.data['hits']['hits']
                if req and req.request: # don't remember 'view' and 'open' requests
                    global request
                    request = req
            except Exception:
                logger.error(_func)
                raise

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
        _args = None
        if params:
            _args = [" ".join(params),]
        elif request:
            _args = [json.dumps(request.request),]
        if _args:
            yield (_func, _args)
    
    elif command == 'count':
        _func = elsec.actions.do_count
        _args = None
        if params:
            _args = [" ".join(params),]
        elif request:
            _args = [json.dumps(request.request),]
        if _args:
            yield (_func, _args)
    
    elif command == 'edit':
        _func = elsec.actions.do_edit
        if request:
            _args = [request,]
            yield (_func, _args)

    elif command == 'flat':
        _func = elsec.actions.do_flat
        if request:
            _args = [request,]
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
            yield (None, elsec.actions.ResponseT(None, elsec.help.OVERVIEW))
        yield (_help, [])
    
    elif command == 'version':
        def _version(*args, **kwargs):
            yield(None, elsec.actions.ResponseT(None, elsec.__version__))
        yield (_version, [])
        
    elif command == 'exit':
        def _exit(*args, **kwargs):
            raise EOFError
        yield (_exit, [])
        

def _output(output_f, request, response, separator=elsec.output.SEPARATOR):

    if request: 
        output_f(request.curl)
        output_f(separator)

    if response:
        output_f(response.data)

    return

