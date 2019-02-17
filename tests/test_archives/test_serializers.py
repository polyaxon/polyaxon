import pytest

from api.archives.serializers import (
    ArchivedBuildJobSerializer,
    ArchivedExperimentGroupSerializer,
    ArchivedExperimentSerializer,
    ArchivedJobSerializer,
    ArchivedProjectSerializer
)
from api.build_jobs.serializers import BookmarkedBuildJobSerializer
from api.experiment_groups.serializers import BookmarkedExperimentGroupSerializer
from api.experiments.serializers import BookmarkedExperimentSerializer
from api.jobs.serializers import BookmarkedJobSerializer
from api.projects.serializers import BookmarkedProjectSerializer
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


@pytest.mark.archives_mark
class TestArchiveSerializer(BaseTest):
    serializer_class = None
    model_serializer_class = None
    model_class = None
    factory_class = None

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.obj1 = self.factory_class(deleted=True)  # pylint:disable=not-callable
        self.obj2 = self.factory_class(deleted=True)  # pylint:disable=not-callable

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data  # pylint:disable=not-callable

        assert 'deleted' in set(data.keys())
        data.pop('deleted')
        assert data == self.model_serializer_class(self.obj1).data  # noqa

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.archived.all(), many=True).data  # noqa
        assert len(data) == 2
        for d in data:
            assert 'deleted' in set(d.keys())


@pytest.mark.archives_mark
class TestArchiveBuildJobSerializer(TestArchiveSerializer):
    serializer_class = ArchivedBuildJobSerializer
    model_serializer_class = BookmarkedBuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory


@pytest.mark.archives_mark
class TestArchiveJobSerializer(TestArchiveSerializer):
    serializer_class = ArchivedJobSerializer
    model_serializer_class = BookmarkedJobSerializer
    model_class = Job
    factory_class = JobFactory


@pytest.mark.archives_mark
class TestArchiveExperimentSerializer(TestArchiveSerializer):
    serializer_class = ArchivedExperimentSerializer
    model_serializer_class = BookmarkedExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory


@pytest.mark.archives_mark
class TestArchiveExperimentGroupSerializer(TestArchiveSerializer):
    serializer_class = ArchivedExperimentGroupSerializer
    model_serializer_class = BookmarkedExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory


@pytest.mark.archives_mark
class TestArchiveProjectSerializer(TestArchiveSerializer):
    serializer_class = ArchivedProjectSerializer
    model_serializer_class = BookmarkedProjectSerializer
    model_class = Project
    factory_class = ProjectFactory


del TestArchiveSerializer
