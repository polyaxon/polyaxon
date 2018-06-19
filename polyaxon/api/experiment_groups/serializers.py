from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from db.models.experiment_groups import ExperimentGroup
from libs.spec_validation import validate_group_spec_content
from polyaxon_schemas.utils import SearchAlgorithms


class ExperimentGroupSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    project = fields.SerializerMethodField()
    project_name = fields.SerializerMethodField()
    user = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()
    num_pending_experiments = fields.SerializerMethodField()
    num_running_experiments = fields.SerializerMethodField()

    class Meta:
        model = ExperimentGroup
        fields = (
            'id',
            'uuid',
            'name',
            'unique_name',
            'user',
            'description',
            'last_status',
            'is_running',
            'is_done',
            'project',
            'project_name',
            'created_at',
            'updated_at',
            'concurrency',
            'tags',
            'search_algorithm',
            'has_tensorboard',
            'num_experiments',
            'num_pending_experiments',
            'num_running_experiments',)

    def get_project(self, obj):
        return obj.project.uuid.hex

    def get_project_name(self, obj):
        return obj.project.unique_name

    def get_user(self, obj):
        return obj.user.username

    def get_num_experiments(self, obj):
        return obj.experiments.count()

    def get_num_pending_experiments(self, obj):
        return obj.pending_experiments.count()

    def get_num_running_experiments(self, obj):
        return obj.running_experiments.count()


class ExperimentGroupDetailSerializer(ExperimentGroupSerializer):
    num_scheduled_experiments = fields.SerializerMethodField()
    num_succeeded_experiments = fields.SerializerMethodField()
    num_failed_experiments = fields.SerializerMethodField()
    num_stopped_experiments = fields.SerializerMethodField()

    class Meta(ExperimentGroupSerializer.Meta):
        fields = ExperimentGroupSerializer.Meta.fields + (
            'current_iteration',
            'content',
            'hptuning',
            'started_at',
            'finished_at',
            'num_scheduled_experiments',
            'num_succeeded_experiments',
            'num_failed_experiments',
            'num_stopped_experiments')

    def get_num_scheduled_experiments(self, obj):
        return obj.scheduled_experiments.count()

    def get_num_succeeded_experiments(self, obj):
        return obj.succeeded_experiments.count()

    def get_num_failed_experiments(self, obj):
        return obj.failed_experiments.count()

    def get_num_stopped_experiments(self, obj):
        return obj.stopped_experiments.count()

    def validate_content(self, content):
        validate_group_spec_content(content)
        return content

    def validate(self, attrs):
        if self.initial_data.get('check_specification') and not attrs.get('content'):
            raise ValidationError('Experiment group expects `content`.')
        return attrs
