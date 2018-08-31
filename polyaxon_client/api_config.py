# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class ApiConfig(object):
    PAGE_SIZE = 20
    BASE_URL = "{}/api/{}"
    BASE_WS_URL = "{}/ws/{}"
    MAX_UPLOAD_SIZE = 1024 * 1024 * 150
    TIME_OUT = 25

    def __init__(self,
                 host,
                 http_port,
                 ws_port,
                 token=None,
                 version='v1',
                 authentication_type='token',
                 reraise=False,
                 use_https=False):
        http_protocol = 'https' if use_https else 'http'
        ws_protocol = 'wss' if use_https else 'ws'
        self.http_host = '{}://{}:{}'.format(http_protocol, host, http_port)
        self.ws_host = '{}://{}:{}'.format(ws_protocol, host, ws_port)
        self.base_url = self.BASE_URL.format(self.http_host, version)
        self.base_ws_url = self.BASE_WS_URL.format(self.ws_host, version)
        self.token = token
        self.authentication_type = authentication_type
        self.reraise = reraise
