#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from tests.utils import BaseTestCase

from polyaxon.proxies.schemas.streams.base import get_base_config


@pytest.mark.proxies_mark
class TestStreamsBase(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_streams_base_config(self):
        expected = """
listen 80;


error_log /polyaxon/logs/error.log warn;


gzip                        on;
gzip_disable                "msie6";
gzip_types                  *;


charset utf-8;


client_max_body_size        4G;
client_body_buffer_size     50m;
client_body_in_file_only clean;
sendfile on;


send_timeout 600;
keepalive_timeout 600;
uwsgi_read_timeout 600;
uwsgi_send_timeout 600;
client_header_timeout 600;
proxy_read_timeout 600;


location / {
    proxy_pass http://polyaxon;
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
}


error_page 500 502 503 504 /50x.html;
error_page 401 403 /permission.html;
error_page 404 /404.html;


location /tmp/ {
    alias                     /tmp/;
    expires                   0;
    add_header                Cache-Control private;
    internal;
}


location /tmp/plx/archives/ {
    alias                     /tmp/plx/archives/;
    expires                   0;
    add_header                Cache-Control private;
    internal;
}
"""  # noqa
        assert get_base_config() == expected
