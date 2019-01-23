import pytest

from api.searches.serializers import SearchSerializer
from constants import content_types
from db.models.searches import Search
from factories.factory_searches import SearchFactory
from factories.factory_users import UserFactory
from tests.utils import BaseTest


@pytest.mark.search_mark
class TestSearchSerializer(BaseTest):
    model_class = Search
    expected_keys = {
        'id',
        'name',
        'query',
        'meta'
    }

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.obj1 = SearchFactory()
        self.obj2 = SearchFactory(content_type=content_types.BUILD_JOB)

    def test_serialize_one(self):
        data = SearchSerializer(self.obj1).data

        assert set(data.keys()) == self.expected_keys

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = SearchSerializer(Search.objects.all(), many=True).data  # noqa
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
