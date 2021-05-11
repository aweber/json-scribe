import datetime
import logging
import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import jsonscribe


class AttributeSetterTests(unittest.TestCase):
    def setUp(self):
        super(AttributeSetterTests, self).setUp()
        self.record = logging.LogRecord(
            'name',
            logging.INFO,
            __file__,
            11,
            'message: %s', ('args', ),
            exc_info=None)

    def test_that_attributes_are_created(self):
        filterer = jsonscribe.AttributeSetter(add_fields={'somename': None})
        filterer.filter(self.record)
        self.assertTrue(hasattr(self.record, 'somename'))
        self.assertEqual(None, self.record.somename)

    def test_that_attributes_are_not_overwritten(self):
        filterer = jsonscribe.AttributeSetter(add_fields={'somename': None})
        setattr(self.record, 'somename', 'somevalue')
        filterer.filter(self.record)
        self.assertEqual('somevalue', self.record.somename)

    def test_that_filter_returns_one(self):
        filterer = jsonscribe.AttributeSetter()
        result = filterer.filter(self.record)
        self.assertEqual(1, result)

    def test_that_default_values_are_set_asis(self):
        filterer = jsonscribe.AttributeSetter(add_fields={
            'string': 'asdf',
            'int': 1234,
            'float': 3.141592653589793,
        })
        filterer.filter(self.record)
        self.assertEqual('asdf', self.record.string)
        self.assertEqual(1234, self.record.int)
        self.assertEqual(3.141592653589793, self.record.float)

    def test_that_ext_uuid_works(self):
        filterer = jsonscribe.AttributeSetter(add_fields={
            'uid': 'ext://UUID',
        })
        filterer.filter(self.record)
        self.assertIsInstance(self.record.uid, uuid.UUID)

    def test_that_ext_now_works(self):
        filterer = jsonscribe.AttributeSetter(add_fields={
            'now': 'ext://now',
        })
        filterer.filter(self.record)
        self.assertIsInstance(self.record.now, datetime.datetime)
