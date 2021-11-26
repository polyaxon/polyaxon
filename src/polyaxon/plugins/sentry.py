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

import logging
import os

from typing import Dict

logger = logging.getLogger("polyaxon.cli")


def set_raven_client(options: Dict = None) -> bool:
    from polyaxon import pkg, settings
    from polyaxon.env_vars.keys import POLYAXON_KEYS_SERVICE

    cli_config = settings.CLI_CONFIG
    options = options or {}
    environment = options.get("environment")
    dsn = options.get("dsn")
    sample_rate = options.get("sample_rate", 0)
    if cli_config and cli_config.log_handler and cli_config.log_handler.decoded_dsn:
        dsn = dsn or cli_config.log_handler.decoded_dsn
        environment = environment or cli_config.log_handler.environment

    if dsn:
        import sentry_sdk

        sentry_sdk.init(
            dsn=dsn,
            release=pkg.VERSION,
            environment=environment,
            server_name=os.environ.get(POLYAXON_KEYS_SERVICE, None),
            sample_rate=sample_rate,
        )
        return True

    return False
