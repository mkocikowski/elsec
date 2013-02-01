import unittest
import logging
import argparse
# import sys
import functools
import StringIO
# import time

import elsec.client
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
    
    @classmethod
    def setUpClass(cls):
        elsec.test.fixture.delete()
        elsec.test.fixture.create()
        logging.debug("Set up ES fixtures.")
        
    
    def test_argparse(self):    
        parser = elsec.client.get_args_parser()
        # test with correct parameters
        args = parser.parse_args("localhost:9200 index_1".split(" "))
        self.assertEqual(args, argparse.Namespace(host='localhost:9200', index='index_1'))
        # test errors 
        with self.assertRaises(SystemExit): 
            args = parser.parse_args([])


    def test_output(self):
        out = StringIO.StringIO()
        lines = ['foo', u'bar', {'foo':'bar', 'x': None}]
        for l in lines:
            elsec.client.output(l, fh=out)     
        expected = """foo
bar
{
    "foo": "bar", 
    "x": null
}
"""
        result = out.getvalue()
        out.close()        
        self.assertEqual(result, expected)
        
    
    def test_get_fieldnames(self):
        result = elsec.client.get_fieldnames('localhost:9200', 'elsec_test_index_1')
        self.assertEqual(result, [u'doctype_2.field_2', u'doctype_2.field_1', 
            u'doctype_1.field_2', u'doctype_1.field_1'])
    
    
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


    def test_parser(self):

        # there is a separate module for thorough testing of the parser, this
        # is more to do a nose-to-tail run, simulating command line input and
        # comparing the output with expectations.

        out = StringIO.StringIO()
        def _output(data):
            return elsec.client.output(data, fh=out)
        
        parser_f = functools.partial(elsec.parser.parse, 'localhost:9200', 'elsec_test_index_1', _output)
    
        # these will get popped in reverse order, the primary purpose here 
        # if to test that the multiline gets dealt with correctly
        in_l = ['last', '   ', 'count doctype_1.field_2:3;', 'first']
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
"""
        result = out.getvalue()
        out.close()
        
        self.assertEqual(result, expected)
        
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(failfast=True)

