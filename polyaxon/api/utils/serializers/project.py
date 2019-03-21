from rest_framework import serializers


class ProjectMixin(serializers.Serializer):

    def get_project(self, obj):
        return obj.project.unique_name
