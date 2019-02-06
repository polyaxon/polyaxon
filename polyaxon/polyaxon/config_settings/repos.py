from polyaxon.config_manager import config

REPOS_ACCESS_TOKEN_KEY = 'POLYAXON_REPOS_ACCESS_TOKEN'
REPOS_ACCESS_TOKEN = config.get_auth(REPOS_ACCESS_TOKEN_KEY,
                                     is_optional=True,
                                     is_secret=True)
