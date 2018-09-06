from corsheaders.defaults import default_headers

from polyaxon.config_manager import config

# session settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SSL_ENABLED = config.get_boolean('POLYAXON_SSL_ENABLED', is_optional=True, default=False)
CORS_ORIGIN_WHITELIST = config.get_list('POLYAXON_CORS_ORIGIN_WHITELIST',
                                        is_optional=True,
                                        default=[])

HEADERS_CLI_VERSION = 'X_POLYAXON_CLI_VERSION'
HEADERS_CLIENT_VERSION = 'X_POLYAXON_CLIENT_VERSION'
HEADERS_INTERNAL = 'X_POLYAXON_INTERNAL'

CORS_ALLOW_HEADERS = default_headers + (
    HEADERS_CLI_VERSION,
    HEADERS_CLIENT_VERSION,
    HEADERS_INTERNAL,
)

PROTOCOL = 'http'
if SSL_ENABLED:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    PROTOCOL = 'https'


class INTERNAL_SERVICES(object):  # noqa
    DOCKERIZER = 'dockerizer'
    HELPER = 'helper'
    TRACKER = 'tracker'

    VALUES = [
        DOCKERIZER,
        HELPER,
        TRACKER,
    ]
