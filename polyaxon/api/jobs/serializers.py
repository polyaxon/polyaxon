from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from db.models.jobs import Job, JobStatus
from libs.spec_validation import validate_job_spec_config


class JobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    job = fields.SerializerMethodField()

    class Meta:
        model = JobStatus
        exclude = ('id',)

    def get_job(self, obj):
        return obj.job.uuid.hex


class JobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    project_name = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = Job
        fields = (
            'uuid', 'unique_name', 'user', 'sequence', 'description', 'created_at', 'updated_at',
            'last_status', 'started_at', 'finished_at', 'is_running', 'is_done',
            'is_clone', 'project', 'project_name',)

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_project_name(self, obj):
        return obj.project.unique_name


class JobDetailSerializer(JobSerializer):
    resources = fields.SerializerMethodField()

    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + (
            'description', 'config', 'declarations', 'resources',
        )

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None


class JobCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            'user', 'description', 'config', 'declarations')

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the JobSpecification to check if this config was
        intended as job.
        """
        # config is optional
        if not config:
            return config

        spec = validate_job_spec_config(config)

        if spec.is_job:
            # Resume normal creation
            return config

        # Raise an error to tell the user to use job creation instead
        raise ValidationError('Current job creation could not be performed.\n'
                              'The reason is that the specification sent correspond '
                              'to a `{}`.\n'.format(spec.kind))

    def validate(self, attrs):
        if self.initial_data.get('check_specification') and not attrs.get('config'):
            raise ValidationError('Experiment expects a `config`.')
        return attrs

    def create(self, validated_data):
        """Check the params or set the value from the specification."""
        if not validated_data.get('declarations') and validated_data.get('config'):
            config = validate_job_spec_config(validated_data['config'])
            validated_data['declarations'] = config.declarations
        return super(JobCreateSerializer, self).create(validated_data=validated_data)
