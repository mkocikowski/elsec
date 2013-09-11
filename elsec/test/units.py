import sys
import os.path
import unittest
import logging


def suite():
    tests = unittest.defaultTestLoader.discover(os.path.dirname(__file__))
    return tests


if __name__ == "__main__":
    logging.basicConfig(level=logging.CRITICAL)
    tests = suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
        sys.exit(1)


