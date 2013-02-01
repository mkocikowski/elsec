import sys
import unittest
import logging


def suite():
    tests = unittest.defaultTestLoader.discover('.')
    return tests


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    tests = suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
        sys.exit(1)


