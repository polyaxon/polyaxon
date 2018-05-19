from django.conf import settings


def sso_enabled(request):
    return {
        'sso_enabled': settings.OAUTH_PROVIDERS.SSO_ENABLED,
        'sso_github': settings.OAUTH_PROVIDERS.GITHUB.IS_ACTIVE,
        'sso_gitlab': settings.OAUTH_PROVIDERS.GITLAB.IS_ACTIVE,
        'sso_bitbucket': settings.OAUTH_PROVIDERS.BITBUCKET.IS_ACTIVE,
    }
