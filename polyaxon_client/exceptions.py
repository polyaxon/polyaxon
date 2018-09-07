# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class PolyaxonClientException(Exception):
    def __init__(self, message=None):
        Exception.__init__(self, message)
        self.message = message

    def __str__(self):
        return self.message


class PolyaxonShouldExitError(PolyaxonClientException):
    pass


class PolyaxonHTTPError(PolyaxonClientException):
    def __init__(self, endpoint, response, message=None, status_code=None):
        super(PolyaxonHTTPError, self).__init__()
        self.endpoint = endpoint
        self.response = response
        self.message = getattr(self, 'message', message)
        self.status_code = getattr(self, 'status_code', status_code)

    def __str__(self):
        return '{status_code} on {endpoint}.'.format(status_code=self.status_code,
                                                     endpoint=self.endpoint)


class BadRequestError(PolyaxonHTTPError):
    status_code = 400
    message = "One or more request parameters is incorrect"


class AuthenticationError(PolyaxonHTTPError):
    staticmethod = 401
    message = "Authentication failed. Retry by invoking Polyaxon login."


class AuthorizationError(PolyaxonHTTPError):
    status_code = 403
    message = "You are not authorized to access this resource on Polyaxon."


class NotFoundError(PolyaxonHTTPError):
    status_code = 404
    message = "The resource you are looking for was not found. Check if the name or id is correct."


class OverLimitError(PolyaxonHTTPError):
    status_code = 429
    message = "You are over the allowed limits for this operation. Consider upgrading your account."


class ServerError(PolyaxonHTTPError):
    status_code = 500
    message = "Internal polyaxon server error, please try again later."


class BadGatewayError(PolyaxonHTTPError):
    status_code = 502
    message = "Invalid response from Polyaxon server."


class ServiceUnavailableError(PolyaxonHTTPError):
    status_code = 503
    message = "A problem was encountered, please try again later."


class GatewayTimeoutError(PolyaxonHTTPError):
    status_code = 504
    message = "Polyaxon server took too long to respond."


class SSLHandshakeError(PolyaxonHTTPError):
    status_code = 525


ERRORS_MAPPING = {
    'base': PolyaxonClientException,
    'http': PolyaxonHTTPError,
    400: BadRequestError,
    401: AuthenticationError,
    403: AuthorizationError,
    404: NotFoundError,
    429: OverLimitError,
    500: ServerError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
    504: GatewayTimeoutError,
    525: SSLHandshakeError,
}
