# -*- coding: utf-8 -*-

import sys
import os.path
import errno
import argparse
import readline
import json
import traceback
import logging

import esclient.http
import esclient.actions
import esclient.parser


logger = logging.getLogger(__name__)

def _get_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".esclient_history")
        readline.read_history_file(fn)
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            print("No command history file found.")
        else:
            logger.warning(exc)


def _save_readline_history():
    try: 
        fn = os.path.join(os.path.expanduser("~"), ".esclient_history")
        readline.set_history_length(20)
        readline.write_history_file(fn)
    except IOError as exc:
        logger.warning(exc)


def configure_readline():
    _get_readline_history()
    readline.set_completer(esclient.parser.complete)
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
    _, _, _, mappings = esclient.actions.get_mappings(host, index)
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
    

def output(data):
    if type(data) in [str, unicode]:
        print(data)
        return
    print(json.dumps(data, indent=4, sort_keys=True))
    return


def get_args_parser():
    parser = argparse.ArgumentParser(description="ElasticSearch client.")
    parser.add_argument('host', type=str, help="elasticsearch server address, including port")
    parser.add_argument('index', type=str, nargs="?", help="name of the index")
    return parser


def input_loop(host, index):
    prompt = None
    buffer = ""
    while True:
        if not prompt: 
            prompt = "%s/%s/> " % (host, index)
        line = raw_input(prompt).strip()
        if not line:
            continue
        buffer += " " + line
        prompt = "> "
        if (buffer.strip().split()[0].lower() not in ['search', 'count']) or (buffer.strip().endswith(";")):
            esclient.parser.parse(host, index, buffer.strip(" ;\n\r\t"))
            buffer = ""
            prompt = None


def main():

    try:
        logging.basicConfig()
#         logging.basicConfig(filename="/Users/mik/dev/esclient/esclient/esc.log", level=logging.DEBUG)
        args = get_args_parser().parse_args()
        if not args.index:
            indices = esclient.actions.get_indices(args.host)
            aliases = esclient.actions.get_aliases(args.host)
            print("Indices: %s, aliases: %s" % (sorted(indices), sorted(aliases)))
            sys.exit(0)
        esclient.parser.completions['fields'] = sorted(get_fieldnames(args.host, args.index))
        configure_readline()

    except (TypeError, ValueError):
        logger.error("Error initializing, check your connection parameters.", exc_info=True)
        sys.exit(1)

    except IOError:
        logger.error("IO (network) error, check your connection parameters.", exc_info=True)
        sys.exit(1)


    try: 
        print ("Type 'help' for help. Exit with Control-D. ")
        input_loop(args.host, args.index)

    
    except EOFError:
        _save_readline_history()
        print("Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()