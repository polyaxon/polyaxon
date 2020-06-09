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
from polyaxon.proxies.schemas.gateway.api import get_api_location_config
from polyaxon.proxies.schemas.gateway.auth import (
    get_auth_config,
    get_auth_location_config,
)
from polyaxon.proxies.schemas.gateway.dns import get_dns_config, get_resolver
from polyaxon.proxies.schemas.gateway.redirect import get_redirect_config
from polyaxon.proxies.schemas.gateway.services import (
    get_plugins_location_config,
    get_services_location_config,
)
from polyaxon.proxies.schemas.gateway.ssl import get_ssl_config
from polyaxon.proxies.schemas.gateway.streams import get_streams_location_config


@pytest.mark.proxies_mark
class TestGatewaySchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_ssl(self):
        expected = """
# SSL
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# modern configuration
ssl_protocols TLSv1.2;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256;
ssl_prefer_server_ciphers on;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s;
resolver_timeout 2s;

ssl_certificate      /etc/ssl/polyaxon/polyaxon.com.crt;
ssl_certificate_key  /etc/ssl/polyaxon/polyaxon.com.key;
"""  # noqa
        assert get_ssl_config() == expected

        expected = """
# SSL
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# modern configuration
ssl_protocols TLSv1.2;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256;
ssl_prefer_server_ciphers on;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s;
resolver_timeout 2s;

ssl_certificate      /foo/polyaxon.com.crt;
ssl_certificate_key  /foo/polyaxon.com.key;
"""  # noqa
        settings.PROXIES_CONFIG.ssl_path = "/foo"
        assert get_ssl_config() == expected

    def test_redirect_config(self):
        expected = """
server {
    listen 80;
    return 301 https://$host$request_uri;
}
"""  # noqa
        settings.PROXIES_CONFIG.ssl_enabled = False
        assert get_redirect_config() == ""
        settings.PROXIES_CONFIG.ssl_enabled = True
        assert get_redirect_config() == expected


@pytest.mark.proxies_mark
class TestGatewayServicesSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_service_dns_resolver(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        expected = """
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_use_resolver = False
        resolver = get_resolver()
        assert (
            get_services_location_config(resolver=resolver, auth="", rewrite=False)
            == expected
        )

        expected = """
location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.kube-system"
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=False
            )
            == expected
        )

    def test_services_dns_backend(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    resolver kube-dns.kube-system.svc.cluster.local valid=5s;
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "kube-dns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            get_services_location_config(resolver=resolver, auth="", rewrite=False)
            == expected
        )

        expected = """
location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.kube-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=False
            )
            == expected
        )

    def test_services_dns_prefix(self):
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=False
            )
            == expected
        )

        expected = """
location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.new-system.svc.new-dns valid=5s;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.new-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.new-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=False
            )
            == expected
        )


@pytest.mark.proxies_mark
class TestGatewayRewriteServicesSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_service_dns_resolver(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        expected = """
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_use_resolver = False
        resolver = get_resolver()
        assert (
            get_services_location_config(resolver=resolver, auth="", rewrite=True)
            == expected
        )

        expected = """
location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.kube-system"
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=True
            )
            == expected
        )

    def test_services_dns_backend(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    resolver kube-dns.kube-system.svc.cluster.local valid=5s;
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "kube-dns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            get_services_location_config(resolver=resolver, auth="", rewrite=True)
            == expected
        )

        expected = """
location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.kube-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=True
            )
            == expected
        )

    def test_services_dns_prefix(self):
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=True
            )
            == expected
        )

        expected = """
location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.new-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.new-dns;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.new-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.new-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            get_services_location_config(
                resolver=resolver, auth=get_auth_config(), rewrite=True
            )
            == expected
        )


@pytest.mark.proxies_mark
class TestGatewayPluginsSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_no_plugins(self):
        assert get_plugins_location_config(resolver="", auth="") == []

    def test_plugins(self):
        proxy_services = {"tensorboard": {"port": 6006}, "notebook": {"port": 8888}}
        assert (
            len(
                get_plugins_location_config(
                    resolver="", auth="", proxy_services=proxy_services
                )
            )
            == 2
        )

    def test_plugins_dns_resolver(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        proxy_services = {"tensorboard": {"port": 6006}, "notebook": {"port": 8888}}
        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_use_resolver = False
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver, auth="", proxy_services=proxy_services
                )
            )
            == expected
        )

        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.kube-system"
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver,
                    auth=get_auth_config(),
                    proxy_services=proxy_services,
                )
            )
            == expected
        )

    def test_plugins_dns_backend(self):
        proxy_services = {"tensorboard": {"port": 6006}, "notebook": {"port": 8888}}
        settings.PROXIES_CONFIG.auth_enabled = False
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    resolver kube-dns.kube-system.svc.cluster.local valid=5s;
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    resolver kube-dns.kube-system.svc.cluster.local valid=5s;
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "kube-dns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver, auth="", proxy_services=proxy_services
                )
            )
            == expected
        )

        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.kube-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.kube-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver,
                    auth=get_auth_config(),
                    proxy_services=proxy_services,
                )
            )
            == expected
        )

    def test_plugins_dns_prefix(self):
        proxy_services = {"tensorboard": {"port": 6006}, "notebook": {"port": 8888}}
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver coredns.kube-system.svc.cluster.local valid=5s;
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver coredns.kube-system.svc.cluster.local valid=5s;
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver,
                    auth=get_auth_config(),
                    proxy_services=proxy_services,
                )
            )
            == expected
        )

        expected = """
location ~ /tensorboard/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.new-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/tensorboard/proxy/([-_.:\w]+)/(.*) /tensorboard/proxy/$1/$2 break;
    proxy_pass http://$1:6006;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}


location ~ /notebook/proxy/([-_.:\w]+)/(.*) {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.new-system.svc.new-dns valid=5s;
    rewrite_log on;
    rewrite ^/notebook/proxy/([-_.:\w]+)/(.*) /notebook/proxy/$1/$2 break;
    proxy_pass http://$1:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.new-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.new-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            "\n".join(
                get_plugins_location_config(
                    resolver=resolver,
                    auth=get_auth_config(),
                    proxy_services=proxy_services,
                )
            )
            == expected
        )


@pytest.mark.proxies_mark
class TestGatewaySTreamsSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_streams_location_with_auth_config(self):
        expected = """
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
"""  # noqa

        assert get_streams_location_config(resolver="", auth="") == expected

        settings.PROXIES_CONFIG.streams_port = 8888
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.streams_host = "foo"
        expected = """
location /streams/ {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    
    proxy_pass http://foo:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        assert (
            get_streams_location_config(resolver="", auth=get_auth_config()) == expected
        )

    def test_streams_location_with_dns_prefix(self):
        settings.PROXIES_CONFIG.auth_enabled = False
        settings.PROXIES_CONFIG.dns_use_resolver = True
        expected = """
location /streams/ {
    
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
"""  # noqa
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()
        assert get_streams_location_config(resolver=resolver, auth="") == expected

        expected = """
location /streams/ {
    
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;

    resolver kube-dns.new-system.svc.new-dns valid=5s;
    proxy_pass http://polyaxon-polyaxon-streams;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.dns_prefix = "kube-dns.new-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "new-dns"
        assert get_dns_config() == "kube-dns.new-system.svc.new-dns"
        resolver = get_resolver()
        assert (
            get_streams_location_config(resolver=resolver, auth=get_auth_config())
            == expected
        )


@pytest.mark.proxies_mark
class TestGatewayApiSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_api_location_config(self):
        expected = """
location / {
    
    
    proxy_pass http://polyaxon-polyaxon-api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        assert get_api_location_config(resolver="") == expected

        settings.PROXIES_CONFIG.api_port = 8888
        settings.PROXIES_CONFIG.api_host = "foo"
        expected = """
location / {
    
    
    proxy_pass http://foo:8888;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}
"""  # noqa
        assert get_api_location_config(resolver="") == expected

    def test_auth_config(self):
        settings.PROXIES_CONFIG.auth_enabled = True
        expected = """
    auth_request     /auth/v1/;
    auth_request_set $auth_status $upstream_status;
"""  # noqa
        assert get_auth_config() == expected

        settings.PROXIES_CONFIG.auth_enabled = False
        assert get_auth_config() == ""

    def test_auth_location_config(self):
        settings.PROXIES_CONFIG.auth_use_resolver = False
        settings.PROXIES_CONFIG.dns_use_resolver = False
        settings.PROXIES_CONFIG.auth_enabled = True
        expected = """
location = /auth/v1/ {
    
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
"""  # noqa
        assert get_auth_location_config(resolver="") == expected

        # Use resolver but do not enable it for auth
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()

        expected = """
location = /auth/v1/ {
    
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
"""  # noqa
        assert get_auth_location_config(resolver=resolver) == expected

        # Enable resolver for auth
        settings.PROXIES_CONFIG.auth_use_resolver = True
        expected = """
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
"""  # noqa
        assert get_auth_location_config(resolver=resolver) == expected

    def test_external_auth_location_config(self):
        settings.PROXIES_CONFIG.auth_use_resolver = False
        settings.PROXIES_CONFIG.auth_enabled = True
        settings.PROXIES_CONFIG.auth_external = "https://cloud.polyaxon.com"
        expected = """
location = /auth/v1/ {
    
    proxy_pass https://cloud.polyaxon.com;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Origin-URI $request_uri;
    proxy_set_header X-Origin-Method $request_method;
    internal;
}
"""  # noqa
        assert get_auth_location_config(resolver="") == expected

        # Use resolver but do not enable it for auth
        settings.PROXIES_CONFIG.dns_use_resolver = True
        settings.PROXIES_CONFIG.dns_prefix = "coredns.kube-system"
        settings.PROXIES_CONFIG.dns_custom_cluster = "cluster.local"
        assert get_dns_config() == "coredns.kube-system.svc.cluster.local"
        resolver = get_resolver()

        expected = """
location = /auth/v1/ {
    
    proxy_pass https://cloud.polyaxon.com;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Origin-URI $request_uri;
    proxy_set_header X-Origin-Method $request_method;
    internal;
}
"""  # noqa
        assert get_auth_location_config(resolver=resolver) == expected
