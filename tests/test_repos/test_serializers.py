from factories.factory_repos import RepoFactory
from repos.models import Repo
from repos.serializers import RepoSerializer
from tests.utils import BaseTest


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
