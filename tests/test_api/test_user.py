# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.user import UserApi


class TestUserApi(TestBaseApi):

    def setUp(self):
        super(TestUserApi, self).setUp()
        self.api_handler = UserApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_activate_user(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/users',
                'activate',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.api_handler.activate_user('test-username')
        assert response.status_code == 200

    @httpretty.activate
    def test_delete_user(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/users',
                'delete',
                'test-username'
            ),
            content_type='application/json',
            status=204)

        response = self.api_handler.delete_user('test-username')
        assert response.status_code == 204

    @httpretty.activate
    def test_grant_superuser(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/superusers',
                'grant',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.api_handler.grant_superuser('test-username')
        assert response.status_code == 200

    @httpretty.activate
    def test_revoke_superuser(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/superusers',
                'revoke',
                'test-username'
            ),
            content_type='application/json',
            status=200)

        response = self.api_handler.revoke_superuser('test-username')
        assert response.status_code == 200
