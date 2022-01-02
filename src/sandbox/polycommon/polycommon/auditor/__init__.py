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

from polycommon.auditor.manager import event_manager
from polycommon.auditor.service import AuditorService
from polycommon.service_interface import LazyServiceWrapper


def get_auditor_backend_path():
    return settings.AUDITOR_BACKEND or "polycommon.auditor.service.AuditorService"


def get_auditor_options():
    return {
        "auditor_events_task": settings.AUDITOR_EVENTS_TASK,
        "workers_service": settings.WORKERS_SERVICE,
        "executor_service": settings.EXECUTOR_SERVICE or "coredb.executor",
    }


backend = LazyServiceWrapper(
    backend_base=AuditorService,
    backend_path=get_auditor_backend_path(),
    options=get_auditor_options(),
)
backend.expose(locals())

subscribe = event_manager.subscribe
