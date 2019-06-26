# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import rhea

from hestia.auth import AuthenticationTypes
from hestia.user_path import polyaxon_user_path
from marshmallow import EXCLUDE, RAISE
from rhea import RheaError  # noqa

TMP_POLYAXON_PATH = '/tmp/.polyaxon/'

TMP_AUTH_TOKEN_PATH = os.path.join(TMP_POLYAXON_PATH, '.authtoken')
CONTEXT_AUTH_TOKEN_PATH = '/plx-context/.authtoken'

TMP_CLIENT_CONFIG_PATH = os.path.join(TMP_POLYAXON_PATH, '.polyaxonclient')
TMP_CONFIG_PATH = os.path.join(TMP_POLYAXON_PATH, '.polyaxonconfig')
TMP_AUTH_PATH = os.path.join(TMP_POLYAXON_PATH, '.polyaxonauth')
USER_CLIENT_CONFIG_PATH = os.path.join(polyaxon_user_path(), '.polyaxonclient')
USER_CONFIG_PATH = os.path.join(polyaxon_user_path(), '.polyaxonconfig')
USER_AUTH_PATH = os.path.join(polyaxon_user_path(), '.polyaxonauth')

global_config = rhea.Rhea.read_configs([
    rhea.ConfigSpec(TMP_CONFIG_PATH, config_type='.json', check_if_exists=False),
    rhea.ConfigSpec(USER_CONFIG_PATH, config_type='.json', check_if_exists=False),
    {'dummy': 'dummy'}
])
auth_config = rhea.Rhea.read_configs([
    rhea.ConfigSpec(TMP_AUTH_PATH, config_type='.json', check_if_exists=False),
    rhea.ConfigSpec(USER_AUTH_PATH, config_type='.json', check_if_exists=False),
    {'dummy': 'dummy'}
])
config = rhea.Rhea.read_configs([
    rhea.ConfigSpec(TMP_CLIENT_CONFIG_PATH, config_type='.json', check_if_exists=False),
    rhea.ConfigSpec(USER_CLIENT_CONFIG_PATH, config_type='.json', check_if_exists=False),
    os.environ,
    rhea.ConfigSpec(TMP_AUTH_TOKEN_PATH, config_type='.json', check_if_exists=False),
    rhea.ConfigSpec(CONTEXT_AUTH_TOKEN_PATH, config_type='.json', check_if_exists=False)
])

IS_LOCAL = config.get_boolean('POLYAXON_IS_LOCAL',
                              is_optional=True,
                              default=False)
IN_CLUSTER = config.get_boolean('POLYAXON_IN_CLUSTER',
                                is_optional=True,
                                default=False)
IS_MANAGED = config.get_boolean('POLYAXON_IS_MANAGED',
                                is_optional=True,
                                default=False)
POLYAXON_NO_OP_KEY = 'POLYAXON_NO_OP'
NO_OP = config.get_boolean(POLYAXON_NO_OP_KEY,
                           is_optional=True,
                           default=False)
API_HOST = config.get_string('POLYAXON_API_HOST',
                             is_optional=True)
if not API_HOST:  # Check global config config
    API_HOST = global_config.get_string('host',
                                        is_optional=True)

HTTP_PORT = config.get_int('POLYAXON_HTTP_PORT',
                           is_optional=True)
if not HTTP_PORT:  # Check global config config
    HTTP_PORT = global_config.get_int('port',
                                      is_optional=True)
WS_PORT = config.get_int('POLYAXON_WS_PORT',
                         is_optional=True)
if not WS_PORT:  # Check global config config
    WS_PORT = global_config.get_int('ws_port',
                                    is_optional=True,
                                    default=HTTP_PORT)
USE_HTTPS = config.get_boolean('POLYAXON_USE_HTTPS',
                               is_optional=True)
if USE_HTTPS is None:  # Check global config config
    USE_HTTPS = global_config.get_boolean('use_https',
                                          is_optional=True,
                                          default=False)
VERIFY_SSL = config.get_boolean('POLYAXON_VERIFY_SSL',
                                is_optional=True)
if VERIFY_SSL is None:  # Check global config config
    try:
        VERIFY_SSL = global_config.get_boolean('verify_ssl',
                                               is_optional=True)
    except RheaError:
        VERIFY_SSL = False
API_HTTP_HOST = config.get_string('POLYAXON_API_HTTP_HOST',
                                  is_optional=True)
API_WS_HOST = config.get_string('POLYAXON_API_WS_HOST',
                                is_optional=True)
SECRET_USER_TOKEN_KEY = 'POLYAXON_SECRET_USER_TOKEN'  # noqa
SECRET_USER_TOKEN = config.get_string(SECRET_USER_TOKEN_KEY,
                                      is_optional=True)
if not SECRET_USER_TOKEN:  # Check global config
    SECRET_USER_TOKEN = auth_config.get_string('token',
                                               is_optional=True,
                                               is_secret=True,
                                               is_local=True)
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
INTERNAL_HEALTH_CHECK_URL = config.get_string('POLYAXON_INTERNAL_HEALTH_CHECK_URL',
                                              is_optional=True)
INTERNAL_RECONCILE_URL = config.get_string('POLYAXON_INTERNAL_RECONCILE_URL',
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
LOGS_LEVEL = config.get_int('POLYAXON_LOGS_LEVEL',
                            is_optional=True)
RECEPTION_UNKNOWN_BEHAVIOUR = config.get_string('POLYAXON_RECEPTION_UNKNOWN_BEHAVIOUR',
                                                is_optional=True,
                                                default=EXCLUDE)
VALIDATION_UNKNOWN_BEHAVIOUR = config.get_string('POLYAXON_VALIDATION_UNKNOWN_BEHAVIOUR',
                                                 is_optional=True,
                                                 default=RAISE)
WARN_UPLOAD_SIZE = config.get_int('POLYAXON_WARN_UPLOAD_SIZE',
                                  is_optional=True,
                                  default=1024 * 1024 * 10)
MAX_UPLOAD_SIZE = config.get_int('POLYAXON_MAX_UPLOAD_SIZE',
                                 is_optional=True,
                                 default=1024 * 1024 * 150)
