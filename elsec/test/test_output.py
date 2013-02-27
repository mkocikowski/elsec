import unittest
import logging
import argparse
# import sys
import functools
import StringIO
# import time

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


class OutputTest(unittest.TestCase):
    
    def test_output(self):
        out = StringIO.StringIO()
        lines = ['foo', u'bar', {'foo':'bar', 'x': None}]
        for l in lines:
            elsec.output.output(l, fh=out)     
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
        
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(failfast=True)


