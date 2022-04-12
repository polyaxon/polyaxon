#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from coredb.administration.utils import DiffModelAdmin


class ProjectAdmin(DiffModelAdmin):
    list_display = ("uuid", "name", "created_at", "updated_at")
    list_display_links = ("uuid", "name")
    readonly_fields = DiffModelAdmin.readonly_fields + ("name",)
    fields = ("name", "live_state", "created_at", "updated_at")

    def get_queryset(self, request):
        qs = self.model.all.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
