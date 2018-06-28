from unittest.mock import patch

import pytest

from api.experiments.serializers import (
    ExperimentDeclarationsSerializer,
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentLastMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from constants.experiments import ExperimentLifeCycle
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment, ExperimentStatus
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentStatusFactory
)
from polyaxon_schemas.polyaxonfile.specification import ExperimentSpecification
from tests.utils import BaseTest


@pytest.mark.experiments_mark
class TestExperimentLastMetricSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentLastMetricSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'unique_name',
        'last_metric',
        'started_at',
        'finished_at',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('last_metric') == self.obj1.last_metric
        data.pop('started_at', None)
        data.pop('finished_at', None)

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.experiments_mark
class TestExperimentDeclarationsSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentDeclarationsSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'unique_name',
        'declarations',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        data.pop('started_at', None)
        data.pop('finished_at', None)

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.experiments_mark
class TestExperimentSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'user',
        'unique_name',
        'description',
        'created_at',
        'updated_at',
        'last_status',
        'started_at',
        'finished_at',
        'tags',
        'original',
        'project',
        'experiment_group',
        'build_job',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('project') == self.obj1.project.unique_name
        assert data.pop('experiment_group') == (self.obj1.experiment_group.unique_name
                                                if self.obj1.experiment_group else None)
        assert data.pop('build_job') == (self.obj1.build_job.unique_name
                                         if self.obj1.build_job else None)
        assert data.pop('original') == (self.obj1.original_experiment.unique_name if
                                        self.obj1.original_experiment else None)
        assert data.pop('last_status') == self.obj1.last_status
        data.pop('created_at')
        data.pop('updated_at')
        data.pop('started_at', None)
        data.pop('finished_at', None)

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

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.experiments_mark
class TestExperimentDetailSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'unique_name',
        'created_at',
        'updated_at',
        'project',
        'user',
        'last_status',
        'last_metric',
        'description',
        'experiment_group',
        'config',
        'started_at',
        'finished_at',
        'is_clone',
        'tags',
        'has_tensorboard',
        'build_job',
        'original',
        'num_jobs',
        'declarations',
        'resources',
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
        assert data.pop('project') == self.obj1.project.unique_name
        assert data.pop('build_job') == (self.obj1.build_job.unique_name if
                                         self.obj1.build_job else None)
        assert data.pop('original') == (self.obj1.original_experiment.unique_name if
                                        self.obj1.original_experiment else None)
        assert data.pop('experiment_group') == (self.obj1.experiment_group.unique_name
                                                if self.obj1.experiment_group else None)
        assert data.pop('last_status') == self.obj1.last_status
        assert data.pop('last_metric') == self.obj1.last_metric
        assert data.pop('num_jobs') == self.obj1.jobs.count()
        data.pop('created_at')
        data.pop('updated_at')
        data.pop('started_at', None)
        data.pop('finished_at', None)

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

    def test_serialize_cluster_resources(self):
        spec_content = """---
            version: 1

            kind: experiment

            environment:
              resources:
                cpu:
                  requests: 2
                  limits: 4
                memory:
                  requests: 4096
                  limits: 10240
              pytorch:
                n_workers: 2
                default_worker_resources:
                  cpu:
                    requests: 2
                    limits: 4
                  memory:
                    requests: 4096
                    limits: 10240

            run:
              image: my_image
              cmd: video_prediction_train --model=DNA --num_masks=1
        """
        spec = ExperimentSpecification.read(spec_content)

        obj = self.factory_class(config=spec.parsed_data)
        self.serializer_class(obj).data  # pylint:disable=expression-not-assigned


@pytest.mark.experiments_mark
class TestExperimentJobSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    expected_keys = {
        'id',
        'uuid',
        'unique_name',
        'role',
        'experiment',
        'last_status',
        'created_at',
        'updated_at',
        'started_at',
        'finished_at',
        'resources',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.id
        data.pop('created_at')
        data.pop('updated_at')
        data.pop('started_at', None)
        data.pop('finished_at', None)

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


class TestExperimentJobDetailsSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentJobDetailSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    expected_keys = {
        'id',
        'uuid',
        'unique_name',
        'role',
        'experiment',
        'definition',
        'last_status',
        'created_at',
        'updated_at',
        'started_at',
        'finished_at',
        'resources',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.id
        data.pop('created_at')
        data.pop('updated_at')
        data.pop('started_at', None)
        data.pop('finished_at', None)

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.experiments_mark
class TestExperimentStatusSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    expected_keys = {'id', 'uuid', 'experiment', 'created_at', 'status', 'message', }

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:  # noqa
            self.obj1 = self.factory_class()
            self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.id
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
