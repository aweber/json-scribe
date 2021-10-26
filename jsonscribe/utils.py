import datetime


class UTCZone(datetime.tzinfo):
    """
    Free-standing implementation of the UTC timezone.

    This is implemented to provide some compatibility with older
    Python versions.

    """

    def tzname(self, dt):  # pragma: no cover -- required
        return 'UTC'

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return None

    def fromutc(self, dt):
        return dt


utc = UTCZone()
"""
UTC timezone instance.

Use this with :meth:`datetime.datetime.now` to produce a timezone
aware UTC timestamp.

"""


def utcnow():
    """
    Get a timezone aware UTC now.

    :returns: a timezone aware version of :func:`datetime.datetime.utcnow`
    :rtype: datetime.datetime

    """
    return datetime.datetime.now(tz=utc)


def parse_boolean(s):
    """Parse a string as a boolean value.

    :returns: boolean value that `s` matches
    :raises: :exc:`ValueError` if `s` does not match a known value

    Acceptable values are 1, y, yes, t, or true for *truthiness* and
    0, n, no, f, or false for *falsiness*.

    """
    if isinstance(s, (int, float)):
        return bool(s)
    if s is None:
        return False

    try:
        value = s.strip().lower()
    except AttributeError:
        pass  # unexpected type, raise a ValueError
    else:
        if value in ('0', 'n', 'no', 'f', 'false'):
            return False
        if value in ('1', 'y', 'yes', 't', 'true'):
            return True

    raise ValueError('cannot determine Boolean value: %r' % (s, ))
