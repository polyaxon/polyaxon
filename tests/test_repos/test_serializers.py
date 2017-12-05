# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from repos.models import Repo
from repos.serializers import RepoSerializer

from tests.factories.factory_repos import RepoFactory
from tests.utils import BaseTest


class TestRepoSerializer(BaseTest):
    serializer_class = RepoSerializer
    model_class = Repo
    factory_class = RepoFactory
    expected_keys = {'uuid', 'name', 'user', 'created_at', 'updated_at', 'is_public', }

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
