
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',  # Any other renders,
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
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
        'user': '120/min',
        'admin': '100/min',
        'anon': '30/min',
        'health': '10/min',
    },

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 30
}
