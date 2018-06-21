from unittest.mock import patch

import pytest

from api.jobs.serializers import JobDetailSerializer, JobSerializer, JobStatusSerializer
from constants.jobs import JobLifeCycle
from db.models.jobs import Job, JobStatus
from factories.factory_jobs import JobFactory, JobStatusFactory
from tests.utils import BaseTest


@pytest.mark.jobs_mark
class TestJobSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory
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
        'project',
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
        assert data.pop('build_job') == (
            self.obj1.build_job.unique_name if self.obj1.build_job else None)
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

        JobStatus.objects.create(job=obj1, status=JobLifeCycle.SCHEDULED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        JobStatus.objects.create(job=obj1, status=JobLifeCycle.SUCCEEDED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is not None

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.jobs_mark
class TestJobDetailSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = JobDetailSerializer
    model_class = Job
    factory_class = JobFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'unique_name',
        'created_at',
        'updated_at',
        'project',
        'build_job',
        'user',
        'last_status',
        'description',
        'config',
        'tags',
        'started_at',
        'finished_at',
        'is_clone',
        'build_job',
        'original',
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
        assert data.pop('project') == self.obj1.project.unique_name
        assert data.pop('build_job') == (self.obj1.build_job.unique_name if
                                         self.obj1.build_job else None)
        assert data.pop('original') == (self.obj1.original_job.unique_name if
                                        self.obj1.original_job else None)
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

        JobStatus.objects.create(job=obj1, status=JobLifeCycle.SCHEDULED)
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['started_at'] is not None
        assert data['finished_at'] is None

        JobStatus.objects.create(job=obj1, status=JobLifeCycle.SUCCEEDED)
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
        obj1.original_job = obj2
        obj1.save()
        data = self.serializer_class(obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data['is_clone'] is True

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.jobs_mark
class TestJobStatusSerializer(BaseTest):
    DISABLE_RUNNER = True
    serializer_class = JobStatusSerializer
    model_class = JobStatus
    factory_class = JobStatusFactory
    expected_keys = {'id', 'uuid', 'job', 'created_at', 'status', 'message', 'details'}

    def setUp(self):
        super().setUp()
        with patch.object(Job, 'set_status') as _:  # noqa
            self.obj1 = self.factory_class()
            self.obj2 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('job') == self.obj1.job.id
        data.pop('created_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
