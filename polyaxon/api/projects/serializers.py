from rest_framework import fields, serializers

from db.models.projects import Project


class ProjectSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()
    num_experiment_groups = fields.SerializerMethodField()
    num_experiments = fields.SerializerMethodField()

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
            'has_tensorboard',
            'has_notebook',
            'num_experiment_groups',
            'num_experiments',
        )

    def get_user(self, obj):
        return obj.user.username

    def get_num_experiment_groups(self, obj):
        return obj.experiment_groups.count()

    def get_num_experiments(self, obj):
        return obj.experiments.count()


class ProjectDetailSerializer(ProjectSerializer):
    num_independent_experiments = fields.SerializerMethodField()

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ('num_independent_experiments',)

    def get_num_independent_experiments(self, obj):
        return obj.experiments.filter(experiment_group__isnull=True).count()
