import unittest
import logging

import elsec.actions
import elsec.test.fixture


class ActionsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        elsec.test.fixture.delete()
        elsec.test.fixture.create()
        logging.debug("Set up ES fixtures.")


    @classmethod
    def tearDownClass(cls): 
        elsec.test.fixture.delete()
        logging.debug("Tore down ES fixtures.")
        

    def test_search(self):
        res = list(elsec.actions.do_search('localhost:9200', 'elsec_test_index_1', 'doctype_1.field_2:3')) 
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0], elsec.actions.RequestT(url='http://localhost:9200/elsec_test_index_1/_search', method='POST', request={'query': {'query_string': {'query': 'doctype_1.field_2:3', 'default_field': '_all'}}, 'from': 0, 'fields': ['_id'], 'size': 10}, curl='curl -XPOST \'http://localhost:9200/elsec_test_index_1/_search\' -d \'{\n    "fields": [\n        "_id"\n    ], \n    "from": 0, \n    "query": {\n        "query_string": {\n            "default_field": "_all", \n            "query": "doctype_1.field_2:3"\n        }\n    }, \n    "size": 10\n}\''))
        # cannot test the whole response because 'took' is variable
        self.assertEqual(res[0][1].status, 200)
        self.assertEqual(res[0][1].data['hits']['total'], 1)


    def test_count(self):
        res = list(elsec.actions.do_count('localhost:9200', 'elsec_test_index_1', 'doctype_1.field_2:3')) 
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0], elsec.actions.RequestT(url='http://localhost:9200/elsec_test_index_1/_count', method='POST', request={'query': {'query_string': {'query': 'doctype_1.field_2:3', 'default_field': '_all'}}, 'from': 0, 'fields': ['_id'], 'size': 10}, curl='curl -XPOST \'http://localhost:9200/elsec_test_index_1/_count\' -d \'{\n    "query_string": {\n        "default_field": "_all", \n        "query": "doctype_1.field_2:3"\n    }\n}\''))
        # cannot test the whole response because 'took' is variable
        self.assertEqual(res[0][1].status, 200)
        self.assertEqual(res[0][1].data['count'], 1)


    def test_flat(self):
        req = elsec.actions.RequestT(url='http://localhost:9200/elsec_test_index_1/_search', method='POST', request={'query': {'query_string': {'query': 'doctype_1.field_2:3', 'default_field': '_all'}}, 'from': 0, 'fields': ['_id'], 'size': 10}, curl='curl -XPOST \'http://localhost:9200/elsec_test_index_1/_search\' -d \'{\n    "fields": [\n        "_id"\n    ], \n    "from": 0, \n    "query": {\n        "query_string": {\n            "default_field": "_all", \n            "query": "doctype_1.field_2:3"\n        }\n    }, \n    "size": 10\n}\'')
        self.assertFalse(elsec.output.FLAT)
        for rreq, rres in elsec.actions.do_flat('localhost:9200', 'elsec_test_index_1', req):
            self.assertEqual(req.request, rreq.request)
            self.assertNotEqual(req.curl, rreq.curl) # in the new request, curl is flattened
            self.assertTrue(elsec.output.FLAT)
        self.assertFalse(elsec.output.FLAT)


    def test_view(self):
        res = list(elsec.actions.do_view('localhost:9200', 'elsec_test_index_1', 1))
        # there are 2 doctypes in the index, so there will be 2 results
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0], elsec.actions.RequestT(url=u'http://localhost:9200/elsec_test_index_1/doctype_1/1', method='GET', request=None, curl=u"curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_1/1'"))
        self.assertEqual(res[0][1], elsec.actions.ResponseT(status=200, data={u'_type': u'doctype_1', u'exists': True, u'_source': {u'field_2': u'value 1', u'field_1': u'in1, dt1'}, u'_index': u'elsec_test_index_1', u'_version': 1, u'_id': u'1'}))


# uncomment if you don't mind browser opening windows
#
#     def test_open(self):
#         res = list(elsec.actions.do_open('localhost:9200', 'elsec_test_index_1', 1))
#         # there are 2 doctypes in the index, so there will be 2 windows open
#         self.assertEqual(len(res), 2)
#         for r in res:
#             self.assertEqual(r[0], None)
#             self.assertEqual(r[1], None)

        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(failfast=True)


