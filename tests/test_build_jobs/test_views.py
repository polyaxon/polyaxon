# pylint:disable=too-many-lines
from faker import Faker
from unittest.mock import patch

import pytest

from rest_framework import status

from api.build_jobs.serializers import (
    BuildJobDetailSerializer,
    BuildJobSerializer,
    BuildJobStatusSerializer
)
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.factory_build_jobs import BuildJobFactory, BuildJobStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import build_spec_parsed_content
from libs.paths.jobs import create_job_logs_path, get_job_logs_path
from polyaxon_schemas.polyaxonfile.specification import BuildSpecification
from tests.utils import BaseViewTest


@pytest.mark.build_jobs_mark
class TestProjectBuildListViewV1(BaseViewTest):
    serializer_class = BuildJobSerializer
    model_class = BuildJob
    factory_class = BuildJobFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_RUNNER = True

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
        self.other_object = self.factory_class(project=self.other_project)

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
    serializer_class = BuildJobSerializer
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

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/builds/{}/'.format(API_V1,
                                                 project.user.username,
                                                 project.name,
                                                 self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data

    def test_get_with_resource_reg_90(self):
        spec_content = """---
            version: 1

            kind: build

            environment:
              resources:
                gpu:
                  requests: 1
                  limits: 1

            build:
              image: my_image
        """
        spec_parsed_content = BuildSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        exp = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/builds/{}/'.format(API_V1,
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

    def test_delete(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as spawner_mock_stop:
            with patch('libs.paths.jobs.delete_path') as outputs_mock_stop:
                resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert outputs_mock_stop.call_count == 2  # Outputs and Logs
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0


@pytest.mark.build_jobs_mark
class TestBuildStatusListViewV1(BaseViewTest):
    serializer_class = BuildJobStatusSerializer
    model_class = BuildJobStatus
    factory_class = BuildJobStatusFactory
    num_objects = 3
    HAS_AUTH = True

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
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        job = BuildJobFactory(project=project)
        self.url = '/{}/{}/{}/builds/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            job.id)

        log_path = get_job_logs_path(job.unique_name)
        create_job_logs_path(job_name=job.unique_name)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs
