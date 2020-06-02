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

# Default configs
from polycommon.celery.routes import get_routes
from polycommon.settings.api import set_api
from polycommon.settings.apps import set_apps
from polycommon.settings.assets import set_assets
from polycommon.settings.celery import set_celery
from polycommon.settings.core import set_core
from polycommon.settings.cors import set_cors
from polycommon.settings.logging import set_logging
from polycommon.settings.admin import set_admin
from polycommon.settings.middlewares import set_middlewares
from polycommon.settings.secrets import set_secrets
from polyconf.config_manager import ROOT_DIR, config

context = locals()
set_logging(
    context=context,
    root_dir=ROOT_DIR,
    log_level=config.log_level,
    log_handlers=config.log_handlers,
    debug=config.is_debug_mode,
)
set_admin(context=context, config=config)
set_secrets(context=context, config=config)
set_apps(
    context=context,
    config=config,
    default_apps=("coredb.apps.CoreDBConfig",),
    third_party_apps=("rest_framework", "corsheaders"),
    project_apps=(
        "polycommon.apis.apps.CommonApisConfig",
        "django.contrib.admin",
        "django.contrib.admindocs",
        "apis.apps.APIsConfig",
        "polycommon.commands.apps.CommandsConfig",
    ),
)

set_core(context=context, config=config)
set_cors(context=context, config=config)
set_api(context=context, config=config)
set_middlewares(context=context, config=config)
set_assets(context=context, root_dir=ROOT_DIR, config=config)
if config.scheduler_enabled:
    set_celery(context=context, config=config, routes=get_routes())

from polycommon.settings.defaults import *

# Service configs
from .rest import *
