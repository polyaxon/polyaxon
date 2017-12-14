# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from experiments.serializers import ExperimentSerializer
from libs.spec_validation import validate_spec_content
from projects.models import Project, ExperimentGroup


class ExperimentGroupSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    project = fields.SerializerMethodField()
    user = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()

    class Meta:
        model = ExperimentGroup
        fields = ('uuid', 'user', 'name', 'description', 'content', 'project', 'num_experiments',)

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_user(self, obj):
        return obj.user.username

    def get_num_experiments(self, obj):
        return obj.experiments.count()

    def validate_content(self, content):
        spec = validate_spec_content(content)

        if spec.matrix_space > 1:
            # Resume normal creation
            return content

        # Raise an error to tell the use to use experiment creation instead
        raise ValidationError('Current experiment group creation could not be performed.\n'
                              'The reason is that the specification sent correspond '
                              'to an independent experiment.\n'
                              'Please use `create experiment endpoint`.')


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    num_experiment_groups = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('uuid', 'user', 'name', 'description', 'created_at', 'updated_at',
                  'is_public', 'has_code', 'num_experiment_groups', 'num_experiments')

    def get_user(self, obj):
        return obj.user.username

    def get_num_experiment_groups(self, obj):
        return obj.experiment_groups.count()

    def get_num_experiments(self, obj):
        return obj.experiments.count()


class ProjectDetailSerializer(ProjectSerializer):
    experiments = ExperimentSerializer(many=True)
    experiment_groups = ExperimentGroupSerializer(many=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('experiments', 'experiment_groups',)
