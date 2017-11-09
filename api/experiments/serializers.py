# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus,
    ExperimentJobMessage,
)


class ExperimentJobMessageSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentJobMessage
        exclude = ('id',)


class ExperimentJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    message = ExperimentJobMessageSerializer(required=False)
    job = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJobStatus
        exclude = ('id',)

    def get_job(self, obj):
        return obj.job.uuid.hex

    def _add_message(self, validated_data, instance=None):
        message_data = validated_data.pop('message', None)
        if message_data:
            if instance.message:
                message_serializer = ExperimentJobMessageSerializer(instance=instance.message,
                                                                    data=message_data,
                                                                    partial=True)
            else:
                message_serializer = ExperimentJobMessageSerializer(data=message_data)
            message_serializer.is_valid(raise_exception=True)
            message = message_serializer.save()
            validated_data['message'] = message
        return validated_data

    def create(self, validated_data):
        validated_data = self._add_message(validated_data)
        return super(ExperimentJobStatusSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._add_message(validated_data, instance)
        return super(ExperimentJobStatusSerializer, self).update(instance, validated_data)


class ExperimentJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    experiment = fields.SerializerMethodField()

    class Meta:
        model = ExperimentJob
        exclude = ('id',)

    def get_experiment(self, obj):
        return obj.experiment.uuid.hex


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
    last_status = serializers.SerializerMethodField()
    user = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = ('uuid', 'user', 'name', 'created_at', 'updated_at',
                  'last_status', 'started_at', 'finished_at', 'is_clone',)

    def get_last_status(self, obj):
        return obj.last_status.status if obj.last_status else None

    def get_user(self, obj):
        return obj.user.username


class ExperimentDetailSerializer(ExperimentSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    cluster = fields.SerializerMethodField()
    polyaxonfile = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    jobs = ExperimentJobSerializer(many=True)

    class Meta:
        model = Experiment
        fields = (
            'uuid', 'created_at', 'updated_at', 'cluster', 'project', 'user', 'name', 'last_status',
            'description', 'polyaxonfile', 'config', 'original_experiment', 'jobs', 'started_at',
            'finished_at', 'is_clone')

    def get_cluster(self, obj):
        return obj.cluster.uuid.hex

    def get_polyaxonfile(self, obj):
        return obj.polyaxonfile.uuid.hex if obj.polyaxonfile else None

    def get_project(self, obj):
        return obj.project.uuid.hex


class ExperimentCreateSerializer(ExperimentSerializer):

    class Meta:
        model = Experiment
        fields = (
            'cluster', 'project', 'user', 'name', 'description',
            'polyaxonfile', 'config', 'original_experiment')
        extra_kwargs = {
            'cluster': {'write_only': True},
            'project': {'write_only': True},
            'polyaxonfile': {'write_only': True}
        }


class StatusSerializer(serializers.Serializer):
    job_id = serializers.CharField()
    status = serializers.CharField()
