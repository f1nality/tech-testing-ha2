#!/usr/bin/env python2
import unittest
import sys

from tests.target_mail_ru import TargetMailRuTestCase


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(TargetMailRuTestCase),
    ))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())




