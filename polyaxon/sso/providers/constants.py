from django.conf import settings


class PROVIDERS(object):
    GITHUB = 'github'
    BITBUCKET = 'bitbucket'
    GITLAB = 'gitlab'

    VALUES = {GITHUB, BITBUCKET, GITHUB}

    CHOICES = (
        (GITHUB, GITHUB),
        (BITBUCKET, BITBUCKET),
        (GITLAB, GITLAB),
    )

    VERIFICATION_SCHEDULES = {
        GITHUB: settings.OAUTH_PROVIDERS.GITHUB.VERIFICATION_SCHEDULE,
        BITBUCKET: settings.OAUTH_PROVIDERS.BITBUCKET.VERIFICATION_SCHEDULE,
        GITLAB: settings.OAUTH_PROVIDERS.GITLAB.VERIFICATION_SCHEDULE,
    }

    @classmethod
    def get_verification_schedule(cls, provider):
        assert provider in cls.VERIFICATION_SCHEDULES
        return cls.VERIFICATION_SCHEDULES[provider]
