# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.schemas import (
    ChartVersionConfig,
    CliVersionConfig,
    LibVersionConfig,
    LogHandlerConfig,
    PlatformVersionConfig
)


class VersionApi(BaseApiHandler):
    """
    Api handler to get API version from the server.
    """
    ENDPOINT = "/versions/"

    def get_cli_version(self):
        request_url = self.build_url(self._get_http_url(), 'cli')
        response = self.transport.get(request_url)
        return self.prepare_results(response_json=response.json(), config=CliVersionConfig)

    def get_platform_version(self):
        request_url = self.build_url(self._get_http_url(), 'platform')
        response = self.transport.get(request_url)
        return self.prepare_results(response_json=response.json(), config=PlatformVersionConfig)

    def get_lib_version(self):
        request_url = self.build_url(self._get_http_url(), 'lib')
        response = self.transport.get(request_url)
        return self.prepare_results(response_json=response.json(), config=LibVersionConfig)

    def get_chart_version(self):
        request_url = self.build_url(self._get_http_url(), 'chart')
        response = self.transport.get(request_url)
        return self.prepare_results(response_json=response.json(), config=ChartVersionConfig)

    def get_log_handler(self):
        request_url = self.build_url(self._get_http_url('/log_handler'))
        response = self.transport.get(request_url)
        return self.prepare_results(response_json=response.json(), config=LogHandlerConfig)
