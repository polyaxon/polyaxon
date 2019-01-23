import pytest

from api.projects import queries
from api.projects.serializers import (
    BookmarkedProjectSerializer,
    ProjectDetailSerializer,
    ProjectSerializer
)
from db.models.projects import Project
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.projects_mark
class TestProjectSerializer(BaseTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'unique_name',
        'description',
        'user',
        'owner',
        'description',
        'created_at',
        'updated_at',
        'is_public',
        'tags',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = queries.projects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('owner') == self.obj1.owner.name

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(queries.projects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.projects_mark
class TestBookmarkedProjectSerializer(TestProjectSerializer):
    serializer_class = BookmarkedProjectSerializer
    expected_keys = TestProjectSerializer.expected_keys | {'bookmarked', }

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('owner') == self.obj1.owner.name
        assert data.pop('bookmarked') is False

        for k, v in data.items():
            assert getattr(self.obj1, k) == v


@pytest.mark.projects_mark
class TestProjectDetailSerializer(BaseTest):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    expected_keys = {
        'id',
        'uuid',
        'unique_name',
        'name',
        'description',
        'readme',
        'user',
        'owner',
        'created_at',
        'updated_at',
        'is_public',
        'tags',
        'has_code',
        'has_tensorboard',
        'has_notebook',
        'num_experiment_groups',
        'num_independent_experiments',
        'num_experiments',
        'num_jobs',
        'num_builds',
        'bookmarked',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1_query = queries.projects_details.get(id=self.obj1.id)
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('owner') == self.obj1.owner.name
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_experiment_groups') == self.obj1.experiment_groups.count()
        assert data.pop('num_independent_experiments') == self.obj1.experiments.filter(
            experiment_group__isnull=True).count()
        assert data.pop('num_jobs') == self.obj1.jobs.count()
        assert data.pop('num_builds') == self.obj1.build_jobs.count()
        assert data.pop('bookmarked') is False

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(queries.projects_details.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
