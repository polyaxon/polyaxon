# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from experiments.models import ExperimentStatus, Experiment, ExperimentJob
from experiments.serializers import (
    ExperimentStatusSerializer,
    ExperimentSerializer,
    ExperimentDetailSerializer,
    ExperimentJobSerializer,
)
from spawner.utils.constants import ExperimentLifeCycle

from factories.factory_experiments import (
    ExperimentStatusFactory,
    ExperimentFactory,
    ExperimentJobFactory,
)
from tests.utils import BaseTest


class TestExperimentSerializer(BaseTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {'uuid', 'user', 'name', 'created_at', 'updated_at',
                     'last_status', 'started_at', 'finished_at', 'is_clone', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('last_status') == self.obj1.last_status
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_one_with_status(self):
        obj1 = self.factory_class()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is None
        assert data['finished_at'] is None

        ExperimentStatus.objects.create(experiment=obj1, status=ExperimentLifeCycle.STARTING)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        ExperimentStatus.objects.create(experiment=obj1, status=ExperimentLifeCycle.SUCCEEDED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is not None

    def test_cloned(self):
        obj1 = self.factory_class()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['is_clone'] is False

        obj2 = self.factory_class()
        obj1.original_experiment = obj2
        obj1.save()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['is_clone'] is True

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestExperimentDetailSerializer(BaseTest):
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'uuid',
        'created_at',
        'updated_at',
        'cluster',
        'project',
        'user',
        'name',
        'last_status',
        'description',
        'spec',
        'config',
        'original_experiment',
        'jobs',
        'started_at',
        'finished_at',
        'is_clone'
    }

    def setUp(self):
        super().setUp()
        self.job1 = ExperimentJobFactory()
        self.obj1 = self.job1.experiment
        self.obj2 = ExperimentJobFactory()
        self.obj2 = self.obj2.experiment

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('cluster') == self.obj1.cluster.uuid.hex
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('spec') == (self.obj1.spec.uuid.hex if self.obj1.spec else None)
        assert data.pop('last_status') == self.obj1.last_status
        assert len(data.pop('jobs')) == 1
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_one_with_status(self):
        obj1 = self.factory_class()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is None
        assert data['finished_at'] is None

        ExperimentStatus.objects.create(experiment=obj1, status=ExperimentLifeCycle.STARTING)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        ExperimentStatus.objects.create(experiment=obj1, status=ExperimentLifeCycle.SUCCEEDED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is not None

    def test_cloned(self):
        obj1 = self.factory_class()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['is_clone'] is False

        obj2 = self.factory_class()
        obj1.original_experiment = obj2
        obj1.save()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['is_clone'] is True

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestExperimentJobSerializer(BaseTest):
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    expected_keys = {'uuid', 'experiment', 'definition', 'created_at', 'updated_at', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.uuid.hex
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestExperimentStatusSerializer(BaseTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    expected_keys = {'uuid', 'experiment', 'created_at', 'status', }

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
            with patch('experiments.tasks.start_experiment.delay') as _:
                self.obj1 = self.factory_class()
                self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.uuid.hex
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
