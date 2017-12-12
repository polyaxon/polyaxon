# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.version import CliVersionConfig, PlatformVersionConfig, LibVersionConfig, \
    ChartVersionConfig

from polyaxon_client.version import VersionClient

faker = Faker()


class TestVersionClient(TestCase):
    def setUp(self):
        self.client = VersionClient(host='localhost',
                                    http_port=8000,
                                    ws_port=1337,
                                    version='v1',
                                    token=faker.uuid4(),
                                    reraise=True)

    @httpretty.activate
    def test_get_cli_version(self):
        object = CliVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'cli'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_cli_version()
        assert object == result.to_dict()

    @httpretty.activate
    def test_get_platform_version(self):
        object = PlatformVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'platform'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_platform_version()
        assert object == result.to_dict()

    @httpretty.activate
    def test_get_lib_version(self):
        object = LibVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'lib'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_lib_version()
        assert object == result.to_dict()

    @httpretty.activate
    def test_get_lib_version(self):
        object = ChartVersionConfig(version='1.0').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'chart'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_chart_version()
        assert object == result.to_dict()
