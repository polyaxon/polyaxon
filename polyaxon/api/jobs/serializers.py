from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.data_refs import DataRefsSerializerMixin
from api.utils.serializers.in_cluster import InClusterMixin
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.tags import TagsSerializerMixin
from db.models.jobs import Job, JobStatus
from libs.spec_validation import validate_job_spec_config


class JobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = JobStatus
        extra_kwargs = {'job': {'read_only': True}}
        exclude = []


class JobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    build_job = fields.SerializerMethodField()
    original = fields.SerializerMethodField()

    class Meta:
        model = Job
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
            'last_status',
            'started_at',
            'finished_at',
            'original',
            'cloning_strategy',
            'tags',
            'project',
            'build_job',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.unique_name

    def get_build_job(self, obj):
        return obj.build_job.unique_name if obj.build_job else None

    def get_original(self, obj):
        return obj.original_job.unique_name if obj.original_job else None


class BookmarkedJobSerializer(JobSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'job'

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + ('bookmarked',)


class JobDetailSerializer(BookmarkedJobSerializer,
                          InClusterMixin,
                          TagsSerializerMixin,
                          DataRefsSerializerMixin,
                          NamesMixin):
    resources = fields.SerializerMethodField()
    merge = fields.BooleanField(write_only=True, required=False)

    class Meta(BookmarkedJobSerializer.Meta):
        fields = BookmarkedJobSerializer.Meta.fields + (
            'merge',
            'is_clone',
            'original_job',
            'description',
            'readme',
            'config',
            'in_cluster',
            'resources',
            'data_refs',
            'node_scheduled',
        )
        extra_kwargs = {'original_job': {'write_only': True}}

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_data_refs(validated_data=validated_data,
                                                  data_refs=instance.data_refs)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=Job.all)

        return super().update(instance=instance, validated_data=validated_data)


class JobCreateSerializer(serializers.ModelSerializer,
                          InClusterMixin,
                          NamesMixin):
    user = fields.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'id',
            'user',
            'name',
            'description',
            'readme',
            'in_cluster',
            'data_refs',
            'config',)

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the JobSpecification to check if this config was
        intended as job.
        """
        validate_job_spec_config(config)
        return config

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=Job.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)
