from rest_framework import fields, serializers

from api.utils.serializers.user import UserMixin
from db.models.repos import ExternalRepo, Repo


class RepoSerializer(serializers.ModelSerializer, UserMixin):
    project = fields.SerializerMethodField()

    class Meta:
        model = Repo
        fields = ('project', 'created_at', 'updated_at', 'is_public', )

    def get_project(self, obj):
        return obj.project.name


class ExternalRepoSerializer(serializers.ModelSerializer, UserMixin):
    project = fields.SerializerMethodField()

    class Meta:
        model = ExternalRepo
        fields = ('project', 'created_at', 'updated_at', 'is_public', 'git_url',)

    def get_project(self, obj):
        return obj.project.name
