from rest_framework import fields, serializers

from models.repos import Repo


class RepoSerializer(serializers.ModelSerializer):
    project = fields.SerializerMethodField()

    class Meta:
        model = Repo
        fields = ('project', 'created_at', 'updated_at', 'is_public', )

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.name
