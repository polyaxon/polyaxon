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

import logging
import os

logger = logging.getLogger("polyaxon.cli")


def set_raven_client() -> bool:
    from polyaxon import pkg
    from polyaxon.env_vars.keys import POLYAXON_KEYS_SERVICE
    from polyaxon import settings

    cli_config = settings.CLI_CONFIG
    if cli_config and cli_config.log_handler and cli_config.log_handler.dsn:
        import sentry_sdk

        sentry_sdk.init(
            dsn=cli_config.log_handler.decoded_dsn,
            release=pkg.VERSION,
            environment=cli_config.log_handler.environment,
            server_name=os.environ.get(POLYAXON_KEYS_SERVICE, None),
        )
        return True

    return False
