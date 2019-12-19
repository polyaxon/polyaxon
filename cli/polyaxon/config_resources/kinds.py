#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from polyaxon_sdk import V1ConfigResourceKind


class ConfigResourceKind(V1ConfigResourceKind):
    VALUES = {
        V1ConfigResourceKind.SECRET,
        V1ConfigResourceKind.CONFIG_MAP,
        V1ConfigResourceKind.IMAGE_PULL_SECRET,
        V1ConfigResourceKind.SERVICE_ACCOUNT,
    }

    @classmethod
    def is_secret(cls, kind):
        return kind in cls.SECRET

    @classmethod
    def is_config_map(cls, kind):
        return kind == cls.CONFIG_MAP

    @classmethod
    def is_image_pull_secret(cls, kind):
        return kind == cls.IMAGE_PULL_SECRET

    @classmethod
    def is_service_account(cls, kind):
        return kind == cls.SERVICE_ACCOUNT
