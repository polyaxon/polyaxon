from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.build import BuildMixin
from api.utils.serializers.data_refs import DataRefsSerializerMixin
from api.utils.serializers.is_managed import IsManagedMixin
from api.utils.serializers.job_resources import JobResourcesSerializer
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.project import ProjectMixin
from api.utils.serializers.tags import TagsSerializerMixin
from api.utils.serializers.tensorboard import TensorboardSerializerMixin
from api.utils.serializers.user import UserMixin
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import (
    Experiment,
    ExperimentChartView,
    ExperimentMetric,
    ExperimentStatus
)
from libs.spec_validation import validate_experiment_spec_config


class ExperimentJobStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentJobStatus
        exclude = []
        extra_kwargs = {'job': {'read_only': True}}


class ExperimentJobSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    resources = JobResourcesSerializer(required=False)
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = ExperimentJob
        extra_kwargs = {'experiment': {'read_only': True}}
        fields = (
            'id',
            'uuid',
            'unique_name',
            'role',
            'experiment',
            'last_status',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'resources',
            'node_scheduled',
            'pod_id'
        )


class ExperimentJobDetailSerializer(ExperimentJobSerializer):
    class Meta(ExperimentJobSerializer.Meta):
        fields = ExperimentJobSerializer.Meta.fields + ('definition',)


class ExperimentStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentStatus
        exclude = []
        extra_kwargs = {'experiment': {'read_only': True}}


class ExperimentMetricSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentMetric
        exclude = []
        extra_kwargs = {'experiment': {'read_only': True}}


class ExperimentChartViewSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentChartView
        exclude = []
        extra_kwargs = {'experiment': {'read_only': True}}


class ExperimentLastMetricSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'last_metric',
            'started_at',
            'finished_at',
        )


class ExperimentDeclarationsSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'declarations',
        )


class ExperimentSerializer(serializers.ModelSerializer, BuildMixin, ProjectMixin, UserMixin):
    uuid = fields.UUIDField(format='hex', read_only=True)
    original = fields.SerializerMethodField()
    user = fields.SerializerMethodField()
    experiment_group = fields.SerializerMethodField()
    project = fields.SerializerMethodField()
    build_job = fields.SerializerMethodField()
    started_at = fields.DateTimeField(read_only=True)
    finished_at = fields.DateTimeField(read_only=True)

    class Meta:
        model = Experiment
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'user',
            'description',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'last_status',
            'original',
            'cloning_strategy',
            'project',
            'experiment_group',
            'build_job',
            'backend',
            'is_managed',
            'framework',
            'tags',
            'last_metric',
            'declarations',
        )
        extra_kwargs = {
            'original_experiment': {'write_only': True},
            'is_managed': {'read_only': True}
        }

    def get_original(self, obj):
        return obj.original_experiment.unique_name if obj.original_experiment else None

    def get_experiment_group(self, obj):
        return obj.experiment_group.unique_name if obj.experiment_group else None


class BookmarkedExperimentSerializer(ExperimentSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'experiment'

    class Meta(ExperimentSerializer.Meta):
        fields = ExperimentSerializer.Meta.fields + ('bookmarked',)


class ExperimentDetailSerializer(BookmarkedExperimentSerializer,
                                 IsManagedMixin,
                                 TagsSerializerMixin,
                                 DataRefsSerializerMixin,
                                 TensorboardSerializerMixin,
                                 NamesMixin):
    resources = fields.SerializerMethodField()
    num_jobs = fields.SerializerMethodField()
    last_metric = fields.SerializerMethodField()
    tensorboard = fields.SerializerMethodField()
    merge = fields.BooleanField(write_only=True, required=False)

    class Meta(BookmarkedExperimentSerializer.Meta):
        fields = BookmarkedExperimentSerializer.Meta.fields + (
            'original_experiment',
            'merge',
            'readme',
            'config',
            'resources',
            'run_env',
            'data_refs',
            'num_jobs',
            'is_clone',
            'code_reference',
            'tensorboard',
            'has_tensorboard',
        )
        extra_kwargs = {'config': {'read_only': True},
                        **BookmarkedExperimentSerializer.Meta.extra_kwargs}

    def get_resources(self, obj):
        resources = obj.resources
        if resources and not isinstance(resources, dict):
            resources = resources.to_dict()
        return resources

    def get_num_jobs(self, obj):
        return obj.jobs__count

    def get_last_metric(self, obj):
        # TODO: Add type handling for experiments
        return {k: round(v, 7) for k, v in obj.last_metric.items()} if obj.last_metric else None

    def validated_declarations(self, validated_data, declarations):
        new_declarations = validated_data.get('declarations')
        if not validated_data.get('merge') or not declarations or not new_declarations:
            # This is the default behavior
            return validated_data

        declarations.update(new_declarations)
        validated_data['declarations'] = declarations
        return validated_data

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_data_refs(validated_data=validated_data,
                                                  data_refs=instance.data_refs)
        validated_data = self.validated_declarations(validated_data=validated_data,
                                                     declarations=instance.declarations)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=Experiment.all)

        return super().update(instance=instance, validated_data=validated_data)


class ExperimentCreateSerializer(serializers.ModelSerializer,
                                 IsManagedMixin,
                                 NamesMixin,
                                 ProjectMixin,
                                 UserMixin):
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = (
            'id',
            'unique_name',
            'project',
            'user',
            'name',
            'description',
            'readme',
            'original_experiment',
            'experiment_group',
            'build_job',
            'config',
            'declarations',
            'backend',
            'framework',
            'is_managed',
            'run_env',
            'data_refs',
            'tags',
        )
        extra_kwargs = {'unique_name': {'read_only': True}}

    def validate_config(self, config):
        """We only validate the config if passed.

        Also we use the ExperimentSpecification to check if this config was
        intended as an experiment.
        """
        # config is optional
        if not config:
            return config

        validate_experiment_spec_config(config)
        return config

    def validate(self, attrs):
        self.check_if_entity_is_managed(attrs=attrs, entity_name='Experiment')
        return attrs

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=Experiment.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)
