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

from django.db import IntegrityError
from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from coredb.abstracts.getter import get_project_model
from coredb.api.base.tags import TagsMixin


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_project_model()
        fields = ("name",)


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format="hex", read_only=True)

    class Meta:
        model = get_project_model()
        fields = (
            "uuid",
            "name",
            "description",
            "tags",
            "created_at",
            "updated_at",
            "deleted",
        )


class ProjectDetailSerializer(ProjectSerializer, TagsMixin):
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ("readme",)

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(
            validated_data=validated_data, tags=instance.tags
        )

        return super().update(instance=instance, validated_data=validated_data)


class ProjectCreateSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ("readme",)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError(
                f"A project with name {validated_data['name']} already exists."
            )
