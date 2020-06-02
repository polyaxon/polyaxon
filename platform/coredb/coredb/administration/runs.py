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

from django.contrib.admin import site

from coredb.administration.utils import DiffModelAdmin, ReadOnlyAdmin
from coredb.models.runs import Run


class OperationAdmin(DiffModelAdmin):
    pass


class RunLightAdmin(DiffModelAdmin, ReadOnlyAdmin):
    list_display = (
        "uuid",
        "user",
        "project",
        "name",
        "status",
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
    )
    fields = (
        "project",
        "name",
        "description",
        "status",
        "created_at",
        "updated_at",
        "started_at",
        "finished_at",
    )
    readonly_fields = ("status",)


site.register(Run, RunLightAdmin)
