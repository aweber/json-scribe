Developer Interface
===================

Logging configuration
---------------------
The ``jsonscribe.config`` module contains functions that generate sane :func:`logging.config.dictConfig`
values for difference scenarios.  Each of the configuration functions uses a template that you can modify before
calling the function (see :data:`~jsonscribe.config.CONFIGURATION_DEFAULTS`).  The configuration functions
also obey the following environment variables if they are present.

.. envvar:: DEBUG

   If this environment variable is set and it can be parsed as a boolean value and the result is *truthy*,
   then the root log level will be :data:`logging.DEBUG` instead of the default value.  See
   :func:`~jsonscribe.utils.parse_boolean` for the list of acceptable values.

.. envvar:: LOG_FORMAT

   If this environment variable is set, then it overrides the default formatter used by the configuration
   functions.  This can be useful if you want to run a service from a shell and want human-readable logs.

   .. warning::

      If ``LOG_FORMAT`` is set to a value that is not a configured formatter, then the configuration functions
      will raise a :exc:`ValueError`.

.. autofunction:: jsonscribe.config.get_service_configuration

.. autofunction:: jsonscribe.config.get_cli_configuration

.. autodata:: jsonscribe.config.CONFIGURATION_DEFAULTS
   :no-value:

Implementation classes
----------------------
.. autoclass:: jsonscribe.AttributeSetter
   :members:

.. autoclass:: jsonscribe.JSONFormatter
   :members:
   :private-members:

Helpers
-------
.. autofunction:: jsonscribe.utils.parse_boolean

.. autoclass:: jsonscribe.utils.UTCZone
   :members:

.. autodata:: jsonscribe.utils.utc
