# -*- coding: utf-8 -*-

import copy
import json
# import traceback
import logging
import subprocess, shlex
import collections
import tempfile
import time

import elsec.http
import elsec.templates
import elsec.exceptions
import elsec.output


logger = logging.getLogger(__name__)

RequestT = collections.namedtuple('RequestT', ['url', 'method', 'request', 'curl'])
ResponseT = collections.namedtuple('ResponseT', ['status', 'data'])

def get_indices(host):
    url = "http://%s/_settings" % (host, )
    status, reason, data = elsec.http.get(url)
    indices = json.loads(data).keys()
    return indices


def get_aliases(host):
    url = "http://%s/_aliases" % (host, )
    status, reason, data = elsec.http.get(url)
    indices = json.loads(data)
    aliases = dict()
    for i in indices:
        for a in indices[i]['aliases']:
            aliases.setdefault(a, set()).add(i)
    aliases = {k: sorted(v) for k, v in aliases.items()}
    return aliases


def get_mappings(host, index): 
    url = "http://%s/%s/_mapping" % (host, index)
    status, reason, data = elsec.http.get(url)
    data = json.loads(data)
    if 'error' in data:
        raise elsec.exceptions.ESRequestError(data['status'], data['error'])
    return data


# ----------------------------------------------------------------------------

def _prepare_request(query):

    # if the input is valid JSON, then assume that the user pasted a complete
    # request, and run it against the search route
    try: 
        # strip single quotes from the beginning and end, this is a silly
        # convenience thing for when people paste in JSON with the single
        # quotes; this happens a whole lot.
        query = query.strip(" '\n\r")
        request = json.loads(query)    

    # if there is trouble parsing, assume that the input is lucene query
    except ValueError: 
        qqs = copy.deepcopy(elsec.templates.QQS)
        qqs['query_string']['query'] = query
        request = copy.deepcopy(elsec.templates.REQUEST)
        request['query'] = qqs
    
    return request


def do_search(host, index, query): 
    request = _prepare_request(query)
    url = "http://%s/%s/_search" % (host, index)
#     curl = "curl -XPOST '%s' -d '%s'" % \
#         (url, json.dumps(request, indent=4, sort_keys=True))
    curl = "curl -XPOST '%s' -d '%s'" % (url, elsec.output.dumps(request))
    status, reason, data = elsec.http.post(url, json.dumps(request))
    
    req = RequestT(url=url, method='POST', request=request, curl=curl)
    res = ResponseT(status=status, data=json.loads(data))
#     yield (curl, json.loads(data))
    yield (req, res)
    return
    

def do_count(host, index, query): 
    request = _prepare_request(query)
    if 'query' in request:
        qqs = request['query']
    else:
        # let's hope for the best, if the request is bum, we'll get an
        # error from the ES
        qqs = request
    url = "http://%s/%s/_count" % (host, index)
#     curl = "curl -XPOST '%s' -d '%s'" % \
#         (url, json.dumps(qqs, indent=4, sort_keys=True))
    curl = "curl -XPOST '%s' -d '%s'" % (url, elsec.output.dumps(qqs))
    status, reason, data = elsec.http.post(url, json.dumps(qqs))

    req = RequestT(url=url, method='POST', request=request, curl=curl)
    res = ResponseT(status=status, data=json.loads(data))
#     yield (curl, json.loads(data))
    yield (req, res)
    return
    

def do_edit(host, index, req):
    
#     f = tempfile.NamedTemporaryFile()
    with open("/tmp/elsecvim", "w") as f:
        for line in json.dumps(req.request, indent=4, sort_keys=True).split("\n"):
            f.write(line + "\n")
    #         print((line, f.name))
        f.flush()
        
    subprocess.call(["vim", "-n", "/tmp/elsecvim"])

    with open("/tmp/elsecvim", "rU") as f:
        edited = f.read()
#     f.close()
#     print(edited)
    
    try:
#         edited = json.loads(edited)
#         curl = "curl -XPOST '%s' -d '%s'" % (req.url, elsec.output.dumps(edited))
# #         RequestT = collections.namedtuple('RequestT', ['url', 'method', 'request', 'curl'])
#         request = RequestT(req.url, req.method, edited, curl)
# #         print(request)
#         yield (request, None)

        if req.url.endswith("_search"):
            for rr in do_search(host, index, edited):
                yield rr
        elif req.url.endswith("_count"):
            for rr in do_count(host, index, edited):
                yield rr


    except ValueError as exc:
#         logger.error(exc, exc_info=True)
        logger.error("Error parsing JSON, reverting to the pre-edit version")
        yield (req, None)
    
    return


def do_view(host, index, docid):

    types = set()
    for _m in get_mappings(host, index).values():
        types.update(_m.keys())

    for _t in sorted(types):
        url = "http://%s/%s/%s/%s" % (host, index, _t, docid)
        curl = "curl -XGET '%s'" % (url, )
        status, reason, data = elsec.http.get(url)
#         if status == 200: 
        req = RequestT(url=url, method='GET', request=None, curl=curl)
        res = ResponseT(status=status, data=json.loads(data))
#         yield (curl, json.loads(data))
        yield (req, res)

    return


def do_open(host, index, docid):

    for req, _ in do_view(host, index, docid):
        url = req.curl.split()[2].strip(" '")
        _command = "open %s" % (url, )
        rc = subprocess.call(shlex.split(_command.encode("utf-8")))
#         req = RequestT(url=url, method='GET', request=None, curl=curl)
        res = ResponseT(status=status, data=json.loads(data))
        yield (None, None)
        
    return
