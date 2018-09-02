# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.auth import AuthApi
from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.schemas import CredentialsConfig, UserConfig
from polyaxon_client.settings import AuthenticationTypes


class TestAuthApi(TestBaseApi):

    def setUp(self):
        super(TestAuthApi, self).setUp()
        self.api_handler = AuthApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_user(self):
        user = UserConfig('user', 'user@test.com').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/users'),
            body=json.dumps(user),
            content_type='application/json', status=200)

        user_result = self.api_handler.get_user('token_value')
        assert user == user_result.to_dict()

    @httpretty.activate
    def test_login(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/users',
                AuthenticationTypes.TOKEN
            ),
            body=json.dumps({AuthenticationTypes.TOKEN: token}),
            content_type='application/json', status=200)

        credentials = CredentialsConfig('user', 'password')
        assert token == self.api_handler.login(credentials=credentials)
