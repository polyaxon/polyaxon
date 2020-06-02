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

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from coredb.api.base.cloning import CloningMixin
from coredb.api.base.is_managed import IsManagedMixin
from coredb.api.base.settings import SettingsMixin
from coredb.managers.operations import compile_operation_run
from coredb.managers.runs import create_run
from coredb.models.runs import Run
from polyaxon.polyaxonfile import OperationSpecification


class RunSerializer(serializers.ModelSerializer, CloningMixin, SettingsMixin):
    uuid = fields.UUIDField(format="hex", read_only=True)
    original = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)
    settings = fields.SerializerMethodField()

    class Meta:
        model = Run
        fields = (
            "uuid",
            "name",
            "description",
            "created_at",
            "updated_at",
            "started_at",
            "finished_at",
            "run_time",
            "kind",
            "meta_info",
            "status",
            "original",
            "is_managed",
            "inputs",
            "outputs",
            "tags",
            "deleted",
            "settings",
        )
        extra_kwargs = {
            "is_managed": {"read_only": True},
            "cloning_kind": {"read_only": True},
        }


class OperationCreateSerializer(serializers.ModelSerializer, IsManagedMixin):
    uuid = fields.UUIDField(format="hex", read_only=True)

    class Meta:
        model = Run
        fields = (
            "uuid",
            "name",
            "description",
            "content",
            "is_managed",
            "tags",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.check_if_entity_is_managed(attrs=attrs, entity_name="Run")
        return attrs

    def create(self, validated_data):
        is_managed = validated_data["is_managed"]
        content = validated_data.get("content")
        if content:
            is_managed = True if is_managed is None else is_managed

        if is_managed and not content:
            raise ValidationError(
                "Managed runs require a content with valid specification"
            )

        if is_managed:
            try:
                op_spec = OperationSpecification.read(content)
            except Exception as e:
                raise ValidationError(e)
            return compile_operation_run(
                project_id=validated_data["project"].id,
                user_id=validated_data["user"].id,
                op_spec=op_spec,
                name=validated_data.get("name"),
                description=validated_data.get("description"),
                tags=validated_data.get("tags"),
            )
        else:
            return create_run(
                project_id=validated_data["project"].id,
                user_id=validated_data["user"].id,
                name=validated_data.get("name"),
                description=validated_data.get("description"),
                tags=validated_data.get("tags"),
            )
