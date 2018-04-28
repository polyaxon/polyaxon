# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json

from faker import Faker
from unittest import TestCase

from polyaxon_client.version import VersionClient
from polyaxon_schemas.log_handler import LogHandlerConfig
from polyaxon_schemas.version import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    PlatformVersionConfig
)

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
        obj = CliVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'cli'),
            body=json.dumps(obj),
            content_type='application/json', status=200)
        result = self.client.get_cli_version()
        assert obj == result.to_dict()

    @httpretty.activate
    def test_get_platform_version(self):
        obj = PlatformVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'platform'),
            body=json.dumps(obj),
            content_type='application/json', status=200)
        result = self.client.get_platform_version()
        assert obj == result.to_dict()

    @httpretty.activate
    def test_get_lib_version(self):
        obj = LibVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'lib'),
            body=json.dumps(obj),
            content_type='application/json', status=200)
        result = self.client.get_lib_version()
        assert obj == result.to_dict()

    @httpretty.activate
    def test_get_chart_version(self):
        obj = ChartVersionConfig(version='1.0').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                VersionClient.ENDPOINT,
                'chart'),
            body=json.dumps(obj),
            content_type='application/json', status=200)
        result = self.client.get_chart_version()
        assert obj == result.to_dict()

    @httpretty.activate
    def test_get_log_handler(self):
        obj = LogHandlerConfig(
            dns='test',
            environment='staging',
            tags={
                'cli_min_version': '0.0.1',
                'cli_latest_version': '0.0.2',
                'platform_min_version': '0.0.1',
                'platform_latest_version': '0.0.1',
                'chart_version': '0.0.1'
            }
        ).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            VersionClient._build_url(
                self.client.base_url,
                '/log_handler'),
            body=json.dumps(obj),
            content_type='application/json', status=200)
        result = self.client.get_log_handler()
        assert obj == result.to_dict()
