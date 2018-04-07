# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.auth import AuthClient
from polyaxon_schemas.authentication import CredentialsConfig
from polyaxon_schemas.user import UserConfig

faker = Faker()


class TestAuthClient(TestCase):

    def setUp(self):
        self.client = AuthClient(host='localhost',
                                 http_port=8000,
                                 ws_port=1337,
                                 version='v1',
                                 token=faker.uuid4(),
                                 reraise=True)

    @httpretty.activate
    def test_get_user(self):
        user = UserConfig('user', 'user@test.com').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            AuthClient._build_url(
                self.client.base_url,
                AuthClient.ENDPOINT),
            body=json.dumps(user),
            content_type='application/json', status=200)

        user_result = self.client.get_user('token_value')
        assert user == user_result.to_dict()

    @httpretty.activate
    def test_login(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            AuthClient._build_url(
                self.client.base_url,
                AuthClient.ENDPOINT,
                'token'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        credentials = CredentialsConfig('user', 'password')
        assert token == self.client.login(credentials=credentials)
