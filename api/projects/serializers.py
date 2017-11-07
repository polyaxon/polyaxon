# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from experiments.serializers import ExperimentSerializer
from projects.models import Project, Polyaxonfile


class PolyaxonfileSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    project = fields.SerializerMethodField()
    user = fields.SerializerMethodField()

    class Meta:
        model = Polyaxonfile
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
        fields = ('uuid', 'user', 'name', 'description', 'created_at', 'updated_at', 'is_public', )

    def get_user(self, obj):
        return obj.user.username


class ProjectDetailSerializer(ProjectSerializer):
    experiments = ExperimentSerializer(many=True)
    polyaxonfiles = PolyaxonfileSerializer(many=True)

    class Meta:
        model = Project
        exclude = ('id',)
