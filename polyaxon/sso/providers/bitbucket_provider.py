import requests

from django.conf import settings

from event_manager.events.user import USER_BITBUCKET
from constants.sso_providers import Providers
from sso.providers.oauth2.provider import OAuth2Provider


class BitbucketIdentityProvider(OAuth2Provider):
    key = 'bitbucket'
    name = 'Bitbucket'
    event_type = USER_BITBUCKET

    web_url = 'https://bitbucket.org'
    api_url = 'https://api.bitbucket.org'
    oauth_access_token_url = '{}/site/oauth2/access_token'.format(web_url)
    oauth_authorize_url = '{}/site/oauth2/authorize'.format(web_url)
    user_url = '{}/2.0/user'.format(api_url)
    emails_url = '{}/emails'.format(user_url)

    oauth_scopes = ()

    def get_oauth_client_id(self):
        return settings.OAUTH_PROVIDERS.BITBUCKET.CLIENT_ID

    def get_oauth_client_secret(self):
        return settings.OAUTH_PROVIDERS.BITBUCKET.CLIENT_SECRET

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
        emails = emails['values'] if emails else []
        email = [e for e in emails if e['is_primary']]
        return email[0]['email'] if email else '{}@{}'.format(username,
                                                              settings.DEFAULT_EMAIL_DOMAIN)

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
        first_name, last_name = self.get_first_last_names(username=username,
                                                          name=user['display_name'])
        email = self.get_email(access_token=access_token, username=username)

        return {
            'type': Providers.BITBUCKET,
            'id': user['uuid'],
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'scopes': [],
            'data': self.get_oauth_data(data),
        }
