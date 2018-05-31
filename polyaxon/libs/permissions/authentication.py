from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from django.conf import settings


class InternalUser(object):
    def __init__(self):
        self.username = 'internal_user'
        self.pk = -1
        self.id = -1
        self.is_internal = True
        self.is_authenticated = True
        self.is_staff = False

    @property
    def access_token(self):
        return settings.INTERNAL_SECRET_TOKEN

    def __eq__(self, other):
        return isinstance(other, InternalUser) and other.username == self.username


def is_internal_user(user):
    if hasattr(user, 'is_internal'):
        return user.is_internal

    return False


def get_internal_header(request):
    """Return request's 'X_POLYAXON_INTERNAL:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    service = request.META.get('HTTP_{}'.format(settings.HEADERS_INTERNAL), b'')
    if isinstance(service, str):
        # Work around django test client oddness
        service = service.encode(HTTP_HEADER_ENCODING)
    return service


class InternalAuthentication(BaseAuthentication):
    """Simple authentication based on internal secret token.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

    As well as one of the supported internal service. For example:

        X_POLYAXON_INTERNAL: experiments
    """

    keyword = 'InternalToken'
    model = None

    def get_model(self):
        return InternalUser()

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        internal_service = get_internal_header(request)

        try:
            internal_service = internal_service.decode()
        except UnicodeError:
            msg = ('Invalid internal_service header. '
                   'internal_service string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if internal_service not in settings.INTERNAL_SERVICES:
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
        internal_user = self.get_model()
        if internal_user.access_token != key:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return internal_user, None

    def authenticate_header(self, request):
        return self.keyword
