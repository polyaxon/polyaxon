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
from typing import Optional

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException


def get_client_or_raise() -> Optional[RunClient]:
    if settings.CLIENT_CONFIG.no_api:
        return None

    try:
        return RunClient()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)
