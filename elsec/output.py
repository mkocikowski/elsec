# -*- coding: utf-8 -*-

import sys
import json

FLAT = False
SEPARATOR = ">"


def dumps(data): 
    if FLAT:
        return json.dumps(data)
    return json.dumps(data, indent=4, sort_keys=True)

def output(data, fh=sys.stdout):
    """Output data, if it is not string, then serialized to JSON. 
    
    Input:
    - data: if str or unicode, output as is. If other, serialize to JSON
    - fh: file handle for output, defaults to sys.stdout
    
    """
    if FLAT and data == SEPARATOR:
        pass
        return
    if type(data) in [str, unicode]:
        fh.write(data)
        fh.write("\n")
        return
    fh.write(dumps(data))
    fh.write("\n")
    return
