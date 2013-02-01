# -*- coding: utf-8 -*-

import sys
import os.path
import errno
import argparse
import readline
import json
# import traceback
import logging
import functools

import elsec.http
import elsec.actions
import elsec.parser


logger = logging.getLogger(__name__)

def _get_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".elsec_history")
        readline.read_history_file(fn)
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            print("No command history file found.")
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
    _get_readline_history()
    readline.set_completer(elsec.parser.complete)
    readline.parse_and_bind("tab: complete")
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    return


def get_fieldnames(host, index):
    def _dot_collapse(pre, d): 
        for k in d.keys():
            try: 
                ps = "%s.%s" % (pre, k) if pre else k
                for f in _dot_collapse(ps, d[k]['properties']): 
                    yield f
            except KeyError:
                yield ("%s.%s" % (pre, k), d[k]['type'])
    _, _, _, mappings = elsec.actions.get_mappings(host, index)
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
    if type(data) in [str, unicode]:
        fh.write(data)
        fh.write("\n")
        return
    fh.write(json.dumps(data, indent=4, sort_keys=True))
    fh.write("\n")
    return


def get_args_parser():
    parser = argparse.ArgumentParser(description="ElasticSearch client.")
    parser.add_argument('host', type=str, help="elasticsearch server address, including port")
    parser.add_argument('index', type=str, nargs="?", help="name of the index")
    return parser


def input_loop(prompt_f, input_f, parser_f):
    prompt = prompt_f()
    buff = ""
    try: 
        while True:
            line = input_f(prompt).strip()
            if not line:
                continue
            buff += " " + line
            prompt = "> "
            if buff.strip().split()[0].lower() not in ['search', 'count'] or \
                    buff.strip().endswith(";"):
                parser_f(buff.strip(" ;\n\r\t"))
                buff = ""
                prompt = prompt_f()
    except EOFError:
        return

def main():

    try:
        logging.basicConfig()
#         logging.basicConfig(filename="/Users/mik/dev/elsec/elsec/esc.log", level=logging.DEBUG)
        args = get_args_parser().parse_args()
        if not args.index:
            indices = elsec.actions.get_indices(args.host)
            aliases = elsec.actions.get_aliases(args.host)
            print("Indices: %s, aliases: %s" % (sorted(indices), sorted(aliases)))
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
    parser_f = functools.partial(elsec.parser.parse, args.host, args.index, output)
    output("Type 'help' for help. Exit with Control-D. ")
    input_loop(prompt_f, raw_input, parser_f)
    _save_readline_history()
    output("Bye!")
    sys.exit(0)


if __name__ == "__main__":
    main()


