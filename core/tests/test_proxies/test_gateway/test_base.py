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

from polyaxon import settings
from polyaxon.proxies.schemas.gateway import get_base_config


@pytest.mark.proxies_mark
class TestGatewayBase(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_gateway_base_config(self):
        expected = """
listen 80;


error_log /polyaxon/logs/error.log warn;


gzip                        on;
gzip_disable                "msie6";
gzip_types                  *;
gzip_proxied                any;


charset utf-8;


client_max_body_size        4G;
client_body_buffer_size     50m;
client_body_in_file_only clean;
sendfile on;


send_timeout 650;
keepalive_timeout 650;
uwsgi_read_timeout 650;
uwsgi_send_timeout 650;
client_header_timeout 650;
proxy_read_timeout 650;
keepalive_requests 10000;


error_page 500 502 503 504 /static/errors/50x.html;
error_page 401 403 /static/errors/permission.html;
error_page 404 /static/errors/404.html;


location = /favicon.ico {
    rewrite ^ /static/images/favicon.ico;
}


location /healthz/ {
    access_log off;
    return 200 "healthy";
}



location /streams/ {
    proxy_pass http://polyaxon-polyaxon-streams;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    proxy_pass http://plx-operation-$4.$1.svc.cluster.local;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.cluster.local;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location = / {
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /api/v1/ {
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /ui/ {
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /sso/ {
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /static/ {
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = False
        settings.PROXIES_CONFIG.dns_use_resolver = False
        assert get_base_config() == expected

    def test_gateway_base_config_with_auth_and_dns(self):
        expected = """
listen 80;


error_log /polyaxon/logs/error.log warn;


gzip                        on;
gzip_disable                "msie6";
gzip_types                  *;
gzip_proxied                any;


charset utf-8;


client_max_body_size        4G;
client_body_buffer_size     50m;
client_body_in_file_only clean;
sendfile on;


send_timeout 650;
keepalive_timeout 650;
uwsgi_read_timeout 650;
uwsgi_send_timeout 650;
client_header_timeout 650;
proxy_read_timeout 650;
keepalive_requests 10000;


error_page 500 502 503 504 /static/errors/50x.html;
error_page 401 403 /static/errors/permission.html;
error_page 404 /static/errors/404.html;


location = /favicon.ico {
    rewrite ^ /static/images/favicon.ico;
}


location /healthz/ {
    access_log off;
    return 200 "healthy";
}


location = /auth/v1/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Origin-URI $request_uri;
    proxy_set_header X-Origin-Method $request_method;
    internal;
}


location /streams/ {
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-streams;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://plx-operation-$4.$1.svc.cluster.local;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver coredns.kube-system.svc.cluster.local valid=5s;
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.cluster.local;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}


location = / {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /api/v1/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /ui/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /sso/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /static/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}


location /_admin/ {
    resolver coredns.kube-system.svc.cluster.local valid=5s;
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $http_host;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.ui_admin_enabled = True
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.auth_use_resolver = True
        settings.PROXIES_CONFIG.api_use_resolver = True
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_base_config() == expected
