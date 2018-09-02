# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import AuthenticationError, PolyaxonHTTPError
from polyaxon_client.schemas import CredentialsConfig, UserConfig
from polyaxon_client.settings import AuthenticationTypes


class AuthApi(BaseApiHandler):
    """
    Auth/User specific api handler.

    Special case client because of the token is not acquired yet,
    so we do not use shared client functions.
    """
    ENDPOINT = "/users"

    def get_user(self, token=None):
        token = token or self.transport.token
        request_url = self._get_http_url()
        response = self.transport.get(request_url,
                                      headers={"Authorization": "{} {}".format(
                                          self.config.authentication_type, token)})
        try:
            user_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code == 401:
                raise AuthenticationError(
                    request_url,
                    response,
                    "Invalid Token.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                    401)
            raise AuthenticationError(
                request_url,
                response,
                "Login failed.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                response.status_code)

        return UserConfig.from_dict(user_dict)

    def login(self, credentials):
        credentials = self.validate_config(config=credentials, config_schema=CredentialsConfig)
        request_url = self._build_url(self._get_http_url(), AuthenticationTypes.TOKEN)
        try:
            response = self.transport.session.post(request_url, data=credentials.to_dict())
        except requests.ConnectionError:
            raise PolyaxonHTTPError(
                request_url,
                None,
                "Connection error.",
                None)
        try:
            token_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code == 401:
                raise AuthenticationError(
                    request_url,
                    response,
                    "Invalid credentials.",
                    401)
            raise AuthenticationError(
                request_url,
                response,
                "Login failed.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                response.status_code)

        return token_dict.get(self.config.authentication_type)
