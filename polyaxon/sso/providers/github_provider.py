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
    emails_url = '{}/emails'.format(user_url)

    oauth_scopes = ('read:user', 'user:email')

    def get_oauth_client_id(self):
        return settings.OAUTH.GITHUB.CLIENT_ID

    def get_oauth_client_secret(self):
        return settings.OAUTH.GITHUB.CLIENT_SECRET

    def get_user(self, access_token):
        resp = requests.get(self.user_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_emails(self, access_token):
        resp = requests.get(self.emails_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_email(self, access_token, username):
        emails = self.get_emails(access_token=access_token)
        email = [e for e in emails if e['primary']]
        return email[0]['email'] if email else '{}@local.polyaxon.com'.format(username)

    @staticmethod
    def get_first_last_names(username, name):
        name = name or username
        name = name.split()
        if len(name) > 1:
            first = name[0]
            last = ' '.join(name[1:])
        else:
            first = name[0]
            last = ''
        return first, last

    def build_identity(self, data):
        data = data['data']
        access_token = data['access_token']
        user = self.get_user(access_token=access_token)
        username = user['login']
        first_name, last_name = self.get_first_last_names(username=username, name=user['name'])
        email = self.get_email(access_token=access_token, username=username)

        return {
            'type': PROVIDERS.GITHUB,
            'id': user['id'],
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'scopes': [],
            'data': self.get_oauth_data(data),
        }
