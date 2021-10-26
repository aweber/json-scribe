import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from jsonscribe import utils


class ParseBooleanTests(unittest.TestCase):
    def assert_parsed_as_false(self, expr):
        self.assertIs(
            utils.parse_boolean(expr), False,
            repr(expr) + ' not parsed as false')

    def assert_parsed_as_true(self, expr):
        self.assertIs(
            utils.parse_boolean(expr), True,
            repr(expr) + ' not parsed as true')

    def test_falsy_values(self):
        self.assert_parsed_as_false(None)
        for value in ('0', 'n', 'no', 'f', 'false'):
            self.assert_parsed_as_false(value.lower())
            self.assert_parsed_as_false(value.upper())
            self.assert_parsed_as_false(value.title())
            self.assert_parsed_as_false(' ' + value + '\t')

    def test_truthy_values(self):
        for value in ('1', 'y', 'yes', 't', 'true'):
            self.assert_parsed_as_true(value.lower())
            self.assert_parsed_as_true(value.upper())
            self.assert_parsed_as_true(value.title())
            self.assert_parsed_as_true(' ' + value + '\t')

    def test_that_unexpected_values_raises(self):
        for unexpected in (str(uuid.uuid4()), dict(), list()):
            with self.assertRaises(ValueError) as context:
                utils.parse_boolean(unexpected)
            self.assertEqual(
                'cannot determine Boolean value: ' + repr(unexpected),
                str(context.exception))

    def test_booleans_and_integers(self):
        for value in (1, 10, True, 1.0):
            self.assert_parsed_as_true(value)

        for value in (0, False, 0.0, None):
            self.assert_parsed_as_false(value)
