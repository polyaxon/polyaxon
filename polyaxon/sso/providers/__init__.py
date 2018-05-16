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
        LDAP: settings.VERIFICATION_SCHEDULES.LDA,
        GITHUB: settings.VERIFICATION_SCHEDULES.GITHUB,
        BITBUCKET: settings.VERIFICATION_SCHEDULES.BITBUCKET,
        GITLAB: settings.VERIFICATION_SCHEDULES.GITLAB,
    }

    @classmethod
    def get_verification_schedule(cls, provider):
        assert provider in cls.VERIFICATION_SCHEDULES
        return cls.VERIFICATION_SCHEDULES[provider]
