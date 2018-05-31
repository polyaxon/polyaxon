import pytest

from rest_framework import status

from constants.urls import API_V1
from db.models.versions import ChartVersion, CliVersion, LibVersion, PlatformVersion
from polyaxon.utils import config
from tests.utils import BaseViewTest


@pytest.mark.versions_mark
class TestVersionViewsV1(BaseViewTest):
    HAS_AUTH = False

    def setUp(self):
        super().setUp()
        self.cli_version = CliVersion.load()
        self.platform_version = PlatformVersion.load()
        self.lib_version = LibVersion.load()
        self.chart_version = ChartVersion.load()
        self.cli_url = '/{}/versions/cli'.format(API_V1)
        self.platform_url = '/{}/versions/platform'.format(API_V1)
        self.lib_url = '/{}/versions/lib'.format(API_V1)
        self.chart_url = '/{}/versions/chart'.format(API_V1)
        self.log_handler_url = '/{}/log_handler'.format(API_V1)

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

    def test_get_lib_version(self):
        resp = self.auth_client.get(self.lib_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['min_version'] == self.lib_version.min_version
        assert resp.data['latest_version'] == self.lib_version.latest_version

    def test_get_chart_version(self):
        resp = self.auth_client.get(self.chart_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['version'] == self.chart_version.version

    def test_get_log_handler(self):
        resp = self.auth_client.get(self.log_handler_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['dns'] == config.cli_dns
        assert resp.data['environment'] == config.env
        assert resp.data['tags'] == {
            'chart_version': self.chart_version.version,
            'cli_min_version': self.cli_version.min_version,
            'cli_latest_version': self.cli_version.latest_version,
            'platform_min_version': self.platform_version.min_version,
            'platform_latest_version': self.platform_version.latest_version
        }
