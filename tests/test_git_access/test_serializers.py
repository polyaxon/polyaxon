import pytest

from api.git_access.serializers import GitAccessNameSerializer, GitAccessSerializer
from db.models.git_access import GitAccess
from factories.factory_git_access import GitAccessFactory
from tests.base.case import BaseTest


@pytest.mark.git_access_mark
class TestGitAccessSerializer(BaseTest):
    serializer_class = GitAccessSerializer
    model_class = GitAccess
    factory_class = GitAccessFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'description',
        'readme',
        'tags',
        'created_at',
        'updated_at',
        'k8s_secret',
        'host'
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = GitAccess.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(GitAccess.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.git_access_mark
class TestGitAccessNameSerializer(BaseTest):
    serializer_class = GitAccessNameSerializer
    model_class = GitAccess
    factory_class = GitAccessFactory
    expected_keys = {
        'id',
        'name',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()  # pylint:disable=not-callable
        self.obj2 = self.factory_class()  # pylint:disable=not-callable

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
