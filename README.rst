Write your logs as json-lines.

|build| |coverage| |docs| |source| |download| |license|

This library is the result of sending docker container logs to loggly.
Loggly works well with structured Syslog data but if you pass structured
Syslog lines to an aggregator as JSON you end up with an unindexed mess.
This library includes a few classes that make it easier and cleaner to send
log content as JSON objects on single lines *including exceptions*.

Usage
-----

Configuration
^^^^^^^^^^^^^

.. code-block:: json

   {
      "version": 1,
      "filters": {
         "defaultsetter": {
            "()": "jsonscribe.AttributeSetter",
            "add_fields": {
               "correlation_id": "ext://UUID"
            }
         }
      },
      "formatters": {
         "jsonlines": {
            "()": "jsonscribe.JSONFormatter",
            "include_fields": [
               "name",
               "levelname",
               "asctime",
               "message",
               "module",
               "correlation_id",
               "exc_info"
            ],
         }
      },
      "handlers": {
         "loggly": {
            "class": "logging.StreamHandler",
            "formatter": "jsonlines",
            "filters": ["defaultsetter"],
            "stream": "ext://sys.stdout"
         }
      },
      "loggers": {
         "somepackage": {
            "level": "DEBUG",
         }
      },
      "root": {
         "level": "INFO",
         "handlers": ["jsonlines"]
      }
   }

Logging
^^^^^^^
The following snippet is the simplest usage.  It is nothing more than the
textbook usage of the logging module.  It uses the logging configuration from
above and generates a JSON blob.

.. code-block:: python

   import logging.config
   import json

   if __name__ == '__main__':
      config = json.load(open('config.json'))
      logging.config.dictConfig(config)
      logger = logging.getLogger(__package__).getChild('main')
      logger.info('processing request')

The JSON message looks something like the following.  It is reformatted to
make it readable.  The default is to render it as compact JSON.

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
