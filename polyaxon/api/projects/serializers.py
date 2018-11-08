from rest_framework import fields, serializers

from api.utils.serializers.bookmarks import BookmarkedSerializerMixin
from api.utils.serializers.tags import TagsSerializerMixin
from db.models.projects import Project


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    owner = fields.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'uuid',
            'user',
            'name',
            'owner',
            'unique_name',
            'description',
            'tags',
            'created_at',
            'updated_at',
            'is_public',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_owner(self, obj):
        return obj.owner_details


class BookmarkedProjectSerializer(ProjectSerializer, BookmarkedSerializerMixin):
    bookmarked_model = 'project'

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('bookmarked',)


class ProjectDetailSerializer(BookmarkedProjectSerializer, TagsSerializerMixin):
    num_experiment_groups = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()
    num_independent_experiments = fields.SerializerMethodField()
    num_jobs = fields.SerializerMethodField()
    num_builds = fields.SerializerMethodField()
    merge = fields.BooleanField(write_only=True, required=False)

    class Meta(BookmarkedProjectSerializer.Meta):
        fields = BookmarkedProjectSerializer.Meta.fields + (
            'merge',
            'readme',
            'has_code',
            'has_tensorboard',
            'has_notebook',
            'num_experiment_groups',
            'num_independent_experiments',
            'num_experiments',
            'num_jobs',
            'num_builds',
        )

    def get_num_independent_experiments(self, obj):
        return obj.experiments.filter(experiment_group__isnull=True).count()

    def get_num_experiment_groups(self, obj):
        return obj.experiment_groups.count()

    def get_num_experiments(self, obj):
        return obj.experiments.count()

    def get_num_jobs(self, obj):
        return obj.jobs.count()

    def get_num_builds(self, obj):
        return obj.build_jobs.count()

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)

        return super().update(instance=instance, validated_data=validated_data)
