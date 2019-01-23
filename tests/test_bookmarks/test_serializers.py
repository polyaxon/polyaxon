import pytest

from api.bookmarks.serializers import (
    BuildJobBookmarkSerializer,
    ExperimentBookmarkSerializer,
    ExperimentGroupBookmarkSerializer,
    JobBookmarkSerializer,
    ProjectBookmarkSerializer
)
from api.build_jobs.serializers import BuildJobSerializer
from api.experiment_groups.serializers import ExperimentGroupSerializer
from api.experiments.serializers import ExperimentSerializer
from api.jobs.serializers import JobSerializer
from api.projects.serializers import ProjectSerializer
from db.models.bookmarks import Bookmark
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.projects import Project
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from tests.utils import BaseTest


@pytest.mark.bookmarks_mark
class TestBookmarkSerializer(BaseTest):
    serializer_class = None
    model_serializer_class = None
    model_class = None
    factory_class = None
    expected_keys = {
        'content_object',
    }

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.obj1 = Bookmark.objects.create(
            user=self.user,
            content_object=self.factory_class())  # pylint:disable=not-callable
        self.obj2 = Bookmark.objects.create(
            user=self.user,
            content_object=self.factory_class())  # pylint:disable=not-callable

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data  # pylint:disable=not-callable

        assert set(data.keys()) == self.expected_keys
        assert data.pop('content_object') == self.model_serializer_class(  # noqa
            self.obj1.content_object).data

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(Bookmark.objects.all(), many=True).data  # noqa
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.bookmarks_mark
class TestBookmarkBuildJobSerializer(TestBookmarkSerializer):
    serializer_class = BuildJobBookmarkSerializer
    model_serializer_class = BuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory


@pytest.mark.bookmarks_mark
class TestBookmarkJobSerializer(TestBookmarkSerializer):
    serializer_class = JobBookmarkSerializer
    model_serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory


@pytest.mark.bookmarks_mark
class TestBookmarkExperimentSerializer(TestBookmarkSerializer):
    serializer_class = ExperimentBookmarkSerializer
    model_serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory


@pytest.mark.bookmarks_mark
class TestBookmarkExperimentGroupSerializer(TestBookmarkSerializer):
    serializer_class = ExperimentGroupBookmarkSerializer
    model_serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory


@pytest.mark.bookmarks_mark
class TestBookmarkProjectSerializer(TestBookmarkSerializer):
    serializer_class = ProjectBookmarkSerializer
    model_serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory


del TestBookmarkSerializer
