import requests

import conf

from constants.sso_providers import Providers
from events.registry.user import USER_GITLAB
from options.registry.auth_gitlab import (
    AUTH_GITLAB_CLIENT_ID,
    AUTH_GITLAB_CLIENT_SECRET,
    AUTH_GITLAB_URL
)
from options.registry.email import EMAIL_DEFAULT_DOMAIN
from sso.providers.oauth2.provider import OAuth2Provider


class GitLabIdentityProvider(OAuth2Provider):
    key = 'gitlab'
    name = 'Gitlab'
    event_type = USER_GITLAB

    oauth_scopes = ('read_user',)

    @property
    def web_url(self):
        return conf.get(AUTH_GITLAB_URL) or 'https://gitlab.com'

    @property
    def api_url(self):
        return '{}/api/v3'.format(self.web_url)

    @property
    def user_url(self):
        return '{}/user'.format(self.api_url)

    @property
    def oauth_authorize_url(self):
        return '{}/oauth/authorize'.format(self.web_url)

    @property
    def oauth_access_token_url(self):
        return '{}/oauth/token'.format(self.web_url)

    def get_oauth_client_id(self):
        return conf.get(AUTH_GITLAB_CLIENT_ID)

    def get_oauth_client_secret(self):
        return conf.get(AUTH_GITLAB_CLIENT_SECRET)

    def get_user(self, access_token):
        resp = requests.get(self.user_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_emails(self, access_token):
        resp = requests.get(self.emails_url, params={'access_token': access_token})
        resp.raise_for_status()
        return resp.json()

    def get_email(self, email, username):
        return email if email else '{}@{}'.format(username, conf.get(EMAIL_DEFAULT_DOMAIN))

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
