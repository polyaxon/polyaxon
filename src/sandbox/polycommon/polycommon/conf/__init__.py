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

from django.conf import settings

from polycommon.conf.option_manager import option_manager
from polycommon.conf.option_service import OptionService
from polycommon.service_interface import LazyServiceWrapper


def get_conf_backend_path():
    return settings.CONF_BACKEND or "polycommon.conf.service.ConfService"


def get_conf_options():
    return {"check_ownership": settings.CONF_CHECK_OWNERSHIP}


backend = LazyServiceWrapper(
    backend_base=OptionService,
    backend_path=get_conf_backend_path(),
    options=get_conf_options(),
)
backend.expose(locals())

subscribe = option_manager.subscribe
