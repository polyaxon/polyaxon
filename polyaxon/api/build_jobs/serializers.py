from typing import Dict

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.in_cluster import InClusterMixin
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.tags import TagsSerializerMixin
from db.models.build_jobs import BuildJob, BuildJobStatus
from db.models.experiments import Experiment
from db.models.jobs import Job
from libs.spec_validation import validate_build_spec_config


class BuildJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = BuildJobStatus
        extra_kwargs = {'job': {'read_only': True}}
        exclude = []


class BuildJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = BuildJob
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'pod_id',
            'user',
            'description',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'last_status',
            'tags',
            'project',
            'backend',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.unique_name


class BookmarkedBuildJobSerializer(BuildJobSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'buildjob'

    class Meta(BuildJobSerializer.Meta):
        fields = BuildJobSerializer.Meta.fields + ('bookmarked',)


class BuildJobDetailSerializer(BookmarkedBuildJobSerializer,
                               InClusterMixin,
                               TagsSerializerMixin,
                               NamesMixin):
    resources = fields.SerializerMethodField()
    num_jobs = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()
    commit = fields.SerializerMethodField()
    merge = fields.BooleanField(write_only=True, required=False)

    class Meta(BookmarkedBuildJobSerializer.Meta):
        fields = BookmarkedBuildJobSerializer.Meta.fields + (
            'merge',
            'description',
            'config',
            'in_cluster',
            'resources',
            'node_scheduled',
            'num_jobs',
            'num_experiments',
            'dockerfile',
            'commit',
            'backend',
        )

    def get_commit(self, obj: 'BuildJob'):
        return obj.code_reference.commit if obj.code_reference else None

    def get_resources(self, obj: 'BuildJob'):
        return obj.resources.to_dict() if obj.resources else None

    def get_num_jobs(self, obj: 'BuildJob'):
        return Job.objects.filter(build_job=obj).count()

    def get_num_experiments(self, obj: 'BuildJob'):
        return Experiment.objects.filter(build_job=obj).count()

    def update(self, instance: 'BuildJob', validated_data: Dict) -> 'BuildJob':
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=BuildJob.all)
        return super().update(instance=instance, validated_data=validated_data)


class BuildJobCreateSerializer(serializers.ModelSerializer,
                               InClusterMixin,
                               NamesMixin):
    user = fields.SerializerMethodField()

    class Meta:
        model = BuildJob
        fields = ('id', 'user', 'name', 'description', 'config', 'in_cluster', 'tags')

    def get_user(self, obj: 'BuildJob'):
        return obj.user.username

    def validate_config(self, config: Dict) -> Dict:
        """We only validate the config if passed.

        Also we use the BuildSpecification to check if this config was
        intended as job.
        """
        validate_build_spec_config(config)
        return config

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=BuildJob.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)
