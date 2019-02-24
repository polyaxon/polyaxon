# pylint:disable=too-many-lines
import os

from faker import Faker
from unittest.mock import patch

import pytest

from hestia.internal_services import InternalServices
from rest_framework import status

import conf
import stores

from api.jobs.serializers import (
    BookmarkedJobSerializer,
    JobDetailSerializer,
    JobSerializer,
    JobStatusSerializer
)
from api.utils.views.protected import ProtectedView
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.bookmarks import Bookmark
from db.models.jobs import Job, JobStatus
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from factories.factory_jobs import JobFactory, JobStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import job_spec_parsed_content
from schemas.specifications import JobSpecification
from tests.utils import BaseFilesViewTest, BaseViewTest


@pytest.mark.jobs_mark
class TestProjectJobListViewV1(BaseViewTest):
    serializer_class = BookmarkedJobSerializer
    model_class = Job
    factory_class = JobFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/jobs/'.format(API_V1,
                                            self.project.user.username,
                                            self.project.name)
        self.other_url = '/{}/{}/{}/jobs/'.format(API_V1,
                                                  self.other_project.user.username,
                                                  self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.other_object = self.factory_class(project=self.other_project)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Test other
        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK

        jobs_count = self.queryset.all().count()
        assert jobs_count == self.num_objects

        # Getting all jobs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == jobs_count

    def test_get_with_bookmarked_objects(self):
        # Other user bookmark
        Bookmark.objects.create(
            user=self.other_project.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]), 0)

        # Authenticated user bookmark
        Bookmark.objects.create(
            user=self.auth_client.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]) == 1

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_filter(self):
        # Wrong filter raises
        resp = self.auth_client.get(self.url + '?query=created_at<2010-01-01')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        resp = self.auth_client.get(self.url + '?query=created_at:<2010-01-01')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:Finished')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:created|running')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_get_filter_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(
            self.url,
            limit,
            '?query=created_at:>=2010-01-01,status:created|running'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '?sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data

    def test_create_ttl(self):
        data = {'config': job_spec_parsed_content.parsed_data, 'ttl': 10}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        job = Job.objects.last()
        assert RedisTTL.get_for_job(job.id) == 10

        data = {'config': job_spec_parsed_content.parsed_data, 'ttl': 'foo'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': job_spec_parsed_content.parsed_data}
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_create_with_runner(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': job_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.jobs_mark
class TestJobListViewV1(BaseViewTest):
    serializer_class = BookmarkedJobSerializer
    model_class = Job
    factory_class = JobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/jobs/'.format(API_V1,
                                            self.project.user,
                                            self.project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data


@pytest.mark.jobs_mark
class TestJobDetailViewV1(BaseViewTest):
    serializer_class = JobDetailSerializer
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/'.format(API_V1,
                                               project.user.username,
                                               project.name,
                                               self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data

    def test_get_with_environment(self):
        spec_content = """---
            version: 1

            kind: job

            environment:
              node_selector: 
                foo: bar
              tolerations:
                - key: "key"
                  operator: "Equal"
                  value: "value"
                  effect: "NoSchedule"
              affinity:
                foo: bar
              resources:
                gpu:
                  requests: 1
                  limits: 1
                gpu:
                  requests: 1
                  limits: 1

            build:
              image: my_image

            run:
              cmd: do_something
        """
        spec_parsed_content = JobSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        exp = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/jobs/{}/'.format(API_V1,
                                          project.user.username,
                                          project.name,
                                          exp.id)

        resp = self.auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        exp.refresh_from_db()
        assert resp.data == self.serializer_class(exp).data

    def test_patch(self):
        new_description = 'updated_xp_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description

        # Update original job
        assert new_object.is_clone is False
        new_job = JobFactory()
        data = {'original_job': new_job.id}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description == new_description
        assert new_object.is_clone is True
        assert new_object.original_job == new_job

        # Update name
        data = {'name': 'new_name'}
        assert new_object.name is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_archives_deletes_immediately_and_schedules_stop(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.jobs.jobs_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_archive_schedule_deletion(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.jobs.jobs_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_archive_schedule_archives_and_schedules_stop(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_restore(self):
        self.object.archive()
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        resp = self.auth_client.post(self.url + 'restore/')
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1


@pytest.mark.jobs_mark
class TestJobStatusListViewV1(BaseViewTest):
    serializer_class = JobStatusSerializer
    model_class = JobStatus
    factory_class = JobStatusFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        with patch.object(Job, 'set_status') as _:
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/statuses/'.format(API_V1,
                                                        project.user.username,
                                                        project.name,
                                                        self.job.id)
        self.objects = [self.factory_class(job=self.job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        resp = self.internal_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.status == JobLifeCycle.CREATED

        data = {'status': JobLifeCycle.RUNNING}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']

        # Create with message and traceback
        data = {'status': JobLifeCycle.FAILED,
                'message': 'message1',
                'traceback': 'traceback1'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 3
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']

        data = {}
        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 4


@pytest.mark.jobs_mark
class TestJobStatusDetailViewV1(BaseViewTest):
    serializer_class = JobStatusSerializer
    model_class = JobStatus
    factory_class = JobStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Job, 'set_status') as _:  # noqa
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                self.job = JobFactory()
        self.object = self.factory_class(job=self.job)
        self.url = '/{}/{}/{}/jobs/{}/statuses/{}/'.format(
            API_V1,
            self.job.project.user.username,
            self.job.project.name,
            self.job.id,
            self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'status': JobLifeCycle.SUCCEEDED}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1


@pytest.mark.jobs_mark
class TestRestartJobViewV1(BaseViewTest):
    serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True
    DISABLE_EXECUTOR = False

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/restart'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_restart(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2

        last_job = self.queryset.last()
        assert last_job.is_clone is True
        assert last_job.is_restart is True
        assert last_job.is_copy is False
        assert last_job.is_resume is False
        assert last_job.original_job == self.object
        assert last_job.original_unique_name == self.object.unique_name

    def test_restart_patch_config(self):
        data = {
            'config': {
                'environment': {
                    'resources': {
                        'cpu': {'limits': 0.1, 'requests': 0.2}
                    }
                }
            }
        }
        assert self.queryset.first().specification.environment is None
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2
        assert self.queryset.first().specification.environment is None
        resources = self.queryset.last().specification.environment.resources.to_light_dict()
        assert resources['cpu'] == data['config']['environment']['resources']['cpu']

        last_job = self.queryset.last()
        assert last_job.is_clone is True
        assert last_job.is_restart is True
        assert last_job.is_copy is False
        assert last_job.is_resume is False
        assert last_job.original_job == self.object
        assert last_job.original_unique_name == self.object.unique_name

    def test_restart_patch_wrong_config_raises(self):
        data = {'config': {'lr': 0.1}}
        assert self.queryset.first().specification is not None
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.queryset.count() == 1


@pytest.mark.jobs_mark
class TestStopJobViewV1(BaseViewTest):
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.jobs_mark
class TestJobLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.job = JobFactory(project=project)
        self.logs = []
        self.url = '/{}/{}/{}/jobs/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            self.job.id)

    def create_logs(self, temp):
        log_path = stores.get_job_logs_path(job_name=self.job.unique_name, temp=temp)
        stores.create_job_logs_path(job_name=self.job.unique_name, temp=temp)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get_done_job(self):
        self.job.set_status(JobLifeCycle.SUCCEEDED)
        self.assertTrue(self.job.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return temp file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs

    @patch('api.jobs.views.process_logs')
    def test_get_non_done_job(self, _):
        self.assertFalse(self.job.is_done)
        # No logs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check the it does not return non temp file
        self.create_logs(temp=False)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        # Check returns the correct file
        self.create_logs(temp=True)
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs


@pytest.mark.jobs_mark
class DownloadJobOutputsViewTest(BaseViewTest):
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True
    HAS_INTERNAL = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.job = self.factory_class(project=self.project)
        self.download_url = '/{}/{}/{}/jobs/{}/outputs/download'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.job.id)
        self.job_outputs_path = stores.get_job_outputs_path(
            persistence=self.job.persistence_outputs,
            job_name=self.job.unique_name)
        self.url = self.download_url

    def create_tmp_outputs(self):
        stores.create_job_outputs_path(
            persistence=self.job.persistence_outputs,
            job_name=self.job.unique_name)
        for i in range(4):
            open('{}/{}'.format(self.job_outputs_path, i), '+w')

    def test_redirects_nginx_to_file(self):
        self.create_tmp_outputs()
        # Assert that the job outputs
        self.assertTrue(os.path.exists(self.job_outputs_path))
        response = self.auth_client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER],
                         '{}/{}.tar.gz'.format(conf.get('OUTPUTS_ARCHIVE_ROOT'),
                                               self.job.unique_name.replace('.', '_')))


@pytest.mark.jobs_mark
class TestJobHeartBeatViewV1(BaseViewTest):
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/_heartbeat'.format(
            API_V1,
            project.user.username,
            project.name,
            self.job.id)

    def test_post_job_heartbeat(self):
        self.assertEqual(RedisHeartBeat.job_is_alive(self.job.id), False)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.job_is_alive(self.job.id), True)

    def test_post_internal_job_heartbeat(self):
        self.assertEqual(RedisHeartBeat.job_is_alive(self.job.id), False)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.job_is_alive(self.job.id), True)


@pytest.mark.jobs_mark
class TestJobOutputsTreeViewV1(BaseFilesViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/outputs/tree'.format(
            API_V1,
            project.user.username,
            project.name,
            job.id)

        outputs_path = stores.get_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        stores.create_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        self.create_paths(path=outputs_path, url=self.url)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.top_level['files'])
        self.assert_same_content(resp.data['dirs'], self.top_level['dirs'])

        resp = self.auth_client.get(self.url_second_level)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.second_level['files'])
        self.assert_same_content(resp.data['dirs'], self.second_level['dirs'])

        resp = self.auth_client.get(self.url_second_level2)
        assert resp.status_code == status.HTTP_200_OK
        self.assert_same_content(resp.data['files'], self.second_level['files'])
        self.assert_same_content(resp.data['dirs'], self.second_level['dirs'])


@pytest.mark.jobs_mark
class TestJobOutputsFilesViewV1(BaseFilesViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/outputs/files'.format(
            API_V1,
            project.user.username,
            project.name,
            job.id)

        outputs_path = stores.get_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        stores.create_job_outputs_path(
            persistence=job.persistence_outputs,
            job_name=job.unique_name)
        self.create_paths(path=outputs_path, url=self.url)

    def test_get(self):
        for file_content in self.top_level_files:
            resp = self.auth_client.get(self.url + '?path={}'.format(file_content['file']))
            assert resp.status_code == status.HTTP_200_OK
            data = [i for i in resp._iterator]  # pylint:disable=protected-access
            assert data[0].decode('utf-8') == file_content['data']

        for file_content in self.second_level_files:
            resp = self.auth_client.get(self.url + '?path={}'.format(file_content['file']))
            assert resp.status_code == status.HTTP_200_OK
            data = [i for i in resp._iterator]  # pylint:disable=protected-access
            assert data[0].decode('utf-8') == file_content['data']
