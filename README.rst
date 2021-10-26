Write your logs as json-lines.

|build| |coverage| |docs| |source| |download| |license| |coc|

This library is the result of sending docker container logs to loggly.
Loggly works well with structured Syslog data but if you pass structured
Syslog lines to an aggregator as JSON you end up with an unindexed mess.
This library includes a few classes that make it easier and cleaner to send
log content as JSON objects on single lines *including exceptions*.

Usage
-----

Configuration
^^^^^^^^^^^^^
The expectation is that you are using the ``logging.config.dictConfig`` function
somewhere to configure the Python logging module.  This library exposes two functions
that return configuration dictionaries appropriate to services and command-line
applications:

:get_cli_configuration:
    Returns a configuration that generates human-readable logs

:get_service_configuration:
    Returns a configuration that generates machine-readable logs

Logging
^^^^^^^
The following snippet is the simplest usage.  It is nothing more than the
textbook usage of the logging module.  It uses the logging configuration for
a service and generates a JSON blob.

.. code-block:: python

   import logging.config

   import jsonscribe

   if __name__ == '__main__':
      logging.config.dictConfig(jsonscribe.get_service_configuration())
      logger = logging.getLogger(__package__).getChild('main')
      logger.info('processing request')

The JSON message looks something like the following (reformatted to
make it readable).  The default is to render it as compact JSON.

.. code-block:: json

   {
      "name": "somepackage.main",
      "levelname": "INFO",
      "asctime": "2018-08-09T07:44:54.231",
      "module": "somepackage.entrypoints",
      "correlation_id": "33CA3FB3-D66F-4D32-83A5-D5A8C3D92A6E",
      "message": "processing request",
      "exc_info": null
   }


.. _aweber/json-scribe: https://github.com/aweber/json-scribe
.. _pypi.org: https://pypi.org/project/json-scribe
.. |build| image:: https://img.shields.io/github/workflow/status/aweber/json-scribe/Testing/main?style=social
   :target: https://github.com/aweber/json-scribe/actions/workflows/testing.yml
.. |coc| image:: https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg?style=social
   :target: CODE_OF_CONDUCT.md
.. |coverage| image:: https://img.shields.io/codecov/c/github/aweber/json-scribe?style=social
   :target: https://app.codecov.io/gh/aweber/json-scribe
.. |docs| image:: https://img.shields.io/readthedocs/json-scribe.svg?style=social
   :target: https://json-scribe.readthedocs.io/en/latest/?badge=latest
.. |download| image:: https://img.shields.io/pypi/pyversions/json-scribe.svg?style=social
   :target: https://pypi.org/project/json-scribe/
.. |license| image:: https://img.shields.io/pypi/l/json-scribe.svg?style=social
   :target: https://github.com/aweber/json-scribe/blob/main/LICENSE
.. |source| image:: https://img.shields.io/badge/source-github.com-green.svg?style=social
   :target: https://github.com/aweber/json-scribe
