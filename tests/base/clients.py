import datetime
import json
import uuid

from collections import Mapping
from urllib.parse import urlparse

from hestia.auth import AuthenticationTypes
from hestia.ephemeral_services import EphemeralServices
from hestia.internal_services import InternalServices

from django.test import Client
from django.test.client import FakePayload

import conf

from db.models.tokens import Token
from factories.factory_users import UserFactory

# pylint:disable=arguments-differ

# Stores the currently valid tokens to check against
_valid_tokens = dict()
CONTENT_TYPE_APPLICATION_JSON = 'application/json'


class BaseClient(Client):
    """Base client class."""

    def do_request(self,
                   method,
                   path,
                   data=None,
                   content_type=CONTENT_TYPE_APPLICATION_JSON,
                   **extra):
        if data is None:
            data = {}

        def validate_data(dvalues):
            if not isinstance(dvalues, Mapping):
                return
            for key, value in dvalues.items():
                # Fix UUIDs for convenience
                if isinstance(value, uuid.UUID):
                    dvalues[key] = value.hex

                # Fix datetimes
                if isinstance(value, datetime.datetime):
                    dvalues[key] = value.strftime('%Y-%m-%d %H:%M')

        if isinstance(data, list):
            for d in data:
                validate_data(d)
        else:
            validate_data(data)

        if content_type == CONTENT_TYPE_APPLICATION_JSON:
            data = json.dumps(data)

        request = self.encode_data(method, path, data, content_type, **extra)
        return self.request(**request)

    def put(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a PUT request."""
        return self.do_request('PUT', path, data, content_type, **extra)

    def patch(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a PATCH request."""
        return self.do_request('PATCH', path, data, content_type, **extra)

    def post(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a PATCH request."""
        return self.do_request('POST', path, data, content_type, **extra)

    def delete(self, path, data=None, content_type=CONTENT_TYPE_APPLICATION_JSON, **extra):
        """Construct a DELETE request."""
        return self.do_request('DELETE', path, data, content_type, **extra)

    def encode_data(self, http_method, path, data, content_type, **extra):
        patch_data = self._encode_data(data, content_type)

        parsed = urlparse(path)
        request = {
            'CONTENT_LENGTH': len(patch_data),
            'CONTENT_TYPE': content_type,
            'PATH_INFO': self._get_path(parsed),
            'QUERY_STRING': parsed[4],
            'REQUEST_METHOD': http_method,
            'wsgi.input': FakePayload(patch_data),
        }
        request.update(extra)

        return request


class EphemeralClient(BaseClient):
    def __init__(self,
                 token,
                 authentication_type=AuthenticationTypes.EPHEMERAL_TOKEN,
                 service=None,
                 **defaults):
        super().__init__(**defaults)
        self.service = service or EphemeralServices.RUNNER
        self.authorization_header = '{} {}'.format(authentication_type, token)

    def request(self, **request):
        updated_request = {
            'HTTP_AUTHORIZATION': self.authorization_header,
            'HTTP_X_POLYAXON_INTERNAL': self.service,
        }
        if 'HTTP_X_REQUEST_ID' not in request:
            request['HTTP_X_REQUEST_ID'] = str(uuid.uuid4())

        updated_request.update(request)
        return super().request(**updated_request)


class InternalClient(BaseClient):
    def __init__(self,
                 authentication_type=AuthenticationTypes.INTERNAL_TOKEN,
                 service=None,
                 **defaults):
        super().__init__(**defaults)
        self.service = service or InternalServices.HELPER
        self.authorization_header = '{} {}'.format(authentication_type,
                                                   conf.get('SECRET_INTERNAL_TOKEN'))

    def request(self, **request):
        updated_request = {
            'HTTP_AUTHORIZATION': self.authorization_header,
            'HTTP_X_POLYAXON_INTERNAL': self.service,
        }
        if 'HTTP_X_REQUEST_ID' not in request:
            request['HTTP_X_REQUEST_ID'] = str(uuid.uuid4())

        updated_request.update(request)
        return super().request(**updated_request)


class AuthorizedClient(BaseClient):
    """Class to instantiate an authorized client.

    This is allowed to make calls to the authenticated endpoints.
    """

    def __init__(self,
                 access_token='',
                 authentication_type=AuthenticationTypes.TOKEN,
                 **defaults):
        super().__init__(**defaults)
        user = defaults.get('user', UserFactory())
        self.login_user(user, access_token, authentication_type)

    def login_user(self, user, access_token='', authentication_type=AuthenticationTypes.TOKEN):
        self.user = user
        self.expires = datetime.datetime.now() + datetime.timedelta(days=1)
        if not access_token:
            token, _ = Token.objects.get_or_create(user=self.user)
            self.access_token = token.key
        else:
            self.access_token = access_token

        if self.user and self.access_token:
            self.patch_validate_token()

        self.authorization_header = '{} {}'.format(authentication_type, self.access_token)

    def patch_validate_token(self,
                             username=None,
                             access_token=None,
                             feature_flags=None,
                             status_code=200):
        # Use the objects user and access_token if none provided
        if username is None:
            username = self.user.username
        if access_token is None:
            access_token = self.access_token

        # Put the current access_token into the dict of valid ones
        _valid_tokens[access_token] = dict(
            username=username,
            feature_flags=feature_flags,
            status_dode=status_code
        )

    def _invalidate_token(self):
        # Remove the current access_token
        del _valid_tokens[self.access_token]

    def request(self, **request):
        updated_request = {'HTTP_AUTHORIZATION': self.authorization_header}
        if 'HTTP_X_REQUEST_ID' not in request:
            request['HTTP_X_REQUEST_ID'] = str(uuid.uuid4())

        updated_request.update(request)
        return super().request(**updated_request)
