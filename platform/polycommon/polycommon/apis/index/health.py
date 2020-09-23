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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from coredb.managers.dummy_key import get_dummy_key
from polyaxon.cli.session import get_compatibility
from polyaxon.schemas.cli.cli_config import CliConfig
from polyaxon.services.headers import PolyaxonServices
from polyaxon.utils.tz_utils import now
from polycommon import conf, pkg
from polycommon.options.registry.installation import ORGANIZATION_KEY


class HealthRateThrottle(AnonRateThrottle):
    scope = "health"


class HealthView(APIView):
    authentication_classes = ()
    throttle_classes = (HealthRateThrottle,)
    HEALTH_FILE = "/tmp/.compatibility"

    def get_config(self):
        try:
            return CliConfig.read(self.HEALTH_FILE, config_type=".json")
        except:  # noqa
            return

    def get(self, request, *args, **kwargs):
        CliConfig.init_file(self.HEALTH_FILE)
        config = self.get_config()
        if config and config.should_check():
            config.version = pkg.VERSION
            key = conf.get(ORGANIZATION_KEY) or get_dummy_key()
            compatibility = get_compatibility(
                key=key,
                service=PolyaxonServices.PLATFORM,
                version=config.version,
                is_cli=False,
            )
            config.compatibility = compatibility.to_dict() if compatibility else None
            config.last_check = now()
            config.write(self.HEALTH_FILE)
        return Response(status=status.HTTP_200_OK)
