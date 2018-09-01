# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.logger import logger
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
        request_url = self._build_url(self._get_http_url(), 'cli')
        response = self.transport.get(request_url)
        data_dict = response.json()
        logger.debug("CLI Version info :%s", data_dict)
        return CliVersionConfig.from_dict(data_dict)

    def get_platform_version(self):
        request_url = self._build_url(self._get_http_url(), 'platform')
        response = self.transport.get(request_url)
        data_dict = response.json()
        logger.debug("Platform Version info :%s", data_dict)
        return PlatformVersionConfig.from_dict(data_dict)

    def get_lib_version(self):
        request_url = self._build_url(self._get_http_url(), 'lib')
        response = self.transport.get(request_url)
        data_dict = response.json()
        logger.debug("Lib Version info :%s", data_dict)
        return LibVersionConfig.from_dict(data_dict)

    def get_chart_version(self):
        request_url = self._build_url(self._get_http_url(), 'chart')
        response = self.transport.get(request_url)
        data_dict = response.json()
        logger.debug("Lib Version info :%s", data_dict)
        return ChartVersionConfig.from_dict(data_dict)

    def get_log_handler(self):
        request_url = self._build_url(self._get_http_url('/log_handler'))
        response = self.transport.get(request_url)
        data_dict = response.json()
        logger.debug("Log handler info :%s", data_dict)
        return LogHandlerConfig.from_dict(data_dict)
