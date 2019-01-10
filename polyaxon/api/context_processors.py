import conf


def sso_enabled(request):
    return {
        'sso_enabled': conf.get('SSO_ENABLED'),
        'sso_github': conf.get('OAUTH_GITHUB_ENABLED'),
        'sso_gitlab': conf.get('OAUTH_GITLAB_ENABLED'),
        'sso_bitbucket': conf.get('OAUTH_BITBUCKET_ENABLED'),
        'sso_azure': conf.get('OAUTH_AZURE_ENABLED'),
        'admin_view_enabled': conf.get('ADMIN_VIEW_ENABLED')
    }
