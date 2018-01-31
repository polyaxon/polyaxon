# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from projects.models import Project, ExperimentGroup
from projects.serializers import (
    ProjectSerializer,
    ExperimentGroupSerializer,
    ProjectDetailSerializer,
    ExperimentGroupDetailSerializer,
)
from factories.factory_projects import ProjectFactory, ExperimentGroupFactory

from tests.utils import BaseTest


class TestExperimentGroupSerializer(BaseTest):
    serializer_class = ExperimentGroupSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    expected_keys = {
        'uuid', 'sequence', 'unique_name', 'description', 'project', 'project_name',
        'user', 'created_at',  'updated_at', 'concurrency', 'num_experiments',
        'num_pending_experiments', 'num_running_experiments', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('project_name') == self.obj1.project.unique_name
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_pending_experiments') == len(self.obj1.pending_experiments)
        assert data.pop('num_running_experiments') == len(self.obj1.running_experiments)

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestExperimentGroupDetailSerializer(BaseTest):
    serializer_class = ExperimentGroupDetailSerializer
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    expected_keys = {
        'uuid', 'sequence', 'unique_name', 'description', 'content', 'project', 'project_name',
        'user', 'created_at',  'updated_at', 'concurrency', 'num_experiments',
        'num_pending_experiments', 'num_running_experiments', 'num_scheduled_experiments',
        'num_succeeded_experiments', 'num_failed_experiments', 'num_stopped_experiments'}

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('project_name') == self.obj1.project.unique_name
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_pending_experiments') == len(self.obj1.pending_experiments)
        assert data.pop('num_running_experiments') == len(self.obj1.running_experiments)
        assert data.pop('num_scheduled_experiments') == len(self.obj1.scheduled_experiments)
        assert data.pop('num_succeeded_experiments') == len(self.obj1.succeeded_experiments)
        assert data.pop('num_failed_experiments') == len(self.obj1.failed_experiments)
        assert data.pop('num_stopped_experiments') == len(self.obj1.stopped_experiments)

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
    expected_keys = {
        'uuid', 'name', 'unique_name', 'description', 'user', 'description', 'created_at',
        'updated_at', 'is_public', 'has_code', 'has_tensorboard', 'has_notebook',
        'num_experiment_groups', 'num_experiments'}

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_experiment_groups') == self.obj1.experiment_groups.count()
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
    expected_keys = {
        'uuid', 'unique_name', 'name', 'description', 'user', 'description', 'created_at',
        'updated_at', 'is_public', 'experiments', 'experiment_groups', 'has_code',
        'has_tensorboard', 'has_notebook', 'num_experiment_groups', 'num_experiments'}

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
        assert len(data.pop('experiments')) == self.obj1.experiments.count()
        assert len(data.pop('experiment_groups')) == self.obj1.experiment_groups.count()
        assert data.pop('num_experiments') == self.obj1.experiments.count()
        assert data.pop('num_experiment_groups') == self.obj1.experiment_groups.count()

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
