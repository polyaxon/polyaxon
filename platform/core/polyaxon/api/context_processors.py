import conf

from options.registry.auth_azure import AUTH_AZURE_ENABLED
from options.registry.auth_bitbucket import AUTH_BITBUCKET_ENABLED
from options.registry.auth_github import AUTH_GITHUB_ENABLED
from options.registry.auth_gitlab import AUTH_GITLAB_ENABLED
from options.registry.core import ADMIN_VIEW_ENABLED


def sso_enabled(request):
    sso_github = conf.get(AUTH_GITHUB_ENABLED)
    sso_gitlab = conf.get(AUTH_GITLAB_ENABLED)
    sso_bitbucket = conf.get(AUTH_BITBUCKET_ENABLED)
    sso_azure = conf.get(AUTH_AZURE_ENABLED)

    _sso_enabled = any([sso_github, sso_gitlab, sso_bitbucket, sso_azure])

    return {
        'sso_enabled': _sso_enabled,
        'sso_github': sso_github,
        'sso_gitlab': sso_gitlab,
        'sso_bitbucket': sso_bitbucket,
        'sso_azure': sso_azure,
        'admin_view_enabled': conf.get(ADMIN_VIEW_ENABLED)
    }
