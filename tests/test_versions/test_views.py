# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status

from api.urls import API_V1
from versions.models import CliVersion, PlatformVersion

from tests.utils import BaseViewTest


class TestCliVersionViewV1(BaseViewTest):
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.cli_version = CliVersion.load()
        self.platform_version = PlatformVersion.load()
        self.cli_url = '/{}/versions/cli'.format(API_V1)
        self.platform_url = '/{}/versions/platform'.format(API_V1)

    def test_get_cli_version(self):
        resp = self.auth_client.get(self.cli_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['min_version'] == self.cli_version.min_version
        assert resp.data['latest_version'] == self.cli_version.latest_version

    def test_get_platform_version(self):
        resp = self.auth_client.get(self.platform_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['min_version'] == self.platform_version.min_version
        assert resp.data['latest_version'] == self.platform_version.latest_version
