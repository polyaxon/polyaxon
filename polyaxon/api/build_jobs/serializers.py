from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from db.models.build_jobs import BuildJob, BuildJobStatus
from libs.spec_validation import validate_build_spec_config


class BuildJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    job = fields.SerializerMethodField()

    class Meta:
        model = BuildJobStatus

    def get_job(self, obj):
        return obj.job.uuid.hex


class BuildJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    project_name = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = BuildJob
        fields = (
            'uuid', 'unique_name', 'user', 'description', 'created_at', 'updated_at',
            'last_status', 'started_at', 'finished_at', 'is_running', 'is_done',
            'project', 'project_name',)

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_project_name(self, obj):
        return obj.project.unique_name


class BuildJobDetailSerializer(BuildJobSerializer):
    resources = fields.SerializerMethodField()

    class Meta(BuildJobSerializer.Meta):
        fields = BuildJobSerializer.Meta.fields + ('description', 'config', 'resources',)

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None


class BuildJobCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = BuildJob
        fields = ('user', 'description', 'config',)

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the BuildSpecification to check if this config was
        intended as job.
        """
        spec = validate_build_spec_config(config)

        if spec.is_build:
            # Resume normal creation
            return config

        # Raise an error to tell the user to use job creation instead
        raise ValidationError('Current job creation could not be performed.\n'
                              'The reason is that the specification sent correspond '
                              'to a `{}`.\n'.format(spec.kind))

    def create(self, validated_data):
        """Check the params or set the value from the specification."""
        config = None
        if validated_data.get('config'):
            config = validate_build_spec_config(validated_data['config'])
        if not validated_data.get('tags') and config:
            validated_data['tags'] = config.tags
        return super().create(validated_data=validated_data)
