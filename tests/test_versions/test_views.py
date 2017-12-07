# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status

from api.urls import API_V1
from versions.models import CliVersion

from tests.utils import BaseViewTest


class TestCliVersionViewV1(BaseViewTest):
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.object = CliVersion.load()
        self.url = '/{}/versions/cli'.format(API_V1)

    def test_get_cli_version(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['min_version'] == self.object.min_version
        assert resp.data['latest_version'] == self.object.latest_version
