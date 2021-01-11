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

# Setting values to None means using defaults

from polyaxon.constants import PLATFORM_DIST_CE
from polycommon import pkg

ENCRYPTION_BACKEND = None
CONF_CHECK_OWNERSHIP = False
AUDITOR_BACKEND = None
AUDITOR_EVENTS_TASK = None
WORKERS_BACKEND = None
EXECUTOR_BACKEND = "coredb.executor.service.ExecutorService"
WORKERS_SERVICE = "polycommon.workers"
EXECUTOR_SERVICE = "coredb.executor"
OPERATIONS_BACKEND = None
PLATFORM_VERSION = pkg.VERSION
PLATFORM_DIST = PLATFORM_DIST_CE
CONF_BACKEND = "polycommon.conf.service.ConfService"
STORE_OPTION = "env"
AUTH_USER_MODEL = "coredb.User"
K8S_IN_CLUSTER = True
