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

from polyaxon import settings


def get_dns_config(dns_prefix=None, dns_backend=None, dns_cluster=None):
    dns_prefix = dns_prefix or settings.PROXIES_CONFIG.dns_prefix
    dns_backend = dns_backend or settings.PROXIES_CONFIG.dns_backend
    dns_cluster = dns_cluster or settings.PROXIES_CONFIG.dns_custom_cluster
    if not dns_prefix:
        dns_prefix = "{}.kube-system".format(dns_backend)
    return "{dns_prefix}.svc.{dns_cluster}".format(
        dns_prefix=dns_prefix, dns_cluster=dns_cluster
    )


def get_resolver():
    if settings.PROXIES_CONFIG.dns_use_resolver:
        dns_config = get_dns_config()
        return "resolver {} valid=5s;".format(dns_config)
    return ""
