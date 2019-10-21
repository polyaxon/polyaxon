from polyaxon.config_manager import config

THROTTLE_RATES_HIGH = config.get_int('POLYAXON_THROTTLE_RATES_HIGH',
                                     is_optional=True,
                                     default=120)
THROTTLE_RATES_INTERNAL = config.get_int('POLYAXON_THROTTLE_RATES_INTERNAL',
                                         is_optional=True,
                                         default=120)
THROTTLE_RATES_IMPERSONATE = config.get_int('POLYAXON_THROTTLE_RATES_IMPERSONATE',
                                            is_optional=True,
                                            default=120)
THROTTLE_RATES_USER = config.get_int('POLYAXON_THROTTLE_RATES_USER',
                                     is_optional=True,
                                     default=120)
THROTTLE_RATES_ADMIN = config.get_int('POLYAXON_THROTTLE_RATES_ADMIN',
                                      is_optional=True,
                                      default=100)
THROTTLE_RATES_ANON = config.get_int('POLYAXON_THROTTLE_RATES_ANON',
                                     is_optional=True,
                                     default=30)
THROTTLE_RATES_CHECKS = config.get_int('POLYAXON_THROTTLE_RATES_CHECKS',
                                       is_optional=True,
                                       default=10)


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'api.openapi.PolyaxonOpenAPISchema',
    'DEFAULT_RENDERER_CLASSES': (
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',  # Any other renders,
        'rest_framework.renderers.JSONRenderer',
    ),

    # 'DEFAULT_PARSER_CLASSES': (
    #     'djangorestframework_camel_case.parser.CamelCaseJSONParser',  # Any other parsers
    # ),

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),

    'DEFAULT_THROTTLE_RATES': {
        'high': '{}/second'.format(THROTTLE_RATES_HIGH),
        'internal': '{}/second'.format(THROTTLE_RATES_INTERNAL),
        'impersonate': '{}/second'.format(THROTTLE_RATES_IMPERSONATE),
        'ephemeral': '120/second',
        'user': '{}/min'.format(THROTTLE_RATES_USER),
        'admin': '{}/min'.format(THROTTLE_RATES_ADMIN),
        'anon': '{}/min'.format(THROTTLE_RATES_ANON),
        'health': '{}/min'.format(THROTTLE_RATES_CHECKS),
        'status': '{}/min'.format(THROTTLE_RATES_CHECKS),
    },

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'scopes.authentication.token.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
