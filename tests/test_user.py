# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty

from faker import Faker
from unittest import TestCase

from polyaxon_client.user import UserClient

faker = Faker()


class TestUserClient(TestCase):
    def setUp(self):
        self.client = UserClient(host='localhost',
                                 http_port=8000,
                                 ws_port=1337,
                                 version='v1',
                                 token=faker.uuid4(),
                                 reraise=True)

    @httpretty.activate
    def test_activate_user(self):
        httpretty.register_uri(
            httpretty.POST,
            UserClient._build_url(
                self.client.base_url,
                UserClient.ENDPOINT,
                'activate',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.client.activate_user('test-username')
        assert response.status_code == 200

    @httpretty.activate
    def test_delete_user(self):
        httpretty.register_uri(
            httpretty.DELETE,
            UserClient._build_url(
                self.client.base_url,
                UserClient.ENDPOINT,
                'delete',
                'test-username'
            ),
            content_type='application/json',
            status=204)

        response = self.client.delete_user('test-username')
        assert response.status_code == 204

    @httpretty.activate
    def test_grant_superuser(self):
        httpretty.register_uri(
            httpretty.POST,
            UserClient._build_url(
                self.client.base_url,
                UserClient.ENDPOINT_SUPERUSERS,
                'grant',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.client.grant_superuser('test-username')
        assert response.status_code == 200

    @httpretty.activate
    def test_revoke_superuser(self):
        httpretty.register_uri(
            httpretty.POST,
            UserClient._build_url(
                self.client.base_url,
                UserClient.ENDPOINT_SUPERUSERS,
                'revoke',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.client.revoke_superuser('test-username')
        assert response.status_code == 200
