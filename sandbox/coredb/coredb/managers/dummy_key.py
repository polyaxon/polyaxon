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
import uuid

from django.contrib.auth import get_user_model

from coredb.models.projects import Owner
from polycommon import conf
from polycommon.options.registry.installation import ORGANIZATION_KEY


def get_dummy_key():
    first_joined = get_user_model().objects.order_by("date_joined").first()
    if first_joined:
        key = uuid.uuid5(Owner.uuid, str(first_joined.date_joined.timestamp())).hex
    else:
        key = uuid.uuid4().hex
    conf.set(ORGANIZATION_KEY, key)
    return key
