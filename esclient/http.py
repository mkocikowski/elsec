# -*- coding: utf-8 -*-

import urlparse
import httplib

def _validate_url(url):
    p = urlparse.urlsplit(url)
    if p.scheme != 'http': 
        raise ValueError("url must begin with 'http://'")
    host = p.netloc
    path = p.path
    if p.query != '':
        path += "?" + p.query
    return host, path


def get(url, timeout=20):
    host, path = _validate_url(url)
    conn = httplib.HTTPConnection(host, timeout=timeout)
    conn.request('GET', path, body=None)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, resp.reason, data


def put(url, data, timeout=20):
    host, path = _validate_url(url)
    conn = httplib.HTTPConnection(host, timeout=timeout)
    head = {'Content-type': 'application/json'}
    conn.request('PUT', path, data, head)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, resp.reason, data


def post(url, data, timeout=20):
    host, path = _validate_url(url)
    conn = httplib.HTTPConnection(host, timeout=timeout)
    head = {'Content-type': 'application/json'}
    conn.request('POST', path, data, head)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, resp.reason, data


def delete(url, timeout=20):
    host, path = _validate_url(url)
    conn = httplib.HTTPConnection(host, timeout=timeout)
    conn.request('DELETE', path, body=None)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, resp.reason, data

