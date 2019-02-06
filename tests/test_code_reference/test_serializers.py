import pytest

from api.code_reference.serializers import CodeReferenceSerializer
from db.models.repos import CodeReference
from factories.factory_code_reference import CodeReferenceFactory
from tests.utils import BaseTest


@pytest.mark.experiments_mark
class TestCodeReferenceSerializer(BaseTest):
    serializer_class = CodeReferenceSerializer
    model_class = CodeReference
    factory_class = CodeReferenceFactory
    expected_keys = {
        'id',
        'repo',
        'external_repo',
        'branch',
        'commit',
        'head',
        'is_dirty',
        'git_url'
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys

        assert data.pop('repo') == self.obj1.repo.id if self.obj1.repo else None
        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
