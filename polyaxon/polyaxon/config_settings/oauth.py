from polyaxon.config_manager import config

OAUTH_GITHUB_VERIFICATION_SCHEDULE = config.get_int(
    'POLYAXON_AUTH_GITHUB_VERIFICATION_SCHEDULE',
    is_optional=True,
    default=0)
OAUTH_GITHUB_CLIENT_ID = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_ID',
                                           is_optional=True,
                                           is_secret=True)
OAUTH_GITHUB_CLIENT_SECRET = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_SECRET',
                                               is_optional=True,
                                               is_secret=True)
OAUTH_GITHUB_ENABLED = config.get_boolean('POLYAXON_AUTH_GITHUB',
                                          is_optional=True,
                                          default=False)

OAUTH_BITBUCKET_VERIFICATION_SCHEDULE = config.get_int(
    'POLYAXON_AUTH_BITBUCKET_VERIFICATION_SCHEDULE',
    is_optional=True,
    default=0)
OAUTH_BITBUCKET_CLIENT_ID = config.get_string('POLYAXON_AUTH_BITBUCKET_CLIENT_ID',
                                              is_optional=True,
                                              is_secret=True)
OAUTH_BITBUCKET_CLIENT_SECRET = config.get_string('POLYAXON_AUTH_BITBUCKET_CLIENT_SECRET',
                                                  is_optional=True,
                                                  is_secret=True)
OAUTH_BITBUCKET_ENABLED = config.get_boolean('POLYAXON_AUTH_BITBUCKET',
                                             is_optional=True,
                                             default=False)

OAUTH_GITLAB_VERIFICATION_SCHEDULE = config.get_int(
    'POLYAXON_AUTH_GITLAB_VERIFICATION_SCHEDULE',
    is_optional=True,
    default=0)
OAUTH_GITLAB_URL = config.get_string('POLYAXON_AUTH_GITLAB_URL',
                                     is_optional=True,
                                     is_secret=True)
OAUTH_GITLAB_CLIENT_ID = config.get_string('POLYAXON_AUTH_GITLAB_CLIENT_ID',
                                           is_optional=True,
                                           is_secret=True)
OAUTH_GITLAB_CLIENT_SECRET = config.get_string('POLYAXON_AUTH_GITLAB_CLIENT_SECRET',
                                               is_optional=True,
                                               is_secret=True)
OAUTH_GITLAB_ENABLED = config.get_boolean('POLYAXON_AUTH_GITLAB',
                                          is_optional=True,
                                          default=False)

OAUTH_AZURE_VERIFICATION_SCHEDULE = config.get_int(
    'POLYAXON_AUTH_AZURE_VERIFICATION_SCHEDULE',
    is_optional=True,
    default=0)
OAUTH_AZURE_TENANT_ID = config.get_string('POLYAXON_AUTH_AZURE_TENANT_ID',
                                          is_optional=True,
                                          is_secret=True)
OAUTH_AZURE_CLIENT_ID = config.get_string('POLYAXON_AUTH_AZURE_CLIENT_ID',
                                          is_optional=True,
                                          is_secret=True)
OAUTH_AZURE_CLIENT_SECRET = config.get_string('POLYAXON_AUTH_AZURE_CLIENT_SECRET',
                                              is_optional=True,
                                              is_secret=True)
OAUTH_AZURE_ENABLED = config.get_boolean('POLYAXON_AUTH_AZURE',
                                         is_optional=True,
                                         default=False)


SSO_ENABLED = any([OAUTH_GITHUB_ENABLED,
                   OAUTH_BITBUCKET_ENABLED,
                   OAUTH_GITLAB_ENABLED,
                   OAUTH_AZURE_ENABLED])
