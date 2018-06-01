import requests

from django.conf import settings

from constants.sso_providers import Providers
from event_manager.events.user import USER_GITLAB
from sso.providers.oauth2.provider import OAuth2Provider


class GitLabIdentityProvider(OAuth2Provider):
    key = 'gitlab'
    name = 'Gitlab'
    event_type = USER_GITLAB

    web_url = settings.OAUTH_PROVIDERS.GITLAB.URL or 'https://gitlab.com'
    api_url = '{}/api/v3'.format(web_url)
    oauth_access_token_url = '{}/oauth/token'.format(web_url)
    oauth_authorize_url = '{}/oauth/authorize'.format(web_url)
    user_url = '{}/user'.format(api_url)

    oauth_scopes = ('read_user',)

    def get_oauth_client_id(self):
        return settings.OAUTH_PROVIDERS.GITLAB.CLIENT_ID

    def get_oauth_client_secret(self):
        return settings.OAUTH_PROVIDERS.GITLAB.CLIENT_SECRET

    def get_user(self, access_token):
        resp = requests.get(self.user_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_emails(self, access_token):
        resp = requests.get(self.emails_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_email(self, email, username):
        return email if email else '{}@{}'.format(username, settings.DEFAULT_EMAIL_DOMAIN)

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

    def build_identity(self, state_data):
        data = state_data['data']
        access_token = data['access_token']
        user = self.get_user(access_token=access_token)
        username = user['username']
        first_name, last_name = self.get_first_last_names(username=username, name=user.get('name'))
        email = self.get_email(user.get('email'), username=username)

        return {
            'type': Providers.GITLAB,
            'id': user['id'],
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'scopes': [],
            'data': self.get_oauth_data(data),
        }
