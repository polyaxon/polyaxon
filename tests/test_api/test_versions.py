# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.version import VersionApi
from polyaxon_client.schemas import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    LogHandlerConfig,
    PlatformVersionConfig
)


class TestVersionApi(TestBaseApi):

    def setUp(self):
        super(TestVersionApi, self).setUp()
        self.api_handler = VersionApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_cli_version(self):
        obj = CliVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/versions/',
                'cli'),
            body=json.dumps(obj),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_cli_version()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_cli_version()
        assert result == obj

    @httpretty.activate
    def test_get_platform_version(self):
        obj = PlatformVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/versions/',
                'platform'),
            body=json.dumps(obj),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_platform_version()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_platform_version()
        assert result == obj

    @httpretty.activate
    def test_get_lib_version(self):
        obj = LibVersionConfig(latest_version='1.0', min_version='0.5').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/versions/',
                'lib'),
            body=json.dumps(obj),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_lib_version()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_lib_version()
        assert result == obj

    @httpretty.activate
    def test_get_chart_version(self):
        obj = ChartVersionConfig(version='1.0').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/versions/',
                'chart'),
            body=json.dumps(obj),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_chart_version()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_chart_version()
        assert result == obj

    @httpretty.activate
    def test_get_log_handler(self):
        obj = LogHandlerConfig(
            dsn='test',
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
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/log_handler'),
            body=json.dumps(obj),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_log_handler()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_log_handler()
        assert result == obj
