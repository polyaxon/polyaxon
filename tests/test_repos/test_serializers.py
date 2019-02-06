import pytest

from api.repos.serializers import ExternalRepoSerializer, RepoSerializer
from db.models.repos import ExternalRepo, Repo
from factories.factory_repos import ExternalRepoFactory, RepoFactory
from tests.utils import BaseTest


@pytest.mark.repos_mark
class TestRepoSerializer(BaseTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    expected_keys = {'project', 'created_at', 'updated_at', 'is_public', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('project') == self.obj1.project.name

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.repos_mark
class TestExternalRepoSerializer(BaseTest):
    serializer_class = ExternalRepoSerializer
    model_class = ExternalRepo
    factory_class = ExternalRepoFactory
    expected_keys = {'project', 'created_at', 'updated_at', 'is_public', 'git_url', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class(git_url='https://github.com/polyaxon/empty.git')
        self.obj2 = self.factory_class(git_url='https://github.com/polyaxon/empty.git')

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('project') == self.obj1.project.name

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
