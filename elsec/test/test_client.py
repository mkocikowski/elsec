import unittest
import logging
import argparse
# import sys
import functools
import StringIO
# import time
import json

import elsec.client
import elsec.output
import elsec.help
import elsec.exceptions
import elsec.test.fixture


# this will feed the lines from the list, and raise EOFError when the
# list is empty, mimicking user entering a bunch of stuff and then
# hitting CTRL-D. The CTRL-D is important, because that is how readline breaks
# out of the input loop.
#
def _input(lines): 
    _lines = list(lines)
    def _i(prompt):
        if _lines: return _lines.pop()
        raise EOFError()    
    return _i


class ClientTest(unittest.TestCase):

#     def setUp(self): 
#         reload(elsec.client)
    
    @classmethod
    def setUpClass(cls):
        elsec.test.fixture.delete()
        elsec.test.fixture.create()
        logging.debug("Set up ES fixtures.")
        

    @classmethod
    def tearDownClass(cls): 
        elsec.test.fixture.delete()
        logging.debug("Tore down ES fixtures.")

    
    def test_argparse(self):    
        parser = elsec.client.get_args_parser()
        # test default parameters
        args = parser.parse_args("".split(" "))
        self.assertEqual(args, argparse.Namespace(host='localhost', port=9200, index='', flat=False))
        # test default parameters with 'index_1'        
        args = parser.parse_args("index_1".split(" "))
        self.assertEqual(args, argparse.Namespace(host='localhost', port=9200, index='index_1', flat=False))        
        # test with correct parameters
        args = parser.parse_args("-h foohost -p 9300 index_1".split(" "))
        self.assertEqual(args, argparse.Namespace(host='foohost', port=9300, index='index_1', flat=False))


#     def test_output(self):
#         out = StringIO.StringIO()
#         lines = ['foo', u'bar', {'foo':'bar', 'x': None}]
#         for l in lines:
#             elsec.client.output(l, fh=out)     
#         expected = """foo
# bar
# {
#     "foo": "bar", 
#     "x": null
# }
# """
#         result = out.getvalue()
#         out.close()        
#         self.assertEqual(result, expected)
        
    
    def test_get_fieldnames(self):
    
        result = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_index_1')
        self.assertEqual(result, [u'doctype_2.field_2', u'doctype_2.field_1', 
            u'doctype_1.field_2', u'doctype_1.field_1'])

        result_A = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_index_1')
        result_B = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_alias_2')
        self.assertEqual(result_A, result_B)

        # elsec_test_alias_1 points to indices 1 and 2; so the results of
        # calling get_fieldnames on the alias and on the two indices should be
        # the same.
        result_A = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_alias_1')
        result_B = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_index_1,elsec_test_index_2')
        self.assertEqual(result_A, result_B)
        
        with self.assertRaises(elsec.exceptions.ESRequestError):
            result = elsec.client.get_fieldnames('localhost:9200', 'FOO')
        with self.assertRaises(elsec.exceptions.ESError):
            result = elsec.client.get_fieldnames('localhost:9200', 'FOO')
        # elsec.exceptions.ESRequestError should also be a ValueError
        with self.assertRaises(ValueError):
            result = elsec.client.get_fieldnames('localhost:9200', 'FOO')
            
        with self.assertRaises(IOError):
            result = elsec.client.get_fieldnames('XXX', 'elsec_test_index_1')
    
    
    def test_collapse_mapping(self):
    
        # this mapping includes a multi field (doc.keywords.data/data.raw)
        s = """{"doc": {"_size": {"enabled": true, "store": "yes"}, "_source": {"enabled": true}, "properties": {"body": {"dynamic": true, "properties": {"data": {"dynamic": true, "properties": {"txt": {"dynamic": true, "properties": {"body": {"type": "string"}, "body_size": {"null_value": 0, "type": "integer"}}}}}}}, "keywords": {"dynamic": "true", "properties": {"count": {"ignore_malformed": false, "type": "short"}, "data": {"fields": {"data": {"type": "string"}, "raw": {"include_in_all": false, "index": "not_analyzed", "type": "string"}}, "path": "full", "type": "multi_field"}}}}}}"""
        m = json.loads(s)
        l = elsec.client._collapse_mapping(m)
        self.assertEqual(l, [u'doc.body.data.txt.body', u'doc.body.data.txt.body_size', u'doc.keywords.count', u'doc.keywords.data.raw', u'doc.keywords.data'])

    
    def test_input_loop(self):
        
        # this parser will store incoming lines into _lines, so that they can
        # be compared with what is expected. This is mostly to test if the
        # multiline input works ok.
        def _parser():
            _lines = []
            def _p(*args): 
                _lines.append(args)
                return
            return _p, _lines
    
        # these will get popped in reverse order, the primary purpose here 
        # if to test that the multiline gets dealt with correctly
        in_l = ['last', ';', '   ', 'line', 'search multi', 'first']
        in_f = _input(in_l)    
        parser_f, parser_l = _parser()
        
        elsec.client.input_loop(lambda: "", in_f, parser_f)
        self.assertEqual(parser_l, [('first',), ('search multi line',), ('last',)])


    def test_main(self): 

        # 'dry run' - no CLI arguments
        with self.assertRaises(SystemExit) as c:
            elsec.client.main([], input_f=None, output_f=lambda x: True, loop_f=None)
        self.assertEqual(c.exception.code, 0)
        
        # 'correct' - single CLI argument naming valid index
        with self.assertRaises(SystemExit) as c:
            elsec.client.main(['elsec_test_index_1'], input_f=None, output_f=lambda x: True, loop_f=lambda x,y,z: True)
        self.assertEqual(c.exception.code, 0)

        # 'correct' - single CLI argument naming valid index, and explicit naming of host and port
        with self.assertRaises(SystemExit) as c:
            elsec.client.main(['elsec_test_index_1', '-h', 'localhost', '-p', '9200'], input_f=None, output_f=lambda x: True, loop_f=lambda x,y,z: True)
        self.assertEqual(c.exception.code, 0)

        # 'incorrect' - invalid port
        with self.assertRaises(SystemExit) as c:
            elsec.client.main(['elsec_test_index_1', '-h', 'localhost', '-p', '9999'], input_f=None, output_f=lambda x: True, loop_f=lambda x,y,z: True)
        self.assertEqual(c.exception.code, 2)

        # 'incorrect' - single CLI argument naming valid index / valid doctype
        with self.assertRaises(SystemExit) as c:
            elsec.client.main(['elsec_test_index_1/doctype_1'], input_f=None, output_f=lambda x: True, loop_f=lambda x,y,z: True)
        self.assertEqual(c.exception.code, 1)
    

    def test_parser(self):

        # there is a separate module for thorough testing of the parser, this
        # is more to do a nose-to-tail run, simulating command line input and
        # comparing the output with expectations.

        out = StringIO.StringIO()
        def _output(data):
            return elsec.output.output(data, fh=out)
        
        parser_f = functools.partial(elsec.parser.handle, 'localhost:9200', 'elsec_test_index_1', _output)
    
        # these will get popped in reverse order, the primary purpose here 
        # if to test that the multiline gets dealt with correctly
        in_l = ['help', 'view 1 2', 'view 3;', '   ', 'count doctype_1.field_2:3;', 'first']
        in_f = _input(in_l)    
        
        elsec.client.input_loop(lambda: "", in_f, parser_f)
        
        expected = """curl -XPOST 'http://localhost:9200/elsec_test_index_1/_count' -d '{
    "query_string": {
        "default_field": "_all", 
        "query": "doctype_1.field_2:3"
    }
}'
>
{
    "_shards": {
        "failed": 0, 
        "successful": 1, 
        "total": 1
    }, 
    "count": 1
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_1/3'
>
{
    "_id": "3", 
    "_index": "elsec_test_index_1", 
    "_source": {
        "field_1": "in1, dt1", 
        "field_2": "value 3"
    }, 
    "_type": "doctype_1", 
    "_version": 1, 
    "exists": true
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_2/3'
>
{
    "_id": "3", 
    "_index": "elsec_test_index_1", 
    "_type": "doctype_2", 
    "exists": false
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_1/1'
>
{
    "_id": "1", 
    "_index": "elsec_test_index_1", 
    "_source": {
        "field_1": "in1, dt1", 
        "field_2": "value 1"
    }, 
    "_type": "doctype_1", 
    "_version": 1, 
    "exists": true
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_2/1'
>
{
    "_id": "1", 
    "_index": "elsec_test_index_1", 
    "_source": {
        "field_1": "in1, dt2", 
        "field_2": "value 1"
    }, 
    "_type": "doctype_2", 
    "_version": 1, 
    "exists": true
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_1/2'
>
{
    "_id": "2", 
    "_index": "elsec_test_index_1", 
    "_source": {
        "field_1": "in1, dt1", 
        "field_2": "value 2"
    }, 
    "_type": "doctype_1", 
    "_version": 1, 
    "exists": true
}
curl -XGET 'http://localhost:9200/elsec_test_index_1/doctype_2/2'
>
{
    "_id": "2", 
    "_index": "elsec_test_index_1", 
    "_type": "doctype_2", 
    "exists": false
}
%s
""" % elsec.help.OVERVIEW
        result = out.getvalue()
        out.close()
        self.assertEqual(result, expected)
        
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(failfast=True)


