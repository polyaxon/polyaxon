from rhea import RheaError
from rhea.specs import AuthSpec

from polyaxon.config_manager import config

REPOS_ACCESS_TOKEN_KEY = 'POLYAXON_REPOS_ACCESS_TOKEN'
try:
    REPOS_ACCESS_TOKEN = config.get_auth(REPOS_ACCESS_TOKEN_KEY,
                                         is_optional=True,
                                         is_secret=True)
except RheaError:
    access_token = config.get_string(REPOS_ACCESS_TOKEN_KEY,
                                     is_optional=True,
                                     is_secret=True)
    REPOS_ACCESS_TOKEN = AuthSpec('polyaxon', access_token)
