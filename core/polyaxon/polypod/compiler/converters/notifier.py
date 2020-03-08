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

from polyaxon.k8s.custom_resources.operation import (
    get_notifier_instance,
    get_notifier_resource_name,
)
from polyaxon.polypod.compiler.converters import JobConverter
from polyaxon.polypod.mixins import NotifierMixin


class NotifierConverter(NotifierMixin, JobConverter):
    def get_instance(self):
        return get_notifier_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_notifier_resource_name(self.run_uuid)
