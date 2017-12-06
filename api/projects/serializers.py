# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from experiments.serializers import ExperimentSerializer
from projects.models import Project, PolyaxonSpec


class PolyaxonSpecSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    project = fields.SerializerMethodField()
    user = fields.SerializerMethodField()

    class Meta:
        model = PolyaxonSpec
        fields = ('uuid', 'user', 'content', 'project', )

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_user(self, obj):
        return obj.user.username


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('uuid', 'user', 'name', 'description', 'created_at', 'updated_at',
                  'is_public', 'has_code')

    def get_user(self, obj):
        return obj.user.username


class ProjectDetailSerializer(ProjectSerializer):
    experiments = ExperimentSerializer(many=True)
    specs = PolyaxonSpecSerializer(many=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('experiments', 'specs', )
