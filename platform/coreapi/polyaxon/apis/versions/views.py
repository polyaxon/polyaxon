#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from rest_framework import status
from rest_framework.response import Response

from coredb.managers.dummy_key import get_dummy_key
from polyaxon.cli.session import get_compatibility
from polycommon import conf
from polycommon.apis.regex import INSTALLATION_KEY, NAME_KEY, VERSION_KEY
from polycommon.endpoints.base import BaseEndpoint, RetrieveEndpoint
from polycommon.options.registry.installation import (
    ORGANIZATION_KEY,
    PLATFORM_DIST,
    PLATFORM_VERSION,
)


class VersionsInstalledView(BaseEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        data = {
            "key": conf.get(ORGANIZATION_KEY) or get_dummy_key(),
            "version": conf.get(PLATFORM_VERSION),
            "dist": conf.get(PLATFORM_DIST),
        }
        return Response(data)


class VersionsCompatibilityView(BaseEndpoint, RetrieveEndpoint):
    ALLOWED_METHODS = ["GET"]
    CONTEXT_KEYS = (INSTALLATION_KEY, VERSION_KEY, NAME_KEY)

    def get(self, request, *args, **kwargs):
        compatibility = get_compatibility(
            key=self.installation,
            service=self.name,
            version=self.version,
            is_cli=False,
            set_config=False,
        )
        return Response(
            data=compatibility.to_dict() if compatibility else {},
            status=status.HTTP_200_OK,
        )
