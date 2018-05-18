from polyaxon.utils import config


class OAUTH(object):
    class LDAP(object):
        VERIFICATION_SCHEDULE = 0

    class GITHUB(object):
        VERIFICATION_SCHEDULE = 0
        CLIENT_ID = config.get_string('POLYAXON_GITHUB_CLIENT_ID',
                                      is_optional=True,
                                      is_secret=True)
        CLIENT_SECRET = config.get_string('POLYAXON_GITHUB_CLIENT_SECRET',
                                          is_optional=True,
                                          is_secret=True)

    class BITBUCKET(object):
        VERIFICATION_SCHEDULE = 0

    class GITLAB(object):
        VERIFICATION_SCHEDULE = 0
