from time import time

from sso.providers.identity_provider import IdentityProvider
from sso.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView


class OAuth2Provider(IdentityProvider):
    """The `OAuth2Provider` provides a generic identity provider
    that uses the OAuth 2.0 protocol as a means for authenticating a user.

    OAuth scopes are configured through the oauth_scopes class property,
    however may be overriden using the ``config['oauth_scopes']`` object.
    """
    oauth_access_token_url = ''
    oauth_authorize_url = ''
    refresh_token_url = ''

    oauth_scopes = ()

    def get_oauth_client_id(self):
        raise NotImplementedError

    def get_oauth_client_secret(self):
        raise NotImplementedError

    def get_oauth_scopes(self):
        return self.config.get('oauth_scopes', self.oauth_scopes)

    def get_wizard_views(self):
        return [
            OAuth2LoginView(
                authorize_url=self.oauth_authorize_url,
                client_id=self.get_oauth_client_id(),
                scope=' '.join(self.get_oauth_scopes()),
            ),
            OAuth2CallbackView(
                access_token_url=self.oauth_access_token_url,
                client_id=self.get_oauth_client_id(),
                client_secret=self.get_oauth_client_secret(),
            ),
        ]

    @staticmethod
    def get_oauth_data(payload):
        data = {'access_token': payload['access_token']}

        if 'expires_in' in payload:
            data['expires_in'] = int(time()) + payload['expires_in']
        if 'refresh_token' in payload:
            data['refresh_token'] = payload['refresh_token']
        if 'token_type' in payload:
            data['token_type'] = payload['token_type']

        return data
