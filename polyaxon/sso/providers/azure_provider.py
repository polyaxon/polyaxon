import requests

import conf

from constants.sso_providers import Providers
from events.registry.user import USER_AZURE
from options.registry.auth_azure import (
    AUTH_AZURE_CLIENT_ID,
    AUTH_AZURE_CLIENT_SECRET,
    AUTH_AZURE_TENANT_ID
)
from sso.providers.oauth2.provider import OAuth2Provider


class AzureIdentityProvider(OAuth2Provider):
    key = 'azure'
    name = 'Azure'
    event_type = USER_AZURE

    api_url = 'https://graph.microsoft.com/v1.0'
    resource = 'https://graph.microsoft.com'
    oauth_scopes = 'openid email profile'

    @property
    def tenant_id(self):
        return conf.get(AUTH_AZURE_TENANT_ID)

    @property
    def web_url(self):
        return 'https://login.microsoft.com/{}'.format(self.tenant_id)

    @property
    def oauth_authorize_url(self):
        return '{}/oauth2/authorize'.format(self.web_url)

    @property
    def oauth_access_token_url(self):
        return '{}/oauth2/token'.format(self.web_url)

    def get_oauth_scopes(self):
        return self.oauth_scopes

    def get_oauth_client_id(self):
        return conf.get(AUTH_AZURE_CLIENT_ID)

    def get_oauth_client_secret(self):
        return conf.get(AUTH_AZURE_CLIENT_SECRET)

    def get_username(self, upn):
        # userPrincipalName format is <alias>@<tenant>.com, we only want the alias
        return upn.split("@")[0]

    def build_identity(self, state_data):
        data = state_data['data']
        access_token = data['access_token']
        resp = requests.get('{}/me'.format(self.api_url),
                            headers={"Authorization": "Bearer {}".format(access_token)})
        resp.raise_for_status()
        user_info = resp.json()

        return {
            'type': Providers.AZURE,
            'id': user_info['id'],
            'email': user_info['mail'],
            'username': self.get_username(user_info['userPrincipalName']),
            'first_name': user_info['givenName'],
            'last_name': user_info['surname'],
            'scopes': [],
            'data': self.get_oauth_data(data),
        }
