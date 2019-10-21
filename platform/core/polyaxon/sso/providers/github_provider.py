import requests

import conf

from constants.sso_providers import Providers
from events.registry.user import USER_GITHUB
from options.registry.auth_github import AUTH_GITHUB_CLIENT_ID, AUTH_GITHUB_CLIENT_SECRET
from options.registry.email import EMAIL_DEFAULT_DOMAIN
from sso.providers.oauth2.provider import OAuth2Provider


class GitHubIdentityProvider(OAuth2Provider):
    key = 'github'
    name = 'Github'
    event_type = USER_GITHUB

    web_url = 'https://github.com'
    api_url = 'https://api.github.com'
    user_url = '{}/user'.format(api_url)
    emails_url = '{}/emails'.format(user_url)

    oauth_scopes = ('read:user', 'user:email')

    @property
    def oauth_authorize_url(self):
        return '{}/login/oauth/authorize'.format(self.web_url)

    @property
    def oauth_access_token_url(self):
        return '{}/login/oauth/access_token'.format(self.web_url)

    def get_oauth_client_id(self):
        return conf.get(AUTH_GITHUB_CLIENT_ID)

    def get_oauth_client_secret(self):
        return conf.get(AUTH_GITHUB_CLIENT_SECRET)

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
        return email[0]['email'] if email else '{}@{}'.format(username,
                                                              conf.get(EMAIL_DEFAULT_DOMAIN))

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
        username = user['login']
        first_name, last_name = self.get_first_last_names(username=username, name=user['name'])
        email = self.get_email(access_token=access_token, username=username)

        return {
            'type': Providers.GITHUB,
            'id': user['id'],
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'scopes': [],
            'data': self.get_oauth_data(data),
        }
