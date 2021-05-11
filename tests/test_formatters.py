# encoding: utf-8
from __future__ import unicode_literals

import datetime
import json
import logging
import sys
import traceback
import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import jsonscribe
import jsonscribe.utils


class JsonFormatterTests(unittest.TestCase):
    def setUp(self):
        super(JsonFormatterTests, self).setUp()
        self.record = logging.LogRecord(
            'name',
            logging.INFO,
            __file__,
            11,
            'message: %s', ('args', ),
            exc_info=None)

    def test_that_include_fields_defaults_to_empty_list(self):
        formatter = jsonscribe.JSONFormatter()
        self.assertEqual([], formatter.include_fields)

    def test_that_include_fields_are_retained(self):
        formatter = jsonscribe.JSONFormatter(include_fields=['one'])
        self.assertEqual(['one'], formatter.include_fields)

    def test_that_format_sets_message_attribute(self):
        formatter = jsonscribe.JSONFormatter()
        formatter.format(self.record)
        self.assertEqual(self.record.getMessage(), self.record.message)

    def test_that_format_sets_asctime_attribute(self):
        formatter = jsonscribe.JSONFormatter()
        formatter.format(self.record)
        then = datetime.datetime.fromtimestamp(
            self.record.created, tz=jsonscribe.utils.utc)
        self.assertEqual(self.record.asctime,
                         then.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))

    def test_that_listed_fields_are_included_in_output(self):
        formatter = jsonscribe.JSONFormatter(
            include_fields=['message', 'created', 'funcName', 'levelname'])
        output = formatter.format(self.record)
        self.assertDictEqual({
            'message': 'message: args',
            'created': self.record.created,
            'funcName': self.record.funcName,
            'levelname': 'INFO',
        }, json.loads(output))

    def test_that_nonexistent_fields_are_defaulted_in_output(self):
        formatter = jsonscribe.JSONFormatter(include_fields=['doesnotexist'])
        output = formatter.format(self.record)
        self.assertDictEqual({'doesnotexist': None}, json.loads(output))

    def test_that_exception_info_is_included(self):
        try:
            raise RuntimeError
        except RuntimeError:
            self.record.exc_info = sys.exc_info()
        expected = traceback.format_exception(self.record.exc_info[0],
                                              self.record.exc_info[1],
                                              self.record.exc_info[2])
        formatter = jsonscribe.JSONFormatter(include_fields=['exc_info'])
        output = formatter.format(self.record)
        self.assertEqual(expected, json.loads(output)['exc_info'])

    def test_that_exception_info_is_none_without_exception(self):
        formatter = jsonscribe.JSONFormatter(include_fields=['exc_info'])
        output = formatter.format(self.record)
        self.assertIsNone(json.loads(output)['exc_info'])

    def test_that_newlines_are_literalized_in_messages(self):
        self.record.args = ('foo\nbar', )
        formatter = jsonscribe.JSONFormatter(include_fields=['message'])
        output = formatter.format(self.record)
        self.assertNotIn('foo\nbar', output)
        self.assertIn('foo\\nbar', output)

    def test_that_unicode_characters_are_literalized(self):
        self.record.msg = 'fü%s'
        self.record.args = ('bår', )
        formatter = jsonscribe.JSONFormatter(include_fields=['message'])
        output = formatter.format(self.record)
        self.assertIn('f\\u00fcb\\u00e5r', output.lower())

    def test_that_uuids_are_jsonified(self):
        uid = uuid.uuid4()
        self.record.__dict__['correlation_id'] = uid
        formatter = jsonscribe.JSONFormatter(include_fields=['correlation_id'])
        output = formatter.format(self.record)
        self.assertEqual(uid, uuid.UUID(json.loads(output)['correlation_id']))

    def test_that_datetimes_are_jsonified(self):
        now = datetime.datetime.now(tz=jsonscribe.utils.utc)
        self.record.__dict__['then'] = now
        formatter = jsonscribe.JSONFormatter(include_fields=['then'])
        output = formatter.format(self.record)
        self.assertEqual(
            now.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            json.loads(output)['then'])

    def test_that_repr_is_used_for_unknown_types(self):
        class Other(object):
            pass

        obj = Other()
        self.record.__dict__['obj'] = obj
        formatter = jsonscribe.JSONFormatter(include_fields=['obj'])
        output = formatter.format(self.record)
        self.assertEqual(repr(obj), json.loads(output)['obj'])


class LogglyFormattingTests(unittest.TestCase):
    def setUp(self):
        super(LogglyFormattingTests, self).setUp()
        self.record = logging.LogRecord(
            'name',
            logging.INFO,
            __file__,
            11,
            'message: %s', ('args', ),
            exc_info=None)

    def test_that_property_names_are_normalized(self):
        try:
            raise RuntimeError
        except RuntimeError:
            self.record.exc_info = sys.exc_info()
        expected = traceback.format_exception(self.record.exc_info[0],
                                              self.record.exc_info[1],
                                              self.record.exc_info[2])
        formatter = jsonscribe.JSONFormatter(
            include_fields=['exc_info'], use_loggly_names=True)
        output = formatter.format(self.record)
        self.assertEqual(expected, json.loads(output)['excinfo'])

    def test_that_goofy_property_names_are_normalized(self):
        formatter = jsonscribe.JSONFormatter(
            include_fields=['__blah__', 'foo-bar', 'with space'],
            use_loggly_names=True)
        self.record.__dict__['__blah__'] = 'blah'
        self.record.__dict__['foo-bar'] = 'quux'
        self.record.__dict__['with space'] = 'ick'

        output = formatter.format(self.record)
        body = json.loads(output)
        self.assertEqual('quux', body['foobar'])
        self.assertEqual('ick', body['withspace'])
        self.assertEqual('blah', body['blah'])
