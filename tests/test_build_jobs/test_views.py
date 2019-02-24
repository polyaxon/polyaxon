# pylint:disable=too-many-lines
from faker import Faker
from unittest.mock import patch

import pytest

from hestia.internal_services import InternalServices
from rest_framework import status

import stores

from api.build_jobs import queries
from api.build_jobs.serializers import (
    BookmarkedBuildJobSerializer,
    BuildJobDetailSerializer,
    BuildJobStatusSerializer
)
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.bookmarks import Bookmark
from db.models.build_jobs import BuildJob, BuildJobStatus
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from factories.factory_build_jobs import BuildJobFactory, BuildJobStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import build_spec_parsed_content
from schemas.specifications import BuildSpecification
from tests.utils import BaseViewTest


@pytest.mark.build_jobs_mark
class TestProjectBuildListViewV1(BaseViewTest):
    serializer_class = BookmarkedBuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/builds/'.format(API_V1,
                                              self.project.user.username,
                                              self.project.name)
        self.other_url = '/{}/{}/{}/builds/'.format(API_V1,
                                                    self.other_project.user.username,
                                                    self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(project=self.project)
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

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_filter(self):
        # Wrong filter format raises
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

    def test_create_ttl(self):
        data = {'config': build_spec_parsed_content.parsed_data, 'ttl': 10}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        job = BuildJob.objects.last()
        assert RedisTTL.get_for_build(job.id) == 10

        data = {'config': build_spec_parsed_content.parsed_data, 'ttl': 'foo'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': build_spec_parsed_content.parsed_data}
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

        data = {'config': build_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.build_jobs.build_jobs_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.build_jobs_mark
class TestBuildListViewV1(BaseViewTest):
    serializer_class = BookmarkedBuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/builds/'.format(API_V1,
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


@pytest.mark.build_jobs_mark
class TestBuildDetailViewV1(BaseViewTest):
    serializer_class = BuildJobDetailSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.DOCKERIZER

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/builds/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 self.object.id)
        self.queryset = self.model_class.objects.all()
        self.object_query = queries.builds_details.get(id=self.object.id)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object_query).data

        resp = self.internal_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object_query).data

    def test_get_with_environment(self):
        spec_content = """---
            version: 1

            kind: build

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
                tpu:
                  requests: 1
                  limits: 1

            build:
              image: my_image
        """
        spec_parsed_content = BuildSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        obj = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/builds/{}/'.format(API_V1,
                                            project.user.username,
                                            project.name,
                                            obj.id)
        obj_query = queries.builds_details.get(id=obj.id)

        resp = self.auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(obj_query).data

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
        dockerfile = 'foo'
        data = {'dockerfile': dockerfile}
        assert new_object.dockerfile is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.dockerfile == dockerfile

        dockerfile = 'boo'
        data = {'dockerfile': dockerfile}
        assert new_object.dockerfile == 'foo'
        resp = self.internal_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.dockerfile == dockerfile

        # Update name
        data = {'name': 'new_name'}
        assert new_object.name is None
        resp = self.internal_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_archives_deletes_immediately_and_schedules_stop(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.build_jobs.'
                   'build_jobs_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_archive_schedule_deletion(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.build_jobs.'
                   'build_jobs_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_archive_schedule_archives_and_schedules_stop(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as spawner_mock_stop:
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


@pytest.mark.build_jobs_mark
class TestBuildStatusListViewV1(BaseViewTest):
    serializer_class = BuildJobStatusSerializer
    model_class = BuildJobStatus
    factory_class = BuildJobStatusFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        with patch.object(BuildJob, 'set_status') as _:
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.job = BuildJobFactory(project=project)
        self.url = '/{}/{}/{}/builds/{}/statuses/'.format(API_V1,
                                                          project.user.username,
                                                          project.name,
                                                          self.job.id)
        self.objects = [self.factory_class(job=self.job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

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

        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 4
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']


@pytest.mark.build_jobs_mark
class TestBuildStatusDetailViewV1(BaseViewTest):
    serializer_class = BuildJobStatusSerializer
    model_class = BuildJobStatus
    factory_class = BuildJobStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(BuildJob, 'set_status') as _:  # noqa
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                self.job = BuildJobFactory()
        self.object = self.factory_class(job=self.job)
        self.url = '/{}/{}/{}/builds/{}/statuses/{}/'.format(
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


@pytest.mark.build_jobs_mark
class TestStopBuildViewV1(BaseViewTest):
    model_class = BuildJob
    factory_class = BuildJobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/builds/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 1


@pytest.mark.build_jobs_mark
class TestBuildLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.logs = []
        self.job = BuildJobFactory(project=project)
        self.url = '/{}/{}/{}/builds/{}/logs'.format(
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

    @patch('api.build_jobs.views.process_logs')
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


@pytest.mark.build_jobs_mark
class TestBuildHeartBeatViewV1(BaseViewTest):
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.build = BuildJobFactory(project=project)
        self.url = '/{}/{}/{}/builds/{}/_heartbeat'.format(
            API_V1,
            project.user.username,
            project.name,
            self.build.id)

    def test_post_build_heartbeat(self):
        self.assertEqual(RedisHeartBeat.build_is_alive(self.build.id), False)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.build_is_alive(self.build.id), True)

    def test_post_internal_build_heartbeat(self):
        self.assertEqual(RedisHeartBeat.build_is_alive(self.build.id), False)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(RedisHeartBeat.build_is_alive(self.build.id), True)
