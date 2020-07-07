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

from urllib.parse import urlparse


def get_service_url(host: str, port: int):
    if port == 80:
        return "http://{}".format(host)
    if port == 443:
        return "https://{}".format(host)
    return "http://{}:{}".format(host, port)


def has_https(url: str):
    return "https" in url


def get_ssl_server_name(url: str):
    if has_https(url):
        return "proxy_ssl_server_name on;"
    return ""


def get_header_host(url: str):
    if has_https(url):
        return "proxy_set_header Host {};".format(urlparse(url).netloc.split(":")[0])
    return "proxy_set_header Host $http_host;"
