from typing import Optional

import conf

from options.registry.auth_azure import AUTH_AZURE_VERIFICATION_SCHEDULE
from options.registry.auth_bitbucket import AUTH_BITBUCKET_VERIFICATION_SCHEDULE
from options.registry.auth_github import AUTH_GITHUB_VERIFICATION_SCHEDULE
from options.registry.auth_gitlab import AUTH_GITLAB_VERIFICATION_SCHEDULE


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
            return conf.get(AUTH_GITHUB_VERIFICATION_SCHEDULE)
        if provider == cls.BITBUCKET:
            return conf.get(AUTH_BITBUCKET_VERIFICATION_SCHEDULE)
        if provider == cls.GITLAB:
            return conf.get(AUTH_GITLAB_VERIFICATION_SCHEDULE)
        if provider == cls.AZURE:
            return conf.get(AUTH_AZURE_VERIFICATION_SCHEDULE)
