from typing import Optional, Tuple

from hestia.auth import AuthenticationTypes
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from django.http import HttpRequest

from db.models.tokens import Token
from scopes.authentication.base import PolyaxonAuthentication


class TokenAuthentication(PolyaxonAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = AuthenticationTypes.TOKEN

    def authenticate(self, request: HttpRequest) -> Optional[Tuple['User', 'Token']]:
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self,  # pylint:disable=arguments-differ
                                 key: str) -> Optional[Tuple['User', 'Token']]:
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.is_expired:
            raise AuthenticationFailed('Token expired')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return token.user, token
