from typing import Optional

import conf


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

    @classmethod
    def get_verification_schedule(cls, provider: str) -> Optional[int]:
        assert provider in cls.VALUES
        if provider == cls.GITHUB:
            return conf.get('OAUTH_GITHUB_VERIFICATION_SCHEDULE')
        if provider == cls.BITBUCKET:
            return conf.get('OAUTH_BITBUCKET_VERIFICATION_SCHEDULE')
        if provider == cls.GITLAB:
            return conf.get('OAUTH_GITLAB_VERIFICATION_SCHEDULE')
        if provider == cls.AZURE:
            return conf.get('OAUTH_AZURE_VERIFICATION_SCHEDULE')
