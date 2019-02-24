from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.names import NamesMixin
from api.utils.serializers.tags import TagsSerializerMixin
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupChartView,
    ExperimentGroupStatus
)
from libs.spec_validation import validate_group_spec_content


class ExperimentGroupStatusSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentGroupStatus
        extra_kwargs = {'experiment_group': {'read_only': True}}
        exclude = []


class ExperimentGroupSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    project = fields.SerializerMethodField()
    user = fields.SerializerMethodField()

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
            'group_type',
            'project',
            'created_at',
            'updated_at',
            'started_at',
            'finished_at',
            'tags',
            'concurrency',
            'search_algorithm'
        )

        extra_kwargs = {'group_type': {'read_only': True}}

    def get_project(self, obj: ExperimentGroup):
        return obj.project.unique_name

    def get_user(self, obj: ExperimentGroup):
        return obj.user.username


class BookmarkedExperimentGroupSerializer(ExperimentGroupSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'experimentgroup'

    class Meta(ExperimentGroupSerializer.Meta):
        fields = ExperimentGroupSerializer.Meta.fields + ('bookmarked',)


class ExperimentGroupDetailSerializer(BookmarkedExperimentGroupSerializer,
                                      TagsSerializerMixin,
                                      NamesMixin):
    num_experiments = fields.SerializerMethodField()
    num_pending_experiments = fields.SerializerMethodField()
    num_running_experiments = fields.SerializerMethodField()
    num_scheduled_experiments = fields.SerializerMethodField()
    num_succeeded_experiments = fields.SerializerMethodField()
    num_failed_experiments = fields.SerializerMethodField()
    num_stopped_experiments = fields.SerializerMethodField()
    current_iteration = fields.SerializerMethodField()
    merge = fields.BooleanField(write_only=True, required=False)

    class Meta(BookmarkedExperimentGroupSerializer.Meta):
        fields = BookmarkedExperimentGroupSerializer.Meta.fields + (
            'merge',
            'readme',
            'current_iteration',
            'content',
            'hptuning',
            'has_tensorboard',
            'num_experiments',
            'num_pending_experiments',
            'num_running_experiments',
            'num_scheduled_experiments',
            'num_succeeded_experiments',
            'num_failed_experiments',
            'num_stopped_experiments',
        )

    def get_num_experiments(self, obj: ExperimentGroup) -> int:
        return obj.group_experiments.count()

    def get_num_pending_experiments(self, obj: ExperimentGroup) -> int:
        return obj.pending_experiments.count()

    def get_num_running_experiments(self, obj: ExperimentGroup) -> int:
        return obj.running_experiments.count()

    def get_num_scheduled_experiments(self, obj: ExperimentGroup) -> int:
        return obj.scheduled_experiments.count()

    def get_num_succeeded_experiments(self, obj: ExperimentGroup) -> int:
        return obj.succeeded_experiments.count()

    def get_num_failed_experiments(self, obj: ExperimentGroup) -> int:
        return obj.failed_experiments.count()

    def get_num_stopped_experiments(self, obj: ExperimentGroup) -> int:
        return obj.stopped_experiments.count()

    def get_current_iteration(self, obj: ExperimentGroup):
        return obj.iterations.count()

    def validate_content(self, content):
        validate_group_spec_content(content)
        return content

    def validate(self, attrs):
        if self.initial_data.get('check_specification') and not attrs.get('content'):
            raise ValidationError('Experiment group expects `content`.')
        return attrs

    def update(self, instance: ExperimentGroup, validated_data) -> ExperimentGroup:
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_name(validated_data,
                                             project=instance.project,
                                             query=ExperimentGroup.all)

        return super().update(instance=instance, validated_data=validated_data)


class ExperimentGroupCreateSerializer(ExperimentGroupSerializer, NamesMixin):

    class Meta(ExperimentGroupSerializer.Meta):
        fields = ExperimentGroupSerializer.Meta.fields + (
            'readme',
            'search_algorithm',
            'content',
        )

    def validate_content(self, content):
        # This is optional
        if not content:
            return content
        validate_group_spec_content(content)
        return content

    def validate(self, attrs):
        if self.initial_data.get('check_specification') and not attrs.get('content'):
            raise ValidationError('Experiment group expects `content`.')
        return attrs

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=ExperimentGroup.all)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)


class ExperimentGroupChartViewSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ExperimentGroupChartView
        exclude = []
        extra_kwargs = {'experiment_group': {'read_only': True}}
