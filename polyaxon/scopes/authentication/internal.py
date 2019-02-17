from typing import Any, Optional, Tuple

from hestia.auth import AuthenticationTypes
from hestia.headers import get_header
from hestia.internal_services import InternalServices
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from django.http import HttpRequest

import conf

from scopes.authentication.base import PolyaxonAuthentication


class InternalUser(object):
    def __init__(self, service):
        if service not in InternalServices.VALUES:
            raise ValueError('Received a non recognized internal service.')
        self.username = 'internal_user'
        self.pk = -1
        self.id = -1
        self.is_internal = True
        self.is_anonymous = False
        self.is_authenticated = True
        self.is_staff = False
        self.is_superuser = False
        self.service = service

    @property
    def access_token(self) -> str:
        return conf.get('SECRET_INTERNAL_TOKEN')

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, InternalUser) and other.username == self.username


def is_internal_user(user: Any) -> bool:
    return hasattr(user, 'is_internal')


def is_authenticated_internal_user(user: Any) -> bool:
    if is_internal_user(user):
        return user.is_internal

    return False


def get_internal_header(request: HttpRequest) -> str:
    """
    Return request's 'X_POLYAXON_INTERNAL:' header, as a bytestring.
    """
    return get_header(request=request, header_service=conf.get('HEADERS_INTERNAL'))


class InternalAuthentication(PolyaxonAuthentication):
    """
    Simple authentication based on internal secret token.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "InternalToken ".  For example:

        Authorization: InternalToken 401f7ac837da42b97f613d789819ff93537bee6a

    As well as one of the supported internal service. For example:

        X_POLYAXON_INTERNAL: experiments
    """

    keyword = AuthenticationTypes.INTERNAL_TOKEN

    def authenticate(self, request: HttpRequest) -> Optional[Tuple['InternalUser', None]]:
        auth = get_authorization_header(request).split()
        internal_service = get_internal_header(request)

        try:
            internal_service = internal_service.decode()
        except UnicodeError:
            msg = ('Invalid internal_service header. '
                   'internal_service string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if internal_service not in InternalServices.VALUES:
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

        return self.authenticate_credentials(internal_service, token)

    def authenticate_credentials(self,  # pylint:disable=arguments-differ
                                 service: str,
                                 key: str) -> Optional[Tuple['InternalUser', None]]:
        internal_user = InternalUser(service=service)
        if internal_user.access_token != key:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return internal_user, None
