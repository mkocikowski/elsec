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


def output(data):
    if type(data) in [str, unicode]:
        print(data)
        return
    print(json.dumps(data, indent=4, sort_keys=True))
    return


def get_args_parser():
    parser = argparse.ArgumentParser(description="ElasticSearch client.")
    parser.add_argument('host', type=str)
    parser.add_argument('index', type=str)
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
        mappings = esclient.actions.get_mappings(args.host, args.index)
        fields = [f[0] for f in esclient.actions.get_fields(mappings)]
        esclient.parser.completions['fields'] = sorted(fields)
        configure_readline()
        print ("Type 'help' for help. Exit with Control-D. ")
        input_loop(args.host, args.index)

    except IOError as exc:
        print("IO (network) error, check your connection parameters. \nError: %s" % (exc,))
        sys.exit(1)
    
    except EOFError:
        _save_readline_history()
        print("Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()