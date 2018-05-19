from polyaxon.utils import config


class OAUTH_PROVIDERS(object):  # noqa
    class GITHUB(object):
        VERIFICATION_SCHEDULE = 0
        CLIENT_ID = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_ID',
                                      is_optional=True,
                                      is_secret=True)
        CLIENT_SECRET = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_SECRET',
                                          is_optional=True,
                                          is_secret=True)
        ENABLED = config.get_boolean('POLYAXON_AUTH_GITHUB',
                                     is_optional=True,
                                     default=False)

    class BITBUCKET(object):
        VERIFICATION_SCHEDULE = 0
        CLIENT_ID = config.get_string('POLYAXON_AUTH_BITBUCKET_CLIENT_ID',
                                      is_optional=True,
                                      is_secret=True)
        CLIENT_SECRET = config.get_string('POLYAXON_AUTH_BITBUCKET_CLIENT_SECRET',
                                          is_optional=True,
                                          is_secret=True)
        ENABLED = config.get_boolean('POLYAXON_AUTH_BITBUCKET',
                                     is_optional=True,
                                     default=False)

    class GITLAB(object):
        VERIFICATION_SCHEDULE = 0
        URL = config.get_string('POLYAXON_AUTH_GITLAB_URL',
                                is_optional=True,
                                is_secret=True)
        CLIENT_ID = config.get_string('POLYAXON_AUTH_GITLAB_CLIENT_ID',
                                      is_optional=True,
                                      is_secret=True)
        CLIENT_SECRET = config.get_string('POLYAXON_AUTH_GITLAB_CLIENT_SECRET',
                                          is_optional=True,
                                          is_secret=True)
        ENABLED = config.get_boolean('POLYAXON_AUTH_GITLAB',
                                     is_optional=True,
                                     default=False)

    SSO_ENABLED = any([GITHUB.ENABLED, BITBUCKET.ENABLED, GITLAB.ENABLED])
