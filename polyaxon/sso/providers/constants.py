from django.conf import settings


class PROVIDERS(object):
    LDAP = 'ldap'
    GITHUB = 'github'
    BITBUCKET = 'bitbucket'
    GITLAB = 'gitlab'

    VALUES = {LDAP, GITHUB, BITBUCKET, GITHUB}

    CHOICES = (
        (LDAP, LDAP),
        (GITHUB, GITHUB),
        (BITBUCKET, BITBUCKET),
        (GITLAB, GITLAB),
    )

    VERIFICATION_SCHEDULES = {
        LDAP: settings.OAUTH.LDAP.VERIFICATION_SCHEDULE,
        GITHUB: settings.OAUTH.GITHUB.VERIFICATION_SCHEDULE,
        BITBUCKET: settings.OAUTH.BITBUCKET.VERIFICATION_SCHEDULE,
        GITLAB: settings.OAUTH.GITLAB.VERIFICATION_SCHEDULE,
    }

    @classmethod
    def get_verification_schedule(cls, provider):
        assert provider in cls.VERIFICATION_SCHEDULES
        return cls.VERIFICATION_SCHEDULES[provider]
