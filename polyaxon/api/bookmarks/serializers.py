from rest_framework import serializers

from api.build_jobs.serializers import BuildJobSerializer
from api.experiment_groups.serializers import ExperimentGroupSerializer
from api.experiments.serializers import ExperimentSerializer
from api.jobs.serializers import JobSerializer
from api.projects.serializers import ProjectSerializer
from db.models.bookmarks import Bookmark


class BuildJobBookmarkSerializer(serializers.ModelSerializer):
    content_object = BuildJobSerializer()

    class Meta:
        model = Bookmark
        exclude = []


class JobBookmarkSerializer(serializers.ModelSerializer):
    content_object = JobSerializer()

    class Meta:
        model = Bookmark
        exclude = []


class ExperimentBookmarkSerializer(serializers.ModelSerializer):
    content_object = ExperimentSerializer()

    class Meta:
        model = Bookmark
        exclude = []


class ExperimentGroupBookmarkSerializer(serializers.ModelSerializer):
    content_object = ExperimentGroupSerializer()

    class Meta:
        model = Bookmark
        exclude = []


class ProjectBookmarkSerializer(serializers.ModelSerializer):
    content_object = ProjectSerializer()

    class Meta:
        model = Bookmark
        exclude = []
