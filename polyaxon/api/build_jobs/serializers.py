from typing import Dict

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.is_managed import IsManagedMixin
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.project import ProjectMixin
from api.utils.serializers.tags import TagsSerializerMixin
from api.utils.serializers.user import UserMixin
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


class BuildJobSerializer(serializers.ModelSerializer, ProjectMixin, UserMixin):
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
            'is_managed',
        )
        extra_kwargs = {'is_managed': {'read_only': True}}


class BookmarkedBuildJobSerializer(BuildJobSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'buildjob'

    class Meta(BuildJobSerializer.Meta):
        fields = BuildJobSerializer.Meta.fields + ('bookmarked',)


class BuildJobDetailSerializer(BookmarkedBuildJobSerializer,
                               IsManagedMixin,
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
            'content',
            'resources',
            'node_scheduled',
            'num_jobs',
            'num_experiments',
            'dockerfile',
            'commit',
        )
        extra_kwargs = {'content': {'read_only': True},
                        **BookmarkedBuildJobSerializer.Meta.extra_kwargs}

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
                               IsManagedMixin,
                               NamesMixin,
                               ProjectMixin,
                               UserMixin):
    project = fields.SerializerMethodField()
    user = fields.SerializerMethodField()

    class Meta:
        model = BuildJob
        fields = (
            'id',
            'user',
            'project',
            'name',
            'unique_name',
            'description',
            'content',
            'backend',
            'is_managed',
            'tags',
        )
        extra_kwargs = {'unique_name': {'read_only': True}}

    def validate_content(self, content):
        """We only validate the content if passed.

        Also we use the BuildSpecification to check if this content was
        intended as an experiment.
        """
        # content is optional
        if not content:
            return content

        validate_build_spec_config(content)
        return content

    def validate(self, attrs):
        self.check_if_entity_is_managed(attrs=attrs, entity_name='Build')
        return attrs

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=BuildJob.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)
