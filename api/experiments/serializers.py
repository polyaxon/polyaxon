# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus,
)
from libs.spec_validation import validate_spec_content


class ExperimentJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    job = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJobStatus
        exclude = ('id',)

    def get_job(self, obj):
        return obj.job.uuid.hex


class ExperimentJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()
    experiment_name = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJob
        fields = (
            'uuid', 'experiment', 'experiment_name', 'definition', 'last_status', 'is_running',
            'is_done', 'created_at', 'updated_at', 'started_at', 'finished_at')

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex

    def get_experiment_name(self, obj):
        return obj.experiment.unique_name


class ExperimentStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentStatus
        exclude = ('id',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex


class ExperimentSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    experiment_group = fields.SerializerMethodField()
    experiment_group_name = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    project_name = fields.SerializerMethodField()
    num_jobs = fields.SerializerMethodField()
    original = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = (
            'uuid', 'unique_name', 'user', 'sequence', 'description', 'created_at', 'updated_at',
            'last_status', 'started_at', 'finished_at', 'is_running', 'is_done', 'is_clone',
            'content', 'config', 'project', 'project_name', 'experiment_group',
            'experiment_group_name', 'original', 'original_experiment', 'num_jobs',)

        extra_kwargs = {'original_experiment': {'write_only': True}}

    def get_user(self, obj):
        return obj.user.username

    def get_experiment_group(self, obj):
        return obj.experiment_group.uuid.hex if obj.experiment_group else None

    def get_experiment_group_name(self, obj):
        return obj.experiment_group.unique_name if obj.experiment_group else None

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_project_name(self, obj):
        return obj.project.unique_name

    def get_num_jobs(self, obj):
        return obj.jobs.count()

    def get_original(self, obj):
        return obj.original_experiment.uuid.hex if obj.original_experiment else None


class ExperimentDetailSerializer(ExperimentSerializer):
    jobs = ExperimentJobSerializer(many=True)

    class Meta(ExperimentSerializer.Meta):
        fields = ExperimentSerializer.Meta.fields + (
            'description', 'config', 'original_experiment', 'jobs',)


class ExperimentCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = (
            'user', 'description', 'content', 'config', 'original_experiment')

    def get_user(self, obj):
        return obj.user.username

    def validate_content(self, content):
        """We only validate the content if passed.

        Also we use the GroupSpecification to check if this content was
        intended as Group experiments.
        """
        # content is optional
        if not content:
            return content

        spec = validate_spec_content(content)

        if spec.matrix_space == 1:
            # Resume normal creation
            return content

        # Raise an error to tell the use to use experiment creation instead
        raise ValidationError('Current experiment creation could not be performed.\n'
                              'The reason is that the specification sent correspond '
                              'to a group experiment.\n'
                              'Please use `create group experiment endpoint`.')
