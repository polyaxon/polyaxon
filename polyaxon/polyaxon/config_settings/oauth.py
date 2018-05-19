from polyaxon.utils import config


class OAUTH_PROVIDERS(object):
    class GITHUB(object):
        VERIFICATION_SCHEDULE = 0
        CLIENT_ID = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_ID',
                                      is_optional=True,
                                      is_secret=True)
        CLIENT_SECRET = config.get_string('POLYAXON_AUTH_GITHUB_CLIENT_SECRET',
                                          is_optional=True,
                                          is_secret=True)
        IS_ACTIVE = config.get_boolean('POLYAXON_AUTH_GITHUB',
                                       is_optional=True,
                                       default=False)

    class BITBUCKET(object):
        VERIFICATION_SCHEDULE = 0
        IS_ACTIVE = config.get_boolean('POLYAXON_AUTH_BITBUCKET',
                                       is_optional=True,
                                       default=False)

    class GITLAB(object):
        VERIFICATION_SCHEDULE = 0
        IS_ACTIVE = config.get_boolean('POLYAXON_AUTH_GITLAB',
                                       is_optional=True,
                                       default=False)

    SSO_ENABLED = any([GITHUB.IS_ACTIVE, BITBUCKET.IS_ACTIVE, GITLAB.IS_ACTIVE])
