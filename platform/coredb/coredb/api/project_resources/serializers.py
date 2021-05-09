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
from marshmallow import ValidationError as MarshmallowValidationError
from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from django.db import IntegrityError

from coredb.abstracts.getter import get_run_model
from coredb.api.base.cloning import CloningMixin
from coredb.api.base.is_managed import IsManagedMixin
from coredb.api.base.pipeline import PipelineMixin
from coredb.api.base.settings import SettingsMixin
from coredb.managers.operations import compile_operation_run
from coredb.managers.runs import create_run
from polyaxon.exceptions import PolyaxonException
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.schemas import V1RunPending


class RunSerializer(
    serializers.ModelSerializer, CloningMixin, PipelineMixin, SettingsMixin
):
    uuid = fields.UUIDField(format="hex", read_only=True)
    original = fields.SerializerMethodField()
    pipeline = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)
    settings = fields.SerializerMethodField()

    class Meta:
        model = get_run_model()
        fields = (
            "uuid",
            "name",
            "created_at",
            "updated_at",
            "started_at",
            "finished_at",
            "wait_time",
            "duration",
            "kind",
            "runtime",
            "meta_info",
            "status",
            "pipeline",
            "original",
            "is_managed",
            "pending",
            "inputs",
            "outputs",
            "tags",
            "settings",
        )
        extra_kwargs = {
            "is_managed": {"read_only": True},
        }


class OfflineRunSerializer(
    serializers.ModelSerializer,
):
    uuid = fields.UUIDField(format="hex")
    created_at = fields.DateTimeField()

    class Meta:
        model = get_run_model()
        fields = (
            "uuid",
            "name",
            "description",
            "tags",
            "created_at",
            "updated_at",
            "started_at",
            "finished_at",
            "wait_time",
            "duration",
            "kind",
            "runtime",
            "meta_info",
            "status",
            "status_conditions",
            "is_managed",
            "inputs",
            "outputs",
        )

    def create(self, validated_data):
        try:
            obj = self.Meta.model.objects.create(**validated_data)
        except IntegrityError:
            raise ValidationError(
                f"A run with uuid {validated_data.get('uuid')} already exists."
            )
        # Override auto-field for created_at
        created_at = validated_data.get("created_at")
        if created_at:
            obj.created_at = created_at
        obj.save()
        return obj


class OperationCreateSerializer(serializers.ModelSerializer, IsManagedMixin):
    uuid = fields.UUIDField(format="hex", read_only=True)
    is_approved = fields.BooleanField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = get_run_model()
        fields = (
            "uuid",
            "name",
            "description",
            "content",
            "is_managed",
            "pending",
            "meta_info",
            "tags",
            "is_approved",
        )
        extra_kwargs = {
            "meta_info": {"write_only": True},
            "pending": {"write_only": True},
            "is_approved": {"write_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.check_if_entity_is_managed(attrs=attrs, entity_name="Run")
        return attrs

    def create(self, validated_data):
        is_managed = validated_data["is_managed"]
        content = validated_data.get("content")
        meta_info = validated_data.get("meta_info") or {}
        if content:
            is_managed = True if is_managed is None else is_managed

        if is_managed and not content:
            raise ValidationError(
                "Managed runs require a content with valid specification"
            )

        project_id = validated_data["project"].id
        user = validated_data.get("user")
        name = validated_data.get("name")
        description = validated_data.get("description")
        tags = validated_data.get("tags")
        pending = validated_data.get("pending")
        # Check the deprecated `is_approved` flag
        if pending is None:
            is_approved = validated_data.get("is_approved")
            if is_approved is False:
                pending = V1RunPending.UPLOAD

        if is_managed or content:
            try:
                op_spec = OperationSpecification.read(content)
            except Exception as e:
                raise ValidationError(e)
            if op_spec.is_template():
                raise ValidationError(
                    "Received a template polyaxonfile, "
                    "Please customize the specification or disable the template."
                )
            try:
                return compile_operation_run(
                    project_id=project_id,
                    user_id=user.id if user else None,
                    op_spec=op_spec,
                    name=name,
                    description=description,
                    tags=tags,
                    meta_info=meta_info,
                    is_managed=is_managed,
                    pending=pending,
                    supported_kinds=validated_data.get("supported_kinds"),
                    supported_owners=validated_data.get("supported_owners"),
                )
            except (MarshmallowValidationError, PolyaxonException, ValueError) as e:
                raise ValidationError(e)
        else:
            return create_run(
                project_id=project_id,
                user_id=user.id if user else None,
                name=name,
                description=description,
                tags=tags,
                meta_info=meta_info,
            )
