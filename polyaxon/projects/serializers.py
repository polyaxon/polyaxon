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
    project_name = fields.SerializerMethodField()
    user = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()
    num_pending_experiments = fields.SerializerMethodField()
    num_running_experiments = fields.SerializerMethodField()

    class Meta:
        model = ExperimentGroup
        fields = (
            'uuid', 'unique_name', 'user', 'sequence', 'description',
            'project', 'project_name', 'created_at', 'updated_at', 'concurrency',
            'num_experiments', 'num_pending_experiments', 'num_running_experiments',)

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_project_name(self, obj):
        return obj.project.unique_name

    def get_user(self, obj):
        return obj.user.username

    def get_num_experiments(self, obj):
        return obj.experiments.count()

    def get_num_pending_experiments(self, obj):
        return obj.pending_experiments.count()

    def get_num_running_experiments(self, obj):
        return obj.running_experiments.count()


class ExperimentGroupDetailSerializer(ExperimentGroupSerializer):
    num_scheduled_experiments = fields.SerializerMethodField()
    num_succeeded_experiments = fields.SerializerMethodField()
    num_failed_experiments = fields.SerializerMethodField()
    num_stopped_experiments = fields.SerializerMethodField()

    class Meta(ExperimentGroupSerializer.Meta):
        fields = ExperimentGroupSerializer.Meta.fields + (
            'content', 'num_scheduled_experiments', 'num_succeeded_experiments',
            'num_failed_experiments', 'num_stopped_experiments')

    def get_num_scheduled_experiments(self, obj):
        return obj.scheduled_experiments.count()

    def get_num_succeeded_experiments(self, obj):
        return obj.succeeded_experiments.count()

    def get_num_failed_experiments(self, obj):
        return obj.failed_experiments.count()

    def get_num_stopped_experiments(self, obj):
        return obj.stopped_experiments.count()

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
        fields = (
            'uuid', 'user', 'name', 'unique_name', 'description', 'created_at', 'updated_at',
            'is_public', 'has_code', 'has_tensorboard', 'has_notebook',
            'num_experiment_groups', 'num_experiments')

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
