import requests

from django.conf import settings

from sso.providers.constants import PROVIDERS
from sso.providers.oauth2.provider import OAuth2Provider


class GitHubIdentityProvider(OAuth2Provider):
    key = 'github'
    name = 'GitHub'

    web_url = 'https://github.com'
    api_url = 'https://api.github.com'
    oauth_access_token_url = '{}/login/oauth/access_token'.format(web_url)
    oauth_authorize_url = '{}/login/oauth/authorize'.format(web_url)
    user_url = '{}/user'.format(api_url)

    oauth_scopes = ()

    def get_oauth_client_id(self):
        return settings.OAUTH.GITHUB.CLIENT_ID

    def get_oauth_client_secret(self):
        return settings.OAUTH.GITHUB.CLIENT_SECRET

    def get_user(self, access_token):
        resp = requests.get(self.user_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def build_identity(self, data):
        data = data['data']
        user = self.get_user(access_token=data['access_token'])

        return {
            'type': PROVIDERS.GITHUB,
            'id': user['id'],
            'email': user['email'],
            'scopes': [],  # GitHub apps do not have user scopes
            'data': self.get_oauth_data(data),
        }
