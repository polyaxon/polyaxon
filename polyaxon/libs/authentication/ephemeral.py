import base64
import binascii

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from django.conf import settings

from libs.authentication.internal import get_internal_header
from libs.redis_db import RedisEphemeralTokens


class EphemeralUser(object):
    def __init__(self, scope):
        self.username = 'ephemeral_user'
        self.pk = -1
        self.id = -1
        self.is_ephemeral = True
        self.is_anonymous = False
        self.is_authenticated = True
        self.is_staff = False
        self.scope = scope

    @property
    def access_token(self):
        return None

    def __eq__(self, other):
        return isinstance(other, EphemeralUser) and other.username == self.username


def is_internal_user(user):
    if hasattr(user, 'is_ephemeral'):
        return user.is_ephemeral

    return False


class EphemeralAuthentication(BaseAuthentication):
    """Simple authentication based on ephemeral secret token.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "EphemeralToken ".  For example:

        Authorization: EphemeralToken 401f7ac837da42b97f613d789819ff93537bee6a:uuid[:resource:id]

    As well as one of the supported internal service. For example:

        X_POLYAXON_INTERNAL: experiments
    """

    keyword = 'EphemeralToken'
    model = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        internal_service = get_internal_header(request)

        try:
            internal_service = internal_service.decode()
        except UnicodeError:
            msg = ('Invalid internal_service header. '
                   'internal_service string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if internal_service not in settings.EPHEMERAL_SERVICES.VALUES:
            return None

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            auth_parts = base64.b64decode(key).decode('utf-8').split(RedisEphemeralTokens.SEPARATOR)
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = 'Invalid basic header. Credentials not correctly base64 encoded.'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth_parts) != 2:
            msg = 'Invalid token header. Token should contain token and uuid.'
            raise exceptions.AuthenticationFailed(msg)

        token = auth_parts[0]
        token_uuid = auth_parts[1]

        ephemeral_token = RedisEphemeralTokens(token_uuid)
        if not ephemeral_token:
            raise exceptions.AuthenticationFailed('Invalid token.')

        scope = ephemeral_token.scope
        if not ephemeral_token.check_token(token=token):
            ephemeral_token.clear()
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        return EphemeralUser(scope=scope), None

    def authenticate_header(self, request):
        return self.keyword
