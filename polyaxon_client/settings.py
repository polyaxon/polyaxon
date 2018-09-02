import os


class AuthenticationTypes(object):
    TOKEN = 'Token'
    INTERNAL_TOKEN = 'Internaltoken'


IN_CLUSTER = os.getenv('POLYAXON_IN_CLUSTER', False)
API_HOST = os.getenv('POLYAXON_POLYAXON_API_HOST', None)
API_WS_HOST = os.getenv('POLYAXON_API_WS_HOST', None)
INTERNAL_SECRET_TOKEN = os.getenv('POLYAXON_INTERNAL_SECRET_TOKEN', None)
SECRET_TOKEN = os.getenv('POLYAXON_SECRET_TOKEN', None)
AUTHENTICATION_TYPE = os.getenv('POLYAXON_AUTHENTICATION_TYPE', AuthenticationTypes.TOKEN)
API_VERSION = os.getenv('POLYAXON_API_VERSION', 'v1')
