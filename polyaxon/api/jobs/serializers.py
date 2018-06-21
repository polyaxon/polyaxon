from rest_framework import fields, serializers

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

    class Meta:
        model = Job
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'user',
            'description',
            'created_at',
            'updated_at',
            'last_status',
            'started_at',
            'finished_at',
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


class JobDetailSerializer(JobSerializer):
    original = fields.SerializerMethodField()
    resources = fields.SerializerMethodField()

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + (
            'is_clone',
            'original',
            'original_job',
            'description',
            'config',
            'resources',
        )
        extra_kwargs = {'original_job': {'write_only': True}}

    def get_original(self, obj):
        return obj.original_job.unique_name if obj.original_job else None

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None


class JobCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = Job
        fields = ('id', 'user', 'name', 'description', 'config',)

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the JobSpecification to check if this config was
        intended as job.
        """
        validate_job_spec_config(config)
        return config
