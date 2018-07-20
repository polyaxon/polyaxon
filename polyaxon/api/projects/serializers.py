from rest_framework import fields, serializers

from db.models.bookmarks import Bookmark
from db.models.projects import Project


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'uuid',
            'user',
            'name',
            'unique_name',
            'description',
            'tags',
            'created_at',
            'updated_at',
            'is_public',
            'has_code',
        )

    def get_user(self, obj):
        return obj.user.username


class ProjectDetailSerializer(ProjectSerializer):
    num_experiment_groups = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()
    num_independent_experiments = fields.SerializerMethodField()
    num_jobs = fields.SerializerMethodField()
    num_builds = fields.SerializerMethodField()
    bookmarked = fields.SerializerMethodField()

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + (
            'has_tensorboard',
            'has_notebook',
            'num_experiment_groups',
            'num_independent_experiments',
            'num_experiments',
            'num_jobs',
            'num_builds',
            'bookmarked',
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

    def get_bookmarked(self, obj):
        return Bookmark.objects.filter(
            content_type__model='project',
            object_id=obj.id,
            enabled=True).exists()
