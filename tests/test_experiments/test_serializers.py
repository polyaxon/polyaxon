from unittest.mock import patch

from django.test import override_settings

from experiments.models import Experiment, ExperimentJob, ExperimentStatus
from experiments.serializers import (
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from experiments.statuses import ExperimentLifeCycle
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentStatusFactory
)
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class TestExperimentSerializer(BaseTest):
    serializer_class = ExperimentSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'uuid', 'user', 'unique_name', 'sequence', 'description', 'created_at', 'updated_at',
        'last_status', 'last_metric', 'started_at', 'finished_at', 'is_running', 'is_done',
        'is_clone', 'project', 'project_name', 'experiment_group',
        'experiment_group_name', 'num_jobs', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('project_name') == self.obj1.project.unique_name
        assert data.pop('experiment_group') == (self.obj1.experiment_group.uuid.hex
                                                if self.obj1.experiment_group else None)
        assert data.pop('experiment_group_name') == (self.obj1.experiment_group.unique_name
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


@override_settings(DEPLOY_RUNNER=False)
class TestExperimentDetailSerializer(BaseTest):
    serializer_class = ExperimentDetailSerializer
    model_class = Experiment
    factory_class = ExperimentFactory
    expected_keys = {
        'uuid',
        'unique_name',
        'created_at',
        'updated_at',
        'project',
        'project_name',
        'user',
        'sequence',
        'last_status',
        'last_metric',
        'description',
        'experiment_group',
        'experiment_group_name',
        'config',
        'started_at',
        'finished_at',
        'is_running',
        'is_done',
        'is_clone',
        'original',
        'num_jobs',
        'declarations',
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
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('project_name') == self.obj1.project.unique_name
        assert data.pop('original') == (self.obj1.original_experiment.unique_name if
                                        self.obj1.original_experiment else None)
        assert data.pop('experiment_group') == (self.obj1.experiment_group.uuid.hex
                                                if self.obj1.experiment_group else None)
        assert data.pop('experiment_group_name') == (self.obj1.experiment_group.unique_name
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


class TestExperimentJobSerializer(BaseTest):
    serializer_class = ExperimentJobSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    expected_keys = {
        'uuid', 'unique_name', 'sequence', 'role', 'experiment', 'experiment_name',
        'last_status', 'is_running', 'is_done', 'created_at', 'updated_at',
        'started_at', 'finished_at', 'resources', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.uuid.hex
        assert data.pop('experiment_name') == self.obj1.experiment.unique_name
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
    serializer_class = ExperimentJobDetailSerializer
    model_class = ExperimentJob
    factory_class = ExperimentJobFactory
    expected_keys = {
        'uuid', 'unique_name', 'sequence', 'role', 'experiment', 'experiment_name',
        'definition', 'last_status', 'is_running', 'is_done', 'created_at', 'updated_at',
        'started_at', 'finished_at', 'resources', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('experiment') == self.obj1.experiment.uuid.hex
        assert data.pop('experiment_name') == self.obj1.experiment.unique_name
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


@override_settings(DEPLOY_RUNNER=False)
class TestExperimentStatusSerializer(BaseTest):
    serializer_class = ExperimentStatusSerializer
    model_class = ExperimentStatus
    factory_class = ExperimentStatusFactory
    expected_keys = {'uuid', 'experiment', 'created_at', 'status', 'message', }

    def setUp(self):
        super().setUp()
        with patch.object(Experiment, 'set_status') as _:
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
