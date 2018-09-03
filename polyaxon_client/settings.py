# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os


class AuthenticationTypes(object):
    TOKEN = 'Token'
    INTERNAL_TOKEN = 'Internaltoken'


IN_CLUSTER = os.getenv('POLYAXON_IN_CLUSTER', False)
API_HOST = os.getenv('POLYAXON_API_HOST', None)
HTTP_PORT = os.getenv('POLYAXON_HTTP_PORT', None)
WS_PORT = os.getenv('POLYAXON_WS_PORT', None)
USE_HTTPS = os.getenv('POLYAXON_USE_HTTPS', False)
API_HTTP_HOST = os.getenv('POLYAXON_API_HTTP_HOST', None)
API_WS_HOST = os.getenv('POLYAXON_API_WS_HOST', None)
INTERNAL_SECRET_TOKEN = os.getenv('POLYAXON_INTERNAL_SECRET_TOKEN', None)
SECRET_TOKEN = os.getenv('POLYAXON_SECRET_TOKEN', None)
AUTHENTICATION_TYPE = os.getenv('POLYAXON_AUTHENTICATION_TYPE', AuthenticationTypes.TOKEN)
API_VERSION = os.getenv('POLYAXON_API_VERSION', 'v1')
HASH_LENGTH = os.getenv('POLYAXON_HASH_LENGTH', 12)
INTERNAL_HEADER = os.getenv('POLYAXON_INTERNAL_HEADER', None)
INTERNAL_HEADER_VALUE = os.getenv('POLYAXON_INTERNAL_HEADER_VALUE', None)

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
