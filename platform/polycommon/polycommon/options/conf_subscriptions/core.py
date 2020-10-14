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

from polycommon import conf
from polycommon.options.registry import core

conf.subscribe(core.Logging)
conf.subscribe(core.Debug)
conf.subscribe(core.Protocol)
conf.subscribe(core.CeleryBrokerBackend)
conf.subscribe(core.CeleryBrokerUrl)
conf.subscribe(core.SecretInternalToken)
conf.subscribe(core.HealthCheckWorkerTimeout)
conf.subscribe(core.SchedulerEnabled)
conf.subscribe(core.UiAdminEnabled)
conf.subscribe(core.UiAssetsVersion)
conf.subscribe(core.UiOffline)
conf.subscribe(core.UiEnabled)
