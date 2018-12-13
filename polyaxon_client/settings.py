# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import rhea

from hestia.auth import AuthenticationTypes

TMP_AUTH_TOKEN_PATH = '/tmp/.polyaxon/.authtoken'
TMP_AUTH_GCS_ACCESS_PATH = '/tmp/.polyaxon/.gcsaccess.json'

config = rhea.Rhea.read_configs([
    os.environ,
    rhea.ConfigSpec(TMP_AUTH_TOKEN_PATH, config_type='.json', check_if_exists=False)
])

IN_CLUSTER = config.get_boolean('POLYAXON_IN_CLUSTER',
                                is_optional=True,
                                default=False)
API_HOST = config.get_string('POLYAXON_API_HOST',
                             is_optional=True)
HTTP_PORT = config.get_int('POLYAXON_HTTP_PORT',
                           is_optional=True)
WS_PORT = config.get_int('POLYAXON_WS_PORT',
                         is_optional=True)
USE_HTTPS = config.get_boolean('POLYAXON_USE_HTTPS',
                               is_optional=True,
                               default=False)
API_HTTP_HOST = config.get_string('POLYAXON_API_HTTP_HOST',
                                  is_optional=True)
API_WS_HOST = config.get_string('POLYAXON_API_WS_HOST',
                                is_optional=True)
SECRET_USER_TOKEN_KEY = 'POLYAXON_SECRET_USER_TOKEN'  # noqa
SECRET_USER_TOKEN = config.get_string('POLYAXON_SECRET_USER_TOKEN',
                                      is_optional=True)
SECRET_EPHEMERAL_TOKEN_KEY = 'POLYAXON_SECRET_EPHEMERAL_TOKEN'  # noqa
SECRET_EPHEMERAL_TOKEN = config.get_string(SECRET_EPHEMERAL_TOKEN_KEY,
                                           is_optional=True)
INTERNAL_TOKEN_KEY = 'POLYAXON_SECRET_INTERNAL_TOKEN'  # noqa
SECRET_INTERNAL_TOKEN = config.get_string(INTERNAL_TOKEN_KEY,
                                          is_optional=True)
AUTHENTICATION_TYPE = config.get_string('POLYAXON_AUTHENTICATION_TYPE',
                                        is_optional=True,
                                        default=AuthenticationTypes.TOKEN)
API_VERSION = config.get_string('POLYAXON_API_VERSION',
                                is_optional=True,
                                default='v1')
HASH_LENGTH = config.get_int('POLYAXON_HASH_LENGTH',
                             is_optional=True,
                             default=12)
INTERNAL_HEADER = config.get_string('POLYAXON_INTERNAL_HEADER',
                                    is_optional=True)
INTERNAL_HEADER_SERVICE = config.get_string('POLYAXON_INTERNAL_HEADER_SERVICE',
                                            is_optional=True)
SCHEMA_RESPONSE = config.get_boolean('POLYAXON_SCHEMA_RESPONSE',
                                     is_optional=True,
                                     default=False)
RUN_STORES_ACCESS_KEYS = config.get_dict('POLYAXON_RUN_STORES_ACCESS_KEYS',
                                         is_optional=True,
                                         default={})
INTERNAL_HEALTH_CHECK_URL = config.get_string('POLYAXON_INTERNAL_HEALTH_CHECK_URL',
                                              is_optional=True)

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
MIN_TIMEOUT = config.get_int('POLYAXON_MIN_TIMEOUT',
                             is_optional=True,
                             default=1)
TIMEOUT = config.get_int('POLYAXON_TIMEOUT',
                         is_optional=True,
                         default=20)
REQUEST_TIMEOUT = config.get_int('POLYAXON_REQUEST_TIMEOUT',
                                 is_optional=True,
                                 default=25)
LONG_REQUEST_TIMEOUT = config.get_int('POLYAXON_LONG_REQUEST_TIMEOUT',
                                      is_optional=True,
                                      default=3600)
INTERVAL = config.get_int('POLYAXON_INTERVAL',
                          is_optional=True,
                          default=1)
HEALTH_CHECK_INTERVAL = config.get_int('HEALTH_CHECK_INTERVAL',
                                       is_optional=True,
                                       default=60)
QUEUE_CALL = config.get_int('POLYAXON_INTERVAL',
                            is_optional=True,
                            default=200)
