"""
Example of logging JSON lines with custom attributes.

This example uses :class:`jsonscribe.AttributeSetter` to create
custom attributes on log records and updates the configuration
to pass the new attribute along in the JSON log bodies.

"""
import logging.config

import jsonscribe


def failure():
    logger = logging.getLogger('simple.failure')
    try:
        raise RuntimeError('failed')
    except Exception:
        logger.exception('something failed')


if __name__ == '__main__':
    config = jsonscribe.get_service_configuration()
    config['filters']['attr-setter'] = {
        '()': 'jsonscribe.AttributeSetter',
        'add_fields': {
            'correlation_id': 'ext://UUID'
        }
    }
    config['formatters']['json']['include_fields'].append('correlation_id')
    config['handlers']['console']['filters'].append('attr-setter')

    logging.config.dictConfig(config)
    logger = logging.getLogger('simple')
    logger.info('hi there')
    failure()
