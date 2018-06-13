from unittest.mock import patch

import pytest

from api.build_jobs.serializers import (
    BuildJobDetailSerializer,
    BuildJobSerializer,
    BuildJobStatusSerializer
)
from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.factory_build_jobs import BuildJobFactory, BuildJobStatusFactory
from tests.utils import BaseTest


@pytest.mark.build_jobs_mark
class TestBuildJobSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = BuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
    expected_keys = {
        'uuid', 'user', 'unique_name', 'sequence', 'description', 'created_at', 'updated_at',
        'last_status', 'started_at', 'finished_at', 'is_running', 'is_done',
        'project', 'project_name', }

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

        BuildJobStatus.objects.create(job=obj1, status=JobLifeCycle.SCHEDULED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        BuildJobStatus.objects.create(job=obj1, status=JobLifeCycle.SUCCEEDED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is not None

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.build_jobs_mark
class TestBuildJobDetailSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = BuildJobDetailSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
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
        'description',
        'config',
        'started_at',
        'finished_at',
        'is_running',
        'is_done',
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
        assert data.pop('user') == self.obj1.user.username
        assert data.pop('project') == self.obj1.project.uuid.hex
        assert data.pop('project_name') == self.obj1.project.unique_name
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

        BuildJobStatus.objects.create(job=obj1, status=JobLifeCycle.SCHEDULED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        BuildJobStatus.objects.create(job=obj1, status=JobLifeCycle.SUCCEEDED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is not None

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.build_jobs_mark
class TestBuildJobStatusSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = BuildJobStatusSerializer
    model_class = BuildJobStatus
    factory_class = BuildJobStatusFactory
    expected_keys = {'uuid', 'job', 'created_at', 'status', 'message', 'details'}

    def setUp(self):
        super().setUp()
        with patch.object(BuildJob, 'set_status') as _:  # noqa
            self.obj1 = self.factory_class()
            self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('job') == self.obj1.job.uuid.hex
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
