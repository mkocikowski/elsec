# -*- coding: utf-8 -*-

import copy
import json
import traceback
import logging

import elsec.http
import elsec.templates
import elsec.exceptions


logger = logging.getLogger(__name__)


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
    curl = "curl -XGET '%s'" % (url,)
    status, reason, data = elsec.http.get(url)
    data = json.loads(data)
    if 'error' in data:
        raise elsec.exceptions.ESRequestError(data['status'], data['error'])
    return (curl, url, None, data)


# def get_fields(mappings):
#     def _dot_collapse(pre, d): 
#         for k in d.keys():
#             try: 
#                 ps = "%s.%s" % (pre, k) if pre else k
#                 for f in _dot_collapse(ps, d[k]['properties']): 
#                     yield f
#             except KeyError:
#                 yield ("%s.%s" % (pre, k), d[k]['type'])
#     return _dot_collapse("", mappings)


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
    curl = "curl -XPOST '%s' -d '%s'" % \
        (url, json.dumps(request, indent=4, sort_keys=True))
    status, reason, data = elsec.http.post(url, json.dumps(request))
    return (curl, url, request, json.loads(data))


def do_count(host, index, query): 
    request = _prepare_request(query)
    if 'query' in request:
        qqs = request['query']
    else:
        # let's hope for the best, if the request is bum, we'll get an
        # error from the ES
        qqs = request
    url = "http://%s/%s/_count" % (host, index)
    curl = "curl -XPOST '%s' -d '%s'" % \
        (url, json.dumps(qqs, indent=4, sort_keys=True))
    status, reason, data = elsec.http.post(url, json.dumps(qqs))
    return (curl, url, qqs, json.loads(data))


def do_view(host, index, mapping, docid):
    url = "http://%s/%s/%s/%s" % (host, index, mapping, docid)
    curl = "curl -XGET '%s'" % (url, )
    status, reason, data = elsec.http.get(url)
    return (curl, url, None, json.loads(data))

