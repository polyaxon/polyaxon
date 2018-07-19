from django.conf import settings


class Providers(object):
    GITHUB = 'github'
    BITBUCKET = 'bitbucket'
    GITLAB = 'gitlab'
    AZURE = 'azure'

    VALUES = {GITHUB, BITBUCKET, GITLAB, AZURE}

    CHOICES = (
        (GITHUB, GITHUB),
        (BITBUCKET, BITBUCKET),
        (GITLAB, GITLAB),
        (AZURE, AZURE),
    )

    VERIFICATION_SCHEDULES = {
        GITHUB: settings.OAUTH_PROVIDERS.GITHUB.VERIFICATION_SCHEDULE,
        BITBUCKET: settings.OAUTH_PROVIDERS.BITBUCKET.VERIFICATION_SCHEDULE,
        GITLAB: settings.OAUTH_PROVIDERS.GITLAB.VERIFICATION_SCHEDULE,
        AZURE: settings.OAUTH_PROVIDERS.AZURE.VERIFICATION_SCHEDULE,
    }

    @classmethod
    def get_verification_schedule(cls, provider):
        assert provider in cls.VERIFICATION_SCHEDULES
        return cls.VERIFICATION_SCHEDULES[provider]
