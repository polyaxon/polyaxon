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

from typing import Any, Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse


def clean_verify_ssl(host: str, verify_ssl: bool = None):
    if verify_ssl is None and "https" in host:
        return True
    return verify_ssl


def clean_host(host: str):
    return host.rstrip("/")


def absolute_uri(url: str, api_host: str = None, protocol: str = None) -> Optional[str]:
    if not url:
        return None

    if not api_host:
        return url
    protocol = protocol or "http"

    url = urljoin(clean_host(api_host) + "/", url.lstrip("/"))
    return f"{protocol}://{url}"


def add_notification_referrer_param(
    url: str, provider: str, is_absolute: bool = True
) -> Optional[Any]:
    if not is_absolute:
        url = absolute_uri(url)
    if not url:
        return None
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    query["referrer"] = provider
    url_list = list(parsed_url)
    url_list[4] = urlencode(query, doseq=True)
    return urlunparse(url_list)
