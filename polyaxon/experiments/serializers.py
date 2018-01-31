# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus,
    ExperimentMetric
)
from jobs.serializers import JobResourcesSerializer
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
    resources = JobResourcesSerializer(required=False)
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = ExperimentJob
        fields = (
            'uuid', 'unique_name', 'sequence', 'role', 'experiment', 'experiment_name',
            'last_status', 'is_running', 'is_done', 'created_at', 'updated_at',
            'started_at', 'finished_at', 'resources',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex

    def get_experiment_name(self, obj):
        return obj.experiment.unique_name


class ExperimentJobDetailSerializer(ExperimentJobSerializer):
    class Meta(ExperimentJobSerializer.Meta):
        fields = ExperimentJobSerializer.Meta.fields + ('definition',)


class ExperimentStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentStatus
        exclude = ('id',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex


class ExperimentMetricSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentMetric
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
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'uuid', 'unique_name', 'user', 'sequence', 'description', 'created_at', 'updated_at',
            'last_status', 'last_metric', 'started_at', 'finished_at', 'is_running', 'is_done',
            'is_clone', 'project', 'project_name', 'experiment_group',
            'experiment_group_name', 'num_jobs',)

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


class ExperimentDetailSerializer(ExperimentSerializer):
    original = fields.SerializerMethodField()

    class Meta(ExperimentSerializer.Meta):
        fields = ExperimentSerializer.Meta.fields + (
            'content', 'config', 'original', 'original_experiment',
            'description', 'config', 'declarations', 'resources',
        )
        extra_kwargs = {'original_experiment': {'write_only': True}}

    def get_original(self, obj):
        return obj.original_experiment.unique_name if obj.original_experiment else None


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
