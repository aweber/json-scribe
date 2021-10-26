from jsonscribe.config import get_cli_configuration, get_service_configuration
from jsonscribe.filters import AttributeSetter
from jsonscribe.formatters import JSONFormatter

version_info = (2, 0, 0)
version = '.'.join(str(c) for c in version_info)

__all__ = [
    'AttributeSetter',
    'JSONFormatter',
    'get_cli_configuration',
    'get_service_configuration',
    'version',
    'version_info',
]
