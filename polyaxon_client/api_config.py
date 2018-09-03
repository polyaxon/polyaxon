# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings
from polyaxon_client.settings import AuthenticationTypes


class ApiConfig(object):
    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"
    BASE_WS_URL = "{}/ws/{}"

    def __init__(self,
                 host,
                 http_port,
                 ws_port,
                 token=None,
                 version='v1',
                 authentication_type=AuthenticationTypes.TOKEN,
                 reraise=False,
                 use_https=False,
                 in_cluster=False):
        if in_cluster:
            if not settings.API_HTTP_HOST:
                print('Could get api host info, '
                      'please make sure this is running inside a polyaxon job.')
            self.http_host = settings.API_HTTP_HOST
            self.ws_host = settings.API_WS_HOST
        else:
            http_protocol = 'https' if use_https else 'http'
            ws_protocol = 'wss' if use_https else 'ws'
            self.http_host = '{}://{}:{}'.format(http_protocol, host, http_port)
            self.ws_host = '{}://{}:{}'.format(ws_protocol, host, ws_port)
        self.base_url = self.BASE_URL.format(self.http_host, version)
        self.base_ws_url = self.BASE_WS_URL.format(self.ws_host, version)
        self.token = token
        self.authentication_type = authentication_type
        self.reraise = reraise
