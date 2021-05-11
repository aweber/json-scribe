"""
Example of logging JSON lines.

This example uses :class:`jsonscribe.AttributeSetter` and
:class:`jsonscribe.JSONFormatter` to emit log lines as JSON objects.

"""
import logging

import jsonscribe


def failure():
    logger = logging.getLogger('simple.failure')
    try:
        raise RuntimeError('failed')
    except Exception:
        logger.exception('something failed')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]
    handler.addFilter(
        jsonscribe.AttributeSetter(
            add_fields={'correlation_id': 'ext://UUID'}))
    handler.setFormatter(
        jsonscribe.JSONFormatter(include_fields=[
            'name', 'levelname', 'asctime', 'message', 'module',
            'correlation_id', 'exc_info'
        ]))

    logger = logging.getLogger('simple')
    logger.info('hi there')
    failure()
