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


def _get_indent(indent):
    return (
        settings.PROXIES_CONFIG.nginx_indent_char
        * settings.PROXIES_CONFIG.nginx_indent_width
        * indent
    )


def get_config(options, indent=0, **kwargs):
    _options = options.format(**kwargs)
    config = []
    for p in _options.split("\n"):
        config.append("{}{}".format(_get_indent(indent), p))

    return clean_config(config)


def clean_config(config):
    return "\n".join(config).replace("    \n", "")
