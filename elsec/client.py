# -*- coding: utf-8 -*-

"""This is the entry point for the application. 

main() does basic setup (readline, command history), and runs the
input_loop(). Commands are passed to the parser.execute() function for parsing
and processing. All application output is handled by the output() function. 

See elsec.__init__ for top-level documentation.

"""

import sys
import os.path
import errno
import argparse
import readline
import json
import logging
import functools

import elsec.http
import elsec.actions
import elsec.parser
import elsec.output


logger = logging.getLogger(__name__)

# all the readline stuff is straight out of tutorials, nothing fancy here
#
def _get_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".elsec_history")
        readline.read_history_file(fn)
        logger.debug("Read readline history from: %s" % (fn,))
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            elsec.output.output("No command history file found.")
        else:
            logger.warning(exc, exc_info=False)


def _save_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".elsec_history")
        readline.set_history_length(20)
        readline.write_history_file(fn)
        logger.debug("Stored readline history to: %s" % (fn,))
    except IOError as exc:
        logger.warning(exc, exc_info=True)


def _configure_readline():
    _get_readline_history()
    readline.set_completer(elsec.parser.complete)
    readline.parse_and_bind("tab: complete")
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
        logger.debug("Using libedit readline")
    return


def _collapse_mapping(element, path="", skip=None): 

    if not skip:
        skip = []

    if "properties" in element:
        return _collapse_mapping(element['properties'], path)

    elif "fields" in element: 
        res = _collapse_mapping(element['fields'], path, skip=[path.rsplit(".", 1)[1]])
        res.extend([path])
        return res

    elif "type" in element:
        return [path]

    else:
        res = []
        for field in element:
            if field in skip: continue
            res.extend(_collapse_mapping(element[field], "%s.%s" % (path, field) if path else field))
        return res


def get_fieldnames(host, index): 
    """Return a list of names of all fields in mappings for the index.
    
    Calls elsec.actions.get_mappings(), and then dot-collapses the field names
    into mapping.object.fieldname format, returning a list of all the fields.
    (This is later used for tab completions)

    Input: 
    - host, index: str
    
    Returns:
    List of str, each element a fully qualified field name
    
    Raises:
    - ESRequestError/ValueError if response from ES has 'error' field. 
    - IOError comes up from the http call if there is an IO problem.
    
    """
    
#     def _dot_collapse(pre, d): 
#         for k in d.keys():
#             try: 
#                 ps = "%s.%s" % (pre, k) if pre else k
#                 for f in _dot_collapse(ps, d[k]['properties']): 
#                     yield f
# #                 for f in _dot_collapse(ps, d[k]['fields']): 
# #                     yield f
#             except KeyError:
#                 yield ("%s.%s" % (pre, k), d[k]['type'])
# #                 yield ("%s.%s" % (pre, k), 'x')
# #                 yield ("foo.bar")
#     

    mappings = elsec.actions.get_mappings(host, index)
    
    # the _mapping call returns a dictionary where keys are index names,
    # and values are dictionaries where keys are mapping names and
    # values are mappings. So if we are doing with a single index, it is
    # simple; however, if we are dealing with an alias, which references
    # multiple indices, we need to collapse the dictionary a bit, and
    # this is what the following three lines do.
    _temp = dict()
    for m in mappings.values():
        _temp.update(m)
        
#     fields = [f[0] for f in _dot_collapse("", _temp)]
#     return fields
    
    return _collapse_mapping(_temp)


def get_args_parser():
    # the reason for the args parser to be defined in a separate function is
    # that it makes it easy to test it.
    epilog = """
Running 'elsec' with no parameters will display indices and aliases available
on the default host:port (localhost:9200). For project info and tutorial see:
'https://github.com/mkocikowski/elsec' 
"""
    parser = argparse.ArgumentParser(description="ElasticSearch client (%s)" % (elsec.__version__, ), epilog=epilog, add_help=False)
    parser.add_argument('-v', '--version', action='version', version=elsec.__version__)
    parser.add_argument('--help', action='help', help='show help and exit')
    parser.add_argument('-h', '--host', type=str, default='localhost', help="server host (default: %(default)s)")
    parser.add_argument('-p', '--port', type=int, default=9200, help="server port (default: %(default)i)")
    parser.add_argument('index', type=str, nargs="?", help="name of the index to access, required")
    parser.add_argument('--flat', action='store_true', help="if set, show requests and responses in single lines")
    return parser


def input_loop(prompt_f, input_f, handler_f):
    """Read command lines, pass them to the parser. 
    
    Takes lines from input_f. If a line begins with 'search' or 'count', allow
    for multiline input, terminated by ';'. Pass complete commands to handler_f
    for execution. Break the input loop on EOFError. 

    Input:
    - prompt_f: callable with signature f(), returning prompt string
    - input_f: callable with signature f(s) where s is a string, when called
    returns a line of text (presumably the input). In its basic form
    input_f=raw_input.
    - handler_f: callable with signature f(s) where s is a string containing
    the entire command line/s. Responsible for parsing and execution.
    
    """
    
    prompt = prompt_f()
    buff = ""
    try: 
        while True:
            line = input_f(prompt).strip()
            if not line:
                continue
            buff += " " + line
            prompt = "> "
            # 'search' and 'count' commands allow for multiline input,
            # terminated by ';', all other commands are single line.
            if buff.strip().split()[0].lower() not in ['search', 'count'] or \
                    len(buff.strip().split()) == 1 or \
                    buff.strip().endswith(";"):
                handler_f(buff.strip(" ;\n\r\t"))
                buff = ""
                prompt = prompt_f()
    except EOFError:
        return


def main(args=None, input_f=None, output_f=None, loop_f=None):
    """Do the basic setup, configure readline, and enter the input loop. 
    
    On exit(0) saves the readline history. On errors exits with exit(1).
    
    """
    
    logging.basicConfig(level=logging.WARNING)
#     logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(filename="esc.log", level=logging.DEBUG)

    input_f = input_f if input_f else raw_input
    output_f = output_f if output_f else elsec.output.output
    loop_f = loop_f if loop_f else input_loop

    try:
        parser = get_args_parser()
        args = parser.parse_args(args)
        server = "%s:%i" % (args.host, args.port)

        indices = elsec.actions.get_indices(server)
        aliases = elsec.actions.get_aliases(server)

        # if no index name provided on invocation, display available indices
        # and aliases and exit
        if not args.index:
            output_f("\n%s" % parser.format_help())
            output_f("-------------------------------------")
            output_f("Server '%s' has the following indices and aliases available: " % (server, ))            
            output_f("INDICES: [%s] ALIASES: [%s]\n" % (", ".join(sorted(indices)), ", ".join(sorted(aliases))))
            sys.exit(0)
        
        # validate that 'index' command line argument is one of existing
        # indices or aliases
        if args.index not in set(indices + list(aliases)): 
            logger.error("Invalid 'index' command line parameter '%s'. It must be one of: %s" % (args.index, ", ".join(set(indices + list(aliases)))))
            raise ValueError("invalid 'index' command line parameter")
        
        # this is ugly, but readline seems to rely on globals
        elsec.parser.completions['fields'] = sorted(get_fieldnames(server, args.index))
        _configure_readline()
        elsec.parser.read_request_history()

    except (TypeError, ValueError):
        logger.error("Error initializing, check your connection parameters (host=%s, port=%i, index=%s). Type 'elsec --help' for help." % (args.host, args.port, args.index), exc_info=False)
        sys.exit(1)

    except IOError:
        logger.error("IO (network) error, check your connection parameters (host=%s, port=%i, index=%s). Type 'elsec --help' for help." % (args.host, args.port, args.index), exc_info=False)
        sys.exit(2)
    
#     input_f = raw_input
#     output_f = elsec.output.output
    prompt_f = lambda: "%s/%s/> " % (server, args.index)

    if args.flat:
        elsec.output.FLAT = True
        def input_f(x):
            line = sys.stdin.readline()
            if not line:
                raise EOFError
            return line
        prompt_f = lambda: ""

    handler_f = functools.partial(elsec.parser.handle, server, args.index, output_f)
    if not args.flat:
        output_f("Type 'help' for help. Exit with Control-D. ")
    loop_f(prompt_f, input_f, handler_f)
    if not args.flat: 
        _save_readline_history()
        elsec.parser.save_request_history()
        output_f("Bye!")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
