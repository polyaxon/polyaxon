# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import requests

from hestia.auth import AuthenticationTypes

from polyaxon_client import settings
from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import AuthenticationError, PolyaxonHTTPError
from polyaxon_client.schemas import CredentialsConfig, UserConfig
from polyaxon_client.utils import create_polyaxon_tmp


class AuthApi(BaseApiHandler):
    """
    Auth/User specific api handler.

    Special case client because of the token is not acquired yet,
    so we do not use shared client functions.
    """
    ENDPOINT = "/users"

    def get_user(self, token=None):
        token = token or self.config.token
        request_url = self._get_http_url()
        response = self.transport.get(request_url,
                                      headers={"Authorization": "{} {}".format(
                                          self.config.authentication_type, token)})
        try:
            user_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code in [401, 403]:
                raise AuthenticationError(
                    request_url,
                    response,
                    "Invalid Token.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                    response.status_code)
            raise AuthenticationError(
                request_url,
                response,
                "Login failed.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                response.status_code)

        return self.prepare_results(response_json=user_dict, config=UserConfig)

    def _persist_token(self, token, token_path):
        create_polyaxon_tmp()
        with open(token_path, "w") as config_file:
            config_file.write(json.dumps({settings.SECRET_USER_TOKEN_KEY: token}))

    def _process_token(self,
                       request_url,
                       response,
                       set_token=True,
                       persist_token=False,
                       token_path=None):
        try:
            token_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code in [401, 403]:
                raise AuthenticationError(
                    request_url,
                    response,
                    "Invalid credentials.",
                    response.status_code)
            raise AuthenticationError(
                request_url,
                response,
                "Login failed.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                response.status_code)

        token = token_dict.get('token')
        if set_token:
            self.config.token = token
        if persist_token:
            self._persist_token(token, token_path)
        return token

    def login(self, credentials, set_token=False):
        credentials = self.validate_config(config=credentials, config_schema=CredentialsConfig)
        request_url = self.build_url(self._get_http_url(), 'token')
        try:
            response = self.transport.session.post(
                request_url,
                data=credentials.to_dict(unknown=settings.VALIDATION_UNKNOWN_BEHAVIOUR))
        except requests.ConnectionError:
            raise PolyaxonHTTPError(
                request_url,
                None,
                "Connection error.",
                None)
        return self._process_token(request_url=request_url, response=response, set_token=set_token)

    def login_experiment_ephemeral_token(self,
                                         username,
                                         project_name,
                                         experiment_id,
                                         ephemeral_token,
                                         set_token=True,
                                         persist_token=True):
        request_url = self.build_url(self._get_http_url('/'),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'ephemeraltoken')
        try:
            response = self.transport.post(
                request_url,
                headers={
                    'Authorization': '{} {}'.format(
                        AuthenticationTypes.EPHEMERAL_TOKEN, ephemeral_token)
                })
        except requests.ConnectionError:
            raise PolyaxonHTTPError(
                request_url,
                None,
                "Connection error.",
                None)
        token = self._process_token(request_url=request_url,
                                    response=response,
                                    set_token=set_token,
                                    persist_token=persist_token,
                                    token_path=settings.TMP_AUTH_TOKEN_PATH)
        # Destroy ephemeral token
        if os.environ.get(settings.SECRET_EPHEMERAL_TOKEN_KEY):
            del os.environ[settings.SECRET_EPHEMERAL_TOKEN_KEY]
        if hasattr(settings, 'SECRET_EPHEMERAL_TOKEN') and settings.SECRET_EPHEMERAL_TOKEN:
            del settings.SECRET_EPHEMERAL_TOKEN
        return token

    def _login_impersonate_token(self,
                                 request_url,
                                 internal_token,
                                 set_token=True,
                                 persist_token=True):
        try:
            response = self.transport.post(
                request_url,
                headers={
                    'Authorization': '{} {}'.format(
                        AuthenticationTypes.INTERNAL_TOKEN, internal_token)
                })
        except requests.ConnectionError:
            raise PolyaxonHTTPError(
                request_url,
                None,
                "Connection error.",
                None)
        token = self._process_token(request_url=request_url,
                                    response=response,
                                    set_token=set_token,
                                    persist_token=persist_token,
                                    token_path=settings.CONTEXT_AUTH_TOKEN_PATH)
        return token

    def login_experiment_impersonate_token(self,
                                           username,
                                           project_name,
                                           experiment_id,
                                           internal_token,
                                           set_token=True,
                                           persist_token=True):
        request_url = self.build_url(self._get_http_url('/'),
                                     username,
                                     project_name,
                                     'experiments',
                                     experiment_id,
                                     'imporsonatetoken')
        return self._login_impersonate_token(request_url=request_url,
                                             internal_token=internal_token,
                                             set_token=set_token,
                                             persist_token=persist_token)

    def login_job_impersonate_token(self,
                                    username,
                                    project_name,
                                    job_id,
                                    internal_token,
                                    set_token=True,
                                    persist_token=True):
        request_url = self.build_url(self._get_http_url('/'),
                                     username,
                                     project_name,
                                     'jobs',
                                     job_id,
                                     'imporsonatetoken')
        return self._login_impersonate_token(request_url=request_url,
                                             internal_token=internal_token,
                                             set_token=set_token,
                                             persist_token=persist_token)

    def login_notebook_impersonate_token(self,
                                         username,
                                         project_name,
                                         internal_token,
                                         set_token=True,
                                         persist_token=True):
        request_url = self.build_url(self._get_http_url('/'),
                                     username,
                                     project_name,
                                     'notebook',
                                     'imporsonatetoken')
        return self._login_impersonate_token(request_url=request_url,
                                             internal_token=internal_token,
                                             set_token=set_token,
                                             persist_token=persist_token)
