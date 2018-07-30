from polyaxon.config_manager import config

DEFAULT_FROM_EMAIL = config.get_string('POLYAXON_EMAIL_FROM',
                                       is_optional=True,
                                       default='polyaxon@localhost')
EMAIL_HOST = config.get_string('POLYAXON_EMAIL_HOST',
                               is_optional=True,
                               default='localhost')
EMAIL_PORT = config.get_int('POLYAXON_EMAIL_PORT',
                            is_optional=True,
                            default=25)
EMAIL_HOST_USER = config.get_string('POLYAXON_EMAIL_HOST_USER',
                                    is_optional=True,
                                    default='')
EMAIL_HOST_PASSWORD = config.get_string('POLYAXON_EMAIL_HOST_PASSWORD',
                                        is_optional=True,
                                        is_secret=True,
                                        default='')
EMAIL_SUBJECT_PREFIX = config.get_string('POLYAXON_EMAIL_SUBJECT_PREFIX',
                                         is_optional=True,
                                         default='[Polyaxon]')
EMAIL_USE_TLS = config.get_boolean('POLYAXON_EMAIL_USE_TLS',
                                   is_optional=True,
                                   default=False)
EMAIL_USE_SSL = config.get_boolean('POLYAXON_EMAIL_USE_SSL',
                                   is_optional=True,
                                   default=False)

if config.is_debug_mode or config.is_testing_env:
    EMAIL_BACKEND = config.get_string('POLYAXON_EMAIL_BACKEND',
                                      is_optional=True,
                                      default='django.core.mail.backends.console.EmailBackend')
