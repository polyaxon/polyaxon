from django.conf import settings


def sso_enabled(request):
    return {
        'sso_enabled': settings.OAUTH_PROVIDERS.SSO_ENABLED,
        'sso_github': settings.OAUTH_PROVIDERS.GITHUB.ENABLED,
        'sso_gitlab': settings.OAUTH_PROVIDERS.GITLAB.ENABLED,
        'sso_bitbucket': settings.OAUTH_PROVIDERS.BITBUCKET.ENABLED,
        'sso_azure': settings.OAUTH_PROVIDERS.AZURE.ENABLED,
        'admin_view_enabled': settings.ADMIN_VIEW_ENABLED
    }
