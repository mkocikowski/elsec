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


logger = logging.getLogger(__name__)

# all the readline stuff is straight out of tutorials, nothing fancy here
#
def _get_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".elsec_history")
        readline.read_history_file(fn)
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            output("No command history file found.")
        else:
            logger.warning(exc)


def _save_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".elsec_history")
        readline.set_history_length(20)
        readline.write_history_file(fn)
    except IOError as exc:
        logger.warning(exc)


def _configure_readline():
#     if 'libedit' in readline.__doc__:
#         output("""
# TAB-completion disabled, because readline library is not installed. 
# To install, do 'easy_install readline' from the command line (not 'pip'!).
# """.strip())
#         return        
    _get_readline_history()
    readline.set_completer(elsec.parser.complete)
    readline.parse_and_bind("tab: complete")
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
        logger.warning("Using libedit readline")
    return


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
    
    def _dot_collapse(pre, d): 
        for k in d.keys():
            try: 
                ps = "%s.%s" % (pre, k) if pre else k
                for f in _dot_collapse(ps, d[k]['properties']): 
                    yield f
            except KeyError:
                yield ("%s.%s" % (pre, k), d[k]['type'])
    
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
        
    fields = [f[0] for f in _dot_collapse("", _temp)]
    return fields
    
    
def output(data, fh=sys.stdout):
    """Output data, if it is not string, then serialized to JSON. 
    
    Input:
    - data: if str or unicode, output as is. If other, serialize to JSON
    - fh: file handle for output, defaults to sys.stdout
    
    """
    if type(data) in [str, unicode]:
        fh.write(data)
        fh.write("\n")
        return
    fh.write(json.dumps(data, indent=4, sort_keys=True))
    fh.write("\n")
    return


def get_args_parser():
    # the reason for the args parser to be defined in a separate function is
    # that it makes it easy to test it.
    parser = argparse.ArgumentParser(description="ElasticSearch client.")
    parser.add_argument('-v', '--version', action='version', version=elsec.__version__)
    parser.add_argument('host', type=str, help="elasticsearch server address, including port")
    parser.add_argument('index', type=str, nargs="?", help="name of the index")
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
                    buff.strip().endswith(";"):
                handler_f(buff.strip(" ;\n\r\t"))
                buff = ""
                prompt = prompt_f()
    except EOFError:
        return


def main():
    """Do the basic setup, configure readline, and enter the input loop. 
    
    On exit(0) saves the readline history. On errors exits with exit(1).
    
    """
    
#     logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename="esc.log", level=logging.DEBUG)

    try:
        args = get_args_parser().parse_args()
        if not args.index:
            indices = elsec.actions.get_indices(args.host)
            aliases = elsec.actions.get_aliases(args.host)
            output("Indices: %s, aliases: %s" % (sorted(indices), sorted(aliases)))
            sys.exit(0)
        # this is ugly, but readline seems to rely on globals
        elsec.parser.completions['fields'] = sorted(get_fieldnames(args.host, args.index))
        _configure_readline()

    except (TypeError, ValueError):
        logger.error("Error initializing, check your connection parameters.", exc_info=True)
        sys.exit(1)

    except IOError:
        logger.error("IO (network) error, check your connection parameters.", exc_info=True)
        sys.exit(1)

    prompt_f = lambda: "%s/%s/> " % (args.host, args.index)
    handler_f = functools.partial(elsec.parser.handle, args.host, args.index, output)
    output("Type 'help' for help. Exit with Control-D. ")
    input_loop(prompt_f, raw_input, handler_f)
    _save_readline_history()
    output("Bye!")
    sys.exit(0)


if __name__ == "__main__":
    main()


