from jsonscribe.filters import AttributeSetter
from jsonscribe.formatters import JSONFormatter

version_info = (2, 0, 0)
version = '.'.join(str(c) for c in version_info)

__all__ = [
    'AttributeSetter',
    'JSONFormatter',
    'version',
    'version_info',
]
