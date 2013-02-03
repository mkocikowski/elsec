import unittest
import logging
import argparse
# import sys
import functools
import StringIO
# import time
import types

import elsec.client
import elsec.parser
import elsec.actions
import elsec.exceptions
import elsec.test.fixture


class ParserTest(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         elsec.test.fixture.delete()
#         elsec.test.fixture.create()
#         logging.debug("Set up ES fixtures.")
        
    
    def test_parse(self):    
        
        line = "search doctype_1.field_1:*"
        _g = elsec.parser._parse(line)
        self.assertIsInstance(_g, types.GeneratorType)
        _l = list(_g)
        self.assertEqual(1, len(_l))
        self.assertEqual(_l[0][0].__name__, 'do_search') 
        self.assertEqual(_l[0][1], ['doctype_1.field_1:*',]) 

        line = "count doctype_1.field_1:*"
        _g = elsec.parser._parse(line)
        self.assertIsInstance(_g, types.GeneratorType)
        _l = list(_g)
        self.assertEqual(1, len(_l))
        self.assertEqual(_l[0][0].__name__, 'do_count') 
        self.assertEqual(_l[0][1], ['doctype_1.field_1:*',]) 

        line = "view doc_1 doc_2"
        _g = elsec.parser._parse(line)
        self.assertIsInstance(_g, types.GeneratorType)
        _l = list(_g)
        self.assertEqual(2, len(_l))
        self.assertEqual(_l[0][0].__name__, 'do_view') 
        self.assertEqual(_l[0][1], ['doc_1',]) 
        self.assertEqual(_l[1][0].__name__, 'do_view') 
        self.assertEqual(_l[1][1], ['doc_2',]) 

        line = "help"
        _g = elsec.parser._parse(line)
        self.assertIsInstance(_g, types.GeneratorType)
        _l = list(_g)
        self.assertEqual(1, len(_l))
        self.assertEqual(_l[0][0].__name__, '_help') 
        self.assertEqual(_l[0][1], []) 
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(failfast=True)


