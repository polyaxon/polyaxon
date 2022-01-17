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

from polyaxon.auxiliaries.cleaner import (
    PolyaxonCleanerSchema,
    V1PolyaxonCleaner,
    get_default_cleaner_container,
)
from polyaxon.auxiliaries.default_scheduling import (
    DefaultSchedulingSchema,
    V1DefaultScheduling,
)
from polyaxon.auxiliaries.init import (
    PolyaxonInitContainerSchema,
    V1PolyaxonInitContainer,
    get_default_init_container,
    get_init_resources,
)
from polyaxon.auxiliaries.notifier import (
    PolyaxonNotifierSchema,
    V1PolyaxonNotifier,
    get_default_notification_container,
)
from polyaxon.auxiliaries.sidecar import (
    PolyaxonSidecarContainerSchema,
    V1PolyaxonSidecarContainer,
    get_default_sidecar_container,
    get_sidecar_resources,
)
from polyaxon.auxiliaries.tuner import get_default_tuner_container
