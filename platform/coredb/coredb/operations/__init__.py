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

from coredb.operations.service import OperationsService
from polycommon.service_interface import LazyServiceWrapper


def get_operation_backend_path():
    return settings.OPERATIONS_BACKEND or "coredb.operations.service.OperationsService"


backend = LazyServiceWrapper(
    backend_base=OperationsService,
    backend_path=get_operation_backend_path(),
    options={},
)
backend.expose(locals())
