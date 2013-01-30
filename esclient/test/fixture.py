# -*- coding: utf-8 -*-

import json

import esclient.http

# delete test indexes
esclient.http.delete("http://localhost:9200/test_1")
esclient.http.delete("http://localhost:9200/test_2")
esclient.http.delete("http://localhost:9200/index_1")
esclient.http.delete("http://localhost:9200/index_2")

# create test indexes
esclient.http.put("http://localhost:9200/index_1/", """{"settings": {"index": {"number_of_replicas": 0, "number_of_shards": 1}}}""")
esclient.http.put("http://localhost:9200/index_2/", """{"settings": {"index": {"number_of_replicas": 0, "number_of_shards": 1}}}""")

# create an alias which joins the two indices
esclient.http.post("http://localhost:9200/_aliases/", """{"actions": [{ "add" : {"index": "index_1", "alias": "alias_1" } }, {"add": {"index": "index_2", "alias": "alias_1" }}, {"add": {"index": "index_1", "alias": "alias_2" }}]}""")

# populate with test documents
esclient.http.put("http://localhost:9200/index_1/doctype_1/1", json.dumps({'field_1': 'in1, dt1', 'field_2': 'value 1', }))
esclient.http.put("http://localhost:9200/index_1/doctype_1/2", json.dumps({'field_1': 'in1, dt1', 'field_2': 'value 2', }))
esclient.http.put("http://localhost:9200/index_1/doctype_1/3", json.dumps({'field_1': 'in1, dt1', 'field_2': 'value 3', }))
esclient.http.put("http://localhost:9200/index_1/doctype_1/4", json.dumps({'field_1': 'in1, dt1', 'field_2': None, }))
esclient.http.put("http://localhost:9200/index_1/doctype_2/1", json.dumps({'field_1': 'in1, dt2', 'field_2': 'value 1', }))
esclient.http.put("http://localhost:9200/index_2/doctype_1/1", json.dumps({'field_1': 'in2, dt1', 'field_2': 'value 1', }))
esclient.http.put("http://localhost:9200/index_2/doctype_2/2", json.dumps({'field_1': 'in2, dt2', 'field_2': 'value 1', }))
esclient.http.put("http://localhost:9200/index_2/doctype_3/2", json.dumps({'field_A': 'in2, dt3', 'field_B': 'value 1', }))

