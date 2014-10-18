#!/usr/bin/env python2
import os
import unittest
import sys
from test import PythonOrgSearch


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(PythonOrgSearch),
    ))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())




