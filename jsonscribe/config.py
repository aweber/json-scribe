import copy
import os

from jsonscribe import utils

CONFIGURATION_DEFAULTS = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': False,
    'filters': {},
    'formatters': {
        'json': {
            '()': 'jsonscribe.JSONFormatter',
            'include_fields': [
                'asctime', 'exc_info', 'levelname', 'message', 'module', 'name'
            ],
        },
        'plain': {
            'format': ' '.join([
                '%(asctime)s',
                '%(levelname)-8s',
                '%(name)s:',
                '%(message)s',
            ])
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': [],
            'stream': 'ext://sys.stdout',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
}
"""Template used to generate configurations.

You may modify this template as you see fit.  The next call to
:func:`get_service_configuration` or :func:`get_cli_configuration`
will reflect modifications.

"""


def get_service_configuration(**kwargs):
    """Retrieve configuration suitable for a service.

    :param bool force_debug: should the root log level be
        ``logging.DEBUG``?
    :param str force_formatter: optional formatter to use

    The default configuration for a "service" is to emit lines
    as minimized JSON objects and to only emit records at the
    info, warning, and error levels.  If the `force_debug`
    parameter is specified and *truthy*, then debug-level records
    are also emitted.

    :returns: :class:`dict` instance suitable for passing to
        :func:`logging.config.dictConfig`
    :raises: :exc:`ValueError` if either the ``force_formatter`` or
        :envvar:`LOG_FORMAT` refers to an unknown formatter

    """
    config = copy.deepcopy(CONFIGURATION_DEFAULTS)
    config['handlers']['console']['formatter'] = 'json'
    _update_configuration(config, **kwargs)

    return config


def get_cli_configuration(**kwargs):
    """Retrieve configuration suitable for a command-line application.

    :param bool force_debug: should the root log level be
        ``logging.DEBUG``?
    :param str force_formatter: optional formatter to use

    The default configuration for a "command-line applicatoin" is
    to emit human-readable log lines and to only emit records at the
    info, warning, and error levels.  If the `force_debug`
    parameter is specified and *truthy*, then debug-level records
    are also emitted.

    :returns: :class:`dict` instance suitable for passing to
        :func:`logging.config.dictConfig`
    :raises: :exc:`ValueError` if either the ``force_formatter`` or
        :envvar:`LOG_FORMAT` refers to an unknown formatter

    """
    config = copy.deepcopy(CONFIGURATION_DEFAULTS)
    config['handlers']['console']['formatter'] = 'plain'
    _update_configuration(config, **kwargs)

    return config


def _update_configuration(config, **kwargs):
    """Update the configuration based on the environment."""
    debug = kwargs.get('force_debug', False)
    if not debug:
        try:
            debug = utils.parse_boolean(os.environ.get('DEBUG', None))
        except ValueError:
            pass  # ignored since we don't "own" $DEBUG

    if debug:
        config['root']['level'] = 'DEBUG'

    selected_format = kwargs.get('force_format',
                                 os.environ.get('LOG_FORMAT', None))
    if selected_format:
        if selected_format in config['formatters']:
            config['handlers']['console']['formatter'] = selected_format
        else:
            raise ValueError(
                'invalid LOG_FORMAT value %r is not in %r' %
                (selected_format, list(config['formatters'].keys())))
