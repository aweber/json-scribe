import logging
import os
import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import jsonscribe.config


class ConfigurationTestMixin(object):
    default_format = 'UNSET'

    def setUp(self):
        super(ConfigurationTestMixin, self).setUp()
        self._env_vars = {
            'DEBUG': os.environ.pop('DEBUG', None),
            'LOG_FORMAT': os.environ.pop('LOG_FORMAT', None),
        }

    def tearDown(self):
        for name, value in self._env_vars.items():
            os.environ.pop(name, None)
            if value is not None:
                os.environ[name] = value

    def get_configuration(self, **kwargs):
        raise NotImplementedError()

    def test_config_defaults(self):
        config = self.get_configuration()
        self.assertEqual(self.default_format,
                         config['handlers']['console']['formatter'])
        self.assertEqual(
            jsonscribe.config.CONFIGURATION_DEFAULTS['root']['level'],
            config['root']['level'])

    def test_that_debug_envvar_overrides_log_level(self):
        os.environ['DEBUG'] = '1'
        config = self.get_configuration()
        self.assertEqual(
            logging.getLevelName(logging.DEBUG), config['root']['level'])

    def test_that_force_debug_overrides_everything(self):
        os.environ['DEBUG'] = '0'
        config = self.get_configuration(force_debug=True)
        self.assertEqual(
            logging.getLevelName(logging.DEBUG), config['root']['level'])

    def test_that_unexpected_debug_value_is_ignored(self):
        os.environ['DEBUG'] = 'not-a-boolean-value'
        config = self.get_configuration()
        self.assertEqual(
            jsonscribe.config.CONFIGURATION_DEFAULTS['root']['level'],
            config['root']['level'])

    def test_that_log_format_envvar_overrides_format(self):
        fmts = set(jsonscribe.config.CONFIGURATION_DEFAULTS['formatters'])
        fmts.discard(self.default_format)
        force_format = next(iter(fmts))

        os.environ['LOG_FORMAT'] = force_format
        config = self.get_configuration()
        self.assertEqual(force_format,
                         config['handlers']['console']['formatter'])

    def test_that_force_log_format_overrides_everything(self):
        fmts = set(jsonscribe.config.CONFIGURATION_DEFAULTS['formatters'])
        fmts.discard(self.default_format)
        force_format = next(iter(fmts))

        os.environ['LOG_FORMAT'] = 'not-used-and-would-fail'
        config = self.get_configuration(force_format=force_format)
        self.assertEqual(force_format,
                         config['handlers']['console']['formatter'])

    def test_that_unknown_log_format_fails(self):
        os.environ['LOG_FORMAT'] = str(uuid.uuid4())
        with self.assertRaises(ValueError):
            self.get_configuration()


class ServiceConfigurationTests(ConfigurationTestMixin, unittest.TestCase):
    default_format = 'json'

    def get_configuration(self, **kwargs):
        return jsonscribe.get_service_configuration(**kwargs)


class CLIConfigurationTests(ConfigurationTestMixin, unittest.TestCase):
    default_format = 'plain'

    def get_configuration(self, **kwargs):
        return jsonscribe.get_cli_configuration(**kwargs)
