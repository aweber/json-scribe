import datetime
import json
import logging
import re
import traceback
import uuid

from jsonscribe import utils

_LOGGLY_KEY_PATTERN = re.compile('[-_ ]')


class JSONFormatter(logging.Formatter):
    """
    Format log records as JSON documents.

    :keyword list include_fields: fields from a :class:`~logging.LogRecord`
        that are included in the JSON bodies
    :keyword bool use_loggly_names: if specified and :data:`True`, then
        spaces, hyphens, and underscores are removed from field names.

    This class will format :class:`logging.LogRecord` instances into JSON
    bodies that are output as single lines by most :class:`logging.Handler`
    instances.  The result is your log messages collected together as a
    nice json-lines file.

    You have to set the list of fields to include in the JSON bodies during
    initialization.  If you are using the :func:`logging.config.dictConfig`
    function to configure the logging layer, then use the following syntax
    to configure the formatter factory with the fields that you want to
    include in the log messages::

        'formatters': {
            'json': {
                '()': 'jsonscribe.JSONFormatter',
                'include_fields': ['message']
            }
        }

    You can use any of the fields of :class:`~logging.LogRecord` and they
    will be included.  This includes fields that you add using either the
    ``extras`` keyword parameter or a :class:`logging.LoggerAdapter`.
    If you happen to reference a field that does not exist, then :data:`None`
    is used by default.  This avoids completely blowing up because when you
    make a mistake logging.

    A few fields have special handling applied to them.  The **exc_info**
    field is formatted as an array of strings instead of a blob of newline
    separated text.  Other fields are passed as-is to the JSON encoder with
    :meth:`._jsonify` used as the *default* keyword to the encoder.

    .. attribute:: json_encoder

       A single :class:`json.JSONEncoder` instance is used throughout
       the lifetime of the formatter instance.  You can modify it if
       necessary.

    .. note::

       The `use_loggly_names` parameter *SHOULD* be set to :data:`True`
       in the configuration if the logs are being sent to loggly.com.
       Failure to do this will result in some fields not being correctly
       indexed.

    """

    def __init__(self, *args, **kwargs):
        self.include_fields = kwargs.pop('include_fields', None) or []
        self.use_loggly_names = kwargs.pop('use_loggly_names', False)
        logging.Formatter.__init__(self, *args, **kwargs)
        self.json_encoder = json.JSONEncoder(
            ensure_ascii=True,
            indent=None,
            separators=(',', ':'),
            default=self._jsonify)
        self._format_exc = 'exc_info' in self.include_fields

    def format(self, record):
        """
        Format a log record to a JSON object.

        :param logging.LogRecord record: the record to format
        :return: the JSON formatted version of `record` as a string
        :rtype: str

        """
        record.message = record.getMessage()
        created = datetime.datetime.fromtimestamp(record.created, tz=utils.utc)
        record.asctime = created.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        data = {}
        for field in self.include_fields:
            if field != 'exc_info':
                data[field] = getattr(record, field, None)
        if self._format_exc:
            if record.exc_info:
                data['exc_info'] = traceback.format_exception(
                    record.exc_info[0], record.exc_info[1], record.exc_info[2])
            else:
                data['exc_info'] = None
        if self.use_loggly_names:
            translated = {}
            for k, v in data.items():
                translated[_LOGGLY_KEY_PATTERN.sub('', k)] = v
            data = translated
        return self.json_encoder.encode(data)

    def _jsonify(self, obj):
        """
        Provide formatting for common object types.

        :param obj: an object that the default :class:`json.JSONEncoder`
            cannot format
        :return: a *decent* :class:`str` representation of `obj`

        Unlike the standard JSON library, this hook **will not** raise
        an exception for an unserializable object.  It returns the objects
        ``repr`` instead.

        """
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return repr(obj)
