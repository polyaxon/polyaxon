from hestia.auth import AuthenticationError, AuthenticationTypes
from rest_framework.authentication import BasicAuthentication


class PolyaxonAuthentication(BasicAuthentication):
    keyword = None

    def __init__(self):
        if self.keyword not in AuthenticationTypes.VALUES:
            raise AuthenticationError('Authentication bad configuration, '
                                      'the keyword `{}` is not supported.'.format(self.keyword))

    def authenticate_header(self, request):
        return self.keyword
