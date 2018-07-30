import requests

from django.conf import settings

from constants.sso_providers import Providers
from event_manager.events.user import USER_AZURE
from sso.providers.oauth2.provider import OAuth2Provider


class AzureIdentityProvider(OAuth2Provider):
    key = 'azure'
    name = 'Azure'
    event_type = USER_AZURE

    tenant_id = settings.OAUTH_PROVIDERS.AZURE.TENANT_ID
    web_url = 'https://login.microsoft.com/{}'.format(tenant_id)
    oauth_authorize_url = '{}/oauth2/authorize'.format(web_url)
    oauth_access_token_url = '{}/oauth2/token'.format(web_url)
    api_url = 'https://graph.microsoft.com/v1.0'
    resource = 'https://graph.microsoft.com'
    oauth_scopes = 'openid email profile'

    def get_oauth_scopes(self):
        return self.oauth_scopes

    def get_oauth_client_id(self):
        return settings.OAUTH_PROVIDERS.AZURE.CLIENT_ID

    def get_oauth_client_secret(self):
        return settings.OAUTH_PROVIDERS.AZURE.CLIENT_SECRET

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
