from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.job_resources import JobResourcesSerializer
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import Experiment, ExperimentMetric, ExperimentStatus
from libs.spec_validation import validate_experiment_spec_config


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
            'id', 'uuid', 'unique_name', 'role', 'experiment', 'experiment_name',
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
    last_metric = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'id', 'uuid', 'unique_name', 'user', 'description', 'created_at', 'updated_at',
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

    def get_last_metric(self, obj):
        return {k: round(v, 7) for k, v in obj.last_metric.items()} if obj.last_metric else None


class ExperimentDetailSerializer(ExperimentSerializer):
    original = fields.SerializerMethodField()
    resources = fields.SerializerMethodField()

    class Meta(ExperimentSerializer.Meta):
        fields = ExperimentSerializer.Meta.fields + (
            'original', 'original_experiment',
            'description', 'config', 'declarations', 'resources',
        )
        extra_kwargs = {'original_experiment': {'write_only': True}}

    def get_original(self, obj):
        return obj.original_experiment.unique_name if obj.original_experiment else None

    def get_resources(self, obj):
        return obj.resources.to_dict() if obj.resources else None


class ExperimentCreateSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = (
            'user', 'description', 'original_experiment', 'config', 'declarations')

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the ExperimentSpecification to check if this config was
        intended as an experiment.
        """
        # config is optional
        if not config:
            return config

        spec = validate_experiment_spec_config(config)

        if spec.is_experiment:
            # Resume normal creation
            return config

        # Raise an error to tell the user to use experiment creation instead
        raise ValidationError('Current experiment creation could not be performed.\n'
                              'The reason is that the specification sent correspond '
                              'to a `{}`.\n'.format(spec.kind))

    def validate(self, attrs):
        if self.initial_data.get('check_specification') and not attrs.get('config'):
            raise ValidationError('Experiment expects a `config`.')
        return attrs

    def create(self, validated_data):
        """Check the params or set the value from the specification."""
        config = None
        if validated_data.get('config'):
            config = validate_experiment_spec_config(validated_data['config'])
        if not validated_data.get('declarations') and config:
            validated_data['declarations'] = config.declarations
        if not validated_data.get('tags') and config:
            validated_data['tags'] = config.tags
        return super().create(validated_data=validated_data)
