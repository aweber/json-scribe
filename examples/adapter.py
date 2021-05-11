"""
Example: using a logging context.

This example uses a instance-level dictionary to inject values into
log messages.  This is useful when you are writing code that processes
messages repeatedly (e.g., a poller or consumer) and each message has
it's own contextual identifier.  At the start of message processing,
you clear the context and store the contextual identifier that you want
to appear in each log message.  Use this in conjunction with the
:class:`jsonscribe.AttributeSetter` to ensure that the value is always
present and you can use it in logging format lines without exploding.

Note that this pattern can be used with or without the JSON formatter
since it is simply a usage of :class:`logging.LoggerAdapter`.

"""
import logging
import uuid

import jsonscribe


class Processor(object):
    def __init__(self):
        self.context = {}
        logger = logging.getLogger('adapter.Processor')
        self.logger = logging.LoggerAdapter(logger, self.context)

    def prepare(self, message):
        self.context.clear()
        self.context['correlation_id'] = message.get('correlation_id',
                                                     uuid.uuid4())

    def process(self, message):
        self.logger.info('processing %r', message['body'])


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('%(levelname)1.1s %(name)s: %(message)s'
                '\t{correlation_id=%(correlation_id)s}'))
    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]
    handler.addFilter(
        jsonscribe.AttributeSetter(
            add_fields={'correlation_id': 'ext://UUID'}))

    processor = Processor()
    for i in range(0, 10):
        msg = {
            'correlation_id': str(uuid.uuid4()),
            'body': [i for i in range(0, i)]
        }
        processor.prepare(msg)
        processor.process(msg)
