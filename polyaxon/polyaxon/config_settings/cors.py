from corsheaders.defaults import default_headers

from polyaxon.utils import ROOT_DIR, config

# session settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SSL_ENABLED = config.get_boolean('POLYAXON_SSL_ENABLED', is_optional=True, default=False)
CORS_ORIGIN_WHITELIST = config.get_string('POLYAXON_CORS_ORIGIN_WHITELIST', is_optional=True)
if CORS_ORIGIN_WHITELIST:
    CORS_ORIGIN_WHITELIST = [i.strip() for i in CORS_ORIGIN_WHITELIST.split(',')]
else:
    CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_HEADERS = default_headers + (
    'x-polyaxon-cli-version',
    'x-polyaxon-client-version',
)

if SSL_ENABLED:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
