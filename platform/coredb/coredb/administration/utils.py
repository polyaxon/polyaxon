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


from django.contrib.admin import ModelAdmin


class ReadOnlyAdmin(ModelAdmin):
    """Disables all editing capabilities."""

    actions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pylint:disable=protected-access
        readonly_fields = [field.name for field in self.model._meta.get_fields()]
        if self.readonly_fields:
            self.readonly_fields += tuple(readonly_fields)
        else:
            self.readonly_fields = readonly_fields

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        extra_context["show_save"] = False
        return super(ReadOnlyAdmin, self).change_view(
            request, object_id, extra_context=extra_context
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass


class DiffModelAdmin(ModelAdmin):
    """Make diff model fields read-only."""

    readonly_fields = ("created_at", "updated_at")
