# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from projects.models import Project, ExperimentGroup
from projects.serializers import ProjectSerializer, ExperimentGroupSerializer, ProjectDetailSerializer
from factories.factory_clusters import ClusterFactory
from factories.factory_projects import ProjectFactory, ExperimentGroupFactory

from tests.utils import BaseTest


class TestExperimentGroupSerializer(BaseTest):
    serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    expected_keys = {'uuid', 'name', 'description', 'content', 'project', 'user', }

    def setUp(self):
        super().setUp()
        cluster = ClusterFactory()
        self.obj1 = self.factory_class(user=cluster.user)
        self.obj2 = self.factory_class(user=cluster.user)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('user') == self.obj1.user.username

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestProjectSerializer(BaseTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    expected_keys = {'uuid', 'name', 'description', 'user', 'description', 'created_at',
                     'updated_at', 'is_public', 'has_code', }

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


class TestProjectDetailSerializer(BaseTest):
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    expected_keys = {'uuid', 'name', 'description', 'user', 'description', 'created_at',
                     'updated_at', 'is_public', 'experiments', 'experiment_groups', 'has_code', }

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
        assert len(data.pop('experiments')) == 0
        assert len(data.pop('experiment_groups')) == 0

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
