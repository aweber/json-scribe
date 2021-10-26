"""Example of logging JSON lines."""
import logging.config

import jsonscribe


def failure():
    logger = logging.getLogger('simple.failure')
    try:
        raise RuntimeError('failed')
    except Exception:
        logger.exception('something failed')


if __name__ == '__main__':
    logging.config.dictConfig(jsonscribe.get_service_configuration())
    logger = logging.getLogger('simple')
    logger.info('hi there')
    failure()
