import pytest

from api.projects.serializers import ProjectDetailSerializer, ProjectSerializer
from db.models.projects import Project
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.projects_mark
class TestProjectSerializer(BaseTest):
    DISABLE_RUNNER = True
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
        'description',
        'created_at',
        'updated_at',
        'is_public',
        'has_code',
        'tags',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.projects_mark
class TestProjectDetailSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    expected_keys = {
        'id',
        'uuid',
        'unique_name',
        'name',
        'description',
        'user',
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
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_experiment_groups') == self.obj1.experiment_groups.count()
        assert data.pop('num_independent_experiments') == self.obj1.experiments.filter(
            experiment_group__isnull=True).count()
        assert data.pop('num_jobs') == self.obj1.jobs.count()
        assert data.pop('num_builds') == self.obj1.build_jobs.count()

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
